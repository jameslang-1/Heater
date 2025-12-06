"use client";

import React, { useState, useEffect } from 'react';
import ProtectedRoute from '@/components/ProtectedRoute';
import { getPickHistory, getUserStats, getActivePicks } from '@/services/picksApi';

export default function HistoryPage() {
  const [stats, setStats] = useState(null);
  const [history, setHistory] = useState([]);
  const [activePicks, setActivePicks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState('all'); // 'all', 'won', 'lost', 'push'
  const [propFilter, setPropFilter] = useState('all'); // 'all', 'points', 'rebounds', 'assists'
  const [viewMode, setViewMode] = useState('active'); // 'active' or 'history'

  useEffect(() => {
    loadData();
  }, [filter, propFilter]);

  const loadData = async () => {
    try {
      setLoading(true);
      const [statsData, historyData, activeData] = await Promise.all([
        getUserStats(),
        getPickHistory({ 
          result: filter !== 'all' ? filter : undefined,
          prop_type: propFilter !== 'all' ? propFilter : undefined,
          limit: 50
        }),
        getActivePicks()
      ]);
      
      setStats(statsData);
      setHistory(historyData);
      setActivePicks(activeData);
    } catch (err) {
      console.error('Error loading data:', err);
    } finally {
      setLoading(false);
    }
  };

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', { 
      month: 'short', 
      day: 'numeric',
      hour: 'numeric',
      minute: '2-digit'
    });
  };

  const getResultBadge = (result) => {
    const styles = {
      won: 'bg-green-600',
      lost: 'bg-red-600',
      push: 'bg-blue-600',
      pending: 'bg-blue-600'
    };
    return styles[result] || 'bg-gray-600';
  };

  const getResultIcon = (result) => {
    if (result === 'won') return '✓';
    if (result === 'lost') return '✗';
    if (result === 'push') return '―';
    return '?';
  };

  const getStreakColor = (streak) => {
    if (streak > 0) return 'text-green-500';
    if (streak < 0) return 'text-red-500';
    return 'text-gray-400';
  };

  const getStreakText = (streak) => {
    if (streak === 0) return 'No Streak';
    if (streak > 0) return `${streak}W`;
    return `${Math.abs(streak)}L`;
  };

  // Filter active picks by prop type
  const filteredActivePicks = propFilter === 'all' 
    ? activePicks 
    : activePicks.filter(pick => pick.prop_type === propFilter);

  if (loading) {
    return (
      <ProtectedRoute>
        <div className="min-h-screen bg-[#0a0a0a] flex items-center justify-center">
          <div className="text-white text-xl">Loading history...</div>
        </div>
      </ProtectedRoute>
    );
  }

  return (
    <ProtectedRoute>
      <div className="min-h-screen bg-[#0a0a0a]">
        <main className="main-content">
          <div className="content-wrapper">
            
            {/* Header */}
            <h1 className="text-4xl font-bold text-white mb-8">My Picks</h1>

            {/* Stats Overview */}
            {stats && (
              <div className="stats-grid mb-8">
                {/* Overall Record */}
                <div className="stats-card">
                  <h2 className="stats-label">Overall Record</h2>
                  <p className="stats-number">{stats.wins}-{stats.losses}</p>
                  <p className="stats-subtext">{stats.win_percentage}% Win Rate</p>
                  {stats.pushes > 0 && (
                    <p className="text-gray-400 text-sm mt-2">{stats.pushes} Pushes</p>
                  )}
                </div>

                {/* Current Streak */}
                <div className="stats-card">
                  <h2 className="stats-label">Current Streak</h2>
                  <p className={`stats-number ${getStreakColor(stats.current_streak)}`}>
                    {getStreakText(stats.current_streak)}
                  </p>
                  <p className="stats-subtext">Best: {stats.best_streak}W</p>
                </div>

                {/* Recent Form */}
                <div className="stats-card">
                  <h2 className="stats-label">Recent Form</h2>
                  <div className="flex gap-2 justify-center mt-4">
                    {stats.recent_form.slice(0, 10).map((result, index) => (
                      <div
                        key={index}
                        className={`w-8 h-8 rounded-full flex items-center justify-center text-white text-xs font-bold ${
                          getResultBadge(result)
                        }`}
                      >
                        {result === 'won' ? 'W' : result === 'lost' ? 'L' : 'P'}
                      </div>
                    ))}
                  </div>
                  <p className="stats-subtext mt-3">Last 10 Picks</p>
                </div>
              </div>
            )}

            {/* By Prop Type Stats */}
            {stats && (
              <div className="stats-grid mb-8">
                <div className="stats-card">
                  <h2 className="stats-label">🏀 Points</h2>
                  <p className="stats-number">{stats.by_prop_type.points.win_rate}%</p>
                  <p className="stats-subtext">
                    {stats.by_prop_type.points.wins}/{stats.by_prop_type.points.total} Correct
                  </p>
                </div>

                <div className="stats-card">
                  <h2 className="stats-label">📊 Rebounds</h2>
                  <p className="stats-number">{stats.by_prop_type.rebounds.win_rate}%</p>
                  <p className="stats-subtext">
                    {stats.by_prop_type.rebounds.wins}/{stats.by_prop_type.rebounds.total} Correct
                  </p>
                </div>

                <div className="stats-card">
                  <h2 className="stats-label">🎯 Assists</h2>
                  <p className="stats-number">{stats.by_prop_type.assists.win_rate}%</p>
                  <p className="stats-subtext">
                    {stats.by_prop_type.assists.wins}/{stats.by_prop_type.assists.total} Correct
                  </p>
                </div>
              </div>
            )}

            {/* View Mode Toggle */}
            <div className="flex gap-4 mb-6">
              <button
                onClick={() => setViewMode('active')}
                className={`px-6 py-3 rounded font-semibold transition-colors ${
                  viewMode === 'active' 
                    ? 'bg-[#ff9f1c] text-black' 
                    : 'bg-[#1a1a1a] text-white hover:bg-[#2a2a2a]'
                }`}
              >
                Active Picks ({filteredActivePicks.length})
              </button>
              <button
                onClick={() => setViewMode('history')}
                className={`px-6 py-3 rounded font-semibold transition-colors ${
                  viewMode === 'history' 
                    ? 'bg-[#ff9f1c] text-black' 
                    : 'bg-[#1a1a1a] text-white hover:bg-[#2a2a2a]'
                }`}
              >
                Completed Picks ({history.length})
              </button>
            </div>

            {/* Filters - Only show for history view */}
            {viewMode === 'history' && (
              <div className="flex gap-4 mb-6 flex-wrap">
                {/* Result Filter */}
                <div className="flex gap-2">
                  <button
                    onClick={() => setFilter('all')}
                    className={`px-4 py-2 rounded font-semibold transition-colors ${
                      filter === 'all' 
                        ? 'bg-[#ff9f1c] text-black' 
                        : 'bg-[#1a1a1a] text-white hover:bg-[#2a2a2a]'
                    }`}
                  >
                    All
                  </button>
                  <button
                    onClick={() => setFilter('won')}
                    className={`px-4 py-2 rounded font-semibold transition-colors ${
                      filter === 'won' 
                        ? 'bg-green-600 text-white' 
                        : 'bg-[#1a1a1a] text-white hover:bg-[#2a2a2a]'
                    }`}
                  >
                    Wins
                  </button>
                  <button
                    onClick={() => setFilter('lost')}
                    className={`px-4 py-2 rounded font-semibold transition-colors ${
                      filter === 'lost' 
                        ? 'bg-red-600 text-white' 
                        : 'bg-[#1a1a1a] text-white hover:bg-[#2a2a2a]'
                    }`}
                  >
                    Losses
                  </button>
                  <button
                    onClick={() => setFilter('push')}
                    className={`px-4 py-2 rounded font-semibold transition-colors ${
                      filter === 'push' 
                        ? 'bg-gray-600 text-white' 
                        : 'bg-[#1a1a1a] text-white hover:bg-[#2a2a2a]'
                    }`}
                  >
                    Pushes
                  </button>
                </div>

                {/* Prop Type Filter */}
                <div className="flex gap-2">
                  <button
                    onClick={() => setPropFilter('all')}
                    className={`px-4 py-2 rounded font-semibold transition-colors ${
                      propFilter === 'all' 
                        ? 'bg-[#ff9f1c] text-black' 
                        : 'bg-[#1a1a1a] text-white hover:bg-[#2a2a2a]'
                    }`}
                  >
                    All Props
                  </button>
                  <button
                    onClick={() => setPropFilter('points')}
                    className={`px-4 py-2 rounded font-semibold transition-colors ${
                      propFilter === 'points' 
                        ? 'bg-[#ff9f1c] text-black' 
                        : 'bg-[#1a1a1a] text-white hover:bg-[#2a2a2a]'
                    }`}
                  >
                    Points
                  </button>
                  <button
                    onClick={() => setPropFilter('rebounds')}
                    className={`px-4 py-2 rounded font-semibold transition-colors ${
                      propFilter === 'rebounds' 
                        ? 'bg-[#ff9f1c] text-black' 
                        : 'bg-[#1a1a1a] text-white hover:bg-[#2a2a2a]'
                    }`}
                  >
                    Rebounds
                  </button>
                  <button
                    onClick={() => setPropFilter('assists')}
                    className={`px-4 py-2 rounded font-semibold transition-colors ${
                      propFilter === 'assists' 
                        ? 'bg-[#ff9f1c] text-black' 
                        : 'bg-[#1a1a1a] text-white hover:bg-[#2a2a2a]'
                    }`}
                  >
                    Assists
                  </button>
                </div>
              </div>
            )}

            {/* Prop Type Filter for Active Picks */}
            {viewMode === 'active' && (
              <div className="flex gap-2 mb-6">
                <button
                  onClick={() => setPropFilter('all')}
                  className={`px-4 py-2 rounded font-semibold transition-colors ${
                    propFilter === 'all' 
                      ? 'bg-[#ff9f1c] text-black' 
                      : 'bg-[#1a1a1a] text-white hover:bg-[#2a2a2a]'
                  }`}
                >
                  All Props
                </button>
                <button
                  onClick={() => setPropFilter('points')}
                  className={`px-4 py-2 rounded font-semibold transition-colors ${
                    propFilter === 'points' 
                      ? 'bg-[#ff9f1c] text-black' 
                      : 'bg-[#1a1a1a] text-white hover:bg-[#2a2a2a]'
                  }`}
                >
                  Points
                </button>
                <button
                  onClick={() => setPropFilter('rebounds')}
                  className={`px-4 py-2 rounded font-semibold transition-colors ${
                    propFilter === 'rebounds' 
                      ? 'bg-[#ff9f1c] text-black' 
                      : 'bg-[#1a1a1a] text-white hover:bg-[#2a2a2a]'
                  }`}
                >
                  Rebounds
                </button>
                <button
                  onClick={() => setPropFilter('assists')}
                  className={`px-4 py-2 rounded font-semibold transition-colors ${
                    propFilter === 'assists' 
                      ? 'bg-[#ff9f1c] text-black' 
                      : 'bg-[#1a1a1a] text-white hover:bg-[#2a2a2a]'
                  }`}
                >
                  Assists
                </button>
              </div>
            )}

            {/* Active Picks View */}
            {viewMode === 'active' && (
              <div className="stats-card">
                <h2 className="stats-label mb-4">Active Picks</h2>
                
                {filteredActivePicks.length === 0 ? (
                  <div className="text-center text-gray-400 py-12">
                    <p>No active picks found</p>
                    <p className="text-sm mt-2">Go to the Predictions page to make some picks!</p>
                  </div>
                ) : (
                  <div className="space-y-3">
                    {filteredActivePicks.map((pick) => (
                      <div
                        key={pick.id}
                        className="bg-[#0a0a0a] p-4 rounded flex items-center justify-between hover:bg-[#1a1a1a] transition-colors"
                      >
                        {/* Pending Badge */}
                        <div className="w-16 h-16 rounded-full flex items-center justify-center bg-blue-600 text-white font-bold text-3xl">
                          ⏳
                        </div>

                        {/* Pick Details */}
                        <div className="flex-1 ml-4">
                          <div className="flex items-center gap-2 mb-1">
                            <span className="text-white font-semibold text-lg">{pick.player_name}</span>
                            <span className="text-gray-400 text-sm">
                              {pick.prop_type.charAt(0).toUpperCase() + pick.prop_type.slice(1)}
                            </span>
                          </div>
                          <div className="text-gray-400 text-sm">
                            {pick.game?.away_team || pick.away_team} @ {pick.game?.home_team || pick.home_team}
                          </div>
                        </div>

                        {/* Pick Info */}
                        <div className="flex items-center gap-8 text-center">
                          <div className="w-20">
                            <div className="text-gray-400 text-xs mb-1">Line</div>
                            <div className="text-white font-bold text-lg">{pick.line}</div>
                          </div>

                          <div className="w-20">
                            <div className="text-gray-400 text-xs mb-1">Pick</div>
                            <div className={`font-bold text-lg ${
                              pick.prediction === 'over' ? 'text-green-500' : 'text-red-500'
                            }`}>
                              {pick.prediction.toUpperCase()}
                            </div>
                          </div>

                          <div className="w-32">
                            <div className="text-gray-400 text-xs mb-1">Game Time</div>
                            <div className="text-[#ff9f1c] text-sm">
                              {formatDate(pick.game_date)}
                            </div>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            )}

            {/* Pick History View */}
            {viewMode === 'history' && (
              <div className="stats-card">
                <h2 className="stats-label mb-4">Completed Picks</h2>
                
                {history.length === 0 ? (
                  <div className="text-center text-gray-400 py-12">
                    <p>No completed picks yet</p>
                    <p className="text-sm mt-2">Your picks will appear here after games are completed</p>
                  </div>
                ) : (
                  <div className="space-y-3">
                    {history.map((pick) => (
                      <div
                        key={pick.id}
                        className="bg-[#0a0a0a] p-4 rounded flex items-center justify-between hover:bg-[#1a1a1a] transition-colors"
                      >
                        {/* Result Badge */}
                        <div className={`w-16 h-16 rounded-full flex items-center justify-center text-white font-bold text-3xl ${
                          getResultBadge(pick.result)
                        }`}>
                          {getResultIcon(pick.result)}
                        </div>

                        {/* Pick Details */}
                        <div className="flex-1 ml-4">
                          <div className="flex items-center gap-2 mb-1">
                            <span className="text-white font-semibold text-lg">{pick.player_name}</span>
                            <span className="text-gray-400 text-sm">
                              {pick.prop_type.charAt(0).toUpperCase() + pick.prop_type.slice(1)}
                            </span>
                          </div>
                          <div className="text-gray-400 text-sm">
                            {pick.game?.away_team || pick.away_team} @ {pick.game?.home_team || pick.home_team}
                          </div>
                        </div>

                        {/* Pick Info */}
                        <div className="flex items-center gap-8 text-center">
                          <div className="w-20">
                            <div className="text-gray-400 text-xs mb-1">Line</div>
                            <div className="text-white font-bold text-lg">{pick.line}</div>
                          </div>

                          <div className="w-20">
                            <div className="text-gray-400 text-xs mb-1">Pick</div>
                            <div className={`font-bold text-lg ${
                              pick.prediction === 'over' ? 'text-green-500' : 'text-red-500'
                            }`}>
                              {pick.prediction.toUpperCase()}
                            </div>
                          </div>

                          <div className="w-20">
                            <div className="text-gray-400 text-xs mb-1">Actual</div>
                            <div className="text-[#ff9f1c] font-bold text-lg">
                              {pick.actual_result ?? '--'}
                            </div>
                          </div>

                          <div className="w-32">
                            <div className="text-gray-400 text-xs mb-1">Completed</div>
                            <div className="text-gray-300 text-sm">
                              {formatDate(pick.completed_at)}
                            </div>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            )}

          </div>
        </main>
      </div>
    </ProtectedRoute>
  );
}