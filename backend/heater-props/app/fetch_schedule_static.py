# fetch_schedule_static.py

import requests
import json
from datetime import datetime, timedelta

def fetch_nba_schedule():
    """Fetch NBA schedule from Dec 5-15, 2025"""
    
    base_url = "https://stats.nba.com/stats/scoreboardv2"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'application/json',
        'Accept-Language': 'en-US,en;q=0.9',
        'Referer': 'https://www.nba.com/',
        'Origin': 'https://www.nba.com'
    }
    
    # Team mapping
    team_mapping = {
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
    
    all_games = []
    start_date = datetime(2025, 12, 5)
    end_date = datetime(2025, 12, 15)
    
    current_date = start_date
    while current_date <= end_date:
        date_str = current_date.strftime('%Y-%m-%d')
        print(f"Fetching games for {date_str}...")
        
        params = {
            'GameDate': date_str,
            'LeagueID': '00',
            'DayOffset': '0'
        }
        
        try:
            response = requests.get(base_url, params=params, headers=headers, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if 'resultSets' in data and len(data['resultSets']) > 0:
                game_header = data['resultSets'][0]
                
                for game in game_header['rowSet']:
                    home_team_id = game[6]
                    away_team_id = game[7]
                    
                    # Skip games without team assignments
                    if home_team_id is None or away_team_id is None or home_team_id == 0 or away_team_id == 0:
                        print(f"  Skipping unscheduled game {game[2]}")
                        continue
                    
                    # Get team names
                    home_team_name = team_mapping.get(home_team_id)
                    away_team_name = team_mapping.get(away_team_id)
                    
                    if not home_team_name or not away_team_name:
                        print(f"  Skipping game {game[2]} - unknown teams")
                        continue
                    
                    game_info = {
                        'game_id': game[2],
                        'game_date': game[0],
                        'home_team_id': home_team_id,
                        'away_team_id': away_team_id,
                        'home_team_name': home_team_name,
                        'away_team_name': away_team_name,
                        'date_simple': date_str
                    }
                    
                    all_games.append(game_info)
                    print(f"  ✓ {away_team_name} @ {home_team_name}")
            
            # Be nice to the API
            import time
            time.sleep(0.5)
            
        except Exception as e:
            print(f"Error fetching {date_str}: {e}")
        
        current_date += timedelta(days=1)
    
    return all_games

if __name__ == "__main__":
    print("Fetching NBA schedule for December 5-15, 2025...")
    print("=" * 60)
    
    games = fetch_nba_schedule()
    
    print("=" * 60)
    print(f"\nTotal games found: {len(games)}")
    
    # Save to JSON file
    output_file = "nba_schedule_dec_5_15_2025.json"
    with open(output_file, 'w') as f:
        json.dump(games, f, indent=2)
    
    print(f"\n✓ Schedule saved to: {output_file}")
    print("\nYou can now use this file in your project!")
    
    # Print summary by date
    print("\nGames by date:")
    from collections import defaultdict
    games_by_date = defaultdict(list)
    for game in games:
        games_by_date[game['date_simple']].append(game)
    
    for date in sorted(games_by_date.keys()):
        print(f"  {date}: {len(games_by_date[date])} games")