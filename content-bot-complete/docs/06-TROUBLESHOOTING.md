# Content Bot - Troubleshooting Guide

## Common Issues & Solutions

### Installation Issues

#### Python Not Found
```bash
# Error: "python: command not found"

# Solution 1: Install Python
sudo apt install -y python3 python3-venv python3-pip

# Solution 2: Use python3 instead
python3 src/bot_main.py test
```

#### Virtual Environment Issues
```bash
# Error: "No module named 'openai'"

# Solution 1: Activate venv
source venv/bin/activate

# Solution 2: Reinstall dependencies
pip install -r requirements.txt

# Solution 3: Upgrade pip first
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

#### Missing .env File
```bash
# Error: "Invalid API key"

# Solution: Create .env
cp .env.example .env

# Edit and add your keys
nano .env

# Verify keys are loaded
python -c "from config import OPENAI_API_KEY; print(OPENAI_API_KEY)"
```

### API Key Errors

#### Invalid OpenAI Key
```bash
# Error: "Invalid authentication credentials" / "401 Unauthorized"

# Check: Is the key correct?
cat .env | grep OPENAI

# Test: Try making API call
python -c "
import openai
openai.api_key = 'YOUR_KEY_HERE'
print(openai.Model.list())
"

# Fix:
1. Visit https://platform.openai.com/api-keys
2. Create new key (old one may be revoked)
3. Copy exactly (no spaces)
4. Update .env
5. Restart bot: systemctl restart content-bot
```

#### Invalid Twitter Credentials
```bash
# Error: "Unauthorized" or "403 Forbidden"

# Check Twitter API permissions
1. Go to https://developer.twitter.com/en/portal/dashboard
2. Verify Bearer Token exists
3. Check permissions (read/write)
4. Regenerate tokens if needed

# Test with tweepy
python -c "
import tweepy
auth = tweepy.OAuthHandler('API_KEY', 'API_SECRET')
auth.set_access_token('TOKEN', 'TOKEN_SECRET')
api = tweepy.API(auth)
print(api.verify_credentials())
"
```

#### Invalid LinkedIn Token
```bash
# Error: "Unauthorized" or "401"

# Note: LinkedIn API access needs approval (2-3 days)

# Check: Has your app been approved?
1. Go to https://www.linkedin.com/developers/apps
2. Check "Authorized applications"
3. Request access if needed (takes 2-3 days)

# In meantime: Disable LinkedIn in config.py
POSTING_SCHEDULE["linkedin"]["enabled"] = False
```

#### Invalid Reddit Credentials
```bash
# Error: "INVALID_REFRESH_TOKEN" or "401"

# Check: Are you using app password?
1. Go to https://www.reddit.com/prefs/apps
2. Don't use your account password!
3. Use the app-specific password shown
4. Update .env

# Test credentials
python -c "
import praw
reddit = praw.Reddit(
    client_id='YOUR_ID',
    client_secret='YOUR_SECRET',
    user_agent='test',
    username='YOUR_USERNAME',
    password='YOUR_PASSWORD'
)
print(reddit.user.me())
"
```

### Content Generation Errors

#### "openai.error.RateLimitError"
```bash
# Error: "Rate limit exceeded"

# Cause: Too many API calls

# Solutions:
1. Wait 5-15 minutes
2. Reduce POSTS_PER_DAY in config
3. Upgrade OpenAI plan
4. Space out requests over time

# Example fix in config.py:
POSTS_PER_DAY = 5  # Was 10
```

#### Content Generation Fails
```bash
# Error: "Content generation failed"

# Check logs
tail -100 content_bot.log | grep ERROR

# Test manually
python src/bot_main.py generate 1

