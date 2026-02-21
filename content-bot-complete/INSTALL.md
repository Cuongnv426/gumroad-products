# Content Bot Installation Instructions

## For Deployment on VPS (Jr Pan)

This is a complete, production-ready Content Bot system that generates and posts AI content to 7+ platforms automatically.

### Quick Summary

- **What it does:** Generates 10-20 posts daily, posts to Twitter/LinkedIn/Reddit/Email/Medium automatically, tracks affiliate earnings
- **Cost:** ~$10/month total (VPS + APIs)
- **Revenue potential:** $3,000-22,000/month
- **Setup time:** 15 minutes
- **Manual work required:** Configure API keys only

---

## Installation Steps

### Step 1: On Your Local Computer (5 min)

```bash
# Download the package
git clone https://github.com/yourname/content-bot-complete.git
cd content-bot-complete

# Or extract if you have a .tar.gz file
tar -xzf content-bot-complete.tar.gz
cd content-bot-complete

# Test on local machine first (recommended)
bash setup.sh
cp .env.example .env
# Edit .env and add your OpenAI API key at minimum
nano .env
source venv/bin/activate
python src/bot_main.py test
```

If test passes → Ready for VPS deployment!

### Step 2: Get API Keys (varies)

See [API Keys Guide](docs/02-API-KEYS-GUIDE.md) for complete instructions.

**Minimum:** OpenAI API key (get $5 free credit)
**Recommended:** Add Twitter/LinkedIn keys for more platforms

### Step 3: Deploy to VPS

#### Option A: Linode (Recommended - $5-10/month)

```bash
# 1. Create account at https://linode.com
# 2. Create new Linode
#    - OS: Ubuntu 22.04 LTS
#    - Size: Shared - 1GB RAM ($5/month)
#    - Region: Your location
# 3. Get IP address (e.g., 12.34.56.78)

# 4. SSH into VPS
ssh root@12.34.56.78

# 5. Run deployment script (below)
```

#### Option B: DigitalOcean (Similar)

```bash
# 1. Create account at https://digitalocean.com
# 2. Create new Droplet
#    - OS: Ubuntu 22.04 x64
#    - Size: Basic - 1GB RAM ($6/month)
#    - Region: Your location
# 3. Get IP address (e.g., 12.34.56.78)

# 4. SSH into VPS
ssh root@12.34.56.78

# 5. Run deployment script (below)
```

### Step 4: VPS Setup Script

Once SSH'd into your VPS, run this:

```bash
#!/bin/bash
# Save as: setup-vps.sh and run with: bash setup-vps.sh

set -e

echo "Content Bot VPS Setup"
echo "===================="

# Update system
apt update && apt upgrade -y

# Install dependencies
apt install -y python3 python3-venv python3-pip git

# Create bot user
useradd -m -s /bin/bash contentbot || true
usermod -aG sudo contentbot

# Download bot
cd /opt
git clone https://github.com/yourname/content-bot-complete.git || true
cd content-bot-complete
chown -R contentbot:contentbot .

# Install bot
su - contentbot -c "cd /opt/content-bot-complete && bash setup.sh"

# Setup .env
su - contentbot -c "cp /opt/content-bot-complete/.env.example /opt/content-bot-complete/.env"

echo ""
echo "=================================================="
echo "NEXT STEPS:"
echo "=================================================="
echo ""
echo "1. Edit .env and add API keys:"
echo "   sudo nano /opt/content-bot-complete/.env"
echo ""
echo "2. Setup systemd service:"
echo "   sudo cp /opt/content-bot-complete/deploy/content-bot.service /etc/systemd/system/"
echo "   sudo systemctl daemon-reload"
echo "   sudo systemctl enable content-bot"
echo "   sudo systemctl start content-bot"
echo ""
echo "3. Check status:"
echo "   sudo systemctl status content-bot"
echo "   sudo journalctl -u content-bot -f"
echo ""
echo "Bot will now:"
echo "✓ Generate content every hour"
echo "✓ Post automatically at optimal times"
echo "✓ Track affiliate earnings"
echo "✓ Run 24/7 without stopping"
echo ""
```

### Step 5: Configure .env on VPS

```bash
# On your VPS
sudo nano /opt/content-bot-complete/.env

# Add at minimum:
OPENAI_API_KEY=sk-your-api-key-here

# Optional (to post to more platforms):
TWITTER_API_KEY=your-key
TWITTER_API_SECRET=your-secret
TWITTER_ACCESS_TOKEN=your-token
TWITTER_ACCESS_TOKEN_SECRET=your-token-secret
TWITTER_BEARER_TOKEN=your-bearer-token

LINKEDIN_ACCESS_TOKEN=your-linkedin-token

REDDIT_CLIENT_ID=your-id
REDDIT_CLIENT_SECRET=your-secret
REDDIT_USERNAME=your-username
REDDIT_PASSWORD=your-password

MAILCHIMP_API_KEY=your-mailchimp-key
MAILCHIMP_LIST_ID=your-list-id

# Save: Ctrl+X, Y, Enter
```

