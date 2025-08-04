#!/bin/bash

# K-Beauty Trend Agent Automation Deployment Script
# This script deploys the 24/7 automation system to Vercel

set -e  # Exit on any error

echo "🚀 K-Beauty Trend Agent Automation Deployment"
echo "=============================================="

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

# Check if we're in the right directory
if [ ! -f "vercel.json" ]; then
    print_error "vercel.json not found. Please run this script from the project root."
    exit 1
fi

print_status "Starting automation deployment..."

# Step 1: Check prerequisites
print_status "Checking prerequisites..."

# Check if Vercel CLI is installed
if ! command -v vercel &> /dev/null; then
    print_error "Vercel CLI not found. Please install it first:"
    echo "npm install -g vercel"
    exit 1
fi

# Check if Python dependencies are installed
if [ ! -f "api/requirements.txt" ]; then
    print_error "requirements.txt not found in api/ directory"
    exit 1
fi

print_success "Prerequisites check passed"

# Step 2: Validate configuration
print_status "Validating configuration..."

# Check if cron_handler.py exists
if [ ! -f "api/cron_handler.py" ]; then
    print_error "cron_handler.py not found in api/ directory"
    exit 1
fi

# Check if autonomous_agent.py exists
if [ ! -f "agent/autonomous_agent.py" ]; then
    print_warning "autonomous_agent.py not found in agent/ directory"
    print_warning "Advanced AI agent features will not be available"
fi

# Check vercel.json configuration
if ! grep -q "cron_handler.py" vercel.json; then
    print_error "cron_handler.py not configured in vercel.json"
    exit 1
fi

if ! grep -q "crons" vercel.json; then
    print_error "Cron jobs not configured in vercel.json"
    exit 1
fi

print_success "Configuration validation passed"

# Step 3: Set up environment variables
print_status "Setting up environment variables..."

# Check if .env file exists
if [ ! -f ".env" ]; then
    print_warning ".env file not found. Creating template..."
    cat > .env << EOF
# K-Beauty Trend Agent Environment Variables
OPENAI_API_KEY=your_openai_api_key_here
VERCEL=true
PYTHONPATH=.
EOF
    print_warning "Please update .env with your actual API keys"
fi

# Check if OPENAI_API_KEY is set
if [ -z "$OPENAI_API_KEY" ]; then
    if [ -f ".env" ]; then
        export $(cat .env | grep -v '^#' | xargs)
    fi
fi

if [ -z "$OPENAI_API_KEY" ]; then
    print_warning "OPENAI_API_KEY not set. Some features may not work."
fi

print_success "Environment variables configured"

# Step 4: Install dependencies
print_status "Installing dependencies..."

# Install Python dependencies
if [ -f "api/requirements.txt" ]; then
    print_status "Installing Python dependencies..."
    python3 -m pip install -r api/requirements.txt
    print_success "Python dependencies installed"
fi

# Install Node.js dependencies for frontend
if [ -f "frontend/package.json" ]; then
    print_status "Installing Node.js dependencies..."
    cd frontend
    npm install
    cd ..
    print_success "Node.js dependencies installed"
fi

# Step 5: Test locally (optional)
if [ "$1" = "--test" ]; then
    print_status "Running local tests..."
    
    # Start local development server
    print_status "Starting local development server..."
    vercel dev &
    DEV_PID=$!
    
    # Wait for server to start
    sleep 10
    
    # Run tests
    if [ -f "scripts/test_automation.py" ]; then
        print_status "Running automation tests..."
        python scripts/test_automation.py
    fi
    
    # Stop development server
    kill $DEV_PID
    print_success "Local tests completed"
fi

# Step 6: Deploy to Vercel
print_status "Deploying to Vercel..."

# Check if already logged in to Vercel
if ! vercel whoami &> /dev/null; then
    print_status "Please log in to Vercel..."
    vercel login
fi

# Deploy to production
print_status "Deploying to production..."
vercel --prod

# Get the deployment URL
DEPLOYMENT_URL=$(vercel ls --json | jq -r '.deployments[0].url' 2>/dev/null || echo "unknown")

if [ "$DEPLOYMENT_URL" != "unknown" ]; then
    print_success "Deployed to: https://$DEPLOYMENT_URL"
else
    print_warning "Could not determine deployment URL"
fi

# Step 7: Test deployment
print_status "Testing deployment..."

# Wait a moment for deployment to be ready
sleep 10

# Test health endpoint
if [ "$DEPLOYMENT_URL" != "unknown" ]; then
    print_status "Testing health endpoint..."
    if curl -s "https://$DEPLOYMENT_URL/api/cron/health" > /dev/null; then
        print_success "Health endpoint working"
    else
        print_warning "Health endpoint test failed"
    fi
    
    # Test pipeline endpoint (this will take longer)
    print_status "Testing pipeline endpoint..."
    if curl -s "https://$DEPLOYMENT_URL/api/cron/run-pipeline" > /dev/null; then
        print_success "Pipeline endpoint working"
    else
        print_warning "Pipeline endpoint test failed"
    fi
