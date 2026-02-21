# Deployment Guide - Run Bot 24/7

Guide to deploy the Content Bot and keep it running continuously.

## Quick Start (Choose One)

### Option 1: Screen (Simplest - Recommended for Testing)
```bash
# Start bot in background screen session
screen -S content-bot -d -m python content-bot-main.py start

# View logs
screen -r content-bot

# Detach from screen
# Press Ctrl+A then D

# Kill screen session
screen -S content-bot -X quit
```

### Option 2: Systemd Service (Best for Production Linux)
```bash
# Create service file
sudo nano /etc/systemd/system/content-bot.service
```

Add this content:
```ini
[Unit]
Description=Content Bot Service
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/root/clawd/content-bot
ExecStart=/usr/bin/python3 /root/clawd/content-bot/content-bot-main.py start
Restart=always
RestartSec=60
StandardOutput=append:/root/clawd/content-bot/logs/bot.log
StandardError=append:/root/clawd/content-bot/logs/bot.log

[Install]
WantedBy=multi-user.target
```

Start it:
```bash
sudo systemctl daemon-reload
sudo systemctl enable content-bot
sudo systemctl start content-bot
sudo systemctl status content-bot

# View logs
sudo journalctl -u content-bot -f

# Stop
sudo systemctl stop content-bot
```

### Option 3: Docker (Best for Cloud/Portability)

Create `Dockerfile`:
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy code
COPY . .

# Create directories
RUN mkdir -p data logs

# Environment
ENV PYTHONUNBUFFERED=1
ENV OPENAI_API_KEY=""
ENV TWITTER_API_KEY=""

EXPOSE 8000

CMD ["python", "content-bot-main.py", "start"]
```

Build and run:
```bash
# Build image
docker build -t content-bot:latest .

# Run container
docker run -d \
  --name content-bot \
  -e OPENAI_API_KEY="sk-..." \
  -e TWITTER_API_KEY="..." \
  -v /path/to/data:/app/data \
  -v /path/to/logs:/app/logs \
  content-bot:latest

# View logs
docker logs -f content-bot

# Stop
docker stop content-bot
```

### Option 4: Nohup (Very Simple Fallback)
```bash
# Start in background
nohup python content-bot-main.py start > logs/bot.log 2>&1 &

# Find process
ps aux | grep content-bot

# Kill process
kill <PID>
```

### Option 5: Supervisor (Multiple Services)
```bash
# Install supervisor
sudo apt-get install supervisor

# Create config
sudo nano /etc/supervisor/conf.d/content-bot.conf
```

Add:
```ini
[program:content-bot]
command=/usr/bin/python3 /root/clawd/content-bot/content-bot-main.py start
directory=/root/clawd/content-bot
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/root/clawd/content-bot/logs/bot.log
user=root
```

Control:
```bash
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start content-bot
sudo supervisorctl status content-bot
```

---

## Monitoring

### Check if Bot is Running

```bash
# Check process
ps aux | grep content-bot

# Check logs
tail -f logs/bot.log

# Check status
python content-bot-main.py status

# Check database
sqlite3 data/analytics.db "SELECT COUNT(*) FROM posts;"
```

### Health Check Script

Create `health-check.sh`:
```bash
#!/bin/bash

# Check if bot is running
if pgrep -f "content-bot-main.py" > /dev/null; then
    echo "✓ Bot is running"
else
    echo "✗ Bot is NOT running - restarting..."
    screen -S content-bot -d -m python content-bot-main.py start
    echo "✓ Bot restarted"
fi

# Check logs for errors
ERROR_COUNT=$(grep ERROR logs/bot.log | tail -100 | wc -l)
echo "Errors (last 100 lines): $ERROR_COUNT"

# Check last post time
LAST_POST=$(tail -50 logs/bot.log | grep "posted\|Posted" | tail -1)
echo "Last post: $LAST_POST"

# Check database size
DB_SIZE=$(du -h data/analytics.db | awk '{print $1}')
echo "Database size: $DB_SIZE"

echo ""
echo "Timestamps:"
date
```

Run daily:
```bash
chmod +x health-check.sh
./health-check.sh
```

Or schedule with cron:
```bash
# Edit crontab
crontab -e

# Add this line (runs health check every 4 hours)
0 */4 * * * /root/clawd/content-bot/health-check.sh >> /root/clawd/content-bot/logs/health-check.log 2>&1
```

---

## Auto-Restart on Failure

### Option A: Systemd (Automatic)
Already configured in systemd file with:
```
Restart=always
RestartSec=60
```

### Option B: Monitor Script

Create `monitor.py`:
```python
import subprocess
import time
import os

while True:
    # Check if bot is running
    result = subprocess.run(
        ["pgrep", "-f", "content-bot-main.py"],
        capture_output=True
    )
    
    if result.returncode != 0:
        # Bot is not running - restart it
        print(f"Bot crashed at {time.strftime('%Y-%m-%d %H:%M:%S')}")
        print("Restarting...")
        
        os.system("screen -S content-bot -X quit")
        time.sleep(5)
        os.system("screen -S content-bot -d -m python content-bot-main.py start")
        
        print("Bot restarted")
    
    # Check every 5 minutes
    time.sleep(300)
