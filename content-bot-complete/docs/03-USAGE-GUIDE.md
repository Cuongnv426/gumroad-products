# Content Bot - Usage Guide

## Command Reference

### Generate Content
```bash
# Generate 1 piece
python src/bot_main.py generate

# Generate 5 pieces
python src/bot_main.py generate 5

# Generate 5 specifically for Twitter
python src/bot_main.py generate 5 twitter

# Generate for specific niche
python src/bot_main.py generate 10 --niche AI_TOOLS
```

### Post Content
```bash
# Generate and post to Twitter
python src/bot_main.py post twitter

# Generate and post to LinkedIn
python src/bot_main.py post linkedin

# Post to multiple platforms
python src/bot_main.py post multi --platforms twitter,linkedin,reddit
```

### Email Management
```bash
# Send email campaign
python src/bot_main.py email send "Your Subject Line"

# Add subscriber
python src/bot_main.py email add user@example.com "John Doe"

# Get subscriber count
python src/bot_main.py email stats
```

### Scheduling & Automation
```bash
# Start 24/7 scheduler
python src/bot_main.py start

# Start in test mode (1 cycle only)
python src/bot_main.py test

# Check next scheduled posts
python src/bot_main.py scheduler next

# Get scheduler status
python src/bot_main.py scheduler status
```

### Analytics & Reporting
```bash
# Get bot status
python src/bot_main.py status

# Get detailed analytics
python src/bot_main.py report

# Export to JSON
python src/bot_main.py report --format json

# Get revenue summary
python src/bot_main.py report --revenue
```

### Help
```bash
python src/bot_main.py help
python src/bot_main.py <command> --help
```

## Workflow Examples

### Example 1: Daily Manual Operation
```bash
# Start session
cd /path/to/content-bot
source venv/bin/activate

# Generate 5 posts
python src/bot_main.py generate 5

# Review content (manually check output)

# Post to Twitter
python src/bot_main.py post twitter

# Post to LinkedIn
python src/bot_main.py post linkedin

# Check status
python src/bot_main.py status

# Exit
deactivate
```

### Example 2: Full Automation
```bash
# Setup one-time:
# 1. Configure all API keys in .env
# 2. Setup systemd service (see deployment guide)
# 3. Start service

# Then bot runs 24/7:
sudo systemctl start content-bot
sudo systemctl enable content-bot  # Auto-start on reboot

# Monitor:
sudo journalctl -u content-bot -f
```

### Example 3: Testing & Verification
```bash
# Test all systems
python src/bot_main.py test

# Generate sample content
python src/bot_main.py generate 3

# Review output in terminal

# Check analytics
python src/bot_main.py report

# Test email (if configured)
python src/bot_main.py email send "Test"
```

## Configuration for Different Strategies

### Strategy 1: Twitter-Focused
Edit `src/config.py`:
```python
POSTING_SCHEDULE = {
    "twitter": {
        "enabled": True,
        "times": ["07:00", "09:00", "12:00", "15:00", "18:00", "21:00"],  # 6x daily
    },
    "linkedin": {
        "enabled": False,
    },
    # ... disable others
}

POSTS_PER_DAY = 20  # Higher limit for Twitter
```

### Strategy 2: Multi-Platform Balanced
```python
POSTING_SCHEDULE = {
    "twitter": {
        "enabled": True,
        "times": ["08:00", "12:00", "18:00"],  # 3x daily
    },
    "linkedin": {
        "enabled": True,
        "times": ["08:30", "12:30", "17:30"],  # 3x daily
    },
    "reddit": {
        "enabled": True,
        "times": ["10:00", "15:00", "20:00"],  # 3x daily
    },
    # ... other platforms
}

POSTS_PER_DAY = 15
```

### Strategy 3: Email-Focused
```python
POSTING_SCHEDULE = {
    "email": {
        "enabled": True,
        "times": ["07:00", "12:00", "17:00", "20:00"],  # 4x daily
    },
    "twitter": {
        "enabled": True,
        "times": ["08:00", "18:00"],  # 2x daily
    },
    # ... minimal others
}
```

## Content Customization

### Add New Keywords/Niche
Edit `src/config.py`:
```python
NICHES = {
    "AI_TOOLS": { ... },
    "MY_NICHE": {
        "keywords": ["keyword1", "keyword2", "keyword3"],
        "tone": "professional, helpful",
        "hashtags": ["#MyTag", "#Topic"]
    }
}
```

### Add Affiliate Products
```python
AFFILIATE_LINKS = {
    "my_product": "https://myaffiliate.com/ref=123",
    # ... others
}

AFFILIATE_COMMISSION_RATES = {
    "my_product": 0.25,  # 25% commission
    # ... others
}
```

### Modify Posting Schedule
```python
POSTING_SCHEDULE = {
    "twitter": {
        "enabled": True,
        "times": ["08:00", "10:00", "12:00"],  # Custom times
        "char_limit": 280,
    },
    # ...
}
```

## Content Calendar Planning

### Using the Analytics
```bash
# Get next 24h of scheduled posts
python src/bot_main.py scheduler next

# Example output:
# Next scheduled posts (24h):
#   2024-01-15 08:00:00: twitter
#   2024-01-15 09:00:00: instagram
#   2024-01-15 12:00:00: twitter
```

### Planning Tools
Export analytics to plan content:
```bash
python src/bot_main.py report --format csv > monthly_report.csv
```

Then use Excel/Google Sheets to analyze and plan.

## Monitoring & Logs

### View Logs
```bash
# Last 20 lines
tail -20 content_bot.log

# Last 50 lines, following updates
tail -f content_bot.log

# Search for errors
grep ERROR content_bot.log

# Search for specific platform
grep twitter content_bot.log
```

### Check Performance
```bash
# Get current metrics
python src/bot_main.py status

# View detailed report
python src/bot_main.py report
```

### Troubleshoot Issues
```bash
# Generate debug output
DEBUG=1 python src/bot_main.py generate --debug

# Test API connections
python src/bot_main.py test

# Verify configuration
python -c "from config import *; print(POSTING_SCHEDULE)"
```

## Production Checklist

Before running in production:

- [ ] All API keys configured in `.env`
- [ ] Tested with `python src/bot_main.py test`
- [ ] Generated sample content and reviewed
- [ ] Posted test content to at least one platform
- [ ] Verified email integration (if using)
- [ ] Set appropriate `POSTS_PER_DAY` limit
- [ ] Configured correct timezones
- [ ] Setup systemd service for VPS
- [ ] Enabled auto-restart on failure
- [ ] Setup monitoring/alerting
- [ ] Backup configuration files

## Quick Reference

| Task | Command |
|------|---------|
| Generate content | `python src/bot_main.py generate 5` |
| Post to Twitter | `python src/bot_main.py post twitter` |
| Send email | `python src/bot_main.py email send "Subject"` |
| Check status | `python src/bot_main.py status` |
| View analytics | `python src/bot_main.py report` |
| Run 24/7 | `python src/bot_main.py start` |
| Test system | `python src/bot_main.py test` |
| Get help | `python src/bot_main.py help` |
