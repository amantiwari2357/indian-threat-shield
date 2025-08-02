#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TMEN SIEM - Security Information and Event Management
TMEN GROUP - Custom SIEM Tool Development
"""
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
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
        """Get simulated system metrics (no psutil required)"""
        try:
            # Simulate system metrics
            cpu_percent = random.uniform(20, 80)
            memory_percent = random.uniform(40, 90)
            disk_percent = random.uniform(30, 85)
            
            return {
                'cpu_percent': round(cpu_percent, 2),
                'memory_percent': round(memory_percent, 2),
                'memory_used': random.randint(4000000000, 16000000000),  # 4-16 GB
                'memory_total': 16000000000,  # 16 GB
                'disk_percent': round(disk_percent, 2),
                'disk_used': random.randint(100000000000, 800000000000),  # 100-800 GB
                'disk_total': 1000000000000,  # 1 TB
                'network_bytes_sent': random.randint(1000000, 10000000),
                'network_bytes_recv': random.randint(1000000, 10000000),
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
                'Suspicious activity detected from {ip}',
                'Multiple failed login attempts from {ip}',
                'Unauthorized file access attempt by {user}',
                'System integrity check failed'
            ]
        }
        
        log_type = random.choice(log_types)
        log_level = random.choice(log_levels)
        
        # Generate random data for log template
        data = {
            'user': random.choice(['admin', 'user1', 'user2', 'analyst', 'guest']),
            'ip': f"{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}",
            'file': random.choice(['/etc/passwd', '/var/log/auth.log', '/home/user/file.txt', '/etc/config.conf']),
            'port': random.randint(80, 65535),
            'service': random.choice(['ssh', 'httpd', 'mysql', 'nginx', 'apache']),
            'app': random.choice(['webapp', 'database', 'backup', 'monitoring']),
            'error': random.choice(['Connection timeout', 'Permission denied', 'File not found', 'Invalid format']),
            'percent': random.randint(70, 95)
        }
        
        template = random.choice(log_templates[log_type])
        message = template.format(**data)
        
        log_entry = {
            'id': str(uuid.uuid4()),
            'timestamp': datetime.now().isoformat(),
            'level': log_level,
            'type': log_type,
            'message': message,
            'source': f"agent-{random.randint(1, 10)}",
            'ip_address': data['ip']
        }
        
        self.logs.append(log_entry)
        
        # Analyze log for potential alerts
        self.analyze_log(log_entry)
        
        return log_entry

    def analyze_log(self, log_entry):
        """Analyze log entry against security rules"""
        message = log_entry['message'].lower()
        
        # Check for suspicious patterns
        suspicious_patterns = [
            'failed login', 'unauthorized', 'suspicious', 'blocked',
            'port scan', 'multiple failed', 'integrity check failed'
        ]
        
        for pattern in suspicious_patterns:
            if pattern in message:
                alert_data = {
                    'id': str(uuid.uuid4()),
                    'timestamp': log_entry['timestamp'],
                    'level': 'HIGH' if log_entry['level'] in ['ERROR', 'CRITICAL'] else 'MEDIUM',
                    'type': 'Security Alert',
                    'message': f"Suspicious activity detected: {log_entry['message']}",
                    'source': log_entry['source'],
                    'ip_address': log_entry.get('ip_address', 'Unknown'),
                    'mitre_technique': self.get_random_mitre_technique(),
                    'status': 'Active'
                }
                self.create_alert(alert_data)
                break

    def create_alert(self, alert_data):
        """Create a new security alert"""
        alert_data['id'] = str(uuid.uuid4())
        alert_data['created_at'] = datetime.now().isoformat()
        alert_data['updated_at'] = alert_data['created_at']
        
        self.alerts.append(alert_data)
        
        # Keep only last 100 alerts
        if len(self.alerts) > 100:
            self.alerts = self.alerts[-100:]

    def get_random_mitre_technique(self):
        """Get a random MITRE ATT&CK technique"""
        techniques = [
            {'technique': 'T1078', 'name': 'Valid Accounts', 'tactic': 'Initial Access'},
            {'technique': 'T1110', 'name': 'Brute Force', 'tactic': 'Credential Access'},
            {'technique': 'T1059', 'name': 'Command and Scripting Interpreter', 'tactic': 'Execution'},
            {'technique': 'T1083', 'name': 'File and Directory Discovery', 'tactic': 'Discovery'},
            {'technique': 'T1071', 'name': 'Application Layer Protocol', 'tactic': 'Command and Control'},
            {'technique': 'T1070', 'name': 'Indicator Removal on Host', 'tactic': 'Defense Evasion'},
            {'technique': 'T1036', 'name': 'Masquerading', 'tactic': 'Defense Evasion'},
            {'technique': 'T1021', 'name': 'Remote Services', 'tactic': 'Lateral Movement'}
        ]
        return random.choice(techniques)

    def get_network_threats(self):
        """Get simulated network threats"""
        threat_types = ['port_scan', 'brute_force', 'ddos', 'malware', 'phishing']
        
        threats = []
        for i in range(random.randint(3, 8)):
            threat_type = random.choice(threat_types)
            source_ip = f"{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}"
            threat = {
                'id': str(uuid.uuid4()),
                'timestamp': (datetime.now() - timedelta(minutes=random.randint(1, 60))).isoformat(),
                'type': threat_type,
                'source_ip': source_ip,
                'destination_ip': f"192.168.1.{random.randint(1, 100)}",
                'severity': random.choice(['LOW', 'MEDIUM', 'HIGH', 'CRITICAL']),
                'status': random.choice(['Active', 'Blocked', 'Investigated']),
                'description': f"{threat_type.replace('_', ' ').title()} attack detected from {source_ip}"
            }
            threats.append(threat)
        
        return threats

    def get_file_integrity_data(self):
        """Get simulated file integrity monitoring data"""
        files = [
            '/etc/passwd', '/etc/shadow', '/var/log/auth.log',
            '/etc/ssh/sshd_config', '/etc/hosts', '/etc/resolv.conf'
        ]
        
        changes = []
        for i in range(random.randint(2, 6)):
            file_path = random.choice(files)
            change = {
                'id': str(uuid.uuid4()),
                'timestamp': (datetime.now() - timedelta(minutes=random.randint(1, 30))).isoformat(),
                'file_path': file_path,
                'change_type': random.choice(['modified', 'created', 'deleted']),
                'user': random.choice(['root', 'admin', 'system']),
                'hash_before': f"sha256:{random.randint(1000000000000000000000000000000000000000000000000000000000000000, 9999999999999999999999999999999999999999999999999999999999999999)}",
                'hash_after': f"sha256:{random.randint(1000000000000000000000000000000000000000000000000000000000000000, 9999999999999999999999999999999999999999999999999999999999999999)}",
                'status': random.choice(['Investigated', 'Pending', 'Resolved'])
            }
            changes.append(change)
        
        return changes

    def get_agents_status(self):
        """Get simulated agent status"""
        agent_statuses = ['Active', 'Disconnected', 'Never Connected']
        
        agents = []
        for i in range(random.randint(5, 15)):
            agent = {
                'id': f"agent-{i+1:03d}",
                'name': f"TMEN-Agent-{i+1:03d}",
                'status': random.choice(agent_statuses),
                'ip_address': f"192.168.1.{random.randint(10, 200)}",
                'version': f"3.13.{random.randint(1, 5)}",
                'last_keep_alive': (datetime.now() - timedelta(minutes=random.randint(1, 60))).isoformat(),
                'os': random.choice(['Windows 10', 'Windows 11', 'Ubuntu 20.04', 'CentOS 7', 'macOS 12']),
                'groups': random.choice([['default'], ['web-servers'], ['database-servers'], ['default', 'monitoring']])
            }
            agents.append(agent)
        
        return agents

    def load_rules(self):
        """Load security rules"""
        return [
            {
                'id': 'rule_001',
                'name': 'Failed Login Detection',
                'description': 'Detect multiple failed login attempts',
                'pattern': 'failed login',
                'severity': 'HIGH',
                'enabled': True
            },
            {
                'id': 'rule_002',
                'name': 'Unauthorized Access',
                'description': 'Detect unauthorized file access',
                'pattern': 'unauthorized',
                'severity': 'CRITICAL',
                'enabled': True
            },
            {
                'id': 'rule_003',
                'name': 'Port Scan Detection',
                'description': 'Detect port scanning activity',
                'pattern': 'port scan',
                'severity': 'MEDIUM',
                'enabled': True
            }
        ]

# Initialize TMEN SIEM
siem = TMENSIEM()

@app.route('/')
def index():
    return jsonify({'message': 'TMEN SIEM API is running'})

@app.route('/api/system/metrics')
def get_system_metrics():
    return jsonify(siem.get_system_metrics())

@app.route('/api/logs')
def get_logs():
    return jsonify(siem.logs[-50:])  # Return last 50 logs

@app.route('/api/logs/generate')
def generate_logs():
    """Generate new security logs"""
    new_logs = []
    for _ in range(random.randint(1, 5)):
        log_entry = siem.generate_security_logs()
        new_logs.append(log_entry)
    
    return jsonify({
        'message': f'Generated {len(new_logs)} new logs',
        'logs': new_logs
    })

@app.route('/api/alerts')
def get_alerts():
    return jsonify(siem.alerts[-20:])  # Return last 20 alerts

@app.route('/api/alerts/<alert_id>')
def get_alert(alert_id):
    for alert in siem.alerts:
        if alert['id'] == alert_id:
            return jsonify(alert)
    return jsonify({'error': 'Alert not found'}), 404

@app.route('/api/network/threats')
def get_network_threats():
    return jsonify(siem.get_network_threats())

@app.route('/api/files/integrity')
def get_file_integrity():
    return jsonify(siem.get_file_integrity_data())

@app.route('/api/agents')
def get_agents():
    return jsonify(siem.get_agents_status())

@app.route('/api/rules')
def get_rules():
    return jsonify(siem.rules)

@app.route('/api/dashboard/overview')
def get_dashboard_overview():
    """Get dashboard overview data"""
    return jsonify({
        'total_alerts': len(siem.alerts),
        'active_alerts': len([a for a in siem.alerts if a['status'] == 'Active']),
        'total_logs': len(siem.logs),
        'agents_count': len(siem.get_agents_status()),
        'system_metrics': siem.get_system_metrics(),
        'recent_alerts': siem.alerts[-5:],
        'recent_logs': siem.logs[-10:]
    })

def background_log_generator():
    """Background thread to generate logs periodically"""
    while True:
        try:
            siem.generate_security_logs()
            time.sleep(random.randint(5, 15))  # Generate logs every 5-15 seconds
        except Exception as e:
            print(f"Error generating logs: {e}")
            time.sleep(30)

if __name__ == '__main__':
    print("🚀 Starting TMEN SIEM Backend Server...")
    print("📊 API Endpoints Available:")
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