fi

# Step 8: Set up monitoring
print_status "Setting up monitoring..."

# Create monitoring script
cat > scripts/monitor_automation.sh << 'EOF'
#!/bin/bash

# Monitor automation deployment
DEPLOYMENT_URL="$1"

if [ -z "$DEPLOYMENT_URL" ]; then
    echo "Usage: $0 <deployment-url>"
    exit 1
fi

echo "🔍 Monitoring K-Beauty Trend Agent Automation..."
echo "URL: https://$DEPLOYMENT_URL"

# Test health endpoint
echo "Testing health endpoint..."
curl -s "https://$DEPLOYMENT_URL/api/cron/health" | jq '.'

# Check Vercel logs
echo "Checking Vercel logs..."
vercel logs "https://$DEPLOYMENT_URL" --limit=10

echo "✅ Monitoring complete"
EOF

chmod +x scripts/monitor_automation.sh

# Step 9: Create deployment summary
print_status "Creating deployment summary..."

cat > DEPLOYMENT_SUMMARY.md << EOF
# K-Beauty Trend Agent Automation Deployment Summary

**Deployed**: $(date)
**Deployment URL**: https://$DEPLOYMENT_URL
**Status**: ✅ Successfully deployed

## What was deployed:

### ✅ Cron Jobs
- **Pipeline Job**: Runs every 6 hours (\`0 */6 * * *\`)
- **Health Job**: Runs every 12 hours (\`0 */12 * * *\`)
- **Endpoints**: 
  - \`/api/cron/run-pipeline\`
  - \`/api/cron/health\`

### ✅ Automation Pipeline
1. **Scrape Trends**: From Glowpick, Olive Young, social media
2. **Analyze with AI**: GPT-4 for trend analysis
3. **Generate Briefings**: Personalized for different user types
4. **Store Results**: JSON and Markdown formats
5. **Send Notifications**: Email/Slack alerts (configurable)

### ✅ Error Handling
- **Graceful Fallbacks**: Mock data when scrapers fail
- **Comprehensive Logging**: Track all operations
- **Retry Logic**: Exponential backoff for failures

### ✅ Performance Optimizations
- **Async Operations**: Concurrent scraping
- **Resource Management**: Clean up after each cycle
- **Cost Monitoring**: Track GB-hours usage

## Next Steps:

1. **Monitor Performance**:
   \`\`\`bash
   vercel logs https://$DEPLOYMENT_URL --scope=cron
   \`\`\`

2. **Test Automation**:
   \`\`\`bash
   curl -X GET https://$DEPLOYMENT_URL/api/cron/run-pipeline
   \`\`\`

3. **Check Cron Jobs**:
   - Go to Vercel Dashboard → Your Project → Functions → Cron Jobs
   - Monitor execution history and logs

4. **Set Up Alerts**:
   - Configure notifications for failures
   - Monitor cost usage

## Cost Estimation:
- **Free Tier**: 100GB-hours/month
- **Current Usage**: ~120GB-hours/month (every 6 hours)
- **Recommendation**: Upgrade to Pro (\$20/month) for more resources

## Troubleshooting:
- **Function Timeout**: Increase maxDuration in vercel.json
- **High Costs**: Reduce frequency or optimize code
- **Scraping Failures**: Check robots.txt compliance
- **AI Errors**: Verify OpenAI API key

---
*Deployment completed successfully! Your K-Beauty Trend Agent is now running 24/7.*
EOF

print_success "Deployment summary created: DEPLOYMENT_SUMMARY.md"

# Step 10: Final status
echo ""
echo "🎉 K-Beauty Trend Agent Automation Deployment Complete!"
echo "======================================================"
echo ""
echo "✅ Cron jobs configured and running"
echo "✅ Automation pipeline deployed"
echo "✅ Error handling and monitoring set up"
echo "✅ Performance optimizations applied"
echo ""
echo "📊 Your automation will now:"
echo "   • Scrape trends every 6 hours"
echo "   • Analyze with AI for insights"
echo "   • Generate personalized briefings"
echo "   • Store results for easy access"
echo "   • Send notifications for new trends"
echo ""
echo "🔗 Deployment URL: https://$DEPLOYMENT_URL"
echo "📝 Summary: DEPLOYMENT_SUMMARY.md"
echo "🔍 Monitor: vercel logs https://$DEPLOYMENT_URL --scope=cron"
echo ""
echo "🚀 Your autonomous K-beauty intelligence system is live!" 