# app/grading_service.py
import requests
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from time import sleep
from sqlalchemy.orm import Session
from app import models

class PickGradingService:
    def __init__(self):
        self.base_url = "https://stats.nba.com/stats"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/json',
            'Accept-Language': 'en-US,en;q=0.9',
            'Referer': 'https://www.nba.com/',
            'Origin': 'https://www.nba.com'
        }
    
    def fetch_game_boxscore(self, game_id: str) -> Optional[Dict[str, Any]]:
        """Fetch boxscore for a completed game"""
        url = f"{self.base_url}/boxscoretraditionalv2"
        
        params = {
            'GameID': game_id,
            'StartPeriod': '0',
            'EndPeriod': '10',
            'StartRange': '0',
            'EndRange': '28800',
            'RangeType': '0'
        }
        
        try:
            response = requests.get(url, params=params, headers=self.headers, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if 'resultSets' in data:
                # resultSets[0] contains player stats
                player_stats = data['resultSets'][0]
                return self._parse_player_stats(player_stats)
            
            return None
            
        except Exception as e:
            print(f"Error fetching boxscore for game {game_id}: {e}")
            return None
    
    def _parse_player_stats(self, player_stats_data: Dict) -> Dict[str, Dict[str, float]]:
        """Parse player stats from boxscore data"""
        headers = player_stats_data['headers']
        rows = player_stats_data['rowSet']
        
        # Find column indices
        player_name_idx = headers.index('PLAYER_NAME')
        pts_idx = headers.index('PTS')
        reb_idx = headers.index('REB')
        ast_idx = headers.index('AST')
        
        player_stats = {}
        
        for row in rows:
            player_name = row[player_name_idx]
            
            player_stats[player_name] = {
                'points': float(row[pts_idx]) if row[pts_idx] is not None else 0.0,
                'rebounds': float(row[reb_idx]) if row[reb_idx] is not None else 0.0,
                'assists': float(row[ast_idx]) if row[ast_idx] is not None else 0.0
            }
        
        return player_stats
    
    def check_game_status(self, game_id: str) -> str:
        """Check if a game is completed"""
        url = f"{self.base_url}/boxscoresummaryv2"
        
        params = {
            'GameID': game_id
        }
        
        try:
            response = requests.get(url, params=params, headers=self.headers, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if 'resultSets' in data and len(data['resultSets']) > 0:
                game_summary = data['resultSets'][0]['rowSet'][0]
                # Game status index - 4 means final
                game_status = game_summary[4]
                return game_status
            
            return "Unknown"
            
        except Exception as e:
            print(f"Error checking game status for {game_id}: {e}")
            return "Unknown"
    
    def grade_pick(self, pick: models.Pick, actual_stat: float) -> str:
        """
        Grade a single pick based on actual result
        
        Returns: 'won', 'lost', or 'push'
        """
        line = pick.line
        selection = pick.selection  # 'over' or 'under'
        
        if actual_stat == line:
            return 'push'
        elif selection == 'over' and actual_stat > line:
            return 'won'
        elif selection == 'under' and actual_stat < line:
            return 'won'
        else:
            return 'lost'
    
    def grade_picks_for_game(self, db: Session, game: models.Game) -> Dict[str, Any]:
        """
        Grade all picks for a completed game
        
        Returns summary of grading results
        """
        # Check if game is completed
        game_status = self.check_game_status(game.external_id)
        
        if game_status not in ['Final', '3']:  # 3 is also final status
            return {
                'game_id': game.id,
                'status': 'not_completed',
                'message': f'Game not completed yet. Status: {game_status}'
            }
        
        print(f"Grading picks for {game.away_team} @ {game.home_team}...")
        
        # Fetch actual game stats
        player_stats = self.fetch_game_boxscore(game.external_id)
        
        if not player_stats:
            return {
                'game_id': game.id,
                'status': 'error',
                'message': 'Could not fetch game boxscore'
            }
        
        # Get all ungraded picks for this game
        picks = db.query(models.Pick).join(models.PlayerProp).filter(
            models.PlayerProp.game_id == game.id,
            models.Pick.result == None  # Only ungraded picks
        ).all()
        
        if not picks:
            return {
                'game_id': game.id,
                'status': 'no_picks',
                'message': 'No ungraded picks found for this game'
            }
        
        graded_count = 0
        results = {'won': 0, 'lost': 0, 'push': 0, 'not_found': 0}
        
        for pick in picks:
            prop = pick.player_prop
            player_name = prop.player_name
            prop_type = prop.prop_type  # 'points', 'rebounds', 'assists'
            
            # Find player in actual stats
            if player_name not in player_stats:
                print(f"  ⚠ Player not found in boxscore: {player_name}")
                results['not_found'] += 1
                continue
            
            # Get actual stat value
            actual_value = player_stats[player_name].get(prop_type, 0.0)
            
            # Grade the pick
            result = self.grade_pick(pick, actual_value)
            
            # Update pick in database
            pick.result = result
            pick.actual_value = actual_value
            pick.graded_at = datetime.utcnow()
            
            results[result] += 1
            graded_count += 1
            
            print(f"  ✓ {player_name} {prop_type}: {actual_value} vs {pick.line} ({pick.selection}) = {result.upper()}")
        
        # Commit all updates
        db.commit()
        
        return {
            'game_id': game.id,
            'game': f"{game.away_team} @ {game.home_team}",
            'status': 'completed',
            'graded': graded_count,
            'results': results
        }
    
    def grade_all_completed_games(self, db: Session) -> List[Dict[str, Any]]:
        """
        Grade picks for all completed games
        """
        # Get all games that have passed
        now = datetime.utcnow()
        completed_games = db.query(models.Game).filter(
            models.Game.commence_time < now
        ).all()
        
        if not completed_games:
            return [{
                'status': 'no_games',
                'message': 'No completed games found'
            }]
        
        results = []
        
        for game in completed_games:
            print(f"\nProcessing game: {game.away_team} @ {game.home_team}")
            result = self.grade_picks_for_game(db, game)
            results.append(result)
            
            # Rate limiting
            sleep(1)
        
        return results

# Global instance
grading_service = PickGradingService()