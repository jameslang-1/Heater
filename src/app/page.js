import Image from "next/image";
import Link from "next/link";

export default function Home() {
  return (
    <div>
      {/*
      <div className="dashboard-container">
        <aside className="sidebar">
          <h2 className="sidebar-title">My Leagues</h2>
          <div className="league-list">
            <div className="league-item league-item-selected">
              <span>Main League</span>
            </div>
            <div className="league-item">
              <span>Friends League</span>
            </div>
            <div className="league-item">
              <span>Work League</span>
            </div>
          </div>
        </aside>
      </div>
      */}

      {/* Main Content Area */}
      <main className="main-content">
        <div className="content-wrapper">
          
          <div className="stats-grid">
            {/* Overall Record Card */}
            <div className="stats-card">
              <h2 className="stats-label">Overall Record</h2>
              <p className="stats-number">24-16</p>
              <p className="stats-subtext">60% Win Rate</p>
            </div>

            {/* This Week Card */}
            <div className="stats-card">
              <h2 className="stats-label">This Week</h2>
              <p className="stats-number">5-3</p>
              <p className="stats-subtext">Week 10</p>
            </div>

            {/* League Standings Card */}
            <div className="stats-card">
              <h2 className="stats-label">League Standings</h2>
              <div className="standings-list">
                
                {/* Rank 1 */}
                <div className="standings-row">
                  <span className="standings-rank">#1</span>
                  <span className="standings-name">The GOAT</span>
                  <span className="standings-record">69-0</span>
                  <span className="standings-streak streak-win">W5</span>
                </div>

                {/* Highlited for effect */}
                <div className="standings-row standings-row-user">
                  <span className="standings-rank">#2</span>
                  <span className="standings-name">You</span>
                  <span className="standings-record">67-67</span>
                  <span className="standings-streak streak-win">W2</span>
                </div>

                {/* Rank 3 */}
                <div className="standings-row">
                  <span className="standings-rank">#3</span>
                  <span className="standings-name">Ris</span>
                  <span className="standings-record">17-38</span>
                  <span className="standings-streak streak-loss">L1</span>
                </div>

                {/* Rank 4 */}
                <div className="standings-row">
                  <span className="standings-rank">#4</span>
                  <span className="standings-name">China</span>
                  <span className="standings-record">20-58</span>
                  <span className="standings-streak streak-loss">L9</span>
                </div>

                {/* Rank 5 */}
                <div className="standings-row">
                  <span className="standings-rank">#5</span>
                  <span className="standings-name">Saturdays</span>
                  <span className="standings-record">41-15</span>
                  <span className="standings-streak streak-win">W5</span>
                </div>
              </div>
            </div>

          </div>

        </div>
      </main>
    </div>
  );
}