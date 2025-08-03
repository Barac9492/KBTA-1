import React, { useState, useEffect } from 'react';
import './dashboard.css';

const Dashboard = () => {
  const [status, setStatus] = useState('idle');
  const [trends, setTrends] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [lastUpdate, setLastUpdate] = useState(null);
  const [error, setError] = useState(null);

  const API_BASE = 'http://localhost:8000';

  // Fetch current status
  const fetchStatus = async () => {
    try {
      const response = await fetch(`${API_BASE}/status`);
      const data = await response.json();
      setStatus(data.last_status);
      setLastUpdate(data.last_run);
    } catch (err) {
      console.error('Error fetching status:', err);
    }
  };

  // Fetch trends data
  const fetchTrends = async () => {
    try {
      const response = await fetch(`${API_BASE}/trends`);
      if (response.ok) {
        const data = await response.json();
        setTrends(data.data);
        setError(null);
      } else {
        setError('No trend data available');
      }
    } catch (err) {
      setError('Failed to fetch trends');
      console.error('Error fetching trends:', err);
    }
  };

  // Trigger analysis
  const triggerAnalysis = async () => {
    setIsLoading(true);
    setError(null);
    
    try {
      const response = await fetch(`${API_BASE}/trigger`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          force_refresh: false,
          include_notion_push: true,
          analysis_type: 'full'
        }),
      });

      if (response.ok) {
        const data = await response.json();
        console.log('Analysis triggered:', data);
        
        // Poll for status updates
        pollStatus();
      } else {
        const errorData = await response.json();
        setError(errorData.detail || 'Failed to trigger analysis');
      }
    } catch (err) {
      setError('Failed to trigger analysis');
      console.error('Error triggering analysis:', err);
    } finally {
      setIsLoading(false);
    }
  };

  // Poll for status updates
  const pollStatus = () => {
    const interval = setInterval(async () => {
      await fetchStatus();
      
      if (status === 'completed' || status === 'failed') {
        clearInterval(interval);
        await fetchTrends();
      }
    }, 5000); // Poll every 5 seconds

    // Clear interval after 10 minutes
    setTimeout(() => clearInterval(interval), 600000);
  };

  // Initial load
  useEffect(() => {
    fetchStatus();
    fetchTrends();
  }, []);

  // Auto-refresh trends every 30 seconds
  useEffect(() => {
    const interval = setInterval(fetchTrends, 30000);
    return () => clearInterval(interval);
  }, []);

  const getStatusColor = (status) => {
    switch (status) {
      case 'completed': return 'green';
      case 'failed': return 'red';
      case 'started': return 'blue';
      case 'webhook_triggered': return 'purple';
      default: return 'gray';
    }
  };

  const getStatusIcon = (status) => {
    switch (status) {
      case 'completed': return '✅';
      case 'failed': return '❌';
      case 'started': return '🔄';
      case 'webhook_triggered': return '🔗';
      default: return '⏸️';
    }
  };

  return (
    <div className="dashboard">
      <header className="dashboard-header">
        <h1>K-Beauty Trend Agent</h1>
        <p>Intelligent trend analysis and synthesis for Korean beauty market</p>
      </header>

      <div className="dashboard-grid">
        {/* Status Card */}
        <div className="card status-card">
          <h2>System Status</h2>
          <div className="status-indicator">
            <span className={`status-badge ${getStatusColor(status)}`}>
              {getStatusIcon(status)} {status}
            </span>
          </div>
          {lastUpdate && (
            <p className="last-update">
              Last run: {new Date(lastUpdate).toLocaleString()}
            </p>
          )}
          <button 
            onClick={triggerAnalysis}
            disabled={isLoading || status === 'started'}
            className="trigger-button"
          >
            {isLoading ? 'Running...' : 'Trigger Analysis'}
          </button>
        </div>

        {/* Quick Stats */}
        <div className="card stats-card">
          <h2>Quick Stats</h2>
          {trends ? (
            <div className="stats-grid">
              <div className="stat">
                <span className="stat-number">
                  {trends.trend_analysis?.trends?.length || 0}
                </span>
                <span className="stat-label">Trends Identified</span>
              </div>
              <div className="stat">
                <span className="stat-number">
                  {trends.synthesis_results?.priority_trends?.length || 0}
                </span>
                <span className="stat-label">Priority Trends</span>
              </div>
              <div className="stat">
                <span className="stat-number">
                  {trends.synthesis_results?.market_opportunities?.length || 0}
                </span>
                <span className="stat-label">Market Opportunities</span>
              </div>
            </div>
          ) : (
            <p>No data available</p>
          )}
        </div>

        {/* Recent Trends */}
        <div className="card trends-card">
          <h2>Recent Trends</h2>
          {trends?.trend_analysis?.trends ? (
            <div className="trends-list">
              {trends.trend_analysis.trends.slice(0, 5).map((trend, index) => (
                <div key={index} className="trend-item">
                  <div className="trend-header">
                    <h3>{trend.trend_name}</h3>
                    <span className={`trend-type ${trend.trend_type}`}>
                      {trend.trend_type}
                    </span>
                  </div>
                  <p className="trend-description">{trend.description}</p>
                  <div className="trend-meta">
                    <span className="trend-category">{trend.category}</span>
                    <span className="trend-confidence">
                      Confidence: {Math.round(trend.confidence * 100)}%
                    </span>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <p>No trends available</p>
          )}
        </div>

        {/* Priority Trends */}
        <div className="card priority-card">
          <h2>Priority Trends</h2>
          {trends?.synthesis_results?.priority_trends ? (
            <div className="priority-list">
              {trends.synthesis_results.priority_trends.slice(0, 3).map((trend, index) => (
                <div key={index} className="priority-item">
                  <div className="priority-rank">#{trend.rank}</div>
                  <div className="priority-content">
                    <h3>{trend.trend_name}</h3>
                    <div className="priority-meta">
                      <span className={`impact-badge ${trend.business_impact}`}>
                        {trend.business_impact} impact
                      </span>
                      <span className="time-to-market">
                        {trend.time_to_market}
                      </span>
                    </div>
                    <p className="target-audience">
                      Target: {trend.target_audience}
                    </p>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <p>No priority trends available</p>
          )}
        </div>

        {/* Market Opportunities */}
        <div className="card opportunities-card">
          <h2>Market Opportunities</h2>
          {trends?.synthesis_results?.market_opportunities ? (
            <div className="opportunities-list">
              {trends.synthesis_results.market_opportunities.slice(0, 3).map((opp, index) => (
                <div key={index} className="opportunity-item">
                  <h3>{opp.opportunity}</h3>
                  <div className="opportunity-meta">
                    <span className="opportunity-size">Size: {opp.size}</span>
                    <span className="opportunity-barriers">
                      Barriers: {opp.barriers}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <p>No market opportunities available</p>
          )}
        </div>

        {/* Error Display */}
        {error && (
          <div className="card error-card">
            <h2>Error</h2>
            <p className="error-message">{error}</p>
            <button onClick={fetchTrends} className="retry-button">
              Retry
            </button>
          </div>
        )}
      </div>

      {/* Footer */}
      <footer className="dashboard-footer">
        <p>
          K-Beauty Trend Agent Dashboard | 
          Last updated: {lastUpdate ? new Date(lastUpdate).toLocaleString() : 'Never'}
        </p>
      </footer>
    </div>
  );
};

export default Dashboard; 