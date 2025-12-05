"use client";

import React, { useState, useEffect } from 'react';
import ProtectedRoute from '@/components/ProtectedRoute';
import { fetchGames } from '@/services/api';

const PredictionsPage = () => {
  const [selectedDate, setSelectedDate] = useState(new Date());
  const [expandedGame, setExpandedGame] = useState(null);
  const [predictions, setPredictions] = useState({});
  const [games, setGames] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Fetch games from backend
  useEffect(() => {
    const loadGames = async () => {
      try {
        setLoading(true);
        const data = await fetchGames();
        
        // Transform backend data to match our component structure
        const transformedGames = transformBackendData(data.games);
        setGames(transformedGames);
        setError(null);
      } catch (err) {
        setError('Failed to load games');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    loadGames();
  }, []);

  // Transform backend data structure to match frontend
  const transformBackendData = (backendGames) => {
    return backendGames.map((game) => {
      // Group player props by player
      const playerMap = {};
      
      game.player_props.forEach((prop) => {
        if (!playerMap[prop.player_name]) {
          playerMap[prop.player_name] = {
            id: prop.id,
            name: prop.player_name,
            team: '', // Backend doesn't have team per player, could infer from game
            props: {}
          };
        }
        
        playerMap[prop.player_name].props[prop.prop_type] = prop.line;
      });

      return {
        id: game.id,
        homeTeam: {
          name: game.home_team,
          abbreviation: getTeamAbbreviation(game.home_team),
          logo: getTeamLogo(game.home_team)  // Changed from getTeamEmoji
        },
        awayTeam: {
          name: game.away_team,
          abbreviation: getTeamAbbreviation(game.away_team),
          logo: getTeamLogo(game.away_team)  // Changed from getTeamEmoji
        },
        time: formatGameTime(game.commence_time),
        date: new Date(game.commence_time),
        status: getGameStatus(game.commence_time),
        players: Object.values(playerMap)
      };
    });
  };

  // Helper function to get team abbreviation
  const getTeamAbbreviation = (teamName) => {
    const abbrevMap = {
      'Atlanta Hawks': 'ATL',
      'Boston Celtics': 'BOS',
      'Brooklyn Nets': 'BKN',
      'Charlotte Hornets': 'CHA',
      'Chicago Bulls': 'CHI',
      'Cleveland Cavaliers': 'CLE',
      'Dallas Mavericks': 'DAL',
      'Denver Nuggets': 'DEN',
      'Detroit Pistons': 'DET',
      'Golden State Warriors': 'GSW',
      'Houston Rockets': 'HOU',
      'Indiana Pacers': 'IND',
      'LA Clippers': 'LAC',
      'Los Angeles Lakers': 'LAL',
      'Memphis Grizzlies': 'MEM',
      'Miami Heat': 'MIA',
      'Milwaukee Bucks': 'MIL',
      'Minnesota Timberwolves': 'MIN',
      'New Orleans Pelicans': 'NOP',
      'New York Knicks': 'NYK',
      'Oklahoma City Thunder': 'OKC',
      'Orlando Magic': 'ORL',
      'Philadelphia 76ers': 'PHI',
      'Phoenix Suns': 'PHX',
      'Portland Trail Blazers': 'POR',
      'Sacramento Kings': 'SAC',
      'San Antonio Spurs': 'SAS',
      'Toronto Raptors': 'TOR',
      'Utah Jazz': 'UTA',
      'Washington Wizards': 'WAS'
    };
    return abbrevMap[teamName] || 'NBA';
  };

const getTeamLogo = (teamName) => {
  const logoMap = {
    'Atlanta Hawks': 'https://cdn.nba.com/logos/nba/1610612737/primary/L/logo.svg',
    'Boston Celtics': 'https://cdn.nba.com/logos/nba/1610612738/primary/L/logo.svg',
    'Brooklyn Nets': 'https://cdn.nba.com/logos/nba/1610612751/primary/L/logo.svg',
    'Charlotte Hornets': 'https://cdn.nba.com/logos/nba/1610612766/primary/L/logo.svg',
    'Chicago Bulls': 'https://cdn.nba.com/logos/nba/1610612741/primary/L/logo.svg',
    'Cleveland Cavaliers': 'https://cdn.nba.com/logos/nba/1610612739/primary/L/logo.svg',
    'Dallas Mavericks': 'https://cdn.nba.com/logos/nba/1610612742/primary/L/logo.svg',
    'Denver Nuggets': 'https://cdn.nba.com/logos/nba/1610612743/primary/L/logo.svg',
    'Detroit Pistons': 'https://cdn.nba.com/logos/nba/1610612765/primary/L/logo.svg',
    'Golden State Warriors': 'https://cdn.nba.com/logos/nba/1610612744/primary/L/logo.svg',
    'Houston Rockets': 'https://cdn.nba.com/logos/nba/1610612745/primary/L/logo.svg',
    'Indiana Pacers': 'https://cdn.nba.com/logos/nba/1610612754/primary/L/logo.svg',
    'LA Clippers': 'https://cdn.nba.com/logos/nba/1610612746/primary/L/logo.svg',
    'Los Angeles Lakers': 'https://cdn.nba.com/logos/nba/1610612747/primary/L/logo.svg',
    'Memphis Grizzlies': 'https://cdn.nba.com/logos/nba/1610612763/primary/L/logo.svg',
    'Miami Heat': 'https://cdn.nba.com/logos/nba/1610612748/primary/L/logo.svg',
    'Milwaukee Bucks': 'https://cdn.nba.com/logos/nba/1610612749/primary/L/logo.svg',
    'Minnesota Timberwolves': 'https://cdn.nba.com/logos/nba/1610612750/primary/L/logo.svg',
    'New Orleans Pelicans': 'https://cdn.nba.com/logos/nba/1610612740/primary/L/logo.svg',
    'New York Knicks': 'https://cdn.nba.com/logos/nba/1610612752/primary/L/logo.svg',
    'Oklahoma City Thunder': 'https://cdn.nba.com/logos/nba/1610612760/primary/L/logo.svg',
    'Orlando Magic': 'https://cdn.nba.com/logos/nba/1610612753/primary/L/logo.svg',
    'Philadelphia 76ers': 'https://cdn.nba.com/logos/nba/1610612755/primary/L/logo.svg',
    'Phoenix Suns': 'https://cdn.nba.com/logos/nba/1610612756/primary/L/logo.svg',
    'Portland Trail Blazers': 'https://cdn.nba.com/logos/nba/1610612757/primary/L/logo.svg',
    'Sacramento Kings': 'https://cdn.nba.com/logos/nba/1610612758/primary/L/logo.svg',
    'San Antonio Spurs': 'https://cdn.nba.com/logos/nba/1610612759/primary/L/logo.svg',
    'Toronto Raptors': 'https://cdn.nba.com/logos/nba/1610612761/primary/L/logo.svg',
    'Utah Jazz': 'https://cdn.nba.com/logos/nba/1610612762/primary/L/logo.svg',
    'Washington Wizards': 'https://cdn.nba.com/logos/nba/1610612764/primary/L/logo.svg'
  };
  
  return logoMap[teamName] || 'https://cdn.nba.com/logos/leagues/logo-nba.svg';
};

  // Format game time
  const formatGameTime = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleTimeString('en-US', { 
      hour: 'numeric', 
      minute: '2-digit',
      hour12: true 
    });
  };

  // Determine game status
  const getGameStatus = (commenceTime) => {
    const now = new Date();
    const gameTime = new Date(commenceTime);
    
    if (gameTime < now) {
      return 'final';
    }
    return 'upcoming';
  };

  // Generate dates for today through end of week
  const getDatesForWeek = () => {
    const dates = [];
    const today = new Date();
    const dayOfWeek = today.getDay();
    const daysUntilSunday = 7 - dayOfWeek;
    
    for (let i = 0; i <= daysUntilSunday; i++) {
      const date = new Date(today);
      date.setDate(today.getDate() + i);
      dates.push(date);
    }
    return dates;
  };

  const formatDate = (date) => {
    const days = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
    const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
    return {
      day: days[date.getDay()],
      date: date.getDate(),
      month: months[date.getMonth()],
    };
  };

  const isToday = (date) => {
    const today = new Date();
    return date.toDateString() === today.toDateString();
  };

  const isSameDay = (date1, date2) => {
    return date1.toDateString() === date2.toDateString();
  };

  // Filter games by selected date
  const filteredGames = games.filter(game => {
    return isSameDay(game.date, selectedDate);
  });

  const toggleGame = (gameId) => {
    setExpandedGame(expandedGame === gameId ? null : gameId);
  };

  const handlePrediction = (playerId, prop, choice) => {
    const key = `${playerId}-${prop}`;
    setPredictions(prev => ({
      ...prev,
      [key]: prev[key] === choice ? null : choice
    }));
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'live': return 'text-red-500';
      case 'final': return 'text-gray-500';
      default: return 'text-[#ff9f1c]';
    }
  };

  const getStatusText = (status) => {
    switch (status) {
      case 'live': return 'LIVE';
      case 'final': return 'FINAL';
      default: return 'UPCOMING';
    }
  };

  if (loading) {
    return (
      <ProtectedRoute>
        <div className="min-h-screen bg-[#0a0a0a] text-white p-6 flex items-center justify-center">
          <div className="text-xl">Loading games...</div>
        </div>
      </ProtectedRoute>
    );
  }

  if (error) {
    return (
      <ProtectedRoute>
        <div className="min-h-screen bg-[#0a0a0a] text-white p-6 flex items-center justify-center">
          <div className="text-xl text-red-500">{error}</div>
        </div>
      </ProtectedRoute>
    );
  }

  return (
    <ProtectedRoute>
      <div className="min-h-screen bg-[#0a0a0a] text-white p-6">
        {/* Header */}
        <h1 className="text-3xl font-bold mb-6">Predictions</h1>

        {/* Date Picker */}
        <div className="flex gap-2 mb-8 overflow-x-auto pb-2">
          {getDatesForWeek().map((date, index) => {
            const formatted = formatDate(date);
            const selected = isSameDay(date, selectedDate);
            
            return (
              <button
                key={index}
                onClick={() => setSelectedDate(date)}
                className={`flex flex-col items-center px-4 py-3 rounded-lg min-w-[70px] transition-all ${
                  selected 
                    ? 'bg-[#ff9f1c] text-black' 
                    : 'bg-[#1a1a1a] hover:bg-[#2a2a2a]'
                }`}
              >
                <span className="text-xs font-medium">
                  {isToday(date) ? 'Today' : formatted.day}
                </span>
                <span className="text-lg font-bold">{formatted.date}</span>
                <span className="text-xs">{formatted.month}</span>
              </button>
            );
          })}
        </div>

        {/* Games List */}
        <div className="space-y-4">
          {filteredGames.map((game) => (
            <div key={game.id} className="bg-[#1a1a1a] rounded-lg overflow-hidden">
              {/* Game Card - Collapsed */}
              <button
                onClick={() => toggleGame(game.id)}
                className="w-full p-4 flex items-center justify-between hover:bg-[#2a2a2a] transition-colors"
              >
                <div className="flex items-center gap-4 flex-1">
                  {/* Away Team */}
                  <div className="flex items-center gap-2 w-32">
                    <img src={game.awayTeam.logo} alt={game.awayTeam.name} className="w-8 h-8" />
                    <span className="font-semibold">
                      {game.awayTeam.abbreviation}
                    </span>
                  </div>

                  {/* VS / Time */}
                  <div className="text-center">
                    <div className="text-gray-400 text-sm">@</div>
                  </div>

                  {/* Home Team */}
                  <div className="flex items-center gap-2 w-32">
                    <img src={game.homeTeam.logo} alt={game.homeTeam.name} className="w-8 h-8" />
                    <span className="font-semibold">
                      {game.homeTeam.abbreviation}
                    </span>
                  </div>
                </div>

                {/* Time & Status */}
                <div className="flex items-center gap-4">
                  <span className="text-gray-400 text-sm">
                    {game.time}
                  </span>
                  <span className={`text-xs font-bold ${getStatusColor(game.status)}`}>
                    {getStatusText(game.status)}
                  </span>
                  <svg
                    className={`w-5 h-5 transition-transform ${
                      expandedGame === game.id ? 'rotate-180' : ''
                    }`}
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                  </svg>
                </div>
              </button>

              {/* Player Props - Expanded */}
              {expandedGame === game.id && (
                <div className="border-t border-[#2a2a2a] p-4">
                  <h3 className="text-sm font-semibold text-gray-400 mb-4">PLAYER PROPS</h3>
                  
                  <div className="space-y-4">
                    {game.players.map((player) => (
                      <div key={player.id} className="bg-[#0a0a0a] rounded-lg p-4">
                        {/* Player Name */}
                        <div className="flex items-center justify-between mb-3">
                          <span className="font-semibold">
                            {player.name}
                          </span>
                          <span className="text-xs text-gray-400">
                            {player.team || '---'}
                          </span>
                        </div>

                        {/* Props */}
                        <div className="grid grid-cols-3 gap-3">
                          {/* Points */}
                          <div className="text-center">
                            <div className="text-xs text-gray-400 mb-2">Points</div>
                            <div className="text-sm font-bold text-[#ff9f1c] mb-2">
                              {player.props.points ?? '--'}
                            </div>
                            <div className="flex gap-1">
                              <button
                                onClick={() => handlePrediction(player.id, 'points', 'over')}
                                className={`flex-1 py-1 px-2 text-xs rounded transition-colors ${
                                  predictions[`${player.id}-points`] === 'over'
                                    ? 'bg-[#ff9f1c] text-black'
                                    : 'bg-[#2a2a2a] hover:bg-[#3a3a3a]'
                                }`}
                              >
                                Over
                              </button>
                              <button
                                onClick={() => handlePrediction(player.id, 'points', 'under')}
                                className={`flex-1 py-1 px-2 text-xs rounded transition-colors ${
                                  predictions[`${player.id}-points`] === 'under'
                                    ? 'bg-[#ff9f1c] text-black'
                                    : 'bg-[#2a2a2a] hover:bg-[#3a3a3a]'
                                }`}
                              >
                                Under
                              </button>
                            </div>
                          </div>

                          {/* Rebounds */}
                          <div className="text-center">
                            <div className="text-xs text-gray-400 mb-2">Rebounds</div>
                            <div className="text-sm font-bold text-[#ff9f1c] mb-2">
                              {player.props.rebounds ?? '--'}
                            </div>
                            <div className="flex gap-1">
                              <button
                                onClick={() => handlePrediction(player.id, 'rebounds', 'over')}
                                className={`flex-1 py-1 px-2 text-xs rounded transition-colors ${
                                  predictions[`${player.id}-rebounds`] === 'over'
                                    ? 'bg-[#ff9f1c] text-black'
                                    : 'bg-[#2a2a2a] hover:bg-[#3a3a3a]'
                                }`}
                              >
                                Over
                              </button>
                              <button
                                onClick={() => handlePrediction(player.id, 'rebounds', 'under')}
                                className={`flex-1 py-1 px-2 text-xs rounded transition-colors ${
                                  predictions[`${player.id}-rebounds`] === 'under'
                                    ? 'bg-[#ff9f1c] text-black'
                                    : 'bg-[#2a2a2a] hover:bg-[#3a3a3a]'
                                }`}
                              >
                                Under
                              </button>
                            </div>
                          </div>

                          {/* Assists */}
                          <div className="text-center">
                            <div className="text-xs text-gray-400 mb-2">Assists</div>
                            <div className="text-sm font-bold text-[#ff9f1c] mb-2">
                              {player.props.assists ?? '--'}
                            </div>
                            <div className="flex gap-1">
                              <button
                                onClick={() => handlePrediction(player.id, 'assists', 'over')}
                                className={`flex-1 py-1 px-2 text-xs rounded transition-colors ${
                                  predictions[`${player.id}-assists`] === 'over'
                                    ? 'bg-[#ff9f1c] text-black'
                                    : 'bg-[#2a2a2a] hover:bg-[#3a3a3a]'
                                }`}
                              >
                                Over
                              </button>
                              <button
                                onClick={() => handlePrediction(player.id, 'assists', 'under')}
                                className={`flex-1 py-1 px-2 text-xs rounded transition-colors ${
                                  predictions[`${player.id}-assists`] === 'under'
                                    ? 'bg-[#ff9f1c] text-black'
                                    : 'bg-[#2a2a2a] hover:bg-[#3a3a3a]'
                                }`}
                              >
                                Under
                              </button>
                            </div>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>

                  {/* Submit Button */}
                  <button className="w-full mt-4 py-3 bg-[#ff9f1c] text-black font-bold rounded-lg hover:bg-[#e8900a] transition-colors">
                    Submit Predictions
                  </button>
                </div>
              )}
            </div>
          ))}
        </div>

        {/* Empty State */}
        {filteredGames.length === 0 && (
          <div className="text-center text-gray-400 py-12">
            <p>No games scheduled for this date</p>
          </div>
        )}
      </div>
    </ProtectedRoute>
  );
};

export default PredictionsPage;