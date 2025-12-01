"use client";

import React, { useState } from 'react';
import ProtectedRoute from '@/components/ProtectedRoute';

const PredictionsPage = () => {
  const [selectedDate, setSelectedDate] = useState(new Date());
  const [expandedGame, setExpandedGame] = useState(null);
  const [predictions, setPredictions] = useState({});

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

  // Placeholder data structure - replace with backend data
  const games = [
    {
      id: 1,
      homeTeam: { name: '', abbreviation: '', logo: '' },
      awayTeam: { name: '', abbreviation: '', logo: '' },
      time: '',
      status: '', // 'upcoming', 'live', 'final'
      players: [
        { id: 1, name: '', team: '', props: { points: null, rebounds: null, assists: null } },
        { id: 2, name: '', team: '', props: { points: null, rebounds: null, assists: null } },
        { id: 3, name: '', team: '', props: { points: null, rebounds: null, assists: null } },
        { id: 4, name: '', team: '', props: { points: null, rebounds: null, assists: null } },
      ],
    },
    {
      id: 2,
      homeTeam: { name: '', abbreviation: '', logo: '' },
      awayTeam: { name: '', abbreviation: '', logo: '' },
      time: '',
      status: '',
      players: [
        { id: 5, name: '', team: '', props: { points: null, rebounds: null, assists: null } },
        { id: 6, name: '', team: '', props: { points: null, rebounds: null, assists: null } },
        { id: 7, name: '', team: '', props: { points: null, rebounds: null, assists: null } },
        { id: 8, name: '', team: '', props: { points: null, rebounds: null, assists: null } },
      ],
    },
  ];

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
          {games.map((game) => (
            <div key={game.id} className="bg-[#1a1a1a] rounded-lg overflow-hidden">
              {/* Game Card - Collapsed */}
              <button
                onClick={() => toggleGame(game.id)}
                className="w-full p-4 flex items-center justify-between hover:bg-[#2a2a2a] transition-colors"
              >
                <div className="flex items-center gap-4 flex-1">
                  {/* Away Team */}
                  <div className="flex items-center gap-2 w-32">
                    <span className="text-2xl">{game.awayTeam.logo || '🏀'}</span>
                    <span className="font-semibold">
                      {game.awayTeam.abbreviation || 'team'}
                    </span>
                  </div>

                  {/* VS / Time */}
                  <div className="text-center">
                    <div className="text-gray-400 text-sm">@</div>
                  </div>

                  {/* Home Team */}
                  <div className="flex items-center gap-2 w-32">
                    <span className="text-2xl">{game.homeTeam.logo || '🏀'}</span>
                    <span className="font-semibold">
                      {game.homeTeam.abbreviation || 'team'}
                    </span>
                  </div>
                </div>

                {/* Time & Status */}
                <div className="flex items-center gap-4">
                  <span className="text-gray-400 text-sm">
                    {game.time || '--:-- --'}
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
                            {player.name || 'Player Name'}
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
        {games.length === 0 && (
          <div className="text-center text-gray-400 py-12">
            <p>No games scheduled for this date</p>
          </div>
        )}
      </div>
    </ProtectedRoute>
  );
};

export default PredictionsPage;