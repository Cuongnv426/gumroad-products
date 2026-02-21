# API Keys & Credentials Guide

Complete list of API keys needed for the Content Bot and how to obtain them.

## Overview

| Platform | Required? | Priority | Cost | Setup Time |
|----------|-----------|----------|------|------------|
| OpenAI (GPT) | YES | Critical | $0.20 per 1M tokens | 5 min |
| Twitter/X | YES | High | Free | 10 min |
| TikTok | NO | Medium | Free | 15 min |
| Instagram | NO | Medium | Free | 10 min |
| LinkedIn | NO | Medium | Free | 15 min |
| Reddit | NO | Low | Free | 5 min |
| Medium | NO | Low | Free | 5 min |
| Mailchimp | NO | Medium | Free tier available | 10 min |
| Google Analytics | NO | Optional | Free | 10 min |

---

## 1. OpenAI API (REQUIRED)

**Purpose**: Generate all content (scripts, posts, blogs, emails)

### Setup Steps:

1. Go to https://platform.openai.com/signup
2. Create account and verify email
3. Go to https://platform.openai.com/account/api-keys
4. Click "Create new secret key"
5. Copy the key (starts with `sk-`)

### Configuration:

```bash
export OPENAI_API_KEY="sk-proj-..."
```

### Pricing:
- GPT-3.5 Turbo: $0.0005 per 1K input tokens
- GPT-4: $0.03 per 1K input tokens
- Estimate: ~$10-50/month for daily content generation

### Test:
```python
from openai import OpenAI
client = OpenAI(api_key="sk-...")
response = client.messages.create(model="gpt-4", messages=[{"role": "user", "content": "Hello"}])
print(response.choices[0].message.content)
```

---

## 2. Twitter API (REQUIRED)

**Purpose**: Post tweets 5x per day

### Setup Steps:

1. Go to https://developer.twitter.com/en/apply/general
2. Apply for Developer Account
3. Wait for approval (usually 24-48 hours)
4. Go to https://developer.twitter.com/en/dashboard
5. Create a new project and app
6. Go to "Keys and tokens" tab
7. Copy:
   - API Key (Consumer Key)
   - API Secret Key (Consumer Secret)
   - Click "Generate" for Access Token and Secret

### Configuration:

```bash
export TWITTER_API_KEY="your_api_key"
export TWITTER_API_SECRET="your_api_secret"
export TWITTER_ACCESS_TOKEN="your_access_token"
export TWITTER_ACCESS_TOKEN_SECRET="your_access_token_secret"
```

### Permissions:
- Make sure app has "Read and Write" permission
- Enable API v2 endpoints

### Test:
```bash
curl -X GET "https://api.twitter.com/2/tweets/search/recent?query=bot" \
  -H "authorization: Bearer $TWITTER_BEARER_TOKEN"
```

---

## 3. TikTok API (OPTIONAL - for video posting)

**Purpose**: Post videos 2x per day

### Setup Steps:

1. Go to https://developers.tiktok.com/
2. Click "Sign up for Creator Marketplace"
3. Fill application form
4. Wait for approval
5. Go to dashboard and create new app
6. Get OAuth 2.0 Access Token

### Configuration:

```bash
export TIKTOK_ACCESS_TOKEN="your_access_token"
export TIKTOK_REFRESH_TOKEN="your_refresh_token"  # Optional
```

### Important:
- Requires video file to post
- Consider using video generation API
- Rate limit: 100 requests/hour

### Test:
```bash
curl -X GET "https://open-api.tiktok.com/v1/video/upload" \
  -H "Authorization: Bearer $TIKTOK_ACCESS_TOKEN"
```

---

## 4. Instagram API (OPTIONAL - for Reels)

**Purpose**: Post Reels 2x per day

### Setup Steps:

1. Go to https://developers.facebook.com/
2. Create app and select "Instagram" product
3. Request Instagram Basic Display access
4. Get Instagram Business Account ID
5. Generate long-lived access token

### Configuration:

```bash
export INSTAGRAM_ACCESS_TOKEN="your_access_token"
export INSTAGRAM_BUSINESS_ACCOUNT_ID="your_account_id"
```

