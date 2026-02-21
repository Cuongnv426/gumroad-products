# Content Bot - VPS Deployment Guide

## Platform Options

### Recommended Hosting
- **Linode** ($5-10/month) - Simple, fast
- **DigitalOcean** ($6-12/month) - Great for Python
- **Vultr** ($6-12/month) - Good uptime
- **AWS Lightsail** ($5-12/month) - Enterprise grade
- **Hetzner** ($5-10/month) - Budget friendly

## Step-by-Step Deployment

### Step 1: Create VPS

**On Linode/DigitalOcean:**
1. Create new instance
2. Choose Ubuntu 22.04 LTS
3. Select $6-12/month plan
4. Add SSH key (or password)
5. Deploy

**You'll get:**
- IP address: `12.34.56.78`
- SSH access: `ssh root@12.34.56.78`

### Step 2: Prepare Server

```bash
# SSH into server
ssh root@12.34.56.78

# Update system
apt update && apt upgrade -y

# Install dependencies
apt install -y python3 python3-venv python3-pip git curl wget

# Create bot user (for security)
useradd -m -s /bin/bash contentbot
usermod -aG sudo contentbot

# Switch to bot user
su - contentbot
```

### Step 3: Install Content Bot

```bash
# As contentbot user
cd ~

# Clone repository
git clone https://github.com/yourname/content-bot-complete.git
cd content-bot-complete

# Run setup
bash setup.sh

# Activate venv
source venv/bin/activate

# Edit configuration
nano .env  # Add your API keys
```

### Step 4: Setup Systemd Service

```bash
# Copy service file
sudo cp deploy/content-bot.service /etc/systemd/system/

# Edit service (optional)
sudo nano /etc/systemd/system/content-bot.service

# Enable and start
sudo systemctl daemon-reload
sudo systemctl enable content-bot
sudo systemctl start content-bot

# Check status
sudo systemctl status content-bot

# View logs
sudo journalctl -u content-bot -f
```

### Step 5: Verify It's Running

```bash
# Check if process is running
ps aux | grep bot_main

# Check logs
sudo journalctl -u content-bot -n 20

# Generate test content
source venv/bin/activate
python src/bot_main.py test
```

## Systemd Service File

The service runs bot in background and auto-restarts on failure.

**File:** `deploy/content-bot.service`

**Key settings:**
- `Type=simple` - Runs continuously
- `Restart=always` - Auto-restart on crash
- `RestartSec=30` - Wait 30s before restart

**Manual commands:**
```bash
# Start
sudo systemctl start content-bot

# Stop
sudo systemctl stop content-bot

# Restart
sudo systemctl restart content-bot

# Reload config (without restart)
sudo systemctl reload content-bot

# Check status
sudo systemctl status content-bot

# View logs
sudo journalctl -u content-bot -f
sudo journalctl -u content-bot -n 50
sudo journalctl -u content-bot --since "1 hour ago"
```

## Monitoring & Maintenance

### View Logs
```bash
# Real-time logs
sudo journalctl -u content-bot -f

# Last 50 lines
sudo journalctl -u content-bot -n 50

# Errors only
sudo journalctl -u content-bot -p err

# Today's logs
sudo journalctl -u content-bot --since today

# Specific time range
sudo journalctl -u content-bot --since "2024-01-15 10:00:00"
```

### Check Resource Usage
```bash
# CPU and memory
ps aux | grep bot_main

# Disk space
df -h

# Check disk usage
du -sh content-bot-complete/

# Monitor in real-time
top
```

### Backup Configuration

```bash
# Backup .env file
cp /opt/content-bot/.env /home/contentbot/.env.backup

# Backup daily
crontab -e
# Add: 0 2 * * * cp /opt/content-bot/.env /backups/.env.$(date +\%Y\%m\%d)
```

## Troubleshooting

### Bot won't start

```bash
# Check service status
sudo systemctl status content-bot

# Check logs
sudo journalctl -u content-bot -n 50

# Try running manually
sudo -u contentbot /opt/content-bot/venv/bin/python /opt/content-bot/src/bot_main.py start

# Common issues:
# 1. API key missing - edit .env
# 2. Permission error - check ownership
# 3. Port already in use - change port or stop other service
```

