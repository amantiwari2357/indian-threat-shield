# Custom SIEM Tool

A company-branded, open-source SIEM (Security Information and Event Management) tool inspired by Wazuh. This tool provides comprehensive security monitoring, threat detection, alerting, and visualization capabilities.

## 🚀 Features

### Core Features
- **Multi-platform agent support** (Linux, Windows, macOS)
- **Real-time and batch log collection**
- **Rule-based alert generation**
- **Interactive dashboard** with filters and graphs
- **Alert response integrations** (Email, Webhook, Slack)
- **Role-based access control**
- **Compliance rules** (PCI-DSS, HIPAA, GDPR)

### Advanced Features
- **Machine learning-based anomaly detection**
- **Geo-location alert tagging**
- **MITRE ATT&CK matrix mapping**
- **Scheduled reporting**
- **File integrity monitoring**
- **Vulnerability assessment**

## 🏗️ Architecture

```
[Agent] --> [Log Collector] --> [Processing Engine + Rule Engine] --> [Indexer (Elasticsearch/OpenSearch)] --> [Dashboard/API Layer]
```

### Components
- **Agent (Client-Side)**: Deployed on monitored machines
- **Log Collector**: Handles ingestion of raw logs
- **Processing Engine**: Parses logs and applies rules
- **Indexer**: Stores alerts and searchable logs
- **Dashboard**: Provides user interface and APIs

## 🛠️ Technology Stack

| Component | Technology |
|-----------|------------|
| Agent | Go / Rust |
| Log Ingestion | Fluent Bit / Kafka / Logstash |
| Rule Engine | Java (Spring Boot) |
| Storage | Elasticsearch / OpenSearch |
| Dashboard (Frontend) | HTML, CSS, JavaScript |
| API/Backend | Java (Spring Boot for RESTful APIs) |
| Authentication | JWT / Spring Security / OAuth2 |
| Deployment | Docker + Kubernetes |

## 📁 Project Structure

```
custom-siem/
├── agent/                  # Go-based log sender
├── backend-api/            # Java Spring Boot API
├── dashboard/              # HTML, CSS, JavaScript frontend
├── rules/                  # Rule definitions (YAML/JSON)
├── docker-compose.yml      # Local dev environment
├── deploy/                 # Kubernetes manifests
├── docs/                   # Markdown documentation
└── branding/               # Logos, color schemes
```

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose
- Java 17+
- Go 1.21+
- Node.js 18+

### Local Development Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd custom-siem
   ```

2. **Start the development environment**
   ```bash
   docker-compose up -d
   ```

3. **Access the dashboard**
   - Open http://localhost:8080
   - Default credentials: admin/admin

4. **Deploy an agent**
   ```bash
   # Linux
   ./agent/install.sh
   
   # Windows
   .\agent\install.ps1
   ```

## 📚 Documentation

### Developer Documentation
1. [System Overview](docs/developer/system-overview.md)
2. [Architecture Diagrams](docs/developer/architecture.md)
3. [Technology Versions](docs/developer/tech-stack.md)
4. [Setup Guide](docs/developer/setup.md)
5. [Module Descriptions](docs/developer/modules.md)
6. [Agent Integration](docs/developer/agent-integration.md)
7. [Rule Engine Guide](docs/developer/rule-engine.md)
8. [API Documentation](docs/developer/api.md)
9. [Logging and Monitoring](docs/developer/logging.md)
10. [CI/CD Guidelines](docs/developer/cicd.md)

### User Documentation
1. [Product Introduction](docs/user/introduction.md)
2. [Installing and Configuring the Agent](docs/user/agent-setup.md)
3. [Viewing Logs and Alerts](docs/user/logs-alerts.md)
4. [Dashboard Filters and Queries](docs/user/dashboard.md)
5. [Creating and Managing Rules](docs/user/rules.md)
6. [Responding to Alerts](docs/user/alert-response.md)
7. [Admin Panel Usage](docs/user/admin.md)
8. [Generating Reports](docs/user/reports.md)
9. [Troubleshooting](docs/user/troubleshooting.md)
10. [FAQs](docs/user/faq.md)

## 🎨 Branding Guidelines

- Custom tool name and logo
- White-label dashboard
- Dark and light theme options
- Custom footer in reports
- Consistent typography and spacing

## 🔧 Development Timeline (MVP)

| Week | Milestone |
|------|-----------|
| 1 | Finalize architecture and tech stack |
| 2 | Build basic log collection agent |
| 3 | Set up log collector and backend API |
| 4 | Develop simple rule engine |
| 5 | Index data in Elasticsearch/OpenSearch |
| 6 | Build alert generation and storage module |
| 7 | Develop basic dashboard with filters |
| 8 | Implement authentication and role control |
| 9 | Set up alert integrations (Slack, Email) |
| 10 | Final testing and deployment |

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- 📧 Email: support@custom-siem.com
- 💬 Slack: [Join our community](https://custom-siem.slack.com)
- 📖 Documentation: [docs.custom-siem.com](https://docs.custom-siem.com)
- 🐛 Issues: [GitHub Issues](https://github.com/your-org/custom-siem/issues)

## 🔒 Security

Please report security issues to security@custom-siem.com instead of using the GitHub issue tracker.

---

**Custom SIEM Tool** - Empowering organizations with comprehensive security monitoring and threat detection capabilities. 