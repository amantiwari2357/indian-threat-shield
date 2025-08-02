#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TMEN SIEM - Security Information and Event Management
TMEN GROUP - Custom SIEM Tool Development
"""
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import psutil
import random
import time
import threading
import json
import uuid
from datetime import datetime, timedelta
import os
import re
from collections import defaultdict

app = Flask(__name__)
CORS(app)

class TMENSIEM:
    def __init__(self):
        self.security_events = []
        self.system_metrics = {}
        self.network_threats = []
        self.file_changes = []
        self.logs = []
        self.alerts = []
        self.rules = self.load_rules()
        self.agents = {}
        self.users = {
            'admin': {'password': 'admin123', 'role': 'admin'},
            'analyst': {'password': 'analyst123', 'role': 'analyst'},
            'viewer': {'password': 'viewer123', 'role': 'viewer'}
        }

    def get_system_metrics(self):
        """Get real-time system metrics"""
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            network = psutil.net_io_counters()
            
            return {
                'cpu_percent': cpu_percent,
                'memory_percent': memory.percent,
                'memory_used': memory.used,
                'memory_total': memory.total,
                'disk_percent': disk.percent,
                'disk_used': disk.used,
                'disk_total': disk.total,
                'network_bytes_sent': network.bytes_sent,
                'network_bytes_recv': network.bytes_recv,
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            return {'error': str(e)}

    def generate_security_logs(self):
        """Generate simulated security logs"""
        log_types = [
            'authentication', 'file_access', 'network_connection', 
            'system_event', 'application_log', 'security_alert'
        ]
        
        log_levels = ['INFO', 'WARNING', 'ERROR', 'CRITICAL']
        
        log_templates = {
            'authentication': [
                'User {user} logged in successfully from {ip}',
                'Failed login attempt for user {user} from {ip}',
                'User {user} logged out from {ip}',
                'Password change requested for user {user}'
            ],
            'file_access': [
                'File {file} accessed by user {user}',
                'Unauthorized access attempt to {file} from {ip}',
                'File {file} modified by {user}',
                'File {file} deleted by {user}'
            ],
            'network_connection': [
                'Connection established to {ip}:{port}',
                'Connection from {ip} blocked by firewall',
                'Suspicious connection pattern detected from {ip}',
                'Port scan detected from {ip}'
            ],
            'system_event': [
                'System service {service} started',
                'System service {service} stopped',
                'System reboot initiated by {user}',
                'Disk space warning: {percent}% used'
            ],
            'application_log': [
                'Application {app} started successfully',
                'Application {app} encountered an error: {error}',
                'Database connection established',
                'Backup process completed successfully'
            ],
            'security_alert': [
                'Malware detection: {file} flagged as suspicious',
                'Intrusion attempt detected from {ip}',
                'Privilege escalation attempt by {user}',
                'Data exfiltration attempt detected'
            ]
        }
        
        users = ['admin', 'user1', 'user2', 'analyst', 'guest']
        ips = ['192.168.1.100', '192.168.1.101', '10.0.0.50', '172.16.0.25']
        files = ['/etc/passwd', '/var/log/auth.log', '/home/user/documents', '/etc/shadow']
        services = ['ssh', 'apache2', 'mysql', 'nginx', 'postgresql']
        apps = ['web_server', 'database', 'mail_server', 'file_server']
        ports = [22, 80, 443, 3306, 5432, 8080]
        
        log_entry = {
            'id': str(uuid.uuid4()),
            'timestamp': datetime.now().isoformat(),
            'type': random.choice(log_types),
            'level': random.choice(log_levels),
            'message': '',
            'source': random.choice(ips),
            'user': random.choice(users),
            'details': {}
        }
        
        log_type = log_entry['type']
        template = random.choice(log_templates[log_type])
        
        # Fill template with random data
        log_entry['message'] = template.format(
            user=log_entry['user'],
            ip=log_entry['source'],
            file=random.choice(files),
            service=random.choice(services),
            app=random.choice(apps),
            port=random.choice(ports),
            percent=random.randint(70, 95),
            error='Connection timeout'
        )
        
        return log_entry

    def analyze_log(self, log_entry):
        """Analyze log entry against security rules"""
        alerts = []
        
        # Rule 1: Multiple failed login attempts
        if 'Failed login attempt' in log_entry['message']:
            alerts.append({
                'id': str(uuid.uuid4()),
                'timestamp': log_entry['timestamp'],
                'level': 'HIGH',
                'rule': 'Multiple Failed Logins',
                'description': 'Multiple failed login attempts detected',
                'source': log_entry['source'],
                'agent': log_entry.get('user', 'Unknown'),
                'status': 'Active'
            })
        
        # Rule 2: Unauthorized file access
        if 'Unauthorized access attempt' in log_entry['message']:
            alerts.append({
                'id': str(uuid.uuid4()),
                'timestamp': log_entry['timestamp'],
                'level': 'CRITICAL',
                'rule': 'Unauthorized File Access',
                'description': 'Unauthorized access to sensitive files',
                'source': log_entry['source'],
                'agent': log_entry.get('user', 'Unknown'),
                'status': 'Active'
            })
        
        # Rule 3: Port scanning
        if 'Port scan detected' in log_entry['message']:
            alerts.append({
                'id': str(uuid.uuid4()),
                'timestamp': log_entry['timestamp'],
                'level': 'HIGH',
                'rule': 'Port Scanning Activity',
                'description': 'Port scanning activity detected',
                'source': log_entry['source'],
                'agent': 'Network Monitor',
                'status': 'Active'
            })
        
        # Rule 4: Malware detection
        if 'Malware detection' in log_entry['message']:
            alerts.append({
                'id': str(uuid.uuid4()),
                'timestamp': log_entry['timestamp'],
                'level': 'CRITICAL',
                'rule': 'Malware Detection',
                'description': 'Suspicious file detected as malware',
                'source': log_entry['source'],
                'agent': 'Antivirus Scanner',
                'status': 'Active'
            })
        
        return alerts

    def create_alert(self, alert_data):
        """Create a new security alert"""
        alert = {
            'id': alert_data['id'],
            'timestamp': alert_data['timestamp'],
            'level': alert_data['level'],
            'rule': alert_data['rule'],
            'description': alert_data['description'],
            'source': alert_data['source'],
            'agent': alert_data['agent'],
            'status': alert_data['status'],
            'mitre_technique': self.get_random_mitre_technique()
        }
        
        self.alerts.append(alert)
        return alert

    def get_random_mitre_technique(self):
        """Get a random MITRE ATT&CK technique"""
        techniques = [
            'T1078 - Valid Accounts',
            'T1055 - Process Injection',
            'T1027 - Obfuscated Files or Information',
            'T1082 - System Information Discovery',
            'T1059 - Command and Scripting Interpreter',
            'T1071 - Application Layer Protocol',
            'T1041 - Exfiltration Over C2 Channel',
            'T1090 - Connection Proxy'
        ]
        return random.choice(techniques)

    def get_network_threats(self):
        """Get simulated network threats"""
        threat_types = [
            'DDoS Attack', 'SQL Injection', 'XSS Attack', 
            'Brute Force', 'Man-in-the-Middle', 'Data Exfiltration'
        ]
        
        threats = []
        for _ in range(random.randint(3, 8)):
            threat = {
                'id': str(uuid.uuid4()),
                'timestamp': datetime.now().isoformat(),
                'type': random.choice(threat_types),
                'source_ip': f"{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}",
                'target_ip': '192.168.1.100',
                'severity': random.choice(['LOW', 'MEDIUM', 'HIGH', 'CRITICAL']),
                'status': random.choice(['Active', 'Blocked', 'Resolved']),
                'description': f"{random.choice(threat_types)} attempt detected"
            }
            threats.append(threat)
        
        return threats

    def get_file_integrity_data(self):
        """Get simulated file integrity monitoring data"""
        files = [
            '/etc/passwd', '/etc/shadow', '/var/log/auth.log',
            '/home/user/.bashrc', '/etc/ssh/sshd_config'
        ]
        
        changes = []
        for _ in range(random.randint(2, 6)):
            change = {
                'id': str(uuid.uuid4()),
                'timestamp': datetime.now().isoformat(),
                'file_path': random.choice(files),
                'change_type': random.choice(['Modified', 'Created', 'Deleted']),
                'user': random.choice(['root', 'admin', 'user1']),
                'hash_before': 'abc123...',
                'hash_after': 'def456...',
                'status': random.choice(['Suspicious', 'Normal', 'Critical'])
            }
            changes.append(change)
        
        return changes

    def get_agents_status(self):
        """Get simulated agent status"""
        agent_types = ['Server', 'Workstation', 'Router', 'Firewall']
        statuses = ['Online', 'Offline', 'Warning']
        
        agents = {}
        for i in range(1, 11):
            agent_type = random.choice(agent_types)
            status = random.choice(statuses)
            
            agents[f"{agent_type}-{i:02d}"] = {
                'id': f"agent-{i:03d}",
                'name': f"{agent_type}-{i:02d}",
                'type': agent_type,
                'status': status,
                'last_seen': datetime.now().isoformat(),
                'version': '4.5.2',
                'ip_address': f"192.168.1.{i+10}",
                'os': random.choice(['Linux', 'Windows', 'macOS']),
                'alerts_count': random.randint(0, 50)
            }
        
        return agents

    def load_rules(self):
        """Load security rules"""
        return [
            {
                'id': 'rule-001',
                'name': 'Multiple Failed Logins',
                'description': 'Detect multiple failed login attempts',
                'severity': 'HIGH',
                'enabled': True
            },
            {
                'id': 'rule-002',
                'name': 'Unauthorized File Access',
                'description': 'Detect unauthorized access to sensitive files',
                'severity': 'CRITICAL',
                'enabled': True
            },
            {
                'id': 'rule-003',
                'name': 'Port Scanning',
                'description': 'Detect port scanning activity',
                'severity': 'HIGH',
                'enabled': True
            },
            {
                'id': 'rule-004',
                'name': 'Malware Detection',
                'description': 'Detect suspicious files and malware',
                'severity': 'CRITICAL',
                'enabled': True
            }
        ]

# Initialize TMEN SIEM
tmen_siem = TMENSIEM()

@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('tmen_siem_dashboard.html')

@app.route('/api/system/metrics')
def get_system_metrics():
    """Get system metrics"""
    return jsonify(tmen_siem.get_system_metrics())

@app.route('/api/logs')
def get_logs():
    """Get security logs"""
    return jsonify(tmen_siem.logs)

@app.route('/api/logs/generate')
def generate_logs():
    """Generate new security logs"""
    for _ in range(random.randint(1, 5)):
        log_entry = tmen_siem.generate_security_logs()
        tmen_siem.logs.append(log_entry)
        
        # Analyze log and create alerts
        alerts = tmen_siem.analyze_log(log_entry)
        for alert in alerts:
            tmen_siem.create_alert(alert)
    
    return jsonify({'message': 'Logs generated successfully', 'count': len(tmen_siem.logs)})

@app.route('/api/alerts')
def get_alerts():
    """Get security alerts"""
    return jsonify(tmen_siem.alerts)

@app.route('/api/alerts/<alert_id>')
def get_alert(alert_id):
    """Get specific alert"""
    for alert in tmen_siem.alerts:
        if alert['id'] == alert_id:
            return jsonify(alert)
    return jsonify({'error': 'Alert not found'}), 404

@app.route('/api/network/threats')
def get_network_threats():
    """Get network threats"""
    return jsonify(tmen_siem.get_network_threats())

@app.route('/api/files/integrity')
def get_file_integrity():
    """Get file integrity data"""
    return jsonify(tmen_siem.get_file_integrity_data())

@app.route('/api/agents')
def get_agents():
    """Get agent status"""
    return jsonify(tmen_siem.get_agents_status())

@app.route('/api/rules')
def get_rules():
    """Get security rules"""
    return jsonify(tmen_siem.rules)

@app.route('/api/dashboard/overview')
def get_dashboard_overview():
    """Get dashboard overview data"""
    return jsonify({
        'total_alerts': len(tmen_siem.alerts),
        'total_logs': len(tmen_siem.logs),
        'active_agents': len([a for a in tmen_siem.get_agents_status().values() if a['status'] == 'Online']),
        'critical_alerts': len([a for a in tmen_siem.alerts if a['level'] == 'CRITICAL']),
        'system_health': 'Good',
        'last_update': datetime.now().isoformat()
    })

def background_log_generator():
    """Background thread to generate logs periodically"""
    while True:
        try:
            # Generate 1-3 logs every 10 seconds
            for _ in range(random.randint(1, 3)):
                log_entry = tmen_siem.generate_security_logs()
                tmen_siem.logs.append(log_entry)
                
                # Analyze log and create alerts
                alerts = tmen_siem.analyze_log(log_entry)
                for alert in alerts:
                    tmen_siem.create_alert(alert)
            
            # Keep only last 1000 logs
            if len(tmen_siem.logs) > 1000:
                tmen_siem.logs = tmen_siem.logs[-1000:]
            
            # Keep only last 500 alerts
            if len(tmen_siem.alerts) > 500:
                tmen_siem.alerts = tmen_siem.alerts[-500:]
                
        except Exception as e:
            print(f"Error in background log generator: {e}")
        
        time.sleep(10)  # Generate logs every 10 seconds

if __name__ == '__main__':
    print("🚀 Starting TMEN SIEM Backend Server...")
    print("📍 API Endpoints:")
    print("   - GET  /api/system/metrics")
    print("   - GET  /api/logs")
    print("   - GET  /api/alerts")
    print("   - GET  /api/network/threats")
    print("   - GET  /api/agents")
    print("   - GET  /api/dashboard/overview")
    print("🌐 Server running on http://localhost:5000")
    
    # Start background log generator
    log_thread = threading.Thread(target=background_log_generator, daemon=True)
    log_thread.start()
    
    app.run(host='0.0.0.0', port=5000, debug=True) 