### API key errors

```bash
# Verify .env is loaded
cat /opt/content-bot/.env | grep OPENAI

# Test specific API
python -c "
from config import OPENAI_API_KEY
print('Key loaded:', 'YES' if OPENAI_API_KEY else 'NO')
"

# Reload service after changing .env
sudo systemctl restart content-bot
```

### Memory issues

```bash
# Check memory
free -h

# If out of memory:
# 1. Reduce POSTS_PER_DAY
# 2. Clear old logs: rm logs/*
# 3. Upgrade VPS plan
```

### Posts not publishing

```bash
# Check if service is running
sudo systemctl status content-bot

# Check recent logs
sudo journalctl -u content-bot -n 100

# Test posting manually
source venv/bin/activate
python src/bot_main.py post twitter

# Common issues:
# 1. API rate limit - wait 15 minutes
# 2. Invalid credentials - check .env
# 3. Account suspended - check platform
```

## Optimization

### Reduce Resource Usage
```bash
# Reduce posting frequency
POSTS_PER_DAY=5  # Instead of 10

# Reduce polling interval
Edit scheduler.py: time.sleep(120)  # Check every 2 min instead of 1
```

### Increase Reliability
```bash
# Setup auto-backup
0 3 * * * /opt/content-bot/backup.sh

# Monitor service
# Add to crontab: */30 * * * * systemctl is-active content-bot || systemctl start content-bot

# Setup alerts
# Use monitoring service like Uptimerobot, Pingdom, etc.
```

## Updating Bot

```bash
# Stop bot
sudo systemctl stop content-bot

# Update code
cd /opt/content-bot
git pull origin main

# Update dependencies
source venv/bin/activate
pip install -r requirements.txt -U

# Start bot
sudo systemctl start content-bot

# Check it started
sudo systemctl status content-bot
```

## Scaling to Multiple Bots

If you want to run multiple instances:

```bash
# Clone to separate directory
cp -r content-bot-complete content-bot-niche2

# Each gets own configuration
cd content-bot-niche2
nano .env  # Different API keys/config

# Create separate systemd service
sudo cp deploy/content-bot.service /etc/systemd/system/content-bot-niche2.service
sudo nano /etc/systemd/system/content-bot-niche2.service
# Edit: ExecStart=/opt/content-bot-niche2/venv/bin/python ...

# Start both
sudo systemctl start content-bot content-bot-niche2
```

## Cost Breakdown

| Item | Cost/Month |
|------|-----------|
| VPS (6GB RAM, 100GB SSD) | $6-12 |
| OpenAI API | $1-5 |
| Twitter API | Free |
| LinkedIn API | Free |
| Mailchimp | Free (<500) |
| Domain (optional) | $1-15 |
| SSL cert (optional) | Free* |
| **TOTAL** | **$8-32** |

*Let's Encrypt free SSL

## Security Best Practices

```bash
# 1. Firewall
sudo ufw enable
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# 2. SSH hardening
sudo nano /etc/ssh/sshd_config
# Set: PasswordAuthentication no
# Set: PermitRootLogin no

# 3. Regular updates
sudo apt update && apt upgrade -y

# 4. Monitor failed logins
sudo tail -f /var/log/auth.log

# 5. Keep .env secure
chmod 600 /opt/content-bot/.env
sudo chown contentbot:contentbot /opt/content-bot/.env
```

## Next Steps

1. ✅ Deploy to VPS
2. ✅ Configure API keys
3. ✅ Run `sudo systemctl start content-bot`
4. ✅ Monitor logs: `sudo journalctl -u content-bot -f`
5. ✅ Check status: `sudo systemctl status content-bot`
6. ✅ Watch earnings grow!

---

**Support:**
- Check logs: `sudo journalctl -u content-bot -f`
- Test manually: `python src/bot_main.py test`
- Documentation: See /docs/ folder
