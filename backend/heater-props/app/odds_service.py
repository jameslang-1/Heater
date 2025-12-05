# app/odds_service.py
import requests
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from time import sleep

class NBAStatsService:
    def __init__(self):
        self.base_url = "https://stats.nba.com/stats"
        # Headers required by NBA Stats API
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/json',
            'Accept-Language': 'en-US,en;q=0.9',
            'Referer': 'https://www.nba.com/',
            'Origin': 'https://www.nba.com'
        }
    
    def get_all_teams(self) -> Dict[int, str]:
        """Get mapping of team IDs to team names"""
        # Using hardcoded mapping as it's most reliable
        return {
            1610612737: 'Atlanta Hawks',
            1610612738: 'Boston Celtics',
            1610612751: 'Brooklyn Nets',
            1610612766: 'Charlotte Hornets',
            1610612741: 'Chicago Bulls',
            1610612739: 'Cleveland Cavaliers',
            1610612742: 'Dallas Mavericks',
            1610612743: 'Denver Nuggets',
            1610612765: 'Detroit Pistons',
            1610612744: 'Golden State Warriors',
            1610612745: 'Houston Rockets',
            1610612754: 'Indiana Pacers',
            1610612746: 'LA Clippers',
            1610612747: 'Los Angeles Lakers',
            1610612763: 'Memphis Grizzlies',
            1610612748: 'Miami Heat',
            1610612749: 'Milwaukee Bucks',
            1610612750: 'Minnesota Timberwolves',
            1610612740: 'New Orleans Pelicans',
            1610612752: 'New York Knicks',
            1610612760: 'Oklahoma City Thunder',
            1610612753: 'Orlando Magic',
            1610612755: 'Philadelphia 76ers',
            1610612756: 'Phoenix Suns',
            1610612757: 'Portland Trail Blazers',
            1610612758: 'Sacramento Kings',
            1610612759: 'San Antonio Spurs',
            1610612761: 'Toronto Raptors',
            1610612762: 'Utah Jazz',
            1610612764: 'Washington Wizards'
        }
    
    def fetch_todays_games(self) -> List[Dict[str, Any]]:
        """Fetch today's NBA games"""
        url = f"{self.base_url}/scoreboardv2"
        
        today = datetime.now().strftime('%Y-%m-%d')
        
        params = {
            'GameDate': today,
            'LeagueID': '00',
            'DayOffset': '0'
        }
        
        try:
            response = requests.get(url, params=params, headers=self.headers, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if 'resultSets' in data:
                game_header = data['resultSets'][0]
                games = []
                
                for game in game_header['rowSet']:
                    games.append({
                        'game_id': game[2],
                        'game_date': game[0],
                        'home_team_id': game[6],
                        'away_team_id': game[7],
                        'home_team_name': game[6],
                        'away_team_name': game[7],
                        'game_status': game[4]
                    })
                
                return games
            
            return []
            
        except Exception as e:
            print(f"Error fetching today's games: {e}")
            return []
    
    def fetch_schedule(self, days_ahead: int = 14) -> List[Dict[str, Any]]:
        """Fetch upcoming games for next N days"""
        all_games = []
        
        # Get team name mapping once
        team_mapping = self.get_all_teams()
        
        for day_offset in range(days_ahead):
            target_date = datetime.now() + timedelta(days=day_offset)
            date_str = target_date.strftime('%Y-%m-%d')
            
            url = f"{self.base_url}/scoreboardv2"
            params = {
                'GameDate': date_str,
                'LeagueID': '00',
                'DayOffset': '0'
            }
            
            try:
                response = requests.get(url, params=params, headers=self.headers, timeout=10)
                response.raise_for_status()
                data = response.json()
                
                if 'resultSets' in data and len(data['resultSets']) > 0:
                    game_header = data['resultSets'][0]
                    
                    for game in game_header['rowSet']:
                        home_team_id = game[6]
                        away_team_id = game[7]
                        
                        games_dict = {
                            'game_id': game[2],
                            'game_date': game[0],
                            'home_team_id': home_team_id,
                            'away_team_id': away_team_id,
                            'home_team_name': team_mapping.get(home_team_id, f"Team {home_team_id}"),
                            'away_team_name': team_mapping.get(away_team_id, f"Team {away_team_id}")
                        }
                        all_games.append(games_dict)
                
                # Be nice to the API
                sleep(0.5)
                
            except Exception as e:
                print(f"Error fetching games for {date_str}: {e}")
        
        return all_games
    
    def fetch_player_game_log(self, player_id: str, season: str = "2024-25") -> List[Dict[str, Any]]:
        """Fetch recent game log for a player"""
        url = f"{self.base_url}/playergamelog"
        
        params = {
            'PlayerID': player_id,
            'Season': season,
            'SeasonType': 'Regular Season',
            'LeagueID': '00'
        }
        
        try:
            response = requests.get(url, params=params, headers=self.headers, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if 'resultSets' in data and len(data['resultSets']) > 0:
                games = data['resultSets'][0]['rowSet']
                return games[:10]  # Last 10 games
            
            return []
            
        except Exception as e:
            print(f"Error fetching game log for player {player_id}: {e}")
            return []
    
    def fetch_team_roster(self, team_id: int, season: str = "2024-25") -> List[Dict[str, Any]]:
        """Fetch roster for a team"""
        url = f"{self.base_url}/commonteamroster"
        
        params = {
            'TeamID': team_id,
            'Season': season,
            'LeagueID': '00'
        }
        
        try:
            response = requests.get(url, params=params, headers=self.headers, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if 'resultSets' in data and len(data['resultSets']) > 0:
                players = data['resultSets'][0]['rowSet']
                
                roster = []
                for player in players:
                    roster.append({
                        'player_id': player[14],  # PLAYER_ID
                        'player_name': player[3]   # PLAYER
                    })
                
                return roster
            
            return []
            
        except Exception as e:
            print(f"Error fetching roster for team {team_id}: {e}")
            return []
    
    def calculate_projection(self, game_log: List[Any], stat_index: int) -> Optional[float]:
        """Calculate average from recent games"""
        if not game_log:
            return None
        
        # Filter valid games and get the stat
        valid_stats = []
        for game in game_log:
            if len(game) > stat_index:
                try:
                    stat_value = float(game[stat_index])
                    if stat_value >= 0:  # Valid stat
                        valid_stats.append(stat_value)
                except (ValueError, TypeError):
                    continue
        
        if not valid_stats:
            return None
        
        avg = sum(valid_stats) / len(valid_stats)
        rounded = round(avg * 2) / 2
        return rounded
    
    def generate_projections_for_game(self, game_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate projections for a game"""
        projections = []
        
        home_team_id = game_data['home_team_id']
        away_team_id = game_data['away_team_id']
        
        # Get rosters
        print(f"  Fetching home team roster...")
        home_roster = self.fetch_team_roster(home_team_id)
        sleep(0.6)
        
        print(f"  Fetching away team roster...")
        away_roster = self.fetch_team_roster(away_team_id)
        sleep(0.6)
        
        # Combine and limit to top 6 players per team (12 total)
        all_players = home_roster[:6] + away_roster[:6]
        
        for player in all_players:
            player_id = player['player_id']
            player_name = player['player_name']
            
            print(f"  Getting stats for {player_name}...")
            
            # Fetch game log
            game_log = self.fetch_player_game_log(player_id)
            sleep(0.6)  # Rate limiting
            
            if not game_log:
                continue
            
            # Calculate projections
            # NBA Stats API game log indices: PTS=24, REB=18, AST=19
            points_proj = self.calculate_projection(game_log, 24)
            rebounds_proj = self.calculate_projection(game_log, 18)
            assists_proj = self.calculate_projection(game_log, 19)
            
            if points_proj and points_proj > 5:
                projections.append({
                    'player_name': player_name,
                    'prop_type': 'points',
                    'line': points_proj,
                    'over_odds': -110,
                    'under_odds': -110,
                    'bookmaker': 'projection'
                })
            
            if rebounds_proj and rebounds_proj > 2:
                projections.append({
                    'player_name': player_name,
                    'prop_type': 'rebounds',
                    'line': rebounds_proj,
                    'over_odds': -110,
                    'under_odds': -110,
                    'bookmaker': 'projection'
                })
            
            if assists_proj and assists_proj > 1:
                projections.append({
                    'player_name': player_name,
                    'prop_type': 'assists',
                    'line': assists_proj,
                    'over_odds': -110,
                    'under_odds': -110,
                    'bookmaker': 'projection'
                })
        
        return projections
    
    def parse_game_data(self, game_data: Dict[str, Any]) -> Dict[str, Any]:
        """Parse game data into our format"""
        # Parse the date string
        game_date = datetime.strptime(game_data['game_date'], '%Y-%m-%dT%H:%M:%S')
        
        return {
            'external_id': game_data['game_id'],
            'home_team': game_data['home_team_name'],
            'away_team': game_data['away_team_name'],
            'commence_time': game_date
        }

stats_service = NBAStatsService()