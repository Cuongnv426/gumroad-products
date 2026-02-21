# Content Bot - Usage Guide

How to use the Content Bot daily, monitor it, and optimize earnings.

## Quick Start

### Option 1: Auto-Run (Recommended)

```bash
# Start bot - runs 24/7 with auto-posting
python content-bot-main.py start
```

Bot will:
- Generate content daily at midnight
- Post automatically at scheduled times
- Track analytics in real-time
- Send emails to subscribers
- Monitor affiliate clicks

### Option 2: Interactive Menu

```bash
# Start interactive menu
python content-bot-main.py
```

Menu options:
1. Start bot (24/7 auto-posting)
2. Generate content batch (manual)
3. Show current status
4. View analytics dashboard
5. Test platform connections
6. Generate sample content
7. Exit

### Option 3: Command Line

```bash
# Generate 20 pieces of content
python content-bot-main.py generate 20

# Show bot status
python content-bot-main.py status

# Test all APIs
python content-bot-main.py test
```

---

## Daily Workflow

### Morning (First thing)

```bash
# 1. Check bot status
python content-bot-main.py status

# 2. View today's analytics
tail -f logs/bot.log

# 3. Check dashboard
open data/dashboard.html
```

### Midday (Optional)

```bash
# 1. Generate additional content (if needed)
python content-bot-main.py generate 10

# 2. Monitor affiliate clicks
sqlite3 data/analytics.db "SELECT * FROM affiliate_clicks WHERE DATE(clicked_at) = DATE('now')"

# 3. Check email engagement
sqlite3 data/analytics.db "SELECT * FROM email_subscribers ORDER BY last_engaged DESC LIMIT 10"
```

### Evening (Optional)

```bash
# 1. Review performance metrics
python content-bot-main.py status | grep -i "posts\|revenue"

# 2. Adjust schedule if needed
# Edit config.py and restart bot

# 3. Prepare next day's content
python content-bot-main.py generate 15
```

---

## Monitoring

### View Real-Time Logs

```bash
# Follow bot logs
tail -f logs/bot.log

# See last 100 lines
tail -100 logs/bot.log

# Search for errors
grep ERROR logs/bot.log

# See Twitter posts
grep "twitter" logs/bot.log -i
```

### Check Analytics

```bash
# View database
sqlite3 data/analytics.db

# Get today's stats
SELECT * FROM posts WHERE DATE(posted_at) = DATE('now');

# Get affiliate revenue
SELECT tool_name, COUNT(*) as clicks, SUM(revenue) as revenue 
FROM affiliate_clicks 
WHERE DATE(clicked_at) = DATE('now') 
GROUP BY tool_name;

# Get email subscribers
SELECT COUNT(*) FROM email_subscribers WHERE status = 'active';
```

### Dashboard

Open in browser: `data/dashboard.html`

Shows:
- Posts created today
- Affiliate clicks and revenue
- Email signups
- Platform performance
- Revenue forecast
- Top performing content

---

## Manual Content Generation

### Generate Specific Content Type

```python
from content_generator import ContentGenerator

gen = ContentGenerator()

# TikTok script
tiktok = gen.generate_tiktok_script()

# Twitter posts (5)
tweets = gen.generate_twitter_posts(5)

# Blog post
blog = gen.generate_blog_post()

# Email
email = gen.generate_email_content()

# LinkedIn post
linkedin = gen.generate_linkedin_post()

# Reddit post
reddit = gen.generate_reddit_post()
```

### Batch Generation

```python
from content_generator import ContentGenerator
import json

gen = ContentGenerator()

batch = {
    "twitter": gen.generate_twitter_posts(10),
    "tiktok": [gen.generate_tiktok_script() for _ in range(4)],
    "linkedin": [gen.generate_linkedin_post() for _ in range(3)],
    "blog": gen.generate_blog_post(),
    "email": gen.generate_email_content()
}

# Save batch
with open("batch.json", "w") as f:
    json.dump(batch, f, indent=2)
```

---

## Manual Posting

### Post to Single Platform

```python
from platform_integrations import PlatformManager

manager = PlatformManager()

content = {
    "content": "Check out this amazing AI tool! 🚀 [link]",
    "hashtags": ["#AITools", "#Productivity"]
}

result = manager.post_to_platform("twitter", content)
print(result)
```

### Post to Multiple Platforms

```python
from platform_integrations import PlatformManager

manager = PlatformManager()

content_map = {
    "twitter": {"content": "Tweet text"},
    "linkedin": {"content": "LinkedIn post"},
    "reddit": {
        "subreddit": "ChatGPT",
        "title": "Post Title",
        "body": "Post body..."
    }
}

results = manager.post_to_all(content_map)
print(results)
```

---

## Email Management

### Add Subscriber Manually

```python
from email_system import EmailListManager

manager = EmailListManager()

# Add single subscriber
manager.add_subscriber(
    email="user@example.com",
    first_name="John",
    last_name="Doe",
    tags=["interested_in_ai", "early_adopter"]
)

# Add multiple
emails = [
    ("user1@example.com", "User", "One"),
    ("user2@example.com", "User", "Two"),
]

for email, fname, lname in emails:
    manager.add_subscriber(email, fname, lname)
```

### Send Manual Campaign

```python
from email_system import EmailListManager
from platform_integrations import EmailIntegration

email_api = EmailIntegration()

content = {
    "subject_line": "5 AI Tools Saving Me 10 Hours/Week",
    "preheader_text": "Check this out...",
    "body": "Email body here...",
    "cta_primary": "Learn More",
    "cta_primary_url": "https://example.com",
}

result = email_api.post(content)
print(result)
```

### View Email Stats