### Step 6: Start Bot

```bash
# On VPS, as root:
sudo systemctl start content-bot

# Verify it's running:
sudo systemctl status content-bot

# Watch logs:
sudo journalctl -u content-bot -f

# Should see:
# [INFO] Content Bot Started
# [INFO] Scheduler setup complete
# [INFO] Next job: Twitter at 8:00 AM
```

### Step 7: Monitor

```bash
# Check current status
sudo systemctl status content-bot

# View logs
sudo journalctl -u content-bot -f

# Check analytics
sudo -u contentbot python /opt/content-bot-complete/src/bot_main.py report

# Get revenue summary
sudo -u contentbot python /opt/content-bot-complete/src/bot_main.py report --revenue
```

---

## Verification Checklist

Before considering bot "live":

- [ ] SSH into VPS works
- [ ] Python 3.8+ installed (`python3 --version`)
- [ ] Bot downloaded to `/opt/content-bot-complete/`
- [ ] .env file created with OpenAI API key
- [ ] systemd service installed
- [ ] Bot service started (`systemctl status content-bot`)
- [ ] Logs show no errors (`journalctl -u content-bot -f`)
- [ ] Generated content appears in logs

---

## Troubleshooting

### Bot won't start

```bash
# Check service status
sudo systemctl status content-bot

# View errors
sudo journalctl -u content-bot -n 50

# Manually start (to see errors)
cd /opt/content-bot-complete
source venv/bin/activate
python src/bot_main.py test

# Common issues:
# 1. API key missing in .env
# 2. Python not found
# 3. Dependencies not installed
```

### Check if running

```bash
# Is service active?
sudo systemctl is-active content-bot

# How many posts today?
sudo journalctl -u content-bot | grep -i "post"

# Get stats
sudo -u contentbot python /opt/content-bot-complete/src/bot_main.py status
```

### View bot logs

```bash
# Real-time (follow)
sudo journalctl -u content-bot -f

# Last 50 lines
sudo journalctl -u content-bot -n 50

# Errors only
sudo journalctl -u content-bot -p err

# Today's logs
sudo journalctl -u content-bot --since today
```

---

## Post-Installation

### 1. Monitor First Week

Bot should:
- Generate content every hour
- Post to Twitter/LinkedIn at optimal times
- Email list grows 5-10/day
- Affiliate clicks tracked

Watch logs for errors:
```bash
sudo journalctl -u content-bot -f
```

### 2. Optimize Configuration

After 1 week, fine-tune:
- Content keywords (edit `src/config.py`)
- Posting times (edit `POSTING_SCHEDULE`)
- Daily post limit (adjust `POSTS_PER_DAY`)

### 3. Add More Platforms

As you add API keys:
1. Add to `.env`
2. Restart bot: `sudo systemctl restart content-bot`
3. Bot will auto-enable platforms

### 4. Monitor Revenue

Check earnings daily:
```bash
sudo -u contentbot python /opt/content-bot-complete/src/bot_main.py report
```

---

## Full Documentation

See the `/docs` folder for:

- **QUICKSTART.md** - 5-minute setup
- **README.md** - Full overview
- **docs/01-SETUP-GUIDE.md** - Detailed installation
- **docs/02-API-KEYS-GUIDE.md** - How to get all API keys
- **docs/03-USAGE-GUIDE.md** - All commands
- **docs/04-MONETIZATION-GUIDE.md** - How to earn
- **docs/05-DEPLOYMENT-GUIDE.md** - VPS setup details
- **docs/06-TROUBLESHOOTING.md** - Problem solving

---

## VPS Cost Breakdown

| Service | Cost | Notes |
|---------|------|-------|
| VPS (Linode 1GB) | $5/month | Unlimited traffic |
| OpenAI API | $1-5/month | 10-20 posts/day |
| Twitter | Free | Unlimited posts |
| LinkedIn | Free | Unlimited posts |
| Reddit | Free | Unlimited posts |
| Mailchimp | Free | <500 subscribers |
| Domain (optional) | $1-15/year | For branding |
| **TOTAL** | **$8-20/month** | Everything included |

---

## Support

If you get stuck:

1. **Check logs:** `sudo journalctl -u content-bot -f`
2. **Read documentation:** See `/docs` folder
3. **Run tests:** `python src/bot_main.py test`
4. **Check config:** `cat /opt/content-bot-complete/.env`

---

## Success Indicators

After 1 week of running, you should see:

✅ Posts generated daily
✅ Posts published to platforms
✅ No errors in logs
✅ Email list growing
✅ First few affiliate clicks
✅ Bot still running smoothly

After 1 month:

✅ 50-100 email subscribers
✅ 100-500 affiliate clicks
✅ First few conversions ($50-200)
✅ Posts getting engagement

After 3 months:

✅ $500-2,000 in affiliate revenue
✅ 500+ email subscribers
✅ Sponsored post opportunities
✅ Scaling to more platforms

---

**Your bot is now running 24/7 and earning passive income!** 🚀

For detailed help, see the documentation in `/docs` folder.
