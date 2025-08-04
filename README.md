# 🎯 K-Beauty Trend Agent

> **AI-Powered Daily Korean Beauty Trend Analysis**  
> Automated scraping, analysis, and synthesis of K-beauty trends using GPT-4

[![Deploy on Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/yourusername/kbeauty-trend-agent)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 🚀 Live Demo

**Frontend**: https://kbeauty-trend-agent-32nl74itm-ethancho12-gmailcoms-projects.vercel.app  
**API**: https://kbeauty-trend-agent-32nl74itm-ethancho12-gmailcoms-projects.vercel.app/api

## ✨ Features

### 🤖 AI-Powered Analysis
- **GPT-4 Integration**: Advanced trend analysis and synthesis
- **Multi-Source Scraping**: Korean beauty blogs, social media, product reviews
- **Real-time Insights**: Daily automated briefings with actionable recommendations

### 🔄 Automated Workflow
- **Serverless Architecture**: Deployed on Vercel with zero maintenance
- **Webhook Integration**: Compatible with Make.com, Zapier, and custom automation
- **Background Processing**: Non-blocking analysis pipeline

### 📊 Rich Output Formats
- **Markdown Reports**: Beautiful, formatted briefings
- **JSON Data**: Structured data for integrations
- **Notion Integration**: Direct publishing to Notion databases
- **Real-time Streaming**: Instant markdown preview

## 🛠 Tech Stack

| Component | Technology |
|-----------|------------|
| **Backend** | FastAPI, Python 3.11+ |
| **Frontend** | Next.js 15, TypeScript, Tailwind CSS |
| **AI/ML** | OpenAI GPT-4, Custom Prompt Engineering |
| **Deployment** | Vercel (Serverless Functions) |
| **Database** | File-based (JSON) + Notion (Optional) |
| **Monitoring** | Built-in logging and health checks |

## 🚀 Quick Start

### 1. Clone & Setup

```bash
git clone https://github.com/yourusername/kbeauty-trend-agent.git
cd kbeauty-trend-agent
```

### 2. Environment Configuration

```bash
cp env.example .env
```

Edit `.env` with your API keys:

```env
# Required
OPENAI_API_KEY=sk-your-openai-key-here

# Optional (for Notion integration)
NOTION_TOKEN=your-notion-token
NOTION_DATABASE_ID=your-database-id

# Optional (for custom sources)
NAVER_CLIENT_ID=your-naver-client-id
NAVER_CLIENT_SECRET=your-naver-client-secret
```

### 3. Local Development

```bash
# Install dependencies
pip install -r requirements.txt
cd frontend && npm install

# Start API server
python api/main.py

# Start frontend (in another terminal)
cd frontend && npm run dev
```

### 4. Deploy to Vercel

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel --prod
```

## 📡 API Endpoints

### Core Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/health` | GET | Health check and configuration status |
| `/api/latest` | GET | Get latest briefing data |
| `/api/markdown` | GET | Stream latest briefing as markdown |
| `/api/download/json` | GET | Download latest briefing as JSON |
| `/api/trigger` | POST | Manually trigger new analysis |
| `/api/webhook` | POST | Webhook endpoint for automation |

### Example Usage

```bash
# Health check
curl https://your-app.vercel.app/api/health

# Get latest briefing
curl https://your-app.vercel.app/api/latest

# Trigger new analysis
curl -X POST https://your-app.vercel.app/api/trigger \
  -H "Content-Type: application/json" \
  -d '{"force_refresh": false, "include_notion_push": true}'

# Download markdown
curl https://your-app.vercel.app/api/markdown
```

## 🔧 Configuration

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `OPENAI_API_KEY` | ✅ | OpenAI API key for GPT-4 |
| `NOTION_TOKEN` | ❌ | Notion integration token |
| `NOTION_DATABASE_ID` | ❌ | Notion database ID |
| `VERCEL` | Auto | Set to "true" on Vercel |

### Customization

#### Adding New Sources

Edit `core/config.py`:

```python
def get_sources_config(self) -> Dict:
    return {
        "your_new_source": {
            "urls": ["https://your-source.com"],
            "selectors": {
                "posts": "your-css-selector",
                "title": "title-selector",
                "content": "content-selector"
            }
        }
    }
```

#### Modifying Analysis Prompts

Edit `core/pipeline.py` to customize GPT-4 prompts for:
- Trend identification
- Executive summaries
- Actionable recommendations

## 🤖 Automation Examples

### Make.com Webhook

```json
{
  "source": "make.com",
  "event_type": "daily_trigger",
  "data": {
    "schedule": "daily",
    "time": "09:00"
  }
}
```

### GitHub Actions (Daily)

```yaml
name: Daily K-Beauty Analysis
on:
  schedule:
    - cron: '0 9 * * *'

jobs:
  trigger-analysis:
    runs-on: ubuntu-latest
    steps:
      - name: Trigger Analysis
        run: |
          curl -X POST ${{ secrets.API_URL }}/api/trigger \
            -H "Content-Type: application/json"
```

### Slack Integration

```python
import requests

def send_to_slack(briefing_data):
    webhook_url = "your-slack-webhook"
    message = {
        "text": f"📊 Daily K-Beauty Briefing\n{briefing_data['executive_summary']}"
    }
    requests.post(webhook_url, json=message)
```

## 📈 Performance & Monitoring

### Built-in Monitoring

- **File Operations Logging**: Track all file writes and sizes
- **Error Tracking**: Comprehensive error logging with stack traces
- **Health Checks**: Real-time API health monitoring
- **Vercel Analytics**: Built-in performance monitoring

### Optimization Tips

1. **Use /tmp for Vercel**: All file operations automatically use ephemeral storage
2. **Background Processing**: Long-running analysis doesn't block API responses
3. **Caching**: Latest briefing data is cached for fast retrieval
4. **Error Recovery**: Graceful fallbacks for failed operations

## 🔍 Troubleshooting

### Common Issues

#### 1. Vercel Function Timeout
```bash
# Increase timeout in vercel.json
{
  "functions": {
    "api/main.py": {
      "maxDuration": 60
    }
  }
}
```

#### 2. OpenAI Rate Limits
```python
# Add retry logic in core/config.py
import time
import openai

def retry_openai_call(func, max_retries=3):
    for i in range(max_retries):
        try:
            return func()
        except openai.RateLimitError:
            time.sleep(2 ** i)  # Exponential backoff
```

#### 3. File System Issues
```python
# Automatic fallback to /tmp
output_dir = "/tmp" if os.getenv("VERCEL") else "output"
```

### Debug Commands

```bash
# Check API health
curl https://your-app.vercel.app/api/health

# View deployment logs
vercel logs your-app.vercel.app

# Test webhook locally
curl -X POST http://localhost:8000/api/webhook \
  -H "Content-Type: application/json" \
  -d '{"source": "test", "event_type": "manual"}'
```

## 🎯 Use Cases

### For Beauty Brands
- **Trend Monitoring**: Track emerging K-beauty trends
- **Product Development**: Identify market opportunities
- **Competitive Analysis**: Monitor competitor activities

### For Content Creators
- **Content Ideas**: Generate trending topics for videos/blogs
- **Product Reviews**: Stay updated on latest releases
- **Audience Engagement**: Understand what resonates with viewers

### For Researchers
- **Market Analysis**: Quantitative trend data
- **Academic Research**: Korean beauty industry insights
- **Data Collection**: Automated scraping and analysis

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines

- **TypeScript**: Strict typing for frontend components
- **Python**: Type hints and docstrings for all functions
- **Testing**: Unit tests for core functionality
- **Documentation**: Comprehensive docstrings and README updates

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **OpenAI**: For GPT-4 API access
- **Vercel**: For serverless hosting
- **Next.js Team**: For the amazing React framework
- **FastAPI**: For the high-performance Python web framework

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/kbeauty-trend-agent/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/kbeauty-trend-agent/discussions)
- **Email**: your-email@example.com

---

**Built with ❤️ for the K-beauty community**

*This project demonstrates modern AI-powered automation, combining web scraping, natural language processing, and serverless architecture to deliver actionable business insights.* 