# Common causes:
1. Invalid OpenAI key
2. Account overdue payment
3. API service down (check https://status.openai.com)
4. Token limit exceeded

# Verify API is working
python -c "
import openai
openai.api_key = 'YOUR_KEY'
response = openai.ChatCompletion.create(
    model='gpt-3.5-turbo',
    messages=[{'role': 'user', 'content': 'Hello'}]
)
print(response)
"
```

#### Duplicate Content Detection
```bash
# Bot is regenerating same content

# Cause: Low similarity threshold

# Fix in content_engine.py:
def _is_duplicate(self, content: str, threshold: float = 0.85) -> bool:
    # Increase threshold to be less strict
    threshold = 0.75  # Was 0.85
```

### Posting Issues

#### Posts Not Publishing to Twitter
```bash
# Error: "TwitterRequestsError" or "403 Forbidden"

# Check 1: Is account suspended?
1. Go to https://twitter.com
2. Check if account works
3. Verify not rate-limited (wait 15 min)

# Check 2: API permissions
1. Dashboard > Settings > Permissions
2. Ensure "Read and write" is enabled
3. Regenerate tokens if needed

# Check 3: Tweet content
1. Over 280 characters?
2. Suspicious links or spam?
3. Violates Twitter rules?

# Test posting manually
python src/bot_main.py post twitter
```

#### Posts Not Publishing to LinkedIn
```bash
# Error: "Unauthorized" or "404 Not found"

# Check: Has app been approved?
1. Go to https://www.linkedin.com/developers/apps
2. Check for "Share on LinkedIn" permission
3. May need additional approval

# Temporary fix: Disable LinkedIn
In config.py:
POSTING_SCHEDULE["linkedin"]["enabled"] = False

# Try again in a few days
```

#### Posts Not Publishing to Reddit
```bash
# Error: "SUBREDDIT_NOT_FOUND" or "403 Forbidden"

# Check 1: Subreddit exists
subreddit_name = "test"  # Is this a real subreddit?

# Check 2: Permissions
1. Are you subscribed?
2. Do you have posting rights?
3. Is subreddit restricted?

# Check 3: Content quality
1. Too short? (Reddit minimum ~100 chars)
2. Too long? (Reddit maximum 40,000 chars)
3. Violates rules? (check r/xxx/rules)

# Fix in config.py
POSTING_SCHEDULE["reddit"]["enabled"] = False  # Disable until fixed
```

### Email Issues

#### Mailchimp Campaign Not Sending
```bash
# Error: "Mailchimp API error" or "403"

# Check 1: API key validity
curl https://YOUR_SERVER.api.mailchimp.com/3.0/ \
  -u user:YOUR_API_KEY

# Check 2: List ID correct
1. Go to Mailchimp audience
2. Copy List ID exactly (case-sensitive)
3. Update .env

# Check 3: Verify approval
1. Your email must be verified
2. List must have at least 1 subscriber
3. Recent API key (not older than 90 days)

# Test API
python -c "
import requests
api_key = 'YOUR_KEY'
server = api_key.split('-')[1]
response = requests.get(
    f'https://{server}.api.mailchimp.com/3.0/lists/YOUR_LIST_ID',
    auth=('user', api_key)
)
print(response.json())
"
```

#### Subscribers Not Being Added
```bash
# Check logs
grep -i mailchimp content_bot.log

# Verify credentials
python -c "
from email_system import mailchimp
stats = mailchimp.get_list_stats()
print(stats)
"

# Check list restrictions
1. Go to Mailchimp list settings
2. Verify double opt-in is enabled/disabled as needed
3. Check for spam traps

# Test adding subscriber manually
python -c "
from email_system import mailchimp
result = mailchimp.add_subscriber('test@example.com', 'Test User')
print(result)
"
```

### Scheduler Issues

#### Bot Not Running 24/7
```bash
# Check if systemd service is running
sudo systemctl status content-bot

# If stopped, restart it
sudo systemctl start content-bot

# Check if it crashed
sudo journalctl -u content-bot --no-pager | tail -50

# Common crash causes:
1. Out of memory
2. Unhandled exception
3. File permissions
4. Missing Python modules

# Fix permissions
sudo chown -R contentbot:contentbot /opt/content-bot
sudo chmod -R 755 /opt/content-bot
```

#### Posts Not Posting at Scheduled Times
```bash
# Check scheduled jobs
python src/bot_main.py scheduler next

# Verify times are in correct timezone
1. Check server timezone: timedatectl
2. Verify config.py times match your timezone
3. Update timezone if needed

# Example timezone conversion
# If VPS is UTC but you want EST:
# Server time 1:00 PM UTC = 8:00 AM EST
# So schedule for 1:00 PM = 8:00 AM your time

# Manually run a job
python src/bot_main.py post twitter

# Check if jobs are being queued
python -c "
from scheduler import scheduler
jobs = scheduler.get_next_jobs(hours=1)
print(jobs)
"
```

#### Too Many Posts Per Day
```bash
# Posts exceeding POSTS_PER_DAY limit

# This is intentional! It's a safety feature.

# To increase limit, edit config.py:
POSTS_PER_DAY = 10  # Increase from 10 to 20

# Reset counter daily at midnight
# (happens automatically)

# Check current count
python -c "
from scheduler import scheduler
print(f'Posts today: {scheduler.posts_today}')
print(f'Daily limit: {scheduler.scheduler.POSTS_PER_DAY}')
"
```

### Performance Issues

#### High CPU Usage
```bash
# Check what's using CPU
top -b -n 1 | grep python

# Possible causes:
1. Too many API calls
2. Large batch processing
3. Inefficient duplication check

# Fixes:
1. Reduce POSTS_PER_DAY
2. Increase time between checks (scheduler.py line ~100)
3. Disable content features temporarily
```

#### High Memory Usage
```bash
# Check memory
free -h

# If running out of memory:
1. Restart bot: sudo systemctl restart content-bot
2. Clear old logs: rm logs/*
3. Upgrade VPS plan
4. Reduce batch size

# Monitor memory
watch -n 1 'free -h'
```

#### Slow Content Generation
```bash
# Takes more than 30 seconds to generate

# Cause: OpenAI API latency

# Solutions:
1. Increase timeout in config.py
2. Use faster model (gpt-3.5-turbo is default)
3. Check internet connection
4. Check OpenAI status

# Test API speed
time python -c "
import openai
openai.api_key = 'YOUR_KEY'
response = openai.ChatCompletion.create(
    model='gpt-3.5-turbo',
    messages=[{'role': 'user', 'content': 'Hi'}]
)
"
```

### Log Reading

#### Find Errors Quickly
```bash
# All errors today
sudo journalctl -u content-bot --since today -p err

# Last 100 lines
sudo journalctl -u content-bot -n 100

# Real-time monitoring
sudo journalctl -u content-bot -f

# Errors in past hour
sudo journalctl -u content-bot --since "1 hour ago" -p err

# Search for specific platform
sudo journalctl -u content-bot | grep twitter

# Export to file for analysis
sudo journalctl -u content-bot > bot_logs.txt
```

## Getting Help

### Before Asking for Help:

1. **Check logs**
   ```bash
   sudo journalctl -u content-bot -f
   ```

2. **Run tests**
   ```bash
   python src/bot_main.py test
   ```

3. **Verify configuration**
   ```bash
   cat .env | grep OPENAI  # Should show your key
   ```

4. **Try manual operations**
   ```bash
   python src/bot_main.py generate 1
   python src/bot_main.py post twitter
   ```

5. **Check documentation**
   - See docs/ folder
   - Check API provider status pages

### Debug Mode

```bash
# Run with debug output
DEBUG=1 python src/bot_main.py test

# Verbose logging
LOGLEVEL=DEBUG python src/bot_main.py start

# Save debug output to file
python src/bot_main.py test 2>&1 | tee debug.log
```

## Quick Fixes Checklist

- [ ] Restart bot: `sudo systemctl restart content-bot`
- [ ] Check logs: `sudo journalctl -u content-bot -f`
- [ ] Verify .env: `cat .env | grep OPENAI`
- [ ] Test API keys manually
- [ ] Clear old files: `rm logs/*`
- [ ] Update dependencies: `pip install -r requirements.txt -U`
- [ ] Check disk space: `df -h`
- [ ] Reboot VPS: `sudo reboot`
