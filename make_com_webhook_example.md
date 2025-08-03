# Make.com Webhook Setup for K-Beauty Daily Briefing

## 🕕 6AM Korea Time Automation

This guide shows how to set up Make.com to trigger your K-beauty briefing every morning at 6AM Korea time (KST).

## 📋 Prerequisites

1. **Make.com account** (formerly Integromat)
2. **Your K-beauty API running** (accessible via webhook)
3. **Korea timezone** - 6AM KST = 9PM EST (previous day) or 5AM UTC

## 🔧 Make.com Scenario Setup

### Step 1: Create New Scenario

1. Log into Make.com
2. Click "Create a new scenario"
3. Name it: "K-Beauty Daily Briefing - 6AM KST"

### Step 2: Add Schedule Trigger

1. **Search for "Schedule"** in the modules
2. **Add "Schedule" module** as your first trigger
3. **Configure Schedule:**
   ```
   Schedule Type: Recurring
   Time: 06:00
   Timezone: Asia/Seoul (KST)
   Days: Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday
   ```

### Step 3: Add HTTP Request

1. **Search for "HTTP"** in the modules
2. **Add "HTTP" module** after the Schedule
3. **Configure HTTP Request:**
   ```
   Method: POST
   URL: https://your-api-domain.com/webhook
   Headers:
     Content-Type: application/json
   Body (JSON):
   {
     "source": "make.com",
     "event_type": "daily_trigger",
     "data": {
       "schedule": "daily",
       "time": "06:00",
       "timezone": "Asia/Seoul",
       "triggered_at": "{{now}}"
     }
   }
   ```

### Step 4: Add Error Handling (Optional)

1. **Add "Router" module** after HTTP
2. **Add "HTTP" module** for error notification
3. **Configure error notification:**
   ```
   Method: POST
   URL: [Your Slack webhook or email service]
   Body: {
     "text": "❌ K-Beauty briefing failed at {{now}}"
   }
   ```

## 🔄 Complete Make.com Flow

```
Schedule (6AM KST) 
    ↓
HTTP Request → K-Beauty API /webhook
    ↓
Router (Check Response)
    ↓
Success: Log to Google Sheets
    ↓
Error: Send Slack/Email Alert
```

## 📊 Monitoring Setup

### Step 5: Add Success Logging

1. **Add "Google Sheets" module** after successful HTTP
2. **Configure logging:**
   ```
   Action: Add a row
   Spreadsheet: K-Beauty Briefing Log
   Sheet: Daily Log
   Data:
     Date: {{now}}
     Status: Success
     Briefing ID: {{http_response.briefing_id}}
     Trends Found: {{http_response.data.trend_analysis.trends.length}}
   ```

### Step 6: Add Status Check

1. **Add another "HTTP" module** to check status
2. **Configure status check:**
   ```
   Method: GET
   URL: https://your-api-domain.com/status
   ```

## 🚀 Deployment Steps

### 1. Deploy Your API

```bash
# Deploy to your server
git clone <your-repo>
cd kbeauty-trend-agent
pip install -r requirements.txt

# Start the API
uvicorn api.main:app --host 0.0.0.0 --port 8000
```

### 2. Test the Webhook

```bash
# Test locally
curl -X POST http://localhost:8000/webhook \
  -H "Content-Type: application/json" \
  -d '{
    "source": "make.com",
    "event_type": "daily_trigger",
    "data": {
      "schedule": "daily",
      "time": "06:00"
    }
  }'
```

### 3. Configure Make.com

1. **Replace URL** in HTTP module with your actual API URL
2. **Test the scenario** using Make.com's test mode
3. **Activate the scenario** when ready

## 📈 Advanced Monitoring

### Step 7: Add Health Checks

1. **Add "HTTP" module** for health check
2. **Configure health check:**
   ```
   Method: GET
   URL: https://your-api-domain.com/health
   ```

### Step 8: Add Slack Notifications

1. **Add "Slack" module** for notifications
2. **Configure Slack message:**
   ```
   Channel: #k-beauty-briefings
   Text: |
     🎀 K-Beauty Daily Briefing Completed
     📊 Briefing ID: {{http_response.briefing_id}}
     📈 Trends: {{http_response.data.trend_analysis.trends.length}}
     🎯 Priority: {{http_response.data.synthesis_results.priority_trends.length}}
     ⏰ Time: {{now}}
   ```

## 🔧 Troubleshooting

### Common Issues

1. **Timezone Problems**
   - Make sure Make.com is set to Asia/Seoul timezone
   - 6AM KST = 9PM EST (previous day)

2. **API Not Responding**
   - Check if your API is running: `curl http://your-api/health`
   - Verify firewall settings
   - Check logs: `tail -f briefing.log`

3. **Webhook Not Triggering**
   - Test webhook manually first
   - Check Make.com scenario logs
   - Verify API endpoint is correct

### Debug Commands

```bash
# Test webhook locally
curl -X POST http://localhost:8000/webhook \
  -H "Content-Type: application/json" \
  -d '{"source": "test", "event_type": "debug"}'

# Check API status
curl http://localhost:8000/status

# Check logs
tail -f briefing.log
tail -f briefing_success.log
tail -f briefing_error.log
```

## 📅 Alternative Scheduling Options

### Option 1: Multiple Times Daily
```
Schedule 1: 6:00 AM KST (Daily briefing)
Schedule 2: 6:00 PM KST (Evening update)
```

### Option 2: Weekdays Only
```
Days: Monday, Tuesday, Wednesday, Thursday, Friday
Time: 6:00 AM KST
```

### Option 3: Custom Time
```
Time: 5:30 AM KST (Earlier for US timezone)
Timezone: Asia/Seoul
```

## 🎯 Expected Results

### Successful Run
```
🎀 K-Beauty Daily Trend Briefing
==================================================
✅ Daily briefing completed successfully!
📊 Briefing ID: briefing_20240115_060000
📈 Trends identified: 8
🎯 Priority trends: 3
💡 Market opportunities: 4
⚠️ Risk factors: 3
📝 Posts analyzed: 45
```

### Make.com Log Entry
```
Date: 2024-01-15 06:00:00
Status: Success
Briefing ID: briefing_20240115_060000
Trends Found: 8
Priority Trends: 3
```

## 🔐 Security Considerations

1. **API Authentication**
   - Add API key to webhook requests
   - Use HTTPS for all communications

2. **Rate Limiting**
   - Implement rate limiting on your API
   - Monitor for abuse

3. **Error Handling**
   - Set up alerts for failed runs
   - Implement retry logic

## 📞 Support

If you encounter issues:
1. Check Make.com scenario logs
2. Verify API is running and accessible
3. Test webhook manually
4. Check briefing logs for errors

---

**This setup will automatically trigger your K-beauty briefing every morning at 6AM Korea time, perfect for US buyers who want fresh insights when they start their day! 🌅** 