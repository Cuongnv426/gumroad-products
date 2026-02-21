# Content Bot - Setup Guide

Complete guide to setup and deploy the AI Tools & Productivity Content Bot.

## Quick Start (5 minutes)

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Set your OpenAI API key
export OPENAI_API_KEY="sk-..."

# 3. Generate some content
python content-bot-main.py generate 10

# 4. View generated content
ls -la data/queue-*.json
```

## Full Setup (30 minutes)

### Step 1: Clone/Download Bot Files

```bash
cd /root/clawd/content-bot
ls -la
```

Expected files:
- `content-bot-main.py` - Main bot
- `config.py` - Configuration
- `content-generator.py` - Content generation
- `platform-integrations.py` - API integrations
- `scheduler.py` - Scheduling
- `email-system.py` - Email/Mailchimp
- `analytics.py` - Analytics & revenue tracking

### Step 2: Install Python Dependencies

```bash
# Create virtual environment (optional but recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install requirements
pip install -r requirements.txt
```

### Step 3: Create Required Directories

```bash
mkdir -p data logs
chmod 755 data logs
```

### Step 4: Configure API Keys

You'll need accounts and API keys for:

1. **OpenAI API** (Required for content generation)
   - Sign up: https://platform.openai.com
   - Create API key in account settings
   - Set as environment variable:
   ```bash
   export OPENAI_API_KEY="sk-..."
   ```

2. **Twitter API** (For posting tweets)
   - Apply at: https://developer.twitter.com
   - Create app and get API keys
   - Set in environment:
   ```bash
   export TWITTER_API_KEY="..."
   export TWITTER_API_SECRET="..."
   export TWITTER_ACCESS_TOKEN="..."
   export TWITTER_ACCESS_TOKEN_SECRET="..."
   ```

3. **TikTok API** (For posting videos)
   - Apply at: https://developers.tiktok.com
   - Get access token
   ```bash
   export TIKTOK_ACCESS_TOKEN="..."
   ```

4. **Instagram API** (For Reels)
   - Use Meta Business Suite
   ```bash
   export INSTAGRAM_ACCESS_TOKEN="..."
   export INSTAGRAM_BUSINESS_ACCOUNT_ID="..."
   ```

5. **LinkedIn API** (For professional posts)
   - Register at: https://www.linkedin.com/developers
   ```bash
   export LINKEDIN_ACCESS_TOKEN="..."
   export LINKEDIN_PERSON_URN="..."
   ```

6. **Reddit API** (For community posts)
   - Create app at: https://www.reddit.com/prefs/apps
   ```bash
   export REDDIT_CLIENT_ID="..."
   export REDDIT_CLIENT_SECRET="..."
   export REDDIT_USERNAME="..."
   export REDDIT_PASSWORD="..."
   ```

7. **Medium API** (For blog posts)
   - Get token at: https://medium.com/me/settings
   ```bash
   export MEDIUM_API_TOKEN="..."
   ```

8. **Mailchimp API** (For email newsletters)
   - Sign up at: https://mailchimp.com
   - Get API key from account settings
   ```bash
   export MAILCHIMP_API_KEY="..."
   export MAILCHIMP_LIST_ID="..."
   export MAILCHIMP_SERVER="us1"  # Replace with your server
   ```

### Step 5: Update Configuration

Edit `config.py` to customize:

```python
# Change niche if needed
NICHE = "AI Tools & Productivity"

# Adjust keywords
CONTENT_KEYWORDS = [...]

# Modify affiliate links
AFFILIATE_LINKS = {...}

# Change posting schedule
POSTING_SCHEDULE = {...}

# Set timezone
TIMEZONE = "UTC"
```

### Step 6: Test the Bot

```bash
# Test content generation
python content-generator.py

# Test platform connections
python platform-integrations.py

# Test scheduler
python scheduler.py

# Check full status
python content-bot-main.py status
```

### Step 7: Start the Bot

```bash
# Interactive mode
python content-bot-main.py

# Or automatic mode
python content-bot-main.py start

# Or generate content batch
python content-bot-main.py generate 20
```

## Production Deployment

### Using systemd (Linux)

Create `/etc/systemd/system/content-bot.service`:

```ini
[Unit]
Description=Content Bot Service
After=network.target

