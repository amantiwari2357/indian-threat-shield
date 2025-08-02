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
        
    def load_rules(self):
        """Load SIEM rules for threat detection"""
        return {
            'brute_force': {
                'pattern': r'Failed login attempt',
                'threshold': 5,
                'time_window': 300,
                'severity': 'high'
            },
            'malware_detection': {
                'pattern': r'(virus|malware|trojan|ransomware)',
                'threshold': 1,
                'time_window': 60,
                'severity': 'critical'
            },
            'unauthorized_access': {
                'pattern': r'Unauthorized access attempt',
                'threshold': 3,
                'time_window': 180,
                'severity': 'high'
            },
            'file_integrity': {
                'pattern': r'File modified without authorization',
                'threshold': 1,
                'time_window': 60,
                'severity': 'medium'
            },
            'network_scan': {
                'pattern': r'Port scan detected',
                'threshold': 10,
                'time_window': 60,
                'severity': 'medium'
            }
        }
    
    def get_system_metrics(self):
        """Get real-time system metrics"""
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            network = psutil.net_io_counters()
            
            return {
                'cpu_usage': round(cpu_percent, 2),
                'memory_usage': round(memory.percent, 2),
                'disk_usage': round(disk.percent, 2),
                'memory_total': round(memory.total / (1024**3), 2),
                'memory_available': round(memory.available / (1024**3), 2),
                'disk_total': round(disk.total / (1024**3), 2),
                'disk_free': round(disk.free / (1024**3), 2),
                'network_sent': round(network.bytes_sent / (1024**2), 2),
                'network_recv': round(network.bytes_recv / (1024**2), 2)
            }
        except Exception as e:
            return {
                'cpu_usage': 0,
                'memory_usage': 0,
                'disk_usage': 0,
                'error': str(e)
            }
    
    def generate_security_logs(self):
        """Generate simulated security logs"""
        log_types = [
            'authentication',
            'file_access',
            'network_activity',
            'system_event',
            'application_log'
        ]
        
        log_messages = {
            'authentication': [
                'User login successful: admin',
                'Failed login attempt: unknown_user',
                'Password change requested: user123',
                'Account locked: suspicious_user',
                'Multi-factor authentication enabled'
            ],
            'file_access': [
                'File accessed: /etc/passwd',
                'File modified: /var/log/auth.log',
                'File deleted: /tmp/temp_file',
                'Permission denied: /root/config',
                'File integrity check passed'
            ],
            'network_activity': [
                'Connection established: 192.168.1.100',
                'Port scan detected from 10.0.0.50',
                'DNS query: google.com',
                'Firewall rule triggered',
                'VPN connection established'
            ],
            'system_event': [
                'System reboot initiated',
                'Service started: sshd',
                'Service stopped: apache2',
                'Disk space warning: 85% used',
                'Memory usage high: 90%'
            ],
            'application_log': [
                'Database connection established',
                'API request processed',
                'Error 404: Page not found',
                'SSL certificate renewed',
                'Backup completed successfully'
            ]
        }
        
        log_type = random.choice(log_types)
        message = random.choice(log_messages[log_type])
        
        log_entry = {
            'id': str(uuid.uuid4()),
            'timestamp': datetime.now().isoformat(),
            'type': log_type,
            'message': message,
            'source_ip': f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}",
            'user': random.choice(['admin', 'user123', 'system', 'unknown']),
            'severity': random.choice(['info', 'warning', 'error', 'critical']),
            'agent_id': f"agent_{random.randint(1,10)}"
        }
        
        self.logs.append(log_entry)
        self.analyze_log(log_entry)
        return log_entry
    
    def analyze_log(self, log_entry):
        """Analyze log entry against SIEM rules"""
        for rule_name, rule in self.rules.items():
            if re.search(rule['pattern'], log_entry['message'], re.IGNORECASE):
                # Check if threshold is exceeded
                recent_logs = [log for log in self.logs 
                             if log['type'] == log_entry['type'] 
                             and datetime.fromisoformat(log['timestamp']) > 
                             datetime.now() - timedelta(seconds=rule['time_window'])]
                
                if len(recent_logs) >= rule['threshold']:
                    self.create_alert(rule_name, log_entry, rule['severity'])
    
    def create_alert(self, rule_name, log_entry, severity):
        """Create security alert"""
        alert = {
            'id': str(uuid.uuid4()),
            'timestamp': datetime.now().isoformat(),
            'rule_name': rule_name,
            'severity': severity,
            'message': f"Rule '{rule_name}' triggered: {log_entry['message']}",
            'source_ip': log_entry['source_ip'],
            'user': log_entry['user'],
            'agent_id': log_entry['agent_id'],
            'status': 'active',
            'assigned_to': None,
            'notes': ''
        }
        
        self.alerts.append(alert)
        return alert
    
    def get_network_threats(self):
        """Get network threat data"""
        threats = []
        for i in range(random.randint(0, 8)):
            threat_types = ['port_scan', 'brute_force', 'ddos', 'malware_traffic', 'data_exfiltration']
            threat = {
                'id': i + 1,
                'ip_address': f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}",
                'threat_type': random.choice(threat_types),
                'severity': random.choice(['low', 'medium', 'high', 'critical']),
                'timestamp': datetime.now().isoformat(),
                'country': random.choice(['Unknown', 'China', 'Russia', 'North Korea', 'Iran']),
                'ports': [random.randint(1,65535) for _ in range(random.randint(1,5))],
                'packets_sent': random.randint(100, 10000)
            }
            threats.append(threat)
        return threats
    
    def get_file_integrity_data(self):
        """Get file integrity monitoring data"""
        files = []
        for i in range(random.randint(0, 15)):
            file_change = {
                'id': i + 1,
                'filename': f"/etc/system/file_{i}.conf",
                'change_type': random.choice(['modified', 'created', 'deleted', 'permission_changed']),
                'timestamp': datetime.now().isoformat(),
                'user': random.choice(['root', 'admin', 'system', 'unknown']),
                'hash': f"sha256:{random.randint(1000000, 9999999)}",
                'size': random.randint(100, 1000000),
                'permissions': random.choice(['644', '755', '600', '777'])
            }
            files.append(file_change)
        return files
    
    def get_agents_status(self):
        """Get agent status information"""
        agents = {}
        for i in range(1, 11):
            agent_id = f"agent_{i}"
            last_seen = datetime.now() - timedelta(minutes=random.randint(0, 60))
            agents[agent_id] = {
                'id': agent_id,
                'name': f"TMEN-Agent-{i:03d}",
                'status': 'online' if random.random() > 0.1 else 'offline',
                'last_seen': last_seen.isoformat(),
                'version': '1.2.3',
                'platform': random.choice(['Linux', 'Windows', 'macOS']),
                'ip_address': f"192.168.1.{i}",
                'logs_sent': random.randint(100, 10000),
                'alerts_generated': random.randint(0, 50)
            }
        return agents

