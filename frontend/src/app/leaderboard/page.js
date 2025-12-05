"use client";

import React, { useState } from 'react';
import ProtectedRoute from '@/components/ProtectedRoute';

export default function LeaderboardPage() {
  const [timeframe, setTimeframe] = useState('overall'); // 'overall', 'week', 'month'
  
  // Mock data - replace with real API call later
  const leaderboardData = [
    { rank: 1, name: 'The GOAT', wins: 69, losses: 0, winRate: 100, streak: 'W69', isUser: false },
    { rank: 2, name: 'You', wins: 67, losses: 67, winRate: 50, streak: 'W2', isUser: true },
    { rank: 3, name: 'Ris', wins: 17, losses: 38, winRate: 30.9, streak: 'L1', isUser: false },
    { rank: 4, name: 'China', wins: 20, losses: 58, winRate: 25.6, streak: 'L9', isUser: false },
    { rank: 5, name: 'Saturdays', wins: 41, losses: 15, winRate: 73.2, streak: 'W5', isUser: false },
    { rank: 6, name: 'Mike', wins: 55, losses: 45, winRate: 55, streak: 'W1', isUser: false },
    { rank: 7, name: 'Sarah', wins: 48, losses: 52, winRate: 48, streak: 'L2', isUser: false },
    { rank: 8, name: 'James', wins: 60, losses: 40, winRate: 60, streak: 'W3', isUser: false },
    { rank: 9, name: 'Alex', wins: 35, losses: 65, winRate: 35, streak: 'L5', isUser: false },
    { rank: 10, name: 'Taylor', wins: 50, losses: 50, winRate: 50, streak: 'W1', isUser: false },
  ];

  const getStreakClass = (streak) => {
    return streak.startsWith('W') ? 'streak-win' : 'streak-loss';
  };

  const getMedalEmoji = (rank) => {
    if (rank === 1) return '🥇';
    if (rank === 2) return '🥈';
    if (rank === 3) return '🥉';
    return '';
  };

  return (
    <ProtectedRoute>
      <div className="min-h-screen bg-[#0a0a0a]">
        <main className="main-content">
          <div className="content-wrapper">
            
            {/* Header */}
            <div className="flex items-center justify-between mb-8">
              <h1 className="text-4xl font-bold text-white">Leaderboard</h1>
              
              {/* Timeframe Selector */}
              <div className="flex gap-2">
                <button
                  onClick={() => setTimeframe('overall')}
                  className={`px-4 py-2 rounded font-semibold transition-colors ${
                    timeframe === 'overall' 
                      ? 'bg-[#ff9f1c] text-black' 
                      : 'bg-[#1a1a1a] text-white hover:bg-[#2a2a2a]'
                  }`}
                >
                  All Time
                </button>
                <button
                  onClick={() => setTimeframe('month')}
                  className={`px-4 py-2 rounded font-semibold transition-colors ${
                    timeframe === 'month' 
                      ? 'bg-[#ff9f1c] text-black' 
                      : 'bg-[#1a1a1a] text-white hover:bg-[#2a2a2a]'
                  }`}
                >
                  This Month
                </button>
                <button
                  onClick={() => setTimeframe('week')}
                  className={`px-4 py-2 rounded font-semibold transition-colors ${
                    timeframe === 'week' 
                      ? 'bg-[#ff9f1c] text-black' 
                      : 'bg-[#1a1a1a] text-white hover:bg-[#2a2a2a]'
                  }`}
                >
                  This Week
                </button>
              </div>
            </div>

            {/* Top 3 Podium */}
            <div className="grid grid-cols-3 gap-4 mb-8">
              {leaderboardData.slice(0, 3).map((player) => (
                <div 
                  key={player.rank}
                  className={`stats-card ${player.rank === 1 ? 'border-2 border-[#ff9f1c]' : ''}`}
                >
                  <div className="text-6xl mb-2">{getMedalEmoji(player.rank)}</div>
                  <h2 className="stats-label">{player.name}</h2>
                  <p className="stats-number">{player.wins}-{player.losses}</p>
                  <p className="stats-subtext">{player.winRate}% Win Rate</p>
                  <div className="mt-3">
                    <span className={`standings-streak ${getStreakClass(player.streak)}`}>
                      {player.streak}
                    </span>
                  </div>
                </div>
              ))}
            </div>

            {/* Full Leaderboard */}
            <div className="stats-card">
              <h2 className="stats-label mb-4">Full Rankings</h2>
              
              <div className="standings-list">
                {/* Header Row */}
                <div className="standings-row" style={{ borderBottom: '2px solid #2a2a2a', paddingBottom: '12px', marginBottom: '8px' }}>
                  <span className="standings-rank text-gray-400 font-bold">Rank</span>
                  <span className="standings-name text-gray-400 font-bold">Player</span>
                  <span className="standings-record text-gray-400 font-bold">Record</span>
                  <span className="standings-record text-gray-400 font-bold">Win %</span>
                  <span className="standings-streak text-gray-400 font-bold">Streak</span>
                </div>

                {/* Leaderboard Rows */}
                {leaderboardData.map((player) => (
                  <div 
                    key={player.rank} 
                    className={`standings-row ${player.isUser ? 'standings-row-user' : ''}`}
                  >
                    <span className="standings-rank">
                      {getMedalEmoji(player.rank) || `#${player.rank}`}
                    </span>
                    <span className="standings-name">
                      {player.name}
                      {player.isUser && (
                        <span className="ml-2 text-xs bg-[#ff9f1c] text-black px-2 py-1 rounded font-bold">
                          YOU
                        </span>
                      )}
                    </span>
                    <span className="standings-record">
                      {player.wins}-{player.losses}
                    </span>
                    <span className="standings-record">
                      {player.winRate}%
                    </span>
                    <span className={`standings-streak ${getStreakClass(player.streak)}`}>
                      {player.streak}
                    </span>
                  </div>
                ))}
              </div>
            </div>

            {/* Stats Summary */}
            <div className="stats-grid mt-8">
              <div className="stats-card">
                <h2 className="stats-label">Your Rank</h2>
                <p className="stats-number">#2</p>
                <p className="stats-subtext">Out of {leaderboardData.length} players</p>
              </div>

              <div className="stats-card">
                <h2 className="stats-label">Points Behind Leader</h2>
                <p className="stats-number">2</p>
                <p className="stats-subtext">Need 2 wins to catch up</p>
              </div>

              <div className="stats-card">
                <h2 className="stats-label">Top 10%</h2>
                <p className="stats-number text-green-500">✓</p>
                <p className="stats-subtext">Keep up the great work!</p>
              </div>
            </div>

          </div>
        </main>
      </div>
    </ProtectedRoute>
  );
}