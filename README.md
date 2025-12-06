# Heater - NBA Player Props Prediction Platform

A full-stack web application for making NBA player prop predictions and competing on leaderboards without gambling.

## Project Overview

Heater allows users to:
- Make predictions on NBA player statistics (points, rebounds, assists)
- View automated grading after games complete
- Compete on leaderboards with other users
- Track pick history and performance statistics

**Technology Stack:**
- **Frontend:** Next.js, React, Tailwind CSS, Firebase Authentication
- **Backend:** FastAPI, SQLAlchemy, SQLite
- **External APIs:** NBA Stats API
- **AI Tool:** Claude Sonnet 4.5 for development assistance

---

## Quick Start Guide

### Prerequisites
- Python 3.11 or higher
- Node.js 18 or higher
- Git

### Step 1: Backend Setup

1. **Navigate to backend folder:**
   ```bash
   cd backend/heater-props
   ```

2. **Create and activate virtual environment:**
   
   **Windows:**
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```
   
   **Mac/Linux:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Start the backend server:**
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

   You should see:
   ```
   INFO:     Uvicorn running on http://0.0.0.0:8000
   ```

   **Keep this terminal window open** - the backend must stay running.

---

### Step 2: Frontend Setup

1. **Open a NEW terminal window** and navigate to frontend folder:
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Start the frontend development server:**
   ```bash
   npm run dev
   ```

   You should see:
   ```
   Ready - started server on http://localhost:3000
   ```

4. **Open your browser and visit:**
   ```
   http://localhost:3000
   ```

---

## Demo Account & Test Data

### Pre-configured Demo Account
- **Email:** `demo@heater.com`
- **Password:** `cpsc8740`

This account has:
- 9 graded picks showing won/lost/push results
- A visible record on the leaderboard
- Example of complete user flow

### Creating Your Own Account
You can also create a new account through the signup page. New accounts will:
- Start with a 0-0 record on the leaderboard
- Be able to make picks on upcoming games
- See their stats update as picks are graded

### Demo Data Included

The application comes pre-populated with:
- **5 test users** on the leaderboard with varied win rates
- **Sample graded picks** demonstrating won/lost/push outcomes
- **Upcoming NBA games** for the next 7 days with player props
- **~500 player props** across multiple games

This demo data allows you to immediately explore all features without waiting for real games to complete.

---

## Features to Test

### 1. Authentication
- Sign up for a new account
- Log in with demo account
- Verify protected routes (can't access picks without login)

### 2. Make Picks (Home Page)
- Browse upcoming NBA games
- Expand game cards to see player props
- Select Over/Under for each prop
- Submit picks and see them saved
- Delete picks before games start

### 3. Leaderboard
- View rankings of all users
- See win/loss records and percentages
- View current streaks (W3, L2, etc.)
- Filter by timeframe (All Time, This Month, This Week)
- Identify your position in rankings

### 4. Pick History
- View active (ungraded) picks
- View completed picks with results
- Filter by result (Wins/Losses/Pushes)
- Filter by prop type (Points/Rebounds/Assists)
- See actual game results vs. predictions
- View performance statistics by category

---

## API Endpoints

The backend provides these key endpoints:

### Games & Props
- `GET /api/games` - List upcoming games
- `GET /api/update-odds` - Refresh game data (loads next 7 days)

### Picks
- `POST /api/picks/` - Submit a pick
- `DELETE /api/picks/` - Delete a pick
- `GET /api/picks/active` - Get ungraded picks
- `GET /api/picks/history` - Get graded picks with filters
- `GET /api/picks/stats` - Get user statistics

### Grading
- `POST /api/grading/grade-all` - Grade all completed games
- `GET /api/grading/leaderboard` - Get rankings

### Documentation
Visit `http://localhost:8000/docs` for interactive API documentation (Swagger UI)

---

## Refreshing Game Data (Optional)

The app includes games for the next 7 days. To load fresh NBA game data:

**Option A - Via Browser:**
```
http://localhost:8000/api/update-odds
```

**Option B - Via Terminal:**
```bash
curl http://localhost:8000/api/update-odds
```

