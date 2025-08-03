#!/bin/bash

# K-Beauty Trend Briefing System Deployment Script

set -e  # Exit on any error

echo "🎀 K-Beauty Trend Briefing System - Deployment"
echo "================================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

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

# Check if Python 3.8+ is installed
print_status "Checking Python version..."
python_version=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
required_version="3.8"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" = "$required_version" ]; then
    print_success "Python $python_version is installed"
else
    print_error "Python 3.8+ is required. Current version: $python_version"
    exit 1
fi

# Create virtual environment
print_status "Setting up virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    print_success "Virtual environment created"
else
    print_warning "Virtual environment already exists"
fi

# Activate virtual environment
print_status "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
print_status "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
print_status "Installing Python dependencies..."
pip install -r requirements.txt
print_success "Dependencies installed"

# Install Playwright browsers
print_status "Installing Playwright browsers..."
playwright install chromium
print_success "Playwright browsers installed"

# Create necessary directories
print_status "Creating directories..."
mkdir -p output logs data
print_success "Directories created"

# Setup environment file
print_status "Setting up environment configuration..."
if [ ! -f ".env" ]; then
    cp env.example .env
    print_warning "Environment file created from template"
    print_warning "Please edit .env with your API keys before running"
else
    print_warning "Environment file already exists"
fi

# Test the setup
print_status "Testing setup..."
python3 run_daily_briefing.py --help > /dev/null 2>&1
if [ $? -eq 0 ]; then
    print_success "Setup test passed"
else
    print_error "Setup test failed"
    exit 1
fi

# Create systemd service file (optional)
print_status "Creating systemd service file..."
cat > kbeauty-briefing.service << EOF
[Unit]
Description=K-Beauty Daily Trend Briefing API
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=$(pwd)
Environment=PATH=$(pwd)/venv/bin
ExecStart=$(pwd)/venv/bin/uvicorn api.main:app --host 0.0.0.0 --port 8000
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

print_success "Systemd service file created: kbeauty-briefing.service"

# Create startup script
print_status "Creating startup script..."
cat > start_api.sh << 'EOF'
#!/bin/bash
cd "$(dirname "$0")"
source venv/bin/activate
uvicorn api.main:app --host 0.0.0.0 --port 8000
EOF

chmod +x start_api.sh
print_success "Startup script created: start_api.sh"

# Create test script
print_status "Creating test script..."
cat > test_deployment.sh << 'EOF'
#!/bin/bash
echo "🧪 Testing K-Beauty Briefing Deployment"
echo "========================================"

# Test API health
echo "Testing API health..."
curl -s http://localhost:8000/health || echo "API not running"

# Test webhook
echo "Testing webhook..."
curl -X POST http://localhost:8000/webhook \
  -H "Content-Type: application/json" \
  -d '{"source": "test", "event_type": "deployment_test"}' || echo "Webhook test failed"

echo "✅ Deployment test completed"
EOF

chmod +x test_deployment.sh
print_success "Test script created: test_deployment.sh"

# Print next steps
echo ""
echo "🎉 Deployment completed successfully!"
echo "====================================="
echo ""
echo "Next steps:"
echo "1. Edit .env file with your API keys:"
echo "   - OPENAI_API_KEY (required)"
echo "   - NOTION_TOKEN (optional)"
echo "   - NOTION_DATABASE_ID (optional)"
echo ""
echo "2. Start the API server:"
echo "   ./start_api.sh"
echo "   # or"
echo "   source venv/bin/activate && uvicorn api.main:app --host 0.0.0.0 --port 8000"
echo ""
echo "3. Test the deployment:"
echo "   ./test_deployment.sh"
echo ""
echo "4. Run a test briefing:"
echo "   python3 run_daily_briefing.py --dry-run --verbose"
echo ""
echo "5. Set up Make.com automation:"
echo "   - Follow make_com_webhook_example.md"
echo "   - Configure 6AM KST schedule"
echo ""
echo "6. Monitor logs:"
echo "   tail -f briefing.log"
echo "   tail -f briefing_success.log"
echo "   tail -f briefing_error.log"
echo ""
echo "📚 Documentation: README.md"
echo "🔧 Configuration: .env"
echo "🚀 API: http://localhost:8000"
echo "" 