```

Run:
```bash
python monitor.py &
```

---

## Backup Strategy

### Backup Data Daily

```bash
#!/bin/bash
# backup.sh

BACKUP_DIR="/backups/content-bot"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

# Create backup directory
mkdir -p $BACKUP_DIR

# Backup database
cp data/analytics.db $BACKUP_DIR/analytics_$TIMESTAMP.db

# Backup config
cp config.py $BACKUP_DIR/config_$TIMESTAMP.py

# Compress
tar -czf $BACKUP_DIR/backup_$TIMESTAMP.tar.gz data/

# Keep last 30 days
find $BACKUP_DIR -mtime +30 -delete

echo "Backup completed: $TIMESTAMP"
```

Schedule daily:
```bash
# Add to crontab
0 2 * * * /root/clawd/content-bot/backup.sh
```

---

## Scaling

### Run Multiple Bots (Different Niches)

```bash
# Bot 1 - AI Tools
screen -S bot-ai -d -m python content-bot-main.py start

# Bot 2 - Productivity
cd /root/clawd/content-bot-productivity
screen -S bot-productivity -d -m python content-bot-main.py start

# Bot 3 - Business
cd /root/clawd/content-bot-business
screen -S bot-business -d -m python content-bot-main.py start
```

### Load Balancing

If running on multiple servers:

```python
# Central dashboard to monitor all bots
import requests

bots = [
    "http://bot1.example.com:8000/status",
    "http://bot2.example.com:8000/status",
    "http://bot3.example.com:8000/status"
]

for bot_url in bots:
    response = requests.get(bot_url)
    print(f"{bot_url}: {response.json()}")
```

---

## Troubleshooting Deployment

### Bot Won't Start
```bash
# Check Python is installed
python --version

# Check dependencies
pip list | grep openai

# Check working directory
cd /root/clawd/content-bot
ls -la

# Try running directly
python content-bot-main.py start

# Check for syntax errors
python -m py_compile content-bot-main.py
```

### Bot Crashes Immediately
```bash
# Run with verbose output
python content-bot-main.py start 2>&1

# Check logs for errors
tail -100 logs/bot.log

# Check API keys
echo $OPENAI_API_KEY

# Test individually
python content-generator.py
python platform-integrations.py
```

### High Memory Usage
```bash
# Monitor memory
top -p $(pgrep -f content-bot-main.py)

# Check database size
du -sh data/analytics.db

# Clean up old logs
rm logs/bot.*.log

# Reset database if necessary
rm data/analytics.db
```

### Slow Performance
```bash
# Check system resources
free -h
df -h

# Check database size
sqlite3 data/analytics.db "SELECT COUNT(*) FROM posts;"

# Optimize database
sqlite3 data/analytics.db "VACUUM;"

# Reduce log verbosity
# Edit config.py: LOG_LEVEL = "WARNING"
```

---

## Monitoring Dashboard

### Create Web Dashboard

Create `dashboard-api.py`:
```python
from flask import Flask, jsonify
import subprocess
import json

app = Flask(__name__)

@app.route('/status')
def status():
    """Get bot status"""
    result = subprocess.run(
        ["python", "content-bot-main.py", "status"],
        capture_output=True,
        text=True
    )
    return jsonify(json.loads(result.stdout))

@app.route('/logs')
def logs():
    """Get recent logs"""
    with open('logs/bot.log', 'r') as f:
        lines = f.readlines()[-100:]
    return jsonify({'logs': lines})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
```

Run:
```bash
python dashboard-api.py
```

Access at: `http://localhost:8000/status`

---

## Uptime Monitoring

### Use External Monitoring

Pingdom, Uptime Robot, etc:
```
Service: http://your-bot.example.com:8000/status
Interval: Every 5 minutes
Alert email: your@email.com
```

### Manual Uptime Log

```bash
#!/bin/bash
# Log uptime daily

echo "$(date): $(python content-bot-main.py status | grep running)" >> logs/uptime.log
```

---

## Production Checklist

- [ ] Bot running 24/7 (systemd or supervisor)
- [ ] Logs being written and rotated
- [ ] Database backed up daily
- [ ] Monitoring enabled
- [ ] Auto-restart configured
- [ ] Error alerts set up
- [ ] All API keys configured
- [ ] Health check running
- [ ] Analytics dashboard accessible
- [ ] Performance baseline established

---

## Maintenance

### Weekly
- [ ] Check logs for errors
- [ ] Review analytics
- [ ] Monitor costs (OpenAI, etc)
- [ ] Verify all platforms posting

### Monthly
- [ ] Optimize based on metrics
- [ ] Update dependencies: `pip install -r requirements.txt --upgrade`
- [ ] Rotate API keys
- [ ] Full backup
- [ ] Performance review

### Quarterly
- [ ] Review and update content strategy
- [ ] Analyze email performance
- [ ] Check affiliate performance
- [ ] Plan scaling strategy

---

## Support

- **Status**: `python content-bot-main.py status`
- **Logs**: `tail -f logs/bot.log`
- **Database**: `sqlite3 data/analytics.db`
- **Health**: `./health-check.sh`

---

**You're all set for 24/7 operation!** 🚀

Next: Read USAGE-GUIDE.md for daily monitoring.
