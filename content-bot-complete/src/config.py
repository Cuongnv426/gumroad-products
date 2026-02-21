"""
Content Bot Configuration
Production-ready settings for all platforms and APIs
"""

import os
from dotenv import load_dotenv

load_dotenv()

# ==================== API KEYS ====================
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
TWITTER_API_KEY = os.getenv("TWITTER_API_KEY", "")
TWITTER_API_SECRET = os.getenv("TWITTER_API_SECRET", "")
TWITTER_ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN", "")
TWITTER_ACCESS_TOKEN_SECRET = os.getenv("TWITTER_ACCESS_TOKEN_SECRET", "")
TWITTER_BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN", "")

TIKTOK_ACCESS_TOKEN = os.getenv("TIKTOK_ACCESS_TOKEN", "")
INSTAGRAM_ACCESS_TOKEN = os.getenv("INSTAGRAM_ACCESS_TOKEN", "")
LINKEDIN_ACCESS_TOKEN = os.getenv("LINKEDIN_ACCESS_TOKEN", "")
REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID", "")
REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET", "")
REDDIT_USERNAME = os.getenv("REDDIT_USERNAME", "")
REDDIT_PASSWORD = os.getenv("REDDIT_PASSWORD", "")

MAILCHIMP_API_KEY = os.getenv("MAILCHIMP_API_KEY", "")
MAILCHIMP_LIST_ID = os.getenv("MAILCHIMP_LIST_ID", "")
SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY", "")

MEDIUM_TOKEN = os.getenv("MEDIUM_TOKEN", "")

# ==================== CONTENT SETTINGS ====================
NICHES = {
    "AI_TOOLS": {
        "keywords": ["AI tools", "ChatGPT", "automation", "machine learning"],
        "tone": "informative, helpful",
        "hashtags": ["#AI", "#ChatGPT", "#AITools", "#Automation"]
    },
    "PRODUCTIVITY": {
        "keywords": ["productivity", "efficiency", "time management", "workflows"],
        "tone": "motivational, practical",
        "hashtags": ["#Productivity", "#LifeHacks", "#TimeManagement"]
    },
    "BUSINESS": {
        "keywords": ["business tips", "entrepreneurship", "startups", "growth"],
        "tone": "professional, insightful",
        "hashtags": ["#Business", "#Entrepreneurship", "#Growth"]
    },
    "TECH": {
        "keywords": ["technology", "software", "development", "coding"],
        "tone": "technical, informative",
        "hashtags": ["#Tech", "#Programming", "#Development"]
    },
}

POSTS_PER_DAY = 10
MIN_POSTS_PER_DAY = 5
MAX_POSTS_PER_DAY = 20

# ==================== CONTENT GENERATION ====================
GPT_MODEL = "gpt-3.5-turbo"
MAX_TOKENS = 500
TEMPERATURE = 0.7

# ==================== POSTING SCHEDULE ====================
POSTING_SCHEDULE = {
    "twitter": {
        "enabled": True,
        "times": ["08:00", "12:00", "15:00", "18:00", "21:00"],
        "char_limit": 280,
    },
    "tiktok": {
        "enabled": True,
        "times": ["10:00", "13:00", "19:00"],
        "char_limit": 2200,
    },
    "instagram": {
        "enabled": True,
        "times": ["09:00", "14:00", "20:00"],
        "char_limit": 2200,
    },
    "linkedin": {
        "enabled": True,
        "times": ["08:30", "12:30", "17:30"],
        "char_limit": 3000,
    },
    "reddit": {
        "enabled": True,
        "times": ["11:00", "16:00", "22:00"],
        "char_limit": 40000,
    },
    "medium": {
        "enabled": True,
        "times": ["09:00", "17:00"],
        "char_limit": 40000,
    },
    "email": {
        "enabled": True,
        "times": ["07:00", "14:00", "19:00"],
        "char_limit": 5000,
    }
}

# ==================== AFFILIATE LINKS ====================
AFFILIATE_LINKS = {
    "chatgpt": "https://openai.com?ref=contentbot",
    "midjourney": "https://www.midjourney.com?ref=contentbot",
    "copy_ai": "https://www.copy.ai?ref=contentbot",
    "grammarly": "https://www.grammarly.com?ref=contentbot",
    "notion": "https://www.notion.so?ref=contentbot",
    "zapier": "https://zapier.com?ref=contentbot",
    "buffer": "https://buffer.com?ref=contentbot",
    "canva": "https://www.canva.com?ref=contentbot",
    "namecheap": "https://www.namecheap.com?ref=contentbot",
    "bluehost": "https://www.bluehost.com?ref=contentbot",
    "kinsta": "https://kinsta.com?ref=contentbot",
    "elementor": "https://elementor.com?ref=contentbot",
    "convertkit": "https://convertkit.com?ref=contentbot",
    "flodesk": "https://flodesk.com?ref=contentbot",
    "airtable": "https://airtable.com?ref=contentbot",
}

AFFILIATE_COMMISSION_RATES = {
    "chatgpt": 0.15,
    "midjourney": 0.20,
    "copy_ai": 0.25,
    "grammarly": 0.30,
    "notion": 0.20,
    "zapier": 0.25,
    "buffer": 0.15,
    "canva": 0.10,
    "namecheap": 0.15,
    "bluehost": 0.40,
    "kinsta": 0.25,
    "elementor": 0.20,
    "convertkit": 0.15,
    "flodesk": 0.20,
    "airtable": 0.15,
}

# ==================== EMAIL SETTINGS ====================
EMAIL_FROM = os.getenv("EMAIL_FROM", "noreply@contentbot.com")
EMAIL_FROM_NAME = "Content Bot"
EMAIL_TEMPLATE_ID = os.getenv("EMAIL_TEMPLATE_ID", "default")

# ==================== DATABASE ====================
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///content_bot.db")
LOG_DIR = "./logs"
DATA_DIR = "./data"

# ==================== RETRY SETTINGS ====================
MAX_RETRIES = 3
RETRY_DELAY = 5  # seconds

# ==================== ANALYTICS ====================
TRACK_ANALYTICS = True
ENABLE_DASHBOARD = True
DASHBOARD_PORT = 8080

# ==================== SAFETY CHECKS ====================
RATE_LIMIT_CHECKS = True
CONTENT_MODERATION = True
DUPLICATE_CHECK = True

print("[CONFIG] Settings loaded successfully")