This fetches upcoming games and generates player prop projections.

**Note:** The NBA Stats API is undocumented and occasionally unreliable. If you encounter issues, the pre-loaded demo data will continue to work.

---

## Project Structure

```
heater-props/
├── backend/
│   └── heater-props/
│       ├── app/
│       │   ├── main.py              # FastAPI application
│       │   ├── models.py            # SQLAlchemy database models
│       │   ├── schemas.py           # Pydantic schemas
│       │   ├── database.py          # Database configuration
│       │   ├── picks_routes.py      # Picks API endpoints
│       │   ├── grading_routes.py    # Grading API endpoints
│       │   └── grading_service.py   # Automated grading logic
│       ├── heater-props-new.db      # SQLite database
│       └── requirements.txt         # Python dependencies
│
└── frontend/
    ├── src/
    │   ├── app/
    │   │   ├── page.js              # Home page (redirects to picks)
    │   │   ├── picks/page.jsx       # Make picks page
    │   │   ├── leaderboard/page.jsx # Leaderboard page
    │   │   ├── history/page.jsx     # Pick history page
    │   │   ├── login/page.jsx       # Login page
    │   │   └── signup/page.jsx      # Signup page
    │   ├── components/
    │   │   ├── AuthContext.jsx      # Firebase auth context
    │   │   ├── ProtectedRoute.jsx   # Route protection
    │   │   └── navbar.jsx           # Navigation bar
    │   └── services/
    │       └── picksApi.js          # API service layer
    └── package.json                 # Node dependencies
```

---

## Key Implementation Details

### Automated Grading
- Fetches boxscore data from NBA Stats API after games complete
- Compares actual player stats vs. predicted line
- Determines won (correct), lost (incorrect), or push (exact)
- Updates database with results and actual values

---

## Known Limitations

1. **Real-time grading:** Grading must be manually triggered via `/api/grading/grade-all` endpoint after games complete. For demonstration, test data with pre-graded picks is included.

2. **NBA API reliability:** The NBA Stats API is undocumented and occasionally returns incomplete data for games 3+ days out. A static schedule file ensures consistent demo experience.

3. **Single sport:** Currently only supports NBA. Expanding to NFL, MLB, or NHL would require additional API integrations.

4. **Mobile optimization:** While responsive, some table layouts (leaderboard) could be further optimized for small screens.

---

## Troubleshooting

### Backend won't start
- Ensure virtual environment is activated
- Verify Python 3.11+ is installed: `python --version`
- Check if port 8000 is already in use
- Install missing dependencies: `pip install -r requirements.txt`

### Frontend won't start
- Ensure Node.js 18+ is installed: `node --version`
- Delete node_modules and reinstall: `rm -rf node_modules && npm install`
- Check if port 3000 is already in use

### "Network Error" on frontend
- Verify backend is running on `http://localhost:8000`
- Check browser console for CORS errors
- Ensure `API_BASE_URL` in `picksApi.js` is correct

### Firebase authentication issues
- Firebase configuration is already included
- If issues persist, you can test without auth (backend defaults to test user)

### Database locked errors
- Only one process should access SQLite database at a time
- Restart backend if database locks occur

---

## Documentation Included

1. **Project Plan** - 8-week development timeline with milestones
2. **AI Tools Setup Summary** - Claude Sonnet 4.5 usage and impact
3. **UI Design and Integration Report** - Design process, technologies, challenges
4. **Testing and Refinement Report** - Testing methodology, issues found, fixes applied
5. **Final Project Report** - Comprehensive 5-page overview
6. **Presentation Slides** - 12-slide PowerPoint deck with Heater branding

---

## Support

For questions or issues:
- Check API documentation at `http://localhost:8000/docs`
- Review error messages in terminal windows (backend/frontend)
- Examine browser console for frontend errors (F12)

---

## Acknowledgments

- **AI Development Assistant:** Claude Sonnet 4.5 by Anthropic
- **NBA Data:** NBA Stats API
- **Authentication:** Firebase by Google
- **Deployment Tools:** FastAPI, Next.js, Vercel-ready

---

**Enjoy exploring Heater!** 🏀🔥
