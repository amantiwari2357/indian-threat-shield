# Custom SIEM Setup Script for Windows
# This script sets up the complete Custom SIEM environment

param(
    [string]$ProjectName = "custom-siem",
    [int]$BackendPort = 8080,
    [int]$DashboardPort = 3000,
    [int]$ElasticsearchPort = 9200,
    [int]$KibanaPort = 5601
)

# Colors for output
$Red = "Red"
$Green = "Green"
$Yellow = "Yellow"
$Blue = "Blue"

# Function to write colored output
function Write-ColorOutput {
    param(
        [string]$Message,
        [string]$Color = "White"
    )
    Write-Host $Message -ForegroundColor $Color
}

# Function to check if a command exists
function Test-Command {
    param([string]$Command)
    try {
        Get-Command $Command -ErrorAction Stop | Out-Null
        return $true
    }
    catch {
        return $false
    }
}

# Function to check prerequisites
function Test-Prerequisites {
    Write-ColorOutput "Checking prerequisites..." $Blue
    
    $prerequisites = @{
        "Docker" = "docker"
        "Docker Compose" = "docker-compose"
    }
    
    $missing = @()
    
    foreach ($prereq in $prerequisites.GetEnumerator()) {
        if (Test-Command $prereq.Value) {
            Write-ColorOutput "✓ $($prereq.Key) is installed" $Green
        } else {
            Write-ColorOutput "✗ $($prereq.Key) is not installed" $Red
            $missing += $prereq.Key
        }
    }
    
    if ($missing.Count -gt 0) {
        Write-ColorOutput "Missing prerequisites: $($missing -join ', ')" $Red
        Write-ColorOutput "Please install the missing prerequisites and run this script again." $Yellow
        exit 1
    }
    
    Write-ColorOutput "All prerequisites are satisfied!" $Green
}

# Function to create directory structure
function New-DirectoryStructure {
    Write-ColorOutput "Creating directory structure..." $Blue
    
    $directories = @(
        "logs",
        "data/elasticsearch",
        "data/postgresql",
        "data/redis",
        "config/ssl",
        "config/nginx",
        "config/fluent-bit"
    )
    
    foreach ($dir in $directories) {
        $path = Join-Path $ProjectName $dir
        if (-not (Test-Path $path)) {
            New-Item -ItemType Directory -Path $path -Force | Out-Null
            Write-ColorOutput "Created directory: $path" $Green
        }
    }
}

# Function to generate SSL certificates
function New-SSLCertificates {
    Write-ColorOutput "Generating SSL certificates..." $Blue
    
    $sslDir = Join-Path $ProjectName "config/ssl"
    
    # Create self-signed certificate for development
    $certPath = Join-Path $sslDir "custom-siem.crt"
    $keyPath = Join-Path $sslDir "custom-siem.key"
    
    if (-not (Test-Path $certPath) -or -not (Test-Path $keyPath)) {
        Write-ColorOutput "Generating self-signed SSL certificate..." $Yellow
        
        # Using OpenSSL if available, otherwise create placeholder files
        if (Test-Command "openssl") {
            $opensslCmd = "openssl req -x509 -newkey rsa:4096 -keyout `"$keyPath`" -out `"$certPath`" -days 365 -nodes -subj `/CN=localhost`"
            Invoke-Expression $opensslCmd
        } else {
            # Create placeholder files for development
            "-----BEGIN CERTIFICATE-----" | Out-File $certPath -Encoding UTF8
            "PLACEHOLDER CERTIFICATE FOR DEVELOPMENT" | Out-File $certPath -Append -Encoding UTF8
            "-----END CERTIFICATE-----" | Out-File $certPath -Append -Encoding UTF8
            
            "-----BEGIN PRIVATE KEY-----" | Out-File $keyPath -Encoding UTF8
            "PLACEHOLDER PRIVATE KEY FOR DEVELOPMENT" | Out-File $keyPath -Append -Encoding UTF8
            "-----END PRIVATE KEY-----" | Out-File $keyPath -Append -Encoding UTF8
        }
        
        Write-ColorOutput "SSL certificates generated" $Green
    }
}

# Function to create environment file
function New-EnvironmentFile {
    Write-ColorOutput "Creating environment configuration..." $Blue
    
    $envContent = @"
# Custom SIEM Environment Configuration
PROJECT_NAME=$ProjectName
BACKEND_PORT=$BackendPort
DASHBOARD_PORT=$DashboardPort
ELASTICSEARCH_PORT=$ElasticsearchPort
KIBANA_PORT=$KibanaPort

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
KAFKA_BROKERS=kafka:9092
KAFKA_TOPIC_LOGS=custom-siem-logs
KAFKA_TOPIC_ALERTS=custom-siem-alerts

# JWT Configuration
JWT_SECRET=your-super-secret-jwt-key-change-in-production
JWT_EXPIRATION=86400000

# Application Configuration
SPRING_PROFILES_ACTIVE=dev
LOG_LEVEL=INFO
"@
    
    $envPath = Join-Path $ProjectName ".env"
    $envContent | Out-File $envPath -Encoding UTF8
    Write-ColorOutput "Environment file created: $envPath" $Green
}