### Important:
- Must have Instagram Business Account
- Connected to Facebook Page
- Access token expires - set up refresh mechanism

### Test:
```bash
curl -X GET "https://graph.instagram.com/v18.0/me" \
  -H "Authorization: Bearer $INSTAGRAM_ACCESS_TOKEN"
```

---

## 5. LinkedIn API (OPTIONAL - for professional posts)

**Purpose**: Post professional content 2x per day

### Setup Steps:

1. Go to https://www.linkedin.com/developers/apps
2. Create new app
3. Request "Sign In with LinkedIn" and "Share on LinkedIn" access
4. Get OAuth 2.0 credentials
5. Get your LinkedIn Person URN (format: `urn:li:person:XXXXXXXXX`)

### Configuration:

```bash
export LINKEDIN_ACCESS_TOKEN="your_access_token"
export LINKEDIN_PERSON_URN="urn:li:person:123456789"
```

### Get Your Person URN:
```bash
curl -X GET "https://api.linkedin.com/v2/me" \
  -H "Authorization: Bearer $LINKEDIN_ACCESS_TOKEN"
# Look for "id" in response
```

### Important:
- Access token expires in 60 days
- Need to implement refresh token mechanism
- API is rate limited

---

## 6. Reddit API (OPTIONAL - for community posts)

**Purpose**: Post to subreddits 2x per day

### Setup Steps:

1. Create Reddit account at https://reddit.com
2. Go to https://www.reddit.com/prefs/apps
3. Click "create another app"
4. Select "script" type
5. Get Client ID and Client Secret
6. Have Reddit username and password ready

### Configuration:

```bash
export REDDIT_CLIENT_ID="your_client_id"
export REDDIT_CLIENT_SECRET="your_client_secret"
export REDDIT_USERNAME="your_username"
export REDDIT_PASSWORD="your_password"
```

### Important:
- Use throwaway account for bot
- Follow subreddit rules strictly
- Respect Reddit's self-promotion limits
- Be helpful, not spammy

### Test:
```bash
python -c "import praw; r = praw.Reddit(...); print(r.user.me())"
```

---

## 7. Medium API (OPTIONAL - for blog posts)

**Purpose**: Publish blog posts 2x per week

### Setup Steps:

1. Create Medium account at https://medium.com
2. Go to https://medium.com/me/settings
3. Scroll to "Security and apps"
4. Generate integration token
5. Copy token

### Configuration:

```bash
export MEDIUM_API_TOKEN="your_integration_token"
```

### Important:
- Token doesn't expire
- Can publish under your account only
- API is simple but limited
- No scheduling - publishes immediately

### Test:
```bash
curl -X GET "https://api.medium.com/v1/me" \
  -H "Authorization: Bearer $MEDIUM_API_TOKEN"
```

---

## 8. Mailchimp API (RECOMMENDED - for email)

**Purpose**: Send newsletters to email list

### Setup Steps:

1. Go to https://mailchimp.com (free account)
2. Create account
3. Create email list
4. Go to Account Settings > Extra
5. Go to "API keys"
6. Create new API key
7. Copy key and server (e.g., "us1")

### Configuration:

```bash
export MAILCHIMP_API_KEY="your_api_key-us1"
export MAILCHIMP_LIST_ID="your_list_id"
export MAILCHIMP_SERVER="us1"  # Replace with your server
```

### Get List ID:
1. In Mailchimp, go to Audience
2. Click your list
3. Settings > List name and defaults
4. Copy Audience ID

### Important:
- Free tier: up to 500 contacts, no cost
- Requires GDPR-compliant opt-in
- Test with test list first

### Test:
```bash
python -c "
import mailchimp_marketing as MailchimpMarketing
client = MailchimpMarketing.Client()
client.set_config({'api_key': 'key-server', 'server': 'us1'})
response = client.lists.get_list('list_id')
print(response)
"
```

---

## 9. Google Analytics (OPTIONAL - for tracking)

**Purpose**: Track blog traffic and conversions

### Setup Steps:

1. Go to https://analytics.google.com
2. Click "Start measuring"
3. Enter website details
4. Get Measurement ID (format: `G-XXXXXXXXXX`)
5. Add tracking code to blog