```python
from email_system import EmailListManager

manager = EmailListManager()

# Get subscriber count
count = manager.get_subscriber_count()
print(f"Total subscribers: {count}")

# Get growth stats
stats = manager.get_list_growth_stats()
print(stats)
```

---

## Analytics & Revenue

### View Revenue

```python
from analytics import DashboardGenerator

dashboard = DashboardGenerator()

# Daily report
daily = dashboard.generate_daily_report()
print(f"Revenue: {daily.get('affiliate_revenue')}")

# Weekly report
weekly = dashboard.generate_weekly_report()
print(f"Weekly revenue: {weekly.get('total_revenue')}")

# Monthly report
monthly = dashboard.generate_monthly_report()
print(f"Monthly forecast: {monthly.get('total_revenue')}")
```

### Track Affiliate Performance

```python
from analytics import AffiliateTracker

tracker = AffiliateTracker()

# Get stats
stats = tracker.get_affiliate_stats()

for tool, data in stats.get("by_tool", {}).items():
    print(f"{tool}: {data['clicks']} clicks, {data['revenue']}")
```

### Analyze Content Performance

```python
from analytics import PerformanceAnalytics

analytics = PerformanceAnalytics()

# Get top performing
top = analytics.get_top_performing_content(limit=5)
for post in top:
    print(f"Post {post['post_id']}: {post['engagement_rate']:.2f}% engagement")

# Platform comparison
platforms = analytics.get_platform_performance()
for platform, data in platforms.items():
    print(f"{platform}: Avg {data['avg_views']} views, {data['avg_engagement']}% engagement")
```

---

## Scheduling

### View Next Scheduled Posts

```python
from scheduler import PostScheduler

scheduler = PostScheduler()

# Next 24 hours
next_posts = scheduler.get_next_posts(hours=24)

for post in next_posts:
    print(f"{post['platform']}: {post['scheduled_time']}")
```

### Adjust Schedule

Edit `config.py`:

```python
POSTING_SCHEDULE = {
    "twitter": {
        "times": ["09:00", "12:00", "15:00", "18:00", "21:00"],  # Adjust times
        "content_per_day": 5
    },
    "tiktok": {
        "times": ["08:00", "18:00"],  # 2x per day
        "content_per_day": 2
    },
    # ... etc
}
```

Restart bot for changes to take effect:
```bash
# Kill running bot (Ctrl+C)
# Restart
python content-bot-main.py start
```

---

## Optimization Tips

### 1. A/B Testing

Test different:
- Post timing
- Content angles
- Affiliate link placement
- Email subject lines

Track in analytics and replicate winners.

### 2. Content Audit

```bash
# Find top performing content
sqlite3 data/analytics.db "SELECT * FROM posts ORDER BY engagement_rate DESC LIMIT 10"

# Replicate the format/topic
```

### 3. Affiliate Optimization

```bash
# Find top converting tools
sqlite3 data/analytics.db "SELECT tool_name, COUNT(*) as clicks FROM affiliate_clicks GROUP BY tool_name ORDER BY clicks DESC"

# Focus content on top performers
```

### 4. Email List Growth

- Add opt-in forms to blog posts
- Include CTAs in videos
- Cross-promote in newsletters
- Target 5-10 new subscribers per day

### 5. Monitor Costs

```bash
# Check OpenAI API usage
curl https://api.openai.com/v1/usage \
  -H "Authorization: Bearer $OPENAI_API_KEY"

# Keep monthly costs under $50
```

---

## Troubleshooting

### Bot Not Posting

```bash
# Check logs for errors
grep ERROR logs/bot.log

# Verify API keys are set
echo $OPENAI_API_KEY
echo $TWITTER_API_KEY

# Test platform connection
python platform-integrations.py
```

### Content Generation Slow

```bash
# Check OpenAI rate limits
# Use GPT-3.5 Turbo instead of GPT-4
# Batch generation during off-peak hours
```

### Email Not Sending

```bash
# Verify Mailchimp setup
python email-system.py

# Check list ID and API key
# Ensure GDPR compliance
```

### Database Errors

```bash
# Reset database
rm data/analytics.db

# Bot will recreate on next run
python content-bot-main.py start
```

---

## Daily Success Checklist

- [ ] Bot is running (`ps aux | grep content-bot`)
- [ ] Logs show no errors (`tail logs/bot.log`)
- [ ] Dashboard updated (`data/dashboard.html`)
- [ ] At least 1 post succeeded
- [ ] No API key errors
- [ ] Email list growing
- [ ] Affiliate clicks tracking
- [ ] Revenue being logged

---

## Performance Targets

### Daily Goals
- ✓ 10-20 posts generated
- ✓ 8-15 posts published
- ✓ 5-10 affiliate clicks
- ✓ 2-5 email signups
- ✓ $10-20 revenue

### Weekly Goals
- ✓ 70-140 posts
- ✓ 50+ affiliate clicks
- ✓ 20+ email signups
- ✓ $100-150 revenue

### Monthly Goals
- ✓ 300-600 posts
- ✓ 200+ affiliate clicks
- ✓ 80+ email signups
- ✓ $400-600 revenue

---

## Next Steps

1. ✓ Set up bot and APIs
2. ✓ Generate first batch of content
3. ✓ Post manually to verify
4. ✓ Start 24/7 auto-posting
5. ✓ Monitor daily for 1 week
6. ✓ Optimize based on data
7. ✓ Scale up platforms
8. ✓ Build email list
9. ✓ Maximize affiliate revenue

See `OPTIMIZATION-GUIDE.md` for advanced tips.

---

## Support

- **Logs**: `logs/bot.log`
- **Dashboard**: `data/dashboard.html`
- **Database**: `data/analytics.db`
- **Config**: `config.py`

Questions? Check the error logs first!