# Initialize TMEN SIEM
tmen_siem = TMENSIEM()

@app.route('/')
def index():
    """TMEN SIEM API Home"""
    return jsonify({
        'message': 'TMEN SIEM - Security Information and Event Management',
        'version': '1.0.0',
        'status': 'running',
        'timestamp': datetime.now().isoformat(),
        'company': 'TMEN GROUP',
        'features': [
            'Log Collection',
            'Threat Detection',
            'Real-time Alerting',
            'File Integrity Monitoring',
            'Network Threat Analysis',
            'Custom Rule Engine'
        ]
    })

@app.route('/api/system/metrics')
def get_system_metrics():
    """Get real-time system metrics"""
    metrics = tmen_siem.get_system_metrics()
    return jsonify({
        'status': 'success',
        'data': metrics,
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/logs')
def get_logs():
    """Get security logs"""
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 50))
    start = (page - 1) * limit
    end = start + limit
    
    logs = tmen_siem.logs[start:end]
    return jsonify({
        'status': 'success',
        'data': logs,
        'total_logs': len(tmen_siem.logs),
        'page': page,
        'limit': limit,
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/logs/generate', methods=['POST'])
def generate_log():
    """Generate a new security log"""
    log_entry = tmen_siem.generate_security_logs()
    return jsonify({
        'status': 'success',
        'message': 'Security log generated',
        'data': log_entry,
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/alerts')
def get_alerts():
    """Get security alerts"""
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 20))
    start = (page - 1) * limit
    end = start + limit
    
    alerts = tmen_siem.alerts[start:end]
    return jsonify({
        'status': 'success',
        'data': alerts,
        'total_alerts': len(tmen_siem.alerts),
        'active_alerts': len([a for a in tmen_siem.alerts if a['status'] == 'active']),
        'critical_alerts': len([a for a in tmen_siem.alerts if a['severity'] == 'critical']),
        'page': page,
        'limit': limit,
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/alerts/<alert_id>', methods=['PUT'])
def update_alert(alert_id):
    """Update alert status"""
    data = request.get_json()
    
    for alert in tmen_siem.alerts:
        if alert['id'] == alert_id:
            alert.update(data)
            return jsonify({
                'status': 'success',
                'message': 'Alert updated',
                'data': alert,
                'timestamp': datetime.now().isoformat()
            })
    
    return jsonify({
        'status': 'error',
        'message': 'Alert not found'
    }), 404

@app.route('/api/network/threats')
def get_network_threats():
    """Get network threats"""
    threats = tmen_siem.get_network_threats()
    return jsonify({
        'status': 'success',
        'data': threats,
        'total_threats': len(threats),
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/files/integrity')
def get_file_integrity():
    """Get file integrity data"""
    files = tmen_siem.get_file_integrity_data()
    return jsonify({
        'status': 'success',
        'data': files,
        'total_changes': len(files),
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/agents')
def get_agents():
    """Get agent status"""
    agents = tmen_siem.get_agents_status()
    return jsonify({
        'status': 'success',
        'data': list(agents.values()),
        'total_agents': len(agents),
        'online_agents': len([a for a in agents.values() if a['status'] == 'online']),
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/rules')
def get_rules():
    """Get SIEM rules"""
    return jsonify({
        'status': 'success',
        'data': tmen_siem.rules,
        'total_rules': len(tmen_siem.rules),
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/dashboard/overview')
def get_dashboard_overview():
    """Get complete dashboard overview"""
    system_metrics = tmen_siem.get_system_metrics()
    network_threats = tmen_siem.get_network_threats()
    file_changes = tmen_siem.get_file_integrity_data()
    agents = tmen_siem.get_agents_status()
    
    return jsonify({
        'status': 'success',
        'data': {
            'system': system_metrics,
            'logs': {
                'total': len(tmen_siem.logs),
                'recent': len([log for log in tmen_siem.logs 
                              if datetime.fromisoformat(log['timestamp']) > 
                              datetime.now() - timedelta(hours=1)])
            },
            'alerts': {
                'total': len(tmen_siem.alerts),
                'active': len([a for a in tmen_siem.alerts if a['status'] == 'active']),
                'critical': len([a for a in tmen_siem.alerts if a['severity'] == 'critical']),
                'high': len([a for a in tmen_siem.alerts if a['severity'] == 'high']),
                'medium': len([a for a in tmen_siem.alerts if a['severity'] == 'medium']),
                'low': len([a for a in tmen_siem.alerts if a['severity'] == 'low'])
            },
            'network_threats': {
                'total': len(network_threats),
                'suspicious_ips': len(set([t['ip_address'] for t in network_threats])),
                'port_scans': len([t for t in network_threats if t['threat_type'] == 'port_scan']),
                'countries': len(set([t['country'] for t in network_threats]))
            },
            'file_integrity': {
                'total_changes': len(file_changes),
                'modified': len([f for f in file_changes if f['change_type'] == 'modified']),
                'created': len([f for f in file_changes if f['change_type'] == 'created']),
                'deleted': len([f for f in file_changes if f['change_type'] == 'deleted'])
            },
            'agents': {
                'total': len(agents),
                'online': len([a for a in agents.values() if a['status'] == 'online']),
                'offline': len([a for a in agents.values() if a['status'] == 'offline'])
            }
        },
        'timestamp': datetime.now().isoformat()
    })

def background_log_generator():
    """Background thread to generate security logs"""
    while True:
        if random.random() < 0.4:  # 40% chance to generate log
            tmen_siem.generate_security_logs()
        time.sleep(random.randint(2, 8))

if __name__ == '__main__':
    print("🚀 Starting TMEN SIEM Backend Server...")
    print("📍 API Server: http://localhost:5000")
    print("📊 Dashboard: http://localhost:5000/dashboard")
    print("🔧 API Endpoints:")
    print("   - GET  /api/system/metrics")
    print("   - GET  /api/logs")
    print("   - POST /api/logs/generate")
    print("   - GET  /api/alerts")
    print("   - PUT  /api/alerts/<id>")
    print("   - GET  /api/network/threats")
    print("   - GET  /api/files/integrity")
    print("   - GET  /api/agents")
    print("   - GET  /api/rules")
    print("   - GET  /api/dashboard/overview")
    
    # Start background log generator
    log_thread = threading.Thread(target=background_log_generator, daemon=True)
    log_thread.start()
    
    # Run the Flask app
    app.run(host='0.0.0.0', port=5000, debug=True) 