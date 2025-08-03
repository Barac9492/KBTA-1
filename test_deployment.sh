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
