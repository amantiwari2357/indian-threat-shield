#!/bin/bash

# Custom SIEM Setup Script
# This script sets up the complete Custom SIEM environment

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
PROJECT_NAME="custom-siem"
DEFAULT_PORT=8080
DEFAULT_DASHBOARD_PORT=3000
DEFAULT_ELASTICSEARCH_PORT=9200
DEFAULT_KIBANA_PORT=5601

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to check prerequisites
check_prerequisites() {
    print_status "Checking prerequisites..."
    
    local missing_deps=()
    
    # Check Docker
    if ! command_exists docker; then
        missing_deps+=("Docker")
    fi
    
    # Check Docker Compose
    if ! command_exists docker-compose; then
        missing_deps+=("Docker Compose")
    fi
    
    # Check Java
    if ! command_exists java; then
        missing_deps+=("Java 17+")
    fi
    
    # Check Node.js
    if ! command_exists node; then
        missing_deps+=("Node.js 18+")
    fi
    
    # Check Go
    if ! command_exists go; then
        missing_deps+=("Go 1.21+")
    fi
    
    if [ ${#missing_deps[@]} -ne 0 ]; then
        print_error "Missing prerequisites: ${missing_deps[*]}"
        echo "Please install the missing dependencies and run this script again."
        exit 1
    fi
    
    print_success "All prerequisites are installed"
}

# Function to create directory structure
create_directories() {
    print_status "Creating directory structure..."
    
    local dirs=(
        "logs"
        "data/elasticsearch"
        "data/postgresql"
        "data/redis"
        "config"
        "certs"
        "backups"
        "scripts"
    )
    
    for dir in "${dirs[@]}"; do
        mkdir -p "$dir"
    done
    
    print_success "Directory structure created"
}

# Function to generate SSL certificates
generate_certificates() {
    print_status "Generating SSL certificates..."
    
    if [ ! -f "certs/ca.key" ]; then
        # Generate CA key and certificate
        openssl genrsa -out certs/ca.key 4096
        openssl req -new -x509 -days 365 -key certs/ca.key -out certs/ca.crt \
            -subj "/C=US/ST=State/L=City/O=CustomSIEM/CN=CustomSIEM-CA"
        
        # Generate server key and certificate
        openssl genrsa -out certs/server.key 2048
        openssl req -new -key certs/server.key -out certs/server.csr \
            -subj "/C=US/ST=State/L=City/O=CustomSIEM/CN=localhost"
        openssl x509 -req -days 365 -in certs/server.csr -CA certs/ca.crt \
            -CAkey certs/ca.key -CAcreateserial -out certs/server.crt
        
        print_success "SSL certificates generated"
    else
        print_warning "SSL certificates already exist, skipping generation"
    fi
}

# Function to create environment file
create_env_file() {
    print_status "Creating environment configuration..."
    
    cat > .env << EOF
# Custom SIEM Environment Configuration

# Application Settings
PROJECT_NAME=${PROJECT_NAME}
ENVIRONMENT=development
LOG_LEVEL=INFO

# Port Configuration
BACKEND_PORT=${DEFAULT_PORT}
DASHBOARD_PORT=${DEFAULT_DASHBOARD_PORT}
ELASTICSEARCH_PORT=${DEFAULT_ELASTICSEARCH_PORT}
KIBANA_PORT=${DEFAULT_KIBANA_PORT}

# Database Configuration
POSTGRES_DB=custom_siem
POSTGRES_USER=custom_siem_user
POSTGRES_PASSWORD=custom_siem_password
POSTGRES_HOST=postgres
POSTGRES_PORT=5432

# Redis Configuration
REDIS_HOST=redis
REDIS_PORT=6379
REDIS_PASSWORD=

# Elasticsearch Configuration
ELASTICSEARCH_URL=http://elasticsearch:9200
ELASTICSEARCH_USERNAME=elastic
ELASTICSEARCH_PASSWORD=changeme

# Kafka Configuration
KAFKA_BOOTSTRAP_SERVERS=kafka:9092
KAFKA_TOPIC_LOGS=custom-siem-logs
KAFKA_TOPIC_ALERTS=custom-siem-alerts

# Security Configuration
JWT_SECRET=your-super-secret-jwt-key-change-in-production
JWT_EXPIRATION=86400000
JWT_REFRESH_EXPIRATION=604800000

# Alerting Configuration
EMAIL_ALERTS_ENABLED=false
SMTP_HOST=
SMTP_PORT=587
SMTP_USERNAME=
SMTP_PASSWORD=

SLACK_ALERTS_ENABLED=false
SLACK_WEBHOOK_URL=

WEBHOOK_ALERTS_ENABLED=false
WEBHOOK_URL=

# Agent Configuration
AGENT_AUTO_APPROVE=false
AGENT_HEARTBEAT_INTERVAL=30
AGENT_HEARTBEAT_TIMEOUT=90

# Rule Engine Configuration
RULE_ENGINE_ENABLED=true
RULE_ENGINE_BATCH_SIZE=1000
RULE_ENGINE_PROCESSING_INTERVAL=5000

# Dashboard Configuration
DASHBOARD_DEFAULT_PAGE_SIZE=50
DASHBOARD_MAX_PAGE_SIZE=1000
DASHBOARD_SESSION_TIMEOUT=3600

# Development Settings
SPRING_PROFILES_ACTIVE=dev
JPA_DDL_AUTO=update
JPA_SHOW_SQL=false
EOF
    
    print_success "Environment configuration created"
}

# Function to build Docker images
build_images() {
    print_status "Building Docker images..."
    
    # Build backend API
    print_status "Building backend API image..."
    docker build -t custom-siem/backend-api:latest ./backend-api/
    
    # Build dashboard
    print_status "Building dashboard image..."
    docker build -t custom-siem/dashboard:latest ./dashboard/
    
    # Build rule engine
    print_status "Building rule engine image..."
    docker build -t custom-siem/rule-engine:latest ./rule-engine/
    
    print_success "All Docker images built successfully"
}

# Function to start services
start_services() {
    print_status "Starting Custom SIEM services..."
    
    # Start infrastructure services first
    docker-compose up -d elasticsearch kibana kafka zookeeper postgres redis
    
    # Wait for services to be ready
    print_status "Waiting for services to be ready..."
    sleep 30
    
    # Start application services
    docker-compose up -d backend-api dashboard rule-engine log-collector
    
    print_success "All services started successfully"
}

# Function to initialize databases
initialize_databases() {
    print_status "Initializing databases..."
    
    # Wait for PostgreSQL to be ready
    print_status "Waiting for PostgreSQL to be ready..."
    until docker-compose exec -T postgres pg_isready -U custom_siem_user; do
        sleep 2
    done
    
    # Initialize PostgreSQL schema
    print_status "Initializing PostgreSQL schema..."
    docker-compose exec -T postgres psql -U custom_siem_user -d custom_siem -c "
        CREATE TABLE IF NOT EXISTS schema_version (
            version VARCHAR(50) PRIMARY KEY,
            applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    "
    
    # Initialize Elasticsearch indices
    print_status "Initializing Elasticsearch indices..."
    curl -X PUT "localhost:9200/custom-siem-logs" -H "Content-Type: application/json" -d '{
        "settings": {
            "number_of_shards": 1,
            "number_of_replicas": 0
        },
        "mappings": {
            "properties": {
                "@timestamp": {"type": "date"},
                "message": {"type": "text"},
                "level": {"type": "keyword"},
                "source": {"type": "keyword"},
                "agent_id": {"type": "keyword"}
            }
        }
    }' || print_warning "Elasticsearch index creation failed (may already exist)"
    
    print_success "Databases initialized successfully"
}

# Function to create default users
create_default_users() {
    print_status "Creating default users..."
    
    # This would typically be done through the API
    # For now, we'll create a simple admin user
    print_status "Default admin user: admin/admin"
    print_warning "Please change the default password after first login"
}

# Function to check service health
check_health() {
    print_status "Checking service health..."
    
    local services=(
        "http://localhost:${DEFAULT_PORT}/api/v1/actuator/health"
        "http://localhost:${DEFAULT_DASHBOARD_PORT}/health"
        "http://localhost:${DEFAULT_ELASTICSEARCH_PORT}/_cluster/health"
        "http://localhost:${DEFAULT_KIBANA_PORT}/api/status"
    )
    
    for service in "${services[@]}"; do
        if curl -f -s "$service" > /dev/null; then
            print_success "Service is healthy: $service"
        else
            print_warning "Service may not be ready: $service"
        fi
    done
}

# Function to display access information
display_access_info() {
    echo
    echo "=========================================="
    echo "Custom SIEM Setup Complete!"
    echo "=========================================="
    echo
    echo "Access URLs:"
    echo "  Dashboard:     http://localhost:${DEFAULT_DASHBOARD_PORT}"
    echo "  API:          http://localhost:${DEFAULT_PORT}/api/v1"
    echo "  Swagger UI:   http://localhost:${DEFAULT_PORT}/swagger-ui.html"
    echo "  Kibana:       http://localhost:${DEFAULT_KIBANA_PORT}"
    echo "  Elasticsearch: http://localhost:${DEFAULT_ELASTICSEARCH_PORT}"
    echo
    echo "Default Credentials:"
    echo "  Username: admin"
    echo "  Password: admin"
    echo
    echo "Management Commands:"
    echo "  View logs:     docker-compose logs -f"
    echo "  Stop services: docker-compose down"
    echo "  Restart:       docker-compose restart"
    echo "  Update:        git pull && docker-compose up -d --build"
    echo
    echo "Next Steps:"
    echo "  1. Access the dashboard and change default password"
    echo "  2. Configure agents for your endpoints"
    echo "  3. Create custom rules for your environment"
    echo "  4. Set up alerting integrations"
    echo "  5. Review and customize security settings"
    echo
    echo "Documentation: ./docs/"
    echo "Support: https://github.com/your-org/custom-siem/issues"
    echo
}

# Function to cleanup on error
cleanup() {
    print_error "Setup failed. Cleaning up..."
    docker-compose down -v
    exit 1
}

# Main execution
main() {
    echo "=========================================="
    echo "Custom SIEM Setup Script"
    echo "=========================================="
    echo
    
    # Set up error handling
    trap cleanup ERR
    
    # Check prerequisites
    check_prerequisites
    
    # Create directory structure
    create_directories
    
    # Generate certificates
    generate_certificates
    
    # Create environment file
    create_env_file
    
    # Build images
    build_images
    
    # Start services
    start_services
    
    # Initialize databases
    initialize_databases
    
    # Create default users
    create_default_users
    
    # Check health
    check_health
    
    # Display access information
    display_access_info
    
    print_success "Custom SIEM setup completed successfully!"
}

# Run main function
main "$@" 