### Configuration:

```bash
export GOOGLE_ANALYTICS_ID="G-XXXXXXXXXX"
```

### Important:
- Free tier includes most features
- Setup takes 24-48 hours to show data
- Requires adding code to website

---

## API Keys Checklist

### Minimum Setup (Content generation only):
- [ ] OpenAI API Key
- [ ] Twitter API Keys

### Recommended Setup (Multi-platform):
- [ ] OpenAI API Key
- [ ] Twitter API Keys
- [ ] LinkedIn API Token
- [ ] Mailchimp API Key
- [ ] Reddit API Credentials

### Full Setup (All platforms):
- [ ] OpenAI API Key
- [ ] Twitter API Keys
- [ ] TikTok API Token
- [ ] Instagram API Token
- [ ] LinkedIn API Token
- [ ] Reddit API Credentials
- [ ] Medium API Token
- [ ] Mailchimp API Key
- [ ] Google Analytics ID

---

## Environment Variables

Create `.env` file:

```bash
# Required
OPENAI_API_KEY="sk-..."
TWITTER_API_KEY="..."
TWITTER_API_SECRET="..."
TWITTER_ACCESS_TOKEN="..."
TWITTER_ACCESS_TOKEN_SECRET="..."

# Optional but recommended
MAILCHIMP_API_KEY="..."
MAILCHIMP_LIST_ID="..."
MAILCHIMP_SERVER="us1"
LINKEDIN_ACCESS_TOKEN="..."
LINKEDIN_PERSON_URN="..."

# Optional
TIKTOK_ACCESS_TOKEN="..."
INSTAGRAM_ACCESS_TOKEN="..."
INSTAGRAM_BUSINESS_ACCOUNT_ID="..."
REDDIT_CLIENT_ID="..."
REDDIT_CLIENT_SECRET="..."
REDDIT_USERNAME="..."
REDDIT_PASSWORD="..."
MEDIUM_API_TOKEN="..."
GOOGLE_ANALYTICS_ID="..."
```

Load in Python:
```python
from dotenv import load_dotenv
import os
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
```

---

## Cost Breakdown

### Monthly Costs (estimated):

| Service | Usage | Cost |
|---------|-------|------|
| OpenAI | 50 posts/day | $20-50 |
| Twitter | Unlimited | Free |
| TikTok | Unlimited | Free |
| LinkedIn | Unlimited | Free |
| Reddit | Unlimited | Free |
| Medium | Unlimited | Free |
| Mailchimp | Up to 500 subscribers | Free |
| **Total** | | **$20-50/month** |

### Optimization:
- Use GPT-3.5 Turbo instead of GPT-4 ($3-10/month)
- Batch content generation during off-peak hours
- Use free tiers of all services
- **Total minimum cost: $5-15/month for unlimited posts**

---

## Troubleshooting

### API Key Not Working
```bash
# Test key validity
curl -X GET "https://api.openai.com/v1/models" \
  -H "Authorization: Bearer $OPENAI_API_KEY"
```

### Rate Limits Hit
- OpenAI: 3,500 RPM (free tier)
- Twitter: 450 requests/15 min
- Reddit: 60 requests/minute
- Solution: Implement exponential backoff

### Token Expiration
- LinkedIn, Instagram, TikTok tokens expire
- Implement automatic refresh mechanism
- Monitor token age in logs

### Permission Denied
- Check app permissions in platform settings
- Regenerate tokens
- Verify OAuth scopes

---

## Security Best Practices

1. **Never commit API keys** to git
2. **Use environment variables** for keys
3. **Use .gitignore** to exclude .env files
4. **Rotate keys regularly** (monthly)
5. **Create separate apps** for dev/prod
6. **Monitor API usage** for suspicious activity
7. **Use API key restrictions** (IP whitelist if available)
8. **Store keys securely** (use password manager)

---

## Next Steps

1. Get OpenAI and Twitter API keys (required)
2. Test bot with just those two APIs
3. Add Mailchimp for email growth
4. Add other platforms gradually
5. Monitor costs and adjust usage
6. Set up automated key rotation

**See BOT-SETUP-GUIDE.md for detailed setup instructions.**
