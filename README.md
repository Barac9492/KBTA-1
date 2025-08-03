# K-Beauty Daily Trend Briefing System

An intelligent, modular AI system that delivers daily Korean beauty trend briefings to US buyers. Built with clean architecture, automated pipelines, and multiple output formats.

## 🎯 Overview

This system automatically:
1. **Scrapes** Korean beauty content from Naver, Instagram, and YouTube
2. **Analyzes** trends using GPT-4-powered AI agents
3. **Synthesizes** insights into actionable business intelligence
4. **Delivers** daily briefings in Markdown, JSON, and Notion formats
5. **Provides** RESTful API for automation and integration

## 🏗️ Architecture

```
kbeauty-trend-agent/
├── core/                    # Core business logic
│   ├── config.py           # Centralized configuration
│   ├── models.py           # Data models and types
│   ├── scraper.py          # Modular web scraper
│   ├── agents.py           # AI agent pipeline
│   ├── output.py           # Output handlers
│   └── pipeline.py         # Main orchestration
├── agents/                  # AI agent prompts
│   ├── trend-researcher.md
│   └── feedback-synthesizer.md
├── api/                     # FastAPI application
│   └── main.py             # RESTful API endpoints
├── output/                  # Generated briefings
├── scripts/                 # Legacy scripts (deprecated)
├── frontend/                # React dashboard
├── data/                    # Sample data
├── run_daily_briefing.py   # Simple execution script
├── requirements.txt         # Dependencies
├── env.example             # Environment template
└── README.md               # This file
```

## 🚀 Quick Start

### 1. Setup Environment

```bash
# Clone and setup
git clone <repository>
cd kbeauty-trend-agent

# Install dependencies
pip install -r requirements.txt
playwright install chromium

# Copy environment template
cp env.example .env
```

### 2. Configure Environment

Edit `.env` with your API keys:

```bash
# Required
OPENAI_API_KEY=your_openai_api_key_here

# Optional - Notion Integration
NOTION_TOKEN=your_notion_token_here
NOTION_DATABASE_ID=your_database_id_here

# Optional - Custom Settings
SCHEDULE_TIME=09:00
AUTO_RUN=false
MARKDOWN_ENABLED=true
JSON_ENABLED=true
```

### 3. Run Daily Briefing

```bash
# Simple execution
python run_daily_briefing.py

# Or via API
uvicorn api.main:app --reload
curl -X POST http://localhost:8000/trigger
```

## 📊 Features

### 🔍 **Intelligent Scraping**
- **Playwright-based** dynamic content scraping
- **Multi-source** collection (Naver, Instagram, YouTube)
- **Relevance filtering** for K-beauty content
- **Rate limiting** and error handling

### 🤖 **AI-Powered Analysis**
- **GPT-4** trend research and synthesis
- **Modular agents** with specialized prompts
- **Business intelligence** generation
- **Confidence scoring** for trends

### 📤 **Multiple Output Formats**
- **Markdown** - Human-readable briefings
- **JSON** - Machine-readable data
- **Notion** - Team collaboration database
- **API** - RESTful endpoints for automation

### ⚡ **Automation Ready**
- **Daily scheduling** with configurable timing
- **Webhook support** for external triggers
- **Background processing** for scalability
- **Status monitoring** and error handling

## 🛠️ Usage

### Manual Execution

```bash
# Run a single briefing
python run_daily_briefing.py

# Run with custom settings
python -c "
import asyncio
from core.pipeline import DailyBriefingPipeline
pipeline = DailyBriefingPipeline()
asyncio.run(pipeline.run_daily_briefing())
"
```

### API Endpoints

```bash
# Start API server
uvicorn api.main:app --reload

# Trigger briefing
curl -X POST http://localhost:8000/trigger

# Get status
curl http://localhost:8000/status

# Get latest briefing
curl http://localhost:8000/latest

# Download briefing files
curl http://localhost:8000/download/markdown
curl http://localhost:8000/download/json

# Start automated scheduler
curl -X POST http://localhost:8000/scheduler/start
```

### Webhook Integration

```bash
# Trigger via webhook
curl -X POST http://localhost:8000/webhook \
  -H "Content-Type: application/json" \
  -d '{"source": "make.com", "event_type": "daily_trigger"}'
```

## 🔧 Configuration

### Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `OPENAI_API_KEY` | ✅ | - | OpenAI API key |
| `NOTION_TOKEN` | ❌ | - | Notion integration token |
| `NOTION_DATABASE_ID` | ❌ | - | Notion database ID |
| `SCHEDULE_TIME` | ❌ | `09:00` | Daily run time (HH:MM) |
| `AUTO_RUN` | ❌ | `false` | Enable automatic scheduling |
| `MARKDOWN_ENABLED` | ❌ | `true` | Enable Markdown output |
| `JSON_ENABLED` | ❌ | `true` | Enable JSON output |
| `OUTPUT_DIR` | ❌ | `output` | Output directory path |

### Scraping Sources

The system scrapes from:
- **Naver Beauty** - Korean beauty blogs and communities
- **Instagram** - K-beauty hashtags and influencers
- **YouTube** - Korean beauty channels and reviews

### Output Formats

#### Markdown Briefing
```markdown
# K-Beauty Daily Briefing - January 15, 2024

## Executive Summary
[AI-generated summary of current trends]

## Priority Trends
### #1 Glass Skin Technique
- **Business Impact**: High
- **Time to Market**: Immediate
- **Target Audience**: 20-35, beauty enthusiasts
- **Recommendations**:
  - Develop multi-step routine products
  - Focus on transparency-enhancing ingredients
```

#### JSON Structure
```json
{
  "briefing_id": "briefing_20240115_103000",
  "date": "2024-01-15T10:30:00",
  "scraped_posts_count": 45,
  "trend_analysis": { ... },
  "synthesis_results": { ... }
}
```

## 🔄 Automation with Make.com

### Webhook Setup
1. Create a Make.com scenario
2. Add HTTP webhook trigger
3. Configure to call `POST /webhook` endpoint
4. Set up daily scheduling in Make.com

### Example Make.com Flow
```
Daily Trigger → HTTP Webhook → K-Beauty API → 
Slack Notification → Notion Update → Email Digest
```

### Webhook Payload
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

## 📈 Monitoring & Analytics

### Pipeline Status
```bash
# Check pipeline status
curl http://localhost:8000/status

# Response
{
  "status": "completed",
  "start_time": "2024-01-15T09:00:00",
  "end_time": "2024-01-15T09:15:30",
  "briefing_id": "briefing_20240115_090000"
}
```

### Health Check
```bash
curl http://localhost:8000/health

# Response
{
  "status": "healthy",
  "openai_configured": true,
  "notion_configured": false,
  "output_dir": "/path/to/output"
}
```

## 🛡️ Error Handling

The system includes comprehensive error handling:
- **Scraping failures** - Graceful degradation with partial results
- **API timeouts** - Retry logic with exponential backoff
- **Rate limiting** - Automatic throttling and delays
- **Invalid data** - Validation and fallback responses

## 🔧 Development

### Adding New Sources
1. Update `core/config.py` with new source configuration
2. Add scraping logic in `core/scraper.py`
3. Test with sample data

### Customizing AI Agents
1. Modify prompts in `agents/` directory
2. Update agent logic in `core/agents.py`
3. Test with different content types

### Adding Output Formats
1. Create new handler in `core/output.py`
2. Implement `OutputHandler` interface
3. Register in `OutputPipeline`

## 📝 Sample Output

### Daily Briefing Summary
```
🎀 K-Beauty Daily Trend Briefing
==================================================
✅ Daily briefing completed successfully!
📊 Briefing ID: briefing_20240115_103000
📈 Trends identified: 8
🎯 Priority trends: 3
💡 Market opportunities: 4
⚠️ Risk factors: 3
📝 Posts analyzed: 45

🏆 Top Priority Trends:
  #1 Glass Skin Technique (high impact)
  #2 Cushion Foundation Innovation (high impact)
  #3 Propolis and Honey Extracts (medium impact)

📁 Output files created:
  • output/kbeauty_briefing_20240115.md
  • output/kbeauty_briefing_20240115_103000.json

⏰ Completed at: 2024-01-15 10:30:00
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details.

## 🆘 Support

For issues and questions:
1. Check the logs in the console output
2. Verify your API keys are correct
3. Ensure all dependencies are installed
4. Check the `/health` endpoint for system status

---

**Built for solo operators who need intelligent, automated K-beauty trend intelligence delivered daily.** 