"""
Content Bot Configuration
All API keys, credentials, and settings in one place
"""

import os
import json
from typing import Dict, List

class Config:
    """Main configuration class"""
    
    # ==================== API KEYS ====================
    # Load from environment variables or config file
    
    # OpenAI / AI Content Generation
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "your-openai-key-here")
    
    # Social Media APIs
    TWITTER_API_KEY = os.getenv("TWITTER_API_KEY", "")
    TWITTER_API_SECRET = os.getenv("TWITTER_API_SECRET", "")
    TWITTER_ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN", "")
    TWITTER_ACCESS_TOKEN_SECRET = os.getenv("TWITTER_ACCESS_TOKEN_SECRET", "")
    
    INSTAGRAM_ACCESS_TOKEN = os.getenv("INSTAGRAM_ACCESS_TOKEN", "")
    INSTAGRAM_BUSINESS_ACCOUNT_ID = os.getenv("INSTAGRAM_BUSINESS_ACCOUNT_ID", "")
    
    TIKTOK_ACCESS_TOKEN = os.getenv("TIKTOK_ACCESS_TOKEN", "")
    TIKTOK_REFRESH_TOKEN = os.getenv("TIKTOK_REFRESH_TOKEN", "")
    TIKTOK_VIDEO_UPLOAD_URL = "https://open-api.tiktok.com/v1/video/upload/"
    
    LINKEDIN_ACCESS_TOKEN = os.getenv("LINKEDIN_ACCESS_TOKEN", "")
    LINKEDIN_PERSON_URN = os.getenv("LINKEDIN_PERSON_URN", "")
    
    REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID", "")
    REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET", "")
    REDDIT_USERNAME = os.getenv("REDDIT_USERNAME", "")
    REDDIT_PASSWORD = os.getenv("REDDIT_PASSWORD", "")
    
    MEDIUM_API_TOKEN = os.getenv("MEDIUM_API_TOKEN", "")
    
    # Email / Mailchimp
    MAILCHIMP_API_KEY = os.getenv("MAILCHIMP_API_KEY", "")
    MAILCHIMP_LIST_ID = os.getenv("MAILCHIMP_LIST_ID", "")
    MAILCHIMP_SERVER = os.getenv("MAILCHIMP_SERVER", "us1")  # e.g., us1, us2, etc
    
    # Analytics
    GOOGLE_ANALYTICS_KEY = os.getenv("GOOGLE_ANALYTICS_KEY", "")
    
    # ==================== CONTENT SETTINGS ====================
    
    # Niche and keywords
    NICHE = "AI Tools & Productivity"
    
    CONTENT_KEYWORDS = [
        "AI tools", "ChatGPT", "Claude", "automation", "productivity",
        "workflow", "Midjourney", "image generation", "video generation",
        "HeyGen", "Synthesia", "Zapier", "Make", "Notion", "Airtable",
        "Grammarly", "writing tools", "copy.ai", "content creation",
        "time management", "efficiency", "AI productivity hacks"
    ]
    
    # Content generation settings
    CONTENT_STYLES = ["educational", "entertaining", "inspirational", "news"]
    CONTENT_TYPES = ["tips", "comparisons", "tutorials", "news", "reviews"]
    
    TIKTOK_SCRIPT_LENGTH = (30, 60)  # seconds
    TWITTER_CHAR_LIMIT = 280
    BLOG_POST_LENGTH = (2000, 3000)  # words
    
    # ==================== POSTING SCHEDULE ====================
    
    POSTING_SCHEDULE = {
        "tiktok": {
            "enabled": True,
            "times": ["08:00", "18:00"],  # 2x/day
            "content_per_day": 2
        },
        "instagram": {
            "enabled": True,
            "times": ["09:00", "18:00"],  # Mirror TikTok
            "content_per_day": 2
        },
        "twitter": {
            "enabled": True,
            "times": ["09:00", "12:00", "15:00", "18:00", "21:00"],  # 5x/day
            "content_per_day": 5
        },
        "linkedin": {
            "enabled": True,
            "times": ["07:00", "16:00"],  # 2x/day
            "content_per_day": 2
        },
        "reddit": {
            "enabled": True,
            "times": ["10:00", "19:00"],  # 2x/day
            "content_per_day": 2,
            "subreddits": ["ChatGPT", "productivity", "automation", "AITools"]
        },
        "medium": {
            "enabled": True,
            "days": [2, 6],  # Wednesday (2), Sunday (6)
            "content_per_week": 2
        },
        "email": {
            "enabled": True,
            "days": [1, 3, 5],  # Tuesday, Thursday, Saturday
            "time": "10:00",
            "content_per_week": 3
        }
    }
    
    # ==================== AFFILIATE LINKS ====================
    
    AFFILIATE_LINKS = {
        "chatgpt_plus": {
            "url": "https://openai.com/plus",
            "display_name": "ChatGPT Plus",
            "category": "llm"
        },
        "claude_api": {
            "url": "https://claude.ai",
            "display_name": "Claude API",
            "category": "llm"
        },
        "gemini_pro": {
            "url": "https://gemini.google.com",
            "display_name": "Google Gemini Pro",
            "category": "llm"
        },
        "midjourney": {
            "url": "https://midjourney.com",
            "display_name": "Midjourney",
            "category": "image_generation"
        },
        "leonardo_ai": {
            "url": "https://leonardo.ai",
            "display_name": "Leonardo.AI",
            "category": "image_generation"
        },
        "synthesia": {
            "url": "https://synthesia.io",
            "display_name": "Synthesia",
            "category": "video_generation"
        },
        "heygen": {
            "url": "https://www.heygen.com",
            "display_name": "HeyGen",
            "category": "video_generation"
        },
        "zapier": {
            "url": "https://zapier.com",
            "display_name": "Zapier",
            "category": "automation"
        },
        "make": {
            "url": "https://make.com",
            "display_name": "Make (formerly Integromat)",
            "category": "automation"
        },
        "notion": {
            "url": "https://notion.so",
            "display_name": "Notion",
            "category": "productivity"
        },
        "airtable": {
            "url": "https://airtable.com",
            "display_name": "Airtable",
            "category": "productivity"
        },
        "copysmith": {
            "url": "https://copysmith.ai",
            "display_name": "Copysmith",
            "category": "copywriting"
        },
        "copy_ai": {
            "url": "https://copy.ai",
            "display_name": "Copy.ai",
            "category": "copywriting"
        },
        "grammarly": {
            "url": "https://grammarly.com",
            "display_name": "Grammarly",
            "category": "writing"
        }
    }
    
    # ==================== DATABASE & LOGGING ====================
    
    DB_PATH = "/root/clawd/content-bot/data/"
    LOG_PATH = "/root/clawd/content-bot/logs/"
    DATA_PATH = "/root/clawd/content-bot/data/"
    
    LOG_LEVEL = "INFO"
    LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # ==================== REVENUE TRACKING ====================
    
    # Affiliate tracking settings
    TRACKING_ENABLED = True
    CLICK_TRACKING_TTL_DAYS = 30  # Track clicks for 30 days
    
    # Revenue multipliers (estimated per action)
    REVENUE_MULTIPLIERS = {
        "affiliate_click": 0.50,  # $0.50 per click
        "affiliate_conversion": 25.00,  # $25 per conversion
        "email_signup": 1.00,  # $1 per email signup
        "blog_view": 0.01,  # $0.01 per blog view
        "adsense_rpm": 5.00,  # $5 per 1000 views
    }
    
    # ==================== FEATURE FLAGS ====================
    
    DRY_RUN = os.getenv("DRY_RUN", "false").lower() == "true"
    GENERATE_ONLY = False  # Only generate content, don't post
    POST_ONLY = False  # Only post existing content
    VERBOSE = True
    DEBUG_MODE = os.getenv("DEBUG_MODE", "false").lower() == "true"
    
    # ==================== TIMING ====================
    
    TIMEZONE = "UTC"
    CHECK_INTERVAL_MINUTES = 5  # Check scheduler every 5 minutes
    RETRY_ATTEMPTS = 3
    RETRY_DELAY_SECONDS = 5

# Load additional config from JSON if exists
def load_config_from_file(path: str = None) -> Dict:
    """Load configuration from JSON file"""
    if path is None:
        path = "/root/clawd/content-bot/config.json"
    
    if os.path.exists(path):
        with open(path, 'r') as f:
            return json.load(f)
    return {}

# Merge loaded config
_file_config = load_config_from_file()
for key, value in _file_config.items():
    if hasattr(Config, key.upper()):
        setattr(Config, key.upper(), value)

if __name__ == "__main__":
    print("Content Bot Configuration Loaded")
    print(f"Niche: {Config.NICHE}")
    print(f"Platforms: {list(Config.POSTING_SCHEDULE.keys())}")
    print(f"Affiliate Links: {len(Config.AFFILIATE_LINKS)}")
