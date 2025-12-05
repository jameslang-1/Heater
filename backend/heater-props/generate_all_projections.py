# generate_all_projections.py
# run just once

import json
import sys
from time import sleep
from app.odds_service import stats_service

def generate_all_projections():
    """Generate projections for all games in the schedule"""
    
    # Load the schedule
    print("Loading schedule...")
    with open('schedule.json', 'r') as f:
        games = json.load(f)
    
    print(f"Found {len(games)} games")
    print("=" * 80)
    
    all_projections = {}
    
    for i, game in enumerate(games, 1):
        game_id = game['game_id']
        away_team = game['away_team_name']
        home_team = game['home_team_name']
        game_date = game['game_date'][:10]  # Just the date
        
        print(f"\n[{i}/{len(games)}] Processing: {away_team} @ {home_team} ({game_date})")
        print("-" * 80)
        
        try:
            # Generate projections for this game
            projections = stats_service.generate_projections_for_game(game)
            
            # Store by game_id
            all_projections[game_id] = {
                'game_info': {
                    'game_id': game_id,
                    'away_team': away_team,
                    'home_team': home_team,
                    'game_date': game['game_date']
                },
                'projections': projections
            }
            
            print(f"✓ Generated {len(projections)} projections")
            
            # Save after each game (in case script crashes)
            with open('projections_cache.json', 'w') as f:
                json.dump(all_projections, f, indent=2)
            
        except Exception as e:
            print(f"✗ Error: {e}")
            all_projections[game_id] = {
                'game_info': {
                    'game_id': game_id,
                    'away_team': away_team,
                    'home_team': home_team,
                    'game_date': game['game_date']
                },
                'projections': [],
                'error': str(e)
            }
    
    print("\n" + "=" * 80)
    print(f"✓ Complete! Generated projections for {len(all_projections)} games")
    print(f"✓ Saved to: projections_cache.json")
    
    # Summary stats
    total_projections = sum(len(p['projections']) for p in all_projections.values())
    print(f"✓ Total player projections: {total_projections}")
    
    return all_projections

if __name__ == "__main__":
    print("NBA Player Projections Generator")
    print("=" * 80)
    print("This will take 20-40 minutes due to NBA API rate limits.")
    print("The script saves progress after each game, so you can stop and resume.")
    print("=" * 80)
    
    response = input("\nContinue? (yes/no): ")
    if response.lower() != 'yes':
        print("Cancelled.")
        sys.exit(0)
    
    print("\nStarting projection generation...\n")
    generate_all_projections()
    
    print("\n✓ Done! You can now use projections_cache.json in your app.")