[Service]
Type=simple
User=content-bot
WorkingDirectory=/root/clawd/content-bot
Environment="OPENAI_API_KEY=sk-..."
Environment="TWITTER_API_KEY=..."
# Add other API keys here
ExecStart=/usr/bin/python3 /root/clawd/content-bot/content-bot-main.py start
Restart=always
RestartSec=60

[Install]
WantedBy=multi-user.target
```

Start service:
```bash
sudo systemctl daemon-reload
sudo systemctl enable content-bot
sudo systemctl start content-bot
sudo systemctl status content-bot
```

View logs:
```bash
sudo journalctl -u content-bot -f
```

### Using Docker

Create `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

# Create data directories
RUN mkdir -p data logs

ENV PYTHONUNBUFFERED=1

CMD ["python", "content-bot-main.py", "start"]
```

Build and run:
```bash
docker build -t content-bot .
docker run -d --name content-bot \
  -e OPENAI_API_KEY="sk-..." \
  -e TWITTER_API_KEY="..." \
  -v /path/to/data:/app/data \
  content-bot
```

### Using Screen (Simple Background)

```bash
# Start bot in background
screen -S content-bot -d -m python content-bot-main.py start

# View logs
tail -f logs/bot.log

# Attach to screen
screen -r content-bot

# Detach (Ctrl+A then D)
```

### Using Nohup (Very Simple)

```bash
nohup python content-bot-main.py start > logs/bot.log 2>&1 &
```

## Configuration File (.env)

For better security, create `.env`:

```
OPENAI_API_KEY=sk-...
TWITTER_API_KEY=...
TWITTER_API_SECRET=...
TWITTER_ACCESS_TOKEN=...
TWITTER_ACCESS_TOKEN_SECRET=...
TIKTOK_ACCESS_TOKEN=...
INSTAGRAM_ACCESS_TOKEN=...
INSTAGRAM_BUSINESS_ACCOUNT_ID=...
LINKEDIN_ACCESS_TOKEN=...
LINKEDIN_PERSON_URN=...
REDDIT_CLIENT_ID=...
REDDIT_CLIENT_SECRET=...
REDDIT_USERNAME=...
REDDIT_PASSWORD=...
MEDIUM_API_TOKEN=...
MAILCHIMP_API_KEY=...
MAILCHIMP_LIST_ID=...
MAILCHIMP_SERVER=us1
TIMEZONE=UTC
```

Load in bot:
```python
from dotenv import load_dotenv
load_dotenv()
```

## Verification Checklist

- [ ] Python 3.8+ installed
- [ ] All dependencies installed (`pip list`)
- [ ] All API keys configured
- [ ] Directories created (data/, logs/)
- [ ] Bot starts without errors
- [ ] Content generation works
- [ ] At least one platform connection successful
- [ ] Logs being written to logs/bot.log
- [ ] Analytics database created (data/analytics.db)

## Next Steps

1. **Generate initial content**: `python content-bot-main.py generate 50`
2. **View analytics**: Check `data/dashboard.html`
3. **Configure email list**: Set up Mailchimp list
4. **Add affiliate links**: Update affiliate-links.json
5. **Schedule 24/7 posting**: Use systemd or Docker
6. **Monitor performance**: Check logs and analytics daily

## Troubleshooting

### OpenAI API key not working
```bash
# Test API connection
curl https://api.openai.com/v1/models \
  -H "Authorization: Bearer $OPENAI_API_KEY"
```

### No content generated
- Check logs: `tail -f logs/bot.log`
- Verify API key is set
- Test content generator: `python content-generator.py`

### Scheduler not posting
- Check scheduler status: `python content-bot-main.py status`
- Verify platform credentials
- Check logs for API errors

### Database errors
- Delete `data/analytics.db` to recreate
- Check directory permissions
- Ensure 100GB free disk space

## Performance Tips

1. **Generate content in batch** during off-peak hours
2. **Use A/B testing** to optimize posting times
3. **Monitor affiliate performance** weekly
4. **Update keywords** monthly based on trends
5. **Rotate affiliate links** to prevent fatigue
6. **Test new platforms** before full deployment

## Support & Updates

- Check logs: `/root/clawd/content-bot/logs/bot.log`
- View dashboard: `/root/clawd/content-bot/data/dashboard.html`
- Generate report: `python content-bot-main.py status`

---

**Status: Production Ready ✓**

For advanced setup and customization, see `OPTIMIZATION-GUIDE.md`
