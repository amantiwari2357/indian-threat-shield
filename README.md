# TMEN SIEM - Security Information and Event Management

## 🚀 Quick Start

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

## 📁 Project Structure

```
TMEN/
├── wazuh/                          # Main TMEN SIEM Application
│   ├── tmen_siem_dashboard.html    # Main dashboard interface
│   ├── tmen_siem_backend.py        # Backend API server
│   ├── requirements.txt            # Python dependencies
│   ├── run_tmen_siem.bat          # Windows startup script
│   └── README_TMEN_SIEM.md        # Detailed documentation
├── fix_git_and_organize.bat        # Git organization script
└── README.md                       # This file
```

## 🔧 Git Organization

To fix the Git submodule issue and organize the project:

1. **Run the organization script:**
   ```bash
   fix_git_and_organize.bat
   ```

This will:
- Remove the Git submodule tracking from the wazuh folder
- Add all files as regular Git files
- Commit and push the organized structure
- Remove the arrow icon from the wazuh folder

## 🛡️ TMEN SIEM Features

### Security Monitoring
- Real-time system metrics monitoring
- Security log collection and analysis
- Threat detection and alerting
- Network threat intelligence
- File integrity monitoring

### Dashboard & Analytics
- Interactive security dashboard
- Real-time charts and metrics
- Alert level visualization
- Agent status monitoring
- MITRE ATT&CK framework integration

### Threat Management
- Automated threat detection
- Security rule engine
- Alert correlation
- Incident response tracking
- Compliance monitoring

## 📊 Dashboard Sections

1. **Dashboard Overview** - System metrics and KPIs
2. **Alert Management** - Security alert monitoring
3. **Log Management** - Security log collection
4. **Agent Management** - Agent status monitoring
5. **Threat Intelligence** - Threat feed integration
6. **Compliance Center** - Compliance framework support
7. **Security Modules** - Module status monitoring

## 🔌 API Endpoints

- `GET /api/system/metrics` - Get real-time system metrics
- `GET /api/logs` - Get security logs
- `GET /api/alerts` - Get security alerts
- `GET /api/network/threats` - Get network threats
- `GET /api/agents` - Get agent status
- `GET /api/dashboard/overview` - Get dashboard overview

## 🛠️ Technology Stack

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

## 📖 Documentation

For detailed documentation, see:
- `wazuh/README_TMEN_SIEM.md` - Complete project documentation

## 🚀 Running the System

1. **Navigate to the wazuh folder:**
   ```bash
   cd wazuh
   ```

2. **Run the system:**
   ```bash
   run_tmen_siem.bat
   ```

3. **Access the dashboard:**
   - The backend will start on http://localhost:5000
   - The frontend will open automatically in your browser

## 🔧 Troubleshooting

### Python Not Found
If you get "Python was not found" error:
1. Install Python 3.7+ from https://python.org
2. Make sure Python is added to PATH during installation
3. Restart your terminal/command prompt

### Git Submodule Arrow
If the wazuh folder shows an arrow icon:
1. Run `fix_git_and_organize.bat`
2. This will remove the submodule tracking

## 📞 Support

For technical support or feature requests, contact TMEN GROUP.

---

**TMEN GROUP** - Advanced Security Solutions
*Security Information & Event Management*

---

## 🎯 Mission

TMEN SIEM provides comprehensive security monitoring and threat detection capabilities, enabling organizations to protect their digital assets with advanced security analytics and real-time threat intelligence. 