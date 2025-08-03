#!/bin/bash

# K-Beauty Trend Agent - Vercel Deployment Script
set -e

echo "🎀 Deploying K-Beauty Trend Agent to Vercel..."

# Check if Vercel CLI is installed
if ! command -v vercel &> /dev/null; then
    echo "❌ Vercel CLI not found. Installing..."
    npm install -g vercel
fi

# Create .vercelignore file
cat > .vercelignore << EOF
venv/
__pycache__/
*.pyc
.env
.env.local
output/
logs/
*.log
test_*
EOF

# Create vercel.json if it doesn't exist
if [ ! -f vercel.json ]; then
    echo "Creating vercel.json configuration..."
    cat > vercel.json << EOF
{
  "version": 2,
  "builds": [
    {
      "src": "frontend/package.json",
      "use": "@vercel/next",
      "config": {
        "distDir": "frontend/.next"
      }
    },
    {
      "src": "api/main.py",
      "use": "@vercel/python",
      "config": {
        "maxLambdaSize": "15mb"
      }
    }
  ],
  "routes": [
    {
      "src": "/api/(.*)",
      "dest": "/api/main.py"
    },
    {
      "src": "/(.*)",
      "dest": "/frontend/$1"
    }
  ],
  "env": {
    "PYTHONPATH": "."
  },
  "functions": {
    "api/main.py": {
      "runtime": "python3.9"
    }
  }
}
EOF
fi

# Set up environment variables
echo "Setting up environment variables..."
if [ -f .env ]; then
    echo "Found .env file. Setting up Vercel environment variables..."
    # Extract and set environment variables
    while IFS= read -r line; do
        if [[ $line =~ ^[A-Z_]+=.*$ ]]; then
            key=$(echo "$line" | cut -d'=' -f1)
            value=$(echo "$line" | cut -d'=' -f2-)
            echo "Setting $key..."
            vercel env add "$key" production <<< "$value" || true
        fi
    done < .env
fi

# Deploy to Vercel
echo "🚀 Deploying to Vercel..."
vercel --prod

echo "✅ Deployment completed!"
echo "📝 Next steps:"
echo "1. Set up your environment variables in Vercel dashboard"
echo "2. Configure your domain (optional)"
echo "3. Set up webhooks for automated briefings" 