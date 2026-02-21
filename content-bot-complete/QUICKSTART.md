# Content Bot - Quick Start (5 Minutes)

Get Content Bot running in just 5 minutes!

## Prerequisites
- Python 3.8+
- OpenAI API key (get free $5 at https://platform.openai.com)
- (Optional) Twitter/LinkedIn/Reddit API keys

## Step 1: Download & Setup (1 min)

```bash
# Clone the repo
git clone https://github.com/yourname/content-bot-complete.git
cd content-bot-complete

# Run setup
bash setup.sh

# Takes ~2 minutes to download dependencies
```

## Step 2: Configure API Keys (1 min)

```bash
# Copy example config
cp .env.example .env

# Edit with your keys
nano .env
```

Minimal config (just need OpenAI):
```
OPENAI_API_KEY=sk-your-key-here
```

Optional: Add Twitter/LinkedIn/Reddit keys for more platforms

## Step 3: Test Installation (1 min)

```bash
# Activate virtual environment
source venv/bin/activate

# Run test
python src/bot_main.py test
```

You should see:
- ✓ Configuration loaded
- ✓ Content generated
- ✓ Analytics working

## Step 4: Generate Content (1 min)

```bash
# Generate 5 pieces of content
python src/bot_main.py generate 5

# You'll see 5 pieces output with topics, hashtags, etc.
```

## Step 5: Start Bot (1 min)

```bash
# Run 24/7 (generates & posts automatically)
python src/bot_main.py start

# Or test with 1 cycle
python src/bot_main.py test
```

## Common Commands

```bash
# Generate content
python src/bot_main.py generate 5

# Post to Twitter
python src/bot_main.py post twitter

# Check status
python src/bot_main.py status

# View analytics
python src/bot_main.py report

# Send email
python src/bot_main.py email send "Your Subject"

# Help
python src/bot_main.py help
```

## Next Steps

1. **Add more API keys** → Post to LinkedIn, Reddit, Medium
   - See [API Keys Guide](docs/02-API-KEYS-GUIDE.md)

2. **Configure email** → Grow subscriber list
   - Get Mailchimp API key (free)
   - Add to .env: MAILCHIMP_API_KEY & MAILCHIMP_LIST_ID

3. **Setup Mailchimp** → Email list for monetization
   - Sign up at https://mailchimp.com
   - Create email list
   - Copy API key & List ID

4. **Deploy to VPS** → Run 24/7 in cloud
   - Get VPS from Linode ($5/month)
   - Follow [Deployment Guide](docs/05-DEPLOYMENT-GUIDE.md)

5. **Start earning** → Track affiliate conversions
   - Configure affiliate links in config.py
   - Watch earnings grow!

## Troubleshooting

**"ModuleNotFoundError: No module named 'openai'"**
```bash
source venv/bin/activate
pip install -r requirements.txt
```

**"Invalid API key"**
```bash
# Make sure key is in .env exactly as provided
cat .env | grep OPENAI
# Should show your actual key, not blank
```

**"Connection error"**
- Check internet connection
- API service may be down (rare)
- Wait a minute and try again

## Full Documentation

- [Setup Guide](docs/01-SETUP-GUIDE.md) - Complete installation
- [API Keys](docs/02-API-KEYS-GUIDE.md) - Get all required keys
- [Usage](docs/03-USAGE-GUIDE.md) - All commands
- [Monetization](docs/04-MONETIZATION-GUIDE.md) - Earn money
- [Deployment](docs/05-DEPLOYMENT-GUIDE.md) - Run on VPS
- [Troubleshooting](docs/06-TROUBLESHOOTING.md) - Fix issues

## Support

- **Stuck?** Check the [Troubleshooting Guide](docs/06-TROUBLESHOOTING.md)
- **Questions?** See the full [README.md](README.md)
- **Setup help?** Follow [Setup Guide](docs/01-SETUP-GUIDE.md) step-by-step

---

**You're done! Now bot is:**
- ✅ Generating content with AI
- ✅ Posting automatically
- ✅ Ready to earn money
- ✅ Can scale to VPS for 24/7 operation

Start making passive income! 🚀
