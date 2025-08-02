# TMEN SIEM - Security Information and Event Management

## Overview
TMEN SIEM is a comprehensive security monitoring and threat detection system developed by TMEN GROUP. This tool provides real-time security monitoring, log analysis, threat detection, and compliance management.

## Features

### 🔒 Security Monitoring
- Real-time system metrics monitoring
- Security log collection and analysis
- Threat detection and alerting
- Network threat intelligence
- File integrity monitoring

### 📊 Dashboard & Analytics
- Interactive security dashboard
- Real-time charts and metrics
- Alert level visualization
- Agent status monitoring
- MITRE ATT&CK framework integration

### 🛡️ Threat Management
- Automated threat detection
- Security rule engine
- Alert correlation
- Incident response tracking
- Compliance monitoring

### 👥 User Management
- Role-based access control
- Admin, Analyst, and Viewer roles
- Secure authentication
- Audit logging

## Quick Start

### Prerequisites
- Python 3.7 or higher
- Windows/Linux/macOS

### Installation & Setup

1. **Navigate to the wazuh folder:**
   ```bash
   cd wazuh
   ```

2. **Run the TMEN SIEM system:**
   ```bash
   # On Windows
   run_tmen_siem.bat
   
   # On Linux/macOS
   python tmen_siem_backend.py
   ```

3. **Access the dashboard:**
   - Backend API: http://localhost:5000
   - Frontend Dashboard: Open `tmen_siem_dashboard.html` in your browser

## API Endpoints

### System Metrics
- `GET /api/system/metrics` - Get real-time system metrics

### Security Logs
- `GET /api/logs` - Get security logs
- `GET /api/logs/generate` - Generate new security logs

### Alerts
- `GET /api/alerts` - Get security alerts
- `GET /api/alerts/<alert_id>` - Get specific alert

### Network Threats
- `GET /api/network/threats` - Get network threats

### Agents
- `GET /api/agents` - Get agent status

### Dashboard
- `GET /api/dashboard/overview` - Get dashboard overview

## Dashboard Sections

### 1. Dashboard Overview
- System metrics and KPIs
- Real-time charts and visualizations
- Recent security alerts
- Top agents and threats

### 2. Alert Management
- Security alert monitoring
- Alert filtering and search
- Alert status management
- Incident response tracking

### 3. Log Management
- Security log collection
- Log analysis and search
- Log level filtering
- Log export capabilities

### 4. Agent Management
- Agent status monitoring
- Agent configuration
- Agent deployment
- Performance metrics

### 5. Threat Intelligence
- Threat feed integration
- Threat categorization
- Threat analysis
- Threat response

### 6. Compliance Center
- Compliance framework support
- Audit trail management
- Compliance reporting
- Regulatory requirements

### 7. Security Modules
- Module status monitoring
- Module configuration
- Module performance
- Module updates

## Technology Stack

### Backend
- **Python 3.7+** - Core programming language
- **Flask** - Web framework for API
- **psutil** - System metrics collection
- **Threading** - Background processing

### Frontend
- **HTML5/CSS3** - User interface
- **JavaScript** - Interactive functionality
- **Chart.js** - Data visualization
- **Real-time updates** - Live data integration

### Security Features
- **MITRE ATT&CK** - Threat framework integration
- **Rule Engine** - Automated threat detection
- **Log Analysis** - Security event processing
- **Alert Correlation** - Intelligent alerting

## Configuration

### Backend Configuration
The backend automatically generates simulated security data for demonstration purposes. In a production environment, you would:

1. Configure real log sources
2. Set up actual agent connections
3. Configure real threat feeds
4. Set up proper authentication

### Frontend Configuration
The frontend connects to the backend API at `http://localhost:5000`. To change this:

1. Edit the `API_BASE` variable in the JavaScript code
2. Update the backend URL in the fetch functions

## Development

### Project Structure
            ```
            wazuh/
            ├── tmen_siem_complete.html     # Complete dashboard with all 7 sections
            ├── tmen_siem_dashboard.html    # Basic dashboard interface
            ├── tmen_siem_backend.py        # Backend API server
            ├── requirements.txt            # Python dependencies
            ├── run_tmen_siem.bat          # Windows startup script
            └── README_TMEN_SIEM.md        # This documentation
            ```

### Adding New Features
1. **Backend**: Add new API endpoints in `tmen_siem_backend.py`
2. **Frontend**: Add new sections in `tmen_siem_dashboard.html`
3. **Integration**: Connect frontend to backend APIs

## Security Considerations

### Production Deployment
- Use HTTPS for all communications
- Implement proper authentication
- Configure firewall rules
- Set up monitoring and alerting
- Regular security updates

### Data Protection
- Encrypt sensitive data
- Implement access controls
- Regular backup procedures
- Audit logging

## Support

For technical support or feature requests, contact TMEN GROUP.

## License

This project is developed by TMEN GROUP for internal use and demonstration purposes.

---

**TMEN GROUP** - Advanced Security Solutions
*Security Information & Event Management* 