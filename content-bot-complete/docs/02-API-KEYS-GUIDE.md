# API Keys Setup Guide

## Complete List of Required Keys

### 1. OpenAI (REQUIRED)
**For:** AI content generation with ChatGPT

**Get Key:**
1. Visit https://platform.openai.com/account/api-keys
2. Click "Create new secret key"
3. Copy immediately (won't show again)
4. Add to `.env`:
```
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxx
```

**Costs:**
- GPT-3.5: ~$0.0005 per 1K input tokens, $0.0015 per 1K output tokens
- Estimate: ~$1-5/month at 10 posts/day

**Verify:**
```bash
python -c "import openai; openai.api_key = 'YOUR_KEY'; print(openai.Model.list())"
```

### 2. Twitter/X API
**For:** Posting tweets, scheduling content

**Get Keys:**
1. Go to https://developer.twitter.com/en/portal/dashboard
2. Create/select project
3. Go to "Keys and tokens"
4. Generate Bearer Token, API Key, API Key Secret
5. Generate Access Token & Secret
6. Add to `.env`:
```
TWITTER_API_KEY=xxxx
TWITTER_API_SECRET=xxxx
TWITTER_ACCESS_TOKEN=xxxx
TWITTER_ACCESS_TOKEN_SECRET=xxxx
TWITTER_BEARER_TOKEN=xxxx
```

**Verify:**
```python
import tweepy
auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)
print(api.verify_credentials())  # Should print your user info
```

### 3. LinkedIn API
**For:** Sharing articles and updates

**Get Token:**
1. Go to https://www.linkedin.com/developers/apps
2. Create application
3. Request access to "Sign In with LinkedIn" and "Share on LinkedIn"
4. Get access token from auth flow
5. Add to `.env`:
```
LINKEDIN_ACCESS_TOKEN=xxxxxxxxxxxx
```

**Note:** LinkedIn API access requires approval. Takes 2-3 days.

### 4. Reddit API
**For:** Posting to subreddits

**Get Credentials:**
1. Go to https://www.reddit.com/prefs/apps
2. Scroll down to "Authorized applications"
3. Click "Create another app..."
4. Fill form, select "script"
5. You'll get CLIENT_ID and SECRET
6. Add to `.env`:
```
REDDIT_CLIENT_ID=xxxx
REDDIT_CLIENT_SECRET=xxxx
REDDIT_USERNAME=your_reddit_username
REDDIT_PASSWORD=your_reddit_password
```

**Important:** Use app password, not your account password!

### 5. Mailchimp (Email List)
**For:** Growing email list, sending campaigns

**Get API Key:**
1. Go to https://mailchimp.com (create account)
2. Go to Account > Extras > API Keys
3. Click "Create A Key"
4. Copy key
5. Get List ID from Audience section
6. Add to `.env`:
```
MAILCHIMP_API_KEY=xxxxxxxx-us1
MAILCHIMP_LIST_ID=xxxxxx
```

**Costs:** Free up to 500 contacts, then tiered

### 6. SendGrid (Alternative Email)
**For:** Email sending (alternative to Mailchimp)

**Get Key:**
1. Go to https://sendgrid.com
2. Dashboard > API Keys > Create API Key
3. Copy key
4. Add to `.env`:
```
SENDGRID_API_KEY=SG.xxxxxxxxxxxx
```

**Costs:** Free up to 100 emails/day

### 7. Medium API
**For:** Publishing long-form articles

**Get Token:**
1. Go to https://medium.com/me/settings
2. Security tab
3. Integration tokens
4. Generate new token
5. Add to `.env`:
```
MEDIUM_TOKEN=xxxxxxxxxxxxxxxxxxxxxxxx
```

**Note:** Medium API requires account with published articles

### 8. TikTok API (Optional)
**For:** Posting TikTok videos (requires image/video generation)

**Status:** Requires complex auth, not fully implemented yet

### 9. Instagram API (Optional)
**For:** Posting to Instagram (requires image generation)

**Status:** Requires complex auth, not fully implemented yet

## Quick Setup (Copy-Paste)

```bash
# 1. Copy template
cp .env.example .env

# 2. Edit and fill in keys
nano .env

# 3. Format should look like:
OPENAI_API_KEY=sk-abc123def456
TWITTER_API_KEY=abc123
TWITTER_API_SECRET=def456
# ... etc

# 4. Test keys
python src/bot_main.py test
```

## Testing Keys

```bash
# Test all configured services
python -c "
from config import *
print('OpenAI:', 'OK' if OPENAI_API_KEY else 'MISSING')
print('Twitter:', 'OK' if TWITTER_API_KEY else 'MISSING')
print('LinkedIn:', 'OK' if LINKEDIN_ACCESS_TOKEN else 'MISSING')
print('Reddit:', 'OK' if REDDIT_CLIENT_ID else 'MISSING')
print('Mailchimp:', 'OK' if MAILCHIMP_API_KEY else 'MISSING')
"
```

## Cost Estimates (Monthly)

| Service | Cost/Month | Usage |
|---------|-----------|-------|
| OpenAI | $1-5 | 10k posts/month |
| Twitter | Free | Unlimited tweets |
| LinkedIn | Free | Unlimited posts |
| Reddit | Free | Unlimited posts |
| Mailchimp | Free | <500 subscribers |
| SendGrid | Free | 100 emails/day |
| Medium | Free | Unlimited articles |
| **TOTAL** | **$1-5** | All platforms |

## Free Alternative Services

**If you don't have keys:**

1. **Generate Content:**
   - Use free GPT alternatives (Llama, etc.)
   - Use content API (contentful, strapi)

2. **Post to Twitter:**
   - Use free APIs

3. **Email List:**
   - Mailchimp free tier (500 contacts)
   - Brevo free tier (300 emails/day)

4. **Analytics:**
   - Use platform native analytics

## Rotating/Refreshing Keys

For security, rotate keys every 90 days:

```bash
# Twitter
1. Go to https://developer.twitter.com
2. Delete old key
3. Generate new key
4. Update .env

# LinkedIn
1. Go to app settings
2. Regenerate token
3. Update .env

# Others
Same process - delete old, create new, update .env
```

## Security Best Practices

✅ **DO:**
- Store keys in `.env` (not in code)
- Add `.env` to `.gitignore`
- Rotate keys periodically
- Use environment variables in production
- Restrict API key permissions

❌ **DON'T:**
- Commit `.env` to GitHub
- Share API keys
- Use same key for test/production
- Leave keys in logs

## Troubleshooting

**"Invalid API key" error:**
- Copy-paste key again carefully
- Check for extra spaces
- Verify key hasn't been revoked
- Check key is for right environment (test vs prod)

**"API rate limit exceeded":**
- Wait 15 minutes
- Upgrade plan
- Reduce posting frequency

**"Connection timeout":**
- Check internet connection
- API service might be down (check status pages)
- Try test endpoint first
