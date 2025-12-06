# add_demo_history.py
from app.database import SessionLocal
from app import models
from datetime import datetime, timedelta
import random

def add_demo_history():
    db = SessionLocal()
    
    # Get your user_id (check by logging in and looking at browser network tab)
    # Or use user_id 1 for the default test account
    demo_user_id = 3762612176  # Your demo account
    
    print(f"Adding demo pick history for user {demo_user_id}...")
    
    # DELETE existing picks for this user first
    existing_picks = db.query(models.Pick).filter(
        models.Pick.user_id == demo_user_id
    ).all()
    
    if existing_picks:
        print(f"  Deleting {len(existing_picks)} existing picks...")
        for pick in existing_picks:
            db.delete(pick)
        db.commit()
        print(f"  ✓ Deleted old picks")
    
    # Get some completed games (games that already happened)
    completed_games = db.query(models.Game).limit(3).all()
    
    if not completed_games:
        print("⚠ No games found in database. Run /api/update-odds first.")
        return
    
    picks_added = 0
    
    for game in completed_games:
        # Get props for this game
        props = db.query(models.PlayerProp).filter(
            models.PlayerProp.game_id == game.id
        ).limit(3).all()  # 3 picks per game
        
        for prop in props:
            # Create a graded pick
            selection = random.choice(['over', 'under'])
            result = random.choice(['won', 'lost', 'push'])
            
            # Calculate actual value based on result (integers only)
            if result == 'won':
                if selection == 'over':
                    actual_value = int(prop.line) + random.randint(1, 5)
                else:
                    actual_value = int(prop.line) - random.randint(1, 5)
            elif result == 'push':
                actual_value = int(prop.line)
            else:  # lost
                if selection == 'over':
                    actual_value = int(prop.line) - random.randint(1, 5)
                else:
                    actual_value = int(prop.line) + random.randint(1, 5)
            
            pick = models.Pick(
                player_prop_id=prop.id,
                user_id=demo_user_id,
                selection=selection,
                line=float(prop.line),
                confidence='high',
                result=result,
                actual_value=float(actual_value),
                created_at=datetime.utcnow() - timedelta(days=random.randint(1, 5)),
                graded_at=datetime.utcnow() - timedelta(hours=random.randint(1, 24))
            )
            
            db.add(pick)
            picks_added += 1
    
    try:
        db.commit()
        print(f"✓ Added {picks_added} graded picks for user {demo_user_id}")
        
        # Show user's record
        total_picks = db.query(models.Pick).filter(
            models.Pick.user_id == demo_user_id,
            models.Pick.result != None
        ).all()
        
        wins = sum(1 for p in total_picks if p.result == 'won')
        losses = sum(1 for p in total_picks if p.result == 'lost')
        pushes = sum(1 for p in total_picks if p.result == 'push')
        
        print(f"  User {demo_user_id} record: {wins}W - {losses}L - {pushes}P")
        
    except Exception as e:
        db.rollback()
        print(f"✗ Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    add_demo_history()