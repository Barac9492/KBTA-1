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