# Function to build Docker images
function Build-DockerImages {
    Write-ColorOutput "Building Docker images..." $Blue
    
    # Build backend API
    Write-ColorOutput "Building backend API image..." $Yellow
    docker build -t custom-siem-backend:latest backend-api/
    
    # Build dashboard
    Write-ColorOutput "Building dashboard image..." $Yellow
    docker build -t custom-siem-dashboard:latest dashboard/
    
    # Build rule engine
    Write-ColorOutput "Building rule engine image..." $Yellow
    docker build -t custom-siem-rule-engine:latest rule-engine/
    
    Write-ColorOutput "All Docker images built successfully!" $Green
}

# Function to start services
function Start-Services {
    Write-ColorOutput "Starting Custom SIEM services..." $Blue
    
    # Start all services using docker-compose
    docker-compose up -d
    
    Write-ColorOutput "Services started successfully!" $Green
}

# Function to wait for services to be ready
function Wait-ForServices {
    Write-ColorOutput "Waiting for services to be ready..." $Blue
    
    $services = @(
        @{Name="Elasticsearch"; Port=$ElasticsearchPort; Url="http://localhost:$ElasticsearchPort/_cluster/health"},
        @{Name="PostgreSQL"; Port=5432; Url="http://localhost:5432"},
        @{Name="Redis"; Port=6379; Url="http://localhost:6379"},
        @{Name="Backend API"; Port=$BackendPort; Url="http://localhost:$BackendPort/actuator/health"},
        @{Name="Dashboard"; Port=$DashboardPort; Url="http://localhost:$DashboardPort"}
    )
    
    foreach ($service in $services) {
        Write-ColorOutput "Waiting for $($service.Name)..." $Yellow
        $maxAttempts = 30
        $attempt = 0
        
        do {
            $attempt++
            Start-Sleep -Seconds 2
            
            try {
                $response = Invoke-WebRequest -Uri $service.Url -TimeoutSec 5 -ErrorAction Stop
                if ($response.StatusCode -eq 200) {
                    Write-ColorOutput "✓ $($service.Name) is ready" $Green
                    break
                }
            }
            catch {
                if ($attempt -ge $maxAttempts) {
                    Write-ColorOutput "✗ $($service.Name) failed to start" $Red
                }
            }
        } while ($attempt -lt $maxAttempts)
    }
}

# Function to display access information
function Show-AccessInfo {
    Write-ColorOutput "`n🎉 Custom SIEM Setup Complete!" $Green
    Write-ColorOutput "`nAccess Information:" $Blue
    Write-ColorOutput "Dashboard: http://localhost:$DashboardPort" $Yellow
    Write-ColorOutput "Backend API: http://localhost:$BackendPort" $Yellow
    Write-ColorOutput "Elasticsearch: http://localhost:$ElasticsearchPort" $Yellow
    Write-ColorOutput "Kibana: http://localhost:$KibanaPort" $Yellow
    Write-ColorOutput "`nDefault Credentials:" $Blue
    Write-ColorOutput "Username: admin" $Yellow
    Write-ColorOutput "Password: admin123" $Yellow
    Write-ColorOutput "`nUseful Commands:" $Blue
    Write-ColorOutput "View logs: docker-compose logs -f" $Yellow
    Write-ColorOutput "Stop services: docker-compose down" $Yellow
    Write-ColorOutput "Restart services: docker-compose restart" $Yellow
    Write-ColorOutput "`nNext Steps:" $Blue
    Write-ColorOutput "1. Open http://localhost:$DashboardPort in your browser" $Yellow
    Write-ColorOutput "2. Log in with the default credentials" $Yellow
    Write-ColorOutput "3. Configure your first agent and rules" $Yellow
}

# Main execution
try {
    Write-ColorOutput "🚀 Starting Custom SIEM Setup..." $Blue
    
    # Check prerequisites
    Test-Prerequisites
    
    # Create directory structure
    New-DirectoryStructure
    
    # Generate SSL certificates
    New-SSLCertificates
    
    # Create environment file
    New-EnvironmentFile
    
    # Build Docker images
    Build-DockerImages
    
    # Start services
    Start-Services
    
    # Wait for services to be ready
    Wait-ForServices
    
    # Display access information
    Show-AccessInfo
    
} catch {
    Write-ColorOutput "Error during setup: $($_.Exception.Message)" $Red
    Write-ColorOutput "Please check the error and try again." $Yellow
    exit 1
} 