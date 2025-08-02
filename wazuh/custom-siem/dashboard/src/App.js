import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [healthStatus, setHealthStatus] = useState(null);
  const [agents, setAgents] = useState([]);
  const [alerts, setAlerts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('dashboard');
  const [selectedAgent, setSelectedAgent] = useState(null);

  const API_BASE = '/api/v1';

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      console.log('Fetching data from:', API_BASE);
      
      // Fetch health status
      const healthResponse = await fetch(`${API_BASE}/health`);
      if (!healthResponse.ok) {
        throw new Error(`Health check failed: ${healthResponse.status}`);
      }
      const healthData = await healthResponse.json();
      setHealthStatus(healthData);
      console.log('Health data:', healthData);

      // Fetch agents
      const agentsResponse = await fetch(`${API_BASE}/agents`);
      if (!agentsResponse.ok) {
        throw new Error(`Agents fetch failed: ${agentsResponse.status}`);
      }
      const agentsData = await agentsResponse.json();
      setAgents(agentsData);
      console.log('Agents data:', agentsData);

      // Fetch alerts stats
      const alertsResponse = await fetch(`${API_BASE}/alerts/stats`);
      if (!alertsResponse.ok) {
        throw new Error(`Alerts stats fetch failed: ${alertsResponse.status}`);
      }
      const alertsData = await alertsResponse.json();
      setAlerts(alertsData);
      console.log('Alerts data:', alertsData);

      setLoading(false);
    } catch (error) {
      console.error('Error fetching data:', error);
      setLoading(false);
    }
  };

  const renderDashboard = () => (
    <div className="dashboard-grid">
      {/* Key Metrics */}
      <div className="metrics-row">
        <div className="metric-card">
          <h3>Total Alerts</h3>
          <div className="metric-value">{alerts.totalAlerts || 0}</div>
        </div>
        <div className="metric-card">
          <h3>Critical Alerts</h3>
          <div className="metric-value critical">{alerts.criticalAlerts || 0}</div>
        </div>
        <div className="metric-card">
          <h3>Active Agents</h3>
          <div className="metric-value">{agents.filter(a => a.status === 'ACTIVE').length}</div>
        </div>
        <div className="metric-card">
          <h3>Total Agents</h3>
          <div className="metric-value">{agents.length}</div>
        </div>
      </div>

      {/* Charts Row */}
      <div className="charts-row">
        <div className="chart-card">
          <h3>Alert Level Evolution</h3>
          <div className="chart-placeholder">
            <div className="chart-line"></div>
            <div className="chart-line"></div>
            <div className="chart-line"></div>
          </div>
        </div>
        <div className="chart-card">
          <h3>Top 5 Agents</h3>
          <div className="chart-placeholder">
            <div className="donut-chart">
              <div className="donut-segment" style={{transform: 'rotate(0deg)', background: '#ff6b6b'}}></div>
              <div className="donut-segment" style={{transform: 'rotate(72deg)', background: '#4ecdc4'}}></div>
              <div className="donut-segment" style={{transform: 'rotate(144deg)', background: '#45b7d1'}}></div>
              <div className="donut-segment" style={{transform: 'rotate(216deg)', background: '#96ceb4'}}></div>
              <div className="donut-segment" style={{transform: 'rotate(288deg)', background: '#feca57'}}></div>
            </div>
          </div>
        </div>
      </div>

      {/* MITRE ATT&CK */}
      <div className="chart-card full-width">
        <h3>Top MITRE ATT&CK Techniques</h3>
        <div className="mitre-tactics">
          <div className="tactic-item">
            <span className="tactic-name">Lateral Movement</span>
            <span className="tactic-count">207</span>
          </div>
          <div className="tactic-item">
            <span className="tactic-name">Credential Access</span>
            <span className="tactic-count">84</span>
          </div>
          <div className="tactic-item">
            <span className="tactic-name">Collection</span>
            <span className="tactic-count">57</span>
          </div>
          <div className="tactic-item">
            <span className="tactic-name">Impact</span>
            <span className="tactic-count">57</span>
          </div>
          <div className="tactic-item">
            <span className="tactic-name">Initial Access</span>
            <span className="tactic-count">32</span>
          </div>
        </div>
      </div>

      {/* Recent Alerts Table */}
      <div className="chart-card full-width">
        <h3>Recent Security Alerts</h3>
        <div className="alerts-table">
          <table>
            <thead>
              <tr>
                <th>Time</th>
                <th>Agent</th>
                <th>Technique</th>
                <th>Tactic</th>
                <th>Description</th>
                <th>Level</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td>Jan 24, 2022 @ 09:39:10</td>
                <td>Windows (006)</td>
                <td>T1190</td>
                <td>Initial Access</td>
                <td>GitHub Organization update member repository creation permission</td>
                <td><span className="alert-level level-7">7</span></td>
              </tr>
              <tr>
                <td>Jan 24, 2022 @ 09:38:45</td>
                <td>RHEL7 (001)</td>
                <td>T1114</td>
                <td>Collection</td>
                <td>Host-based anomaly detection event (rootcheck)</td>
                <td><span className="alert-level level-5">5</span></td>
              </tr>
              <tr>
                <td>Jan 24, 2022 @ 09:38:22</td>
                <td>ubuntu_web_server (003)</td>
                <td>T1071</td>
                <td>Command and Control</td>
                <td>Apache: Attempt to access forbidden directory index</td>
                <td><span className="alert-level level-8">8</span></td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );

  const renderAgents = () => (
    <div className="agents-page">
      <div className="agents-header">
        <h2>Agents ({agents.length})</h2>
        <div className="agents-actions">
          <button className="btn-primary">+ Deploy new agent</button>
          <button className="btn-secondary">Export formatted</button>
        </div>
      </div>

      <div className="agents-stats">
        <div className="stat-card">
          <div className="stat-title">Active</div>
          <div className="stat-value">{agents.filter(a => a.status === 'ACTIVE').length}</div>
        </div>
        <div className="stat-card">
          <div className="stat-title">Disconnected</div>
          <div className="stat-value">{agents.filter(a => a.status === 'DISCONNECTED').length}</div>
        </div>
        <div className="stat-card">
          <div className="stat-title">Never Connected</div>
          <div className="stat-value">{agents.filter(a => a.status === 'NEVER_CONNECTED').length}</div>
        </div>
      </div>

      <div className="agents-table">
        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>Name</th>
              <th>IP</th>
              <th>Group(s)</th>
              <th>OS</th>
              <th>Status</th>
              <th>Last Keep Alive</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {agents.length === 0 ? (
              <tr>
                <td colSpan="8" className="no-data">No agents registered</td>
              </tr>
            ) : (
              agents.map((agent, index) => (
                <tr key={agent.agentId || index}>
                  <td>{String(index + 1).padStart(3, '0')}</td>
                  <td>{agent.name || `Agent-${index + 1}`}</td>
                  <td>{agent.ipAddress || 'N/A'}</td>
                  <td>{agent.groups || 'default'}</td>
                  <td>{agent.platform || 'Unknown'}</td>
                  <td>
                    <span className={`status-dot ${agent.status === 'ACTIVE' ? 'online' : 'offline'}`}></span>
                    {agent.status || 'UNKNOWN'}
                  </td>
                  <td>{agent.lastHeartbeat ? new Date(agent.lastHeartbeat).toLocaleString() : 'Never'}</td>
                  <td>
                    <button className="btn-icon" onClick={() => setSelectedAgent(agent)}>👁️</button>
                    <button className="btn-icon">⚙️</button>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  );

  const renderModules = () => (
    <div className="modules-page">
      <div className="modules-header">
        <h2>Wazuh Modules</h2>
        <div className="modules-stats">
          <div className="stat-item">
            <span className="stat-label">Total agents:</span>
            <span className="stat-value">{agents.length}</span>
          </div>
          <div className="stat-item">
            <span className="stat-label">Active agents:</span>
            <span className="stat-value">{agents.filter(a => a.status === 'ACTIVE').length}</span>
          </div>
          <div className="stat-item">
            <span className="stat-label">Disconnected agents:</span>
            <span className="stat-value">{agents.filter(a => a.status === 'DISCONNECTED').length}</span>
          </div>
          <div className="stat-item">
            <span className="stat-label">Never connected agents:</span>
            <span className="stat-value">{agents.filter(a => a.status === 'NEVER_CONNECTED').length}</span>
          </div>
        </div>
      </div>

      <div className="modules-grid">
        {/* Security Information Management */}
        <div className="module-category">
          <h3>SECURITY INFORMATION MANAGEMENT</h3>
          <div className="module-cards">
            <div className="module-card">
              <div className="module-icon">📊</div>
              <h4>Security events</h4>
              <p>Browse through your security alerts, identifying issues and threats in your environment.</p>
            </div>
            <div className="module-card">
              <div className="module-icon">🔍</div>
              <h4>Integrity monitoring</h4>
              <p>Alerts related to file changes, including permissions, content, ownership and attributes.</p>
            </div>
            <div className="module-card">
              <div className="module-icon">☁️</div>
              <h4>Amazon AWS</h4>
              <p>Security events related to your Amazon AWS services, collected directly via AWS API.</p>
            </div>
            <div className="module-card">
              <div className="module-icon">📧</div>
              <h4>Office 365</h4>
              <p>Security events related to your Office 365 services.</p>
            </div>
            <div className="module-card">
              <div className="module-icon">🌐</div>
              <h4>Google Cloud Platform</h4>
              <p>Security events related to your Google Cloud Platform services, collected directly via GCP API.</p>
            </div>
            <div className="module-card">
              <div className="module-icon">🐙</div>
              <h4>GitHub</h4>
              <p>Monitoring events from audit logs of your GitHub organizations.</p>
            </div>
          </div>
        </div>

        {/* Auditing and Policy Monitoring */}
        <div className="module-category">
          <h3>AUDITING AND POLICY MONITORING</h3>
          <div className="module-cards">
            <div className="module-card">
              <div className="module-icon">📋</div>
              <h4>Policy monitoring</h4>
              <p>Verify that your systems are configured according to your security policies baseline.</p>
            </div>
            <div className="module-card">
              <div className="module-icon">💓</div>
              <h4>System auditing</h4>
              <p>Audit users behavior, monitoring command execution and alerting on access to critical files.</p>
            </div>
            <div className="module-card">
              <div className="module-icon">🛡️</div>
              <h4>OpenSCAP</h4>
              <p>Configuration assessment and automation of compliance monitoring using SCAP checks.</p>
            </div>
            <div className="module-card">
              <div className="module-icon">🔒</div>
              <h4>CIS-CAT</h4>
              <p>Configuration assessment using Center of Internet Security scanner and SCAP checks.</p>
            </div>
            <div className="module-card">
              <div className="module-icon">✅</div>
              <h4>Security configuration assessment</h4>
              <p>Scan your assets as part of a configuration assessment audit.</p>
            </div>
          </div>
        </div>

        {/* Threat Detection and Response */}
        <div className="module-category">
          <h3>THREAT DETECTION AND RESPONSE</h3>
          <div className="module-cards">
            <div className="module-card">
              <div className="module-icon">🕳️</div>
              <h4>Vulnerabilities</h4>
              <p>Discover what applications in your environment are affected by well-known vulnerabilities.</p>
            </div>
            <div className="module-card">
              <div className="module-icon">🦠</div>
              <h4>VirusTotal</h4>
              <p>Alerts resulting from VirusTotal analysis of suspicious files via an integration with their API.</p>
            </div>
            <div className="module-card">
              <div className="module-icon">🔎</div>
              <h4>Osquery</h4>
              <p>Osquery can be used to expose an operating system as a high-performance relational database.</p>
            </div>
            <div className="module-card">
              <div className="module-icon">🐳</div>
              <h4>Docker listener</h4>
              <p>Monitor and collect the activity from Docker containers such as creation, running, starting, stopping or pausing events.</p>
            </div>
            <div className="module-card">
              <div className="module-icon">🎯</div>
              <h4>MITRE ATT&CK</h4>
              <p>Security events from the knowledge base of adversary tactics and techniques based on real-world observations.</p>
            </div>
          </div>
        </div>

        {/* Regulatory Compliance */}
        <div className="module-category">
          <h3>REGULATORY COMPLIANCE</h3>
          <div className="module-cards">
            <div className="module-card">
              <div className="module-icon">💳</div>
              <h4>PCI DSS</h4>
              <p>Global security standard for entities that process, store or transmit payment cardholder data.</p>
            </div>
            <div className="module-card">
              <div className="module-icon">🏛️</div>
              <h4>NIST 800-53</h4>
              <p>National Institute of Standards and Technology Special Publication 800-53 (NIST 800-53) sets guidelines for federal information systems.</p>
            </div>
            <div className="module-card">
              <div className="module-icon">🔐</div>
              <h4>TSC</h4>
              <p>Trust Services Criteria for Security, Availability, Processing Integrity, Confidentiality, and Privacy.</p>
            </div>
            <div className="module-card">
              <div className="module-icon">🇪🇺</div>
              <h4>GDPR</h4>
              <p>General Data Protection Regulation (GDPR) sets guidelines for processing of personal data.</p>
            </div>
            <div className="module-card">
              <div className="module-icon">🏥</div>
              <h4>HIPAA</h4>
              <p>Health Insurance Portability and Accountability Act of 1996 (HIPAA) provides data privacy and security provisions for safeguarding medical information.</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );

  if (loading) {
    return (
      <div className="App">
        <div className="loading">
          <h2>Loading Custom SIEM Dashboard...</h2>
        </div>
      </div>
    );
  }

  return (
    <div className="App">
      <header className="App-header">
        <div className="header-left">
          <h1>wazuh.</h1>
          <nav className="main-nav">
            <button 
              className={`nav-btn ${activeTab === 'dashboard' ? 'active' : ''}`}
              onClick={() => setActiveTab('dashboard')}
            >
              Dashboard
            </button>
            <button 
              className={`nav-btn ${activeTab === 'agents' ? 'active' : ''}`}
              onClick={() => setActiveTab('agents')}
            >
              Agents
            </button>
            <button 
              className={`nav-btn ${activeTab === 'modules' ? 'active' : ''}`}
              onClick={() => setActiveTab('modules')}
            >
              Modules
            </button>
          </nav>
        </div>
        <div className="header-right">
          <div className="status-indicator">
            <span className={`status-dot ${healthStatus?.status === 'UP' ? 'online' : 'offline'}`}></span>
            <span>API: {healthStatus?.status || 'Unknown'}</span>
          </div>
          <button className="btn-secondary">API</button>
          <button className="btn-secondary">default</button>
          <button className="btn-icon">🔍</button>
          <button className="btn-icon">📊</button>
        </div>
      </header>

      <main className="App-main">
        {activeTab === 'dashboard' && renderDashboard()}
        {activeTab === 'agents' && renderAgents()}
        {activeTab === 'modules' && renderModules()}
      </main>
    </div>
  );
}

export default App; 