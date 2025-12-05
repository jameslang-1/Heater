# populate_test_data.py
# Run this once


from app.database import SessionLocal, engine
from app import models
from datetime import datetime, timedelta
import random

def populate_test_data():
    """Populate database with test graded picks for leaderboard demo"""
    
    db = SessionLocal()
    
    print("Starting test data population...")
    print("=" * 60)
    
    # Create 5 test users
    test_users = [1, 2, 3, 4, 5]
    
    # Get all player props (we'll create test data as if games already happened)
    props = db.query(models.PlayerProp).limit(50).all()
    
    if not props:
        print("⚠ No player props found! Run /api/update-odds first.")
        return
    
    print(f"Found {len(props)} player props to use")
    
    # Stats for each user (to make it realistic)
    user_stats = {
        1: {'win_rate': 0.65, 'total_picks': 20},  # You - good player
        2: {'win_rate': 0.58, 'total_picks': 25},  # Competitive
        3: {'win_rate': 0.55, 'total_picks': 18},  # Average
        4: {'win_rate': 0.48, 'total_picks': 22},  # Below average
        5: {'win_rate': 0.42, 'total_picks': 15},  # Struggling
    }
    
    total_created = 0
    
    for user_id in test_users:
        stats = user_stats[user_id]
        num_picks = stats['total_picks']
        win_rate = stats['win_rate']
        
        print(f"\nCreating picks for User {user_id}...")
        
        # Select random props for this user
        user_props = random.sample(props, min(num_picks, len(props)))
        
        for prop in user_props:
            # Create a pick
            selection = random.choice(['over', 'under'])
            
            # Determine result based on user's win rate
            rand = random.random()
            if rand < win_rate:
                result = 'won'
                # If over, actual is higher than line; if under, actual is lower
                if selection == 'over':
                    actual_value = float(prop.line) + random.uniform(0.5, 5.0)
                else:
                    actual_value = float(prop.line) - random.uniform(0.5, 5.0)
            elif rand < win_rate + 0.05:  # 5% push rate
                result = 'push'
                actual_value = float(prop.line)
            else:
                result = 'lost'
                # If over, actual is lower than line; if under, actual is higher
                if selection == 'over':
                    actual_value = float(prop.line) - random.uniform(0.5, 5.0)
                else:
                    actual_value = float(prop.line) + random.uniform(0.5, 5.0)
            
            # Create the pick
            pick = models.Pick(
                player_prop_id=prop.id,
                user_id=user_id,
                selection=selection,
                line=float(prop.line),
                confidence=random.choice(['high', 'medium', 'low']),
                result=result,
                actual_value=round(actual_value, 1),
                created_at=datetime.now() - timedelta(days=random.randint(1, 30)),
                graded_at=datetime.now() - timedelta(hours=random.randint(1, 12))
            )
            
            db.add(pick)
            total_created += 1
        
        # Show user's record
        wins = sum(1 for p in db.new if hasattr(p, 'result') and p.result == 'won' and p.user_id == user_id)
        losses = sum(1 for p in db.new if hasattr(p, 'result') and p.result == 'lost' and p.user_id == user_id)
        pushes = sum(1 for p in db.new if hasattr(p, 'result') and p.result == 'push' and p.user_id == user_id)
        
        win_pct = round(wins/(wins+losses)*100, 1) if (wins + losses) > 0 else 0
        print(f"  User {user_id}: {wins}W - {losses}L - {pushes}P ({win_pct}% win rate)")
    
    # Commit all picks
    try:
        db.commit()
        print("\n" + "=" * 60)
        print(f"✓ Successfully created {total_created} test picks!")
        print("\nNow you can:")
        print("1. Visit http://localhost:8000/api/grading/leaderboard?current_user_id=1")
        print("2. Check your leaderboard page in the frontend")
        print("\n✓ Test data population complete!")
    except Exception as e:
        db.rollback()
        print(f"\n✗ Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    print("NBA Props Test Data Populator")
    print("=" * 60)
    print("This will create test graded picks for 5 users")
    print("User 1 (you) will have a ~65% win rate")
    print("=" * 60)
    
    response = input("\nContinue? (yes/no): ")
    if response.lower() == 'yes':
        populate_test_data()
    else:
        print("Cancelled.")