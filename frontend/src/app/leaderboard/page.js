"use client";

import React, { useState, useEffect } from 'react';
import ProtectedRoute from '@/components/ProtectedRoute';
import { getLeaderboard } from '@/services/picksApi';

export default function LeaderboardPage() {
  const [timeframe, setTimeframe] = useState('overall');
  const [leaderboardData, setLeaderboardData] = useState([]);
  const [currentUserRank, setCurrentUserRank] = useState(null);
  const [totalUsers, setTotalUsers] = useState(0);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    loadLeaderboard();
  }, [timeframe]);

  const loadLeaderboard = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await getLeaderboard(timeframe);
      setLeaderboardData(data.leaderboard || []);
      setCurrentUserRank(data.current_user_rank);
      setTotalUsers(data.total_users || 0);
    } catch (error) {
      console.error('Error loading leaderboard:', error);
      setError('Failed to load leaderboard. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const getStreakClass = (streak) => {
    return streak?.startsWith('W') ? 'streak-win' : 'streak-loss';
  };

  const getMedalEmoji = (rank) => {
    if (rank === 1) return '🥇';
    if (rank === 2) return '🥈';
    if (rank === 3) return '🥉';
    return '';
  };

  if (loading) {
    return (
      <ProtectedRoute>
        <div className="min-h-screen bg-[#0a0a0a] flex items-center justify-center">
          <div className="text-white text-xl">Loading leaderboard...</div>
        </div>
      </ProtectedRoute>
    );
  }

  if (error) {
    return (
      <ProtectedRoute>
        <div className="min-h-screen bg-[#0a0a0a] flex items-center justify-center">
          <div className="text-center">
            <p className="text-red-500 text-xl mb-4">{error}</p>
            <button 
              onClick={loadLeaderboard}
              className="px-6 py-3 bg-[#ff9f1c] text-black rounded font-semibold hover:bg-[#ff8c00] transition-colors"
            >
              Try Again
            </button>
          </div>
        </div>
      </ProtectedRoute>
    );
  }

  const top3 = leaderboardData.slice(0, 3);
  const currentUser = leaderboardData.find(u => u.is_user);
  const leader = leaderboardData[0];
  const pointsBehind = currentUser && leader ? leader.wins - currentUser.wins : 0;
  const isTop10Percent = currentUserRank && totalUsers > 0 && (currentUserRank / totalUsers) <= 0.1;

  return (
    <ProtectedRoute>
      <div className="min-h-screen bg-[#0a0a0a]">
        <main className="main-content">
          <div className="content-wrapper">
            
            {/* Header */}
            <div className="flex items-center justify-between mb-8">
              <div>
                <h1 className="text-4xl font-bold text-white">Leaderboard</h1>
                <p className="text-gray-400 mt-2">See how you rank against other players</p>
              </div>
              
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

            {/* No Data Message */}
            {leaderboardData.length === 0 && (
              <div className="stats-card text-center py-12">
                <div className="text-6xl mb-4">🏆</div>
                <p className="text-gray-400 text-lg">No graded picks yet for this timeframe</p>
                <p className="text-gray-500 text-sm mt-2">
                  Make some picks on completed games and check back after they're graded!
                </p>
              </div>
            )}

            {/* Top 3 Podium */}
            {top3.length > 0 && (
              <div className="grid grid-cols-3 gap-4 mb-8">
                {top3.map((player) => (
                  <div 
                    key={player.rank}
                    className={`stats-card ${player.rank === 1 ? 'border-2 border-[#ff9f1c]' : ''} ${player.is_user ? 'ring-2 ring-blue-500' : ''}`}
                  >
                    <div className="text-6xl mb-2">{getMedalEmoji(player.rank)}</div>
                    <h2 className="stats-label">
                      {player.is_user ? 'You' : `User ${player.user_id.slice(0, 8)}`}
                    </h2>
                    <p className="stats-number">{player.wins}-{player.losses}</p>
                    <p className="stats-subtext">{player.win_rate}% Win Rate</p>
                    {player.push > 0 && (
                      <p className="text-xs text-gray-500 mt-1">{player.push} pushes</p>
                    )}
                    <div className="mt-3">
                      <span className={`standings-streak ${getStreakClass(player.streak)}`}>
                        {player.streak || '0'}
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            )}

            {/* Full Leaderboard */}
            {leaderboardData.length > 0 && (
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
                      key={player.user_id} 
                      className={`standings-row ${player.is_user ? 'standings-row-user' : ''}`}
                    >
                      <span className="standings-rank">
                        {getMedalEmoji(player.rank) || `#${player.rank}`}
                      </span>
                      <span className="standings-name">
                        {player.is_user ? 'You' : `User ${player.user_id.slice(0, 8)}`}
                        {player.is_user && (
                          <span className="ml-2 text-xs bg-[#ff9f1c] text-black px-2 py-1 rounded font-bold">
                            YOU
                          </span>
                        )}
                      </span>
                      <span className="standings-record">
                        {player.wins}-{player.losses}
                        {player.push > 0 && (
                          <span className="text-xs text-gray-500 ml-1">({player.push}P)</span>
                        )}
                      </span>
                      <span className="standings-record">
                        {player.win_rate}%
                      </span>
                      <span className={`standings-streak ${getStreakClass(player.streak)}`}>
                        {player.streak || '0'}
                      </span>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Stats Summary */}
            {currentUser && (
              <div className="stats-grid mt-8">
                <div className="stats-card">
                  <h2 className="stats-label">Your Rank</h2>
                  <p className="stats-number">#{currentUserRank}</p>
                  <p className="stats-subtext">Out of {totalUsers} players</p>
                </div>

                <div className="stats-card">
                  <h2 className="stats-label">Wins Behind Leader</h2>
                  <p className="stats-number">{pointsBehind}</p>
                  <p className="stats-subtext">
                    {pointsBehind === 0 ? "You're #1! 👑" : `Need ${pointsBehind} more wins to catch up`}
                  </p>
                </div>

                <div className="stats-card">
                  <h2 className="stats-label">Top 10%</h2>
                  <p className={`stats-number ${isTop10Percent ? 'text-green-500' : 'text-gray-400'}`}>
                    {isTop10Percent ? '✓' : '✗'}
                  </p>
                  <p className="stats-subtext">
                    {isTop10Percent ? 'Elite player! 🔥' : 'Keep grinding!'}
                  </p>
                </div>
              </div>
            )}

          </div>
        </main>
      </div>
    </ProtectedRoute>
  );
}