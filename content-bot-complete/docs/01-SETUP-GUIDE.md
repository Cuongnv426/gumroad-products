# Content Bot - Complete Setup Guide

## Overview
Content Bot is a production-ready system that:
- ✅ Generates AI content using ChatGPT
- ✅ Posts to 7+ platforms automatically
- ✅ Manages email lists (Mailchimp/SendGrid)
- ✅ Tracks affiliate links and earnings
- ✅ Provides analytics dashboard
- ✅ Runs 24/7 without manual intervention

## Prerequisites
- Python 3.8+
- API keys for services you want to use
- 500MB free disk space
- For VPS: Ubuntu 20.04+ or CentOS 7+

## Step 1: Get API Keys

### OpenAI (ChatGPT)
1. Go to https://platform.openai.com/api-keys
2. Create new secret key
3. Copy and save (you won't see it again)
4. Add to `.env` as `OPENAI_API_KEY`

**Cost:** ~$0.002 per 1000 tokens (ChatGPT-3.5)

### Twitter/X
1. Go to https://developer.twitter.com
2. Create application
3. Generate API keys and access tokens
4. Add to `.env`:
   - `TWITTER_API_KEY`
   - `TWITTER_API_SECRET`
   - `TWITTER_ACCESS_TOKEN`
   - `TWITTER_ACCESS_TOKEN_SECRET`
   - `TWITTER_BEARER_TOKEN`

### LinkedIn
1. Go to https://www.linkedin.com/developers
2. Create app
3. Get access token
4. Add to `.env` as `LINKEDIN_ACCESS_TOKEN`

### Reddit
1. Go to https://www.reddit.com/prefs/apps
2. Create script application
3. Get credentials
4. Add to `.env`:
   - `REDDIT_CLIENT_ID`
   - `REDDIT_CLIENT_SECRET`
   - `REDDIT_USERNAME`
   - `REDDIT_PASSWORD`

### Mailchimp (Email)
1. Go to https://mailchimp.com
2. Create account and list
3. Get API key from Account > Extras > API Keys
4. Get List ID from Audience
5. Add to `.env`:
   - `MAILCHIMP_API_KEY`
   - `MAILCHIMP_LIST_ID`

### Medium
1. Go to https://medium.com/me/settings/security
2. Create integration token
3. Add to `.env` as `MEDIUM_TOKEN`

## Step 2: Install Bot

### Local Installation
```bash
# Clone/extract bot
cd content-bot-complete

# Run setup
bash setup.sh

# Edit configuration
nano .env  # Add your API keys

# Run tests
source venv/bin/activate
python src/bot_main.py test

# Start bot (manual)
python src/bot_main.py start

# Or test with 1 cycle
python src/bot_main.py generate 5
```

### VPS Installation (Ubuntu)
```bash
# Connect to VPS
ssh user@your-vps-ip

# Create bot user
sudo useradd -m -s /bin/bash contentbot

# Install Python and dependencies
sudo apt update
sudo apt install -y python3 python3-venv python3-pip git

# Clone bot
cd /opt
sudo git clone https://github.com/yourname/content-bot.git
cd content-bot
sudo chown -R contentbot:contentbot .

# Setup
sudo -u contentbot bash setup.sh

# Configure
sudo -u contentbot nano .env  # Add your API keys

# Install systemd service
sudo cp deploy/content-bot.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable content-bot
sudo systemctl start content-bot

# Check status
sudo systemctl status content-bot
sudo journalctl -u content-bot -f
```

## Step 3: Configuration

### Content Niches
Edit `src/config.py` to customize:
- Content topics/keywords
- Posting schedule
- Affiliate links
- Daily post limits

### Posting Schedule
Default: 
- Twitter: 5x daily (8am, 12pm, 3pm, 6pm, 9pm)
- LinkedIn: 3x daily (8:30am, 12:30pm, 5:30pm)
- Reddit: 3x daily (11am, 4pm, 10pm)
- Plus Instagram, TikTok, Medium, Email

### Monetization
Configure affiliate links in `config.py`:
- Add your referral codes
- Set commission rates
- Bot auto-includes in content

## Step 4: Run & Monitor

### Commands
```bash
# Generate content
python src/bot_main.py generate 10

# Post to specific platform
python src/bot_main.py post twitter

# Get status
python src/bot_main.py status

# Get full analytics
python src/bot_main.py report

# Send email campaign
python src/bot_main.py email send "Subject Here"

# Run scheduler (24/7)
python src/bot_main.py start
```

### Monitoring
```bash
# View logs (local)
tail -f content_bot.log

# View logs (VPS)
sudo journalctl -u content-bot -f

# Check bot status
curl http://localhost:8080/status  # If dashboard running
```

## Troubleshooting

### API Errors
1. Check `.env` has correct keys
2. Verify API keys have proper permissions
3. Check rate limits haven't been exceeded
4. Test API keys in browser/Postman first

### Content Not Posting
1. Run `python src/bot_main.py test`
2. Check logs in `content_bot.log`
3. Verify API keys are correct
4. Check platform API status

### Email Not Working
1. Verify Mailchimp API key
2. Check list ID matches
3. Test with `python src/bot_main.py email send "Test"`
4. Check spam folder

### Bot Not Running (VPS)
```bash
# Check service status
sudo systemctl status content-bot

# Restart service
sudo systemctl restart content-bot

# View detailed logs
sudo journalctl -u content-bot -n 50

# Check if process is running
ps aux | grep bot_main
```

## Next Steps

1. ✅ Follow setup guide above
2. ✅ Configure API keys
3. ✅ Run tests: `python src/bot_main.py test`
4. ✅ Start bot: `python src/bot_main.py start`
5. ✅ Monitor earnings: `python src/bot_main.py report`

See other docs for:
- API_KEYS.md - Detailed key setup
- USAGE.md - All commands
- MONETIZATION.md - Revenue strategies
- DEPLOYMENT.md - VPS setup
- TROUBLESHOOTING.md - Common issues
