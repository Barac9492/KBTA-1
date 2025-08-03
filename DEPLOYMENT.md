# 🚀 K-Beauty Trend Agent - Vercel Deployment Guide

This guide will help you deploy your K-Beauty Trend Agent to Vercel with both the FastAPI backend and Next.js frontend.

## 📋 Prerequisites

- Vercel account (free tier available)
- GitHub repository with your code
- Environment variables ready

## 🛠️ Deployment Steps

### 1. Prepare Your Repository

Make sure your repository has the following structure:
```
kbeauty-trend-agent/
├── api/
│   ├── main.py
│   └── requirements.txt
├── frontend/
│   ├── package.json
│   └── src/
├── core/
├── vercel.json
├── .vercelignore
└── requirements.txt
```

### 2. Environment Variables

Set up these environment variables in your Vercel dashboard:

**Required:**
- `OPENAI_API_KEY` - Your OpenAI API key
- `NOTION_TOKEN` - Your Notion integration token (if using Notion)
- `NOTION_DATABASE_ID` - Your Notion database ID (if using Notion)

**Optional:**
- `API_HOST` - API host (default: 0.0.0.0)
- `API_PORT` - API port (default: 8000)
- `LOG_LEVEL` - Logging level (default: INFO)
- `SCHEDULE_TIME` - Daily briefing time (default: 06:00)
- `AUTO_RUN` - Auto-run briefings (default: false)

### 3. Deploy to Vercel

#### Option A: Using Vercel CLI

1. **Install Vercel CLI:**
   ```bash
   npm install -g vercel
   ```

2. **Login to Vercel:**
   ```bash
   vercel login
   ```

3. **Deploy:**
   ```bash
   vercel --prod
   ```

#### Option B: Using GitHub Integration

1. Go to [vercel.com](https://vercel.com)
2. Click "New Project"
3. Import your GitHub repository
4. Configure build settings:
   - **Framework Preset:** Other
   - **Build Command:** `npm run build` (for frontend)
   - **Output Directory:** `frontend/.next`
   - **Install Command:** `cd frontend && npm install`

### 4. Configure Build Settings

In your Vercel project settings:

1. **Build & Development Settings:**
   - Framework Preset: Other
   - Build Command: `cd frontend && npm run build`
   - Output Directory: `frontend/.next`
   - Install Command: `cd frontend && npm install`

2. **Environment Variables:**
   Add all required environment variables from step 2.

3. **Functions:**
   - Runtime: Python 3.9
   - Max Duration: 30 seconds (for API functions)

### 5. Test Your Deployment

After deployment, test these endpoints:

- **Frontend:** `https://your-project.vercel.app`
- **API Health:** `https://your-project.vercel.app/api/health`
- **Latest Briefing:** `https://your-project.vercel.app/api/latest`

## 🔧 Configuration Files

### vercel.json
```json
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
```

### .vercelignore
```
venv/
__pycache__/
*.pyc
.env
output/
logs/
*.log
node_modules/
```

## 🚨 Common Issues & Solutions

### Issue 1: Python Dependencies Not Found
**Solution:** Make sure `api/requirements.txt` exists and contains all necessary dependencies.

### Issue 2: Frontend Not Building
**Solution:** 
1. Check that `frontend/package.json` exists
2. Ensure all dependencies are listed
3. Verify Next.js configuration

### Issue 3: API Routes Not Working
**Solution:**
1. Check that `api/main.py` exists
2. Verify environment variables are set
3. Check function timeout settings

### Issue 4: CORS Errors
**Solution:** The API is configured to handle CORS automatically, but if issues persist, check the FastAPI CORS settings in `api/main.py`.

## 📊 Monitoring & Logs

### View Logs
1. Go to your Vercel dashboard
2. Select your project
3. Click on "Functions" tab
4. View logs for each function

### Monitor Performance
- Check function execution times
- Monitor API response times
- Track error rates

## 🔄 Continuous Deployment

### Automatic Deployments
- Push to `main` branch triggers automatic deployment
- Preview deployments for pull requests
- Branch deployments for testing

### Manual Deployments
```bash
vercel --prod
```

## 🛡️ Security Considerations

1. **Environment Variables:** Never commit sensitive data
2. **API Keys:** Use Vercel's environment variable system
3. **CORS:** Configure properly for production domains
4. **Rate Limiting:** Consider implementing rate limiting for API endpoints

## 📈 Scaling Considerations

### Free Tier Limits
- 100GB bandwidth/month
- 100 serverless function executions/day
- 10-second function timeout

### Pro Tier Benefits
- Unlimited bandwidth
- 10,000 serverless function executions/day
- 60-second function timeout
- Custom domains

## 🔧 Post-Deployment Setup

### 1. Set Up Custom Domain (Optional)
1. Go to Vercel dashboard
2. Navigate to "Settings" > "Domains"
3. Add your custom domain
4. Configure DNS records

### 2. Set Up Webhooks
Configure your Make.com webhook to point to:
```
https://your-project.vercel.app/api/webhook
```

### 3. Monitor Performance
- Set up alerts for function errors
- Monitor API response times
- Track user engagement

## 🆘 Troubleshooting

### Debug Deployment Issues
```bash
# View deployment logs
vercel logs

# Check function status
vercel ls

# Redeploy specific function
vercel --prod --force
```

### Common Error Messages

**"Module not found"**
- Check that all dependencies are in `requirements.txt`
- Verify Python version compatibility

**"Function timeout"**
- Increase timeout in vercel.json
- Optimize your code for faster execution

**"Build failed"**
- Check build logs in Vercel dashboard
- Verify all required files exist
- Check for syntax errors

## 📞 Support

If you encounter issues:

1. Check the [Vercel documentation](https://vercel.com/docs)
2. Review your deployment logs
3. Test locally first
4. Contact Vercel support if needed

## 🎉 Success!

Once deployed, your K-Beauty Trend Agent will be available at:
- **Frontend:** `https://your-project.vercel.app`
- **API:** `https://your-project.vercel.app/api/*`

The system will automatically handle both the Next.js frontend and FastAPI backend on the same domain! 