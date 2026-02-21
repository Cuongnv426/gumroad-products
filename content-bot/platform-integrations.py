"""
Platform Integrations - Post to all social media platforms
Handles TikTok, Instagram, Twitter, LinkedIn, Reddit, Medium, and Email
"""

import json
import logging
from typing import Dict, Optional, List
from datetime import datetime
from abc import ABC, abstractmethod

from config import Config

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=getattr(logging, Config.LOG_LEVEL),
    format=Config.LOG_FORMAT
)

# ==================== BASE PLATFORM CLASS ====================

class PlatformBase(ABC):
    """Abstract base class for all platforms"""
    
    def __init__(self, platform_name: str):
        self.platform_name = platform_name
        self.last_error = None
        self.last_success = None
    
    @abstractmethod
    def post(self, content: Dict) -> Dict:
        """Post content to platform"""
        pass
    
    @abstractmethod
    def authenticate(self) -> bool:
        """Authenticate with platform"""
        pass
    
    def log_success(self, post_id: str):
        """Log successful post"""
        self.last_success = datetime.now()
        logger.info(f"{self.platform_name} - Posted successfully: {post_id}")
    
    def log_error(self, error: str):
        """Log error"""
        self.last_error = error
        logger.error(f"{self.platform_name} - Error: {error}")

# ==================== TWITTER ====================

class TwitterIntegration(PlatformBase):
    """Twitter API Integration"""
    
    def __init__(self):
        super().__init__("Twitter")
        self.authenticated = False
        self.authenticate()
    
    def authenticate(self) -> bool:
        """Authenticate with Twitter API v2"""
        try:
            import tweepy
            
            if not all([Config.TWITTER_API_KEY, Config.TWITTER_API_SECRET]):
                logger.warning("Twitter credentials not configured")
                return False
            
            # Note: This is simplified. Implement full OAuth2 flow in production
            self.client = tweepy.Client(
                consumer_key=Config.TWITTER_API_KEY,
                consumer_secret=Config.TWITTER_API_SECRET,
                access_token=Config.TWITTER_ACCESS_TOKEN,
                access_token_secret=Config.TWITTER_ACCESS_TOKEN_SECRET,
                wait_on_rate_limit=True
            )
            
            self.authenticated = True
            logger.info("Twitter authenticated successfully")
            return True
        
        except ImportError:
            logger.error("tweepy not installed")
            return False
        except Exception as e:
            self.log_error(str(e))
            return False
    
    def post(self, content: Dict) -> Dict:
        """Post tweet"""
        if not self.authenticated:
            return {"success": False, "error": "Not authenticated", "mock": True}
        
        try:
            if Config.DRY_RUN:
                logger.info(f"[DRY RUN] Would post to Twitter: {content.get('content', '')[:100]}")
                return {
                    "success": True,
                    "platform": "twitter",
                    "post_id": "mock_" + str(datetime.now().timestamp()),
                    "dry_run": True
                }
            
            # Post tweet
            response = self.client.create_tweet(
                text=content.get("content", ""),
                reply_settings="everyone"
            )
            
            self.log_success(response.data["id"])
            
            return {
                "success": True,
                "platform": "twitter",
                "post_id": response.data["id"],
                "url": f"https://twitter.com/user/status/{response.data['id']}"
            }
        
        except Exception as e:
            self.log_error(str(e))
            return {"success": False, "error": str(e), "platform": "twitter"}

# ==================== TIKTOK ====================

class TikTokIntegration(PlatformBase):
    """TikTok API Integration"""
    
    def __init__(self):
        super().__init__("TikTok")
        self.authenticated = False
        self.authenticate()
    
    def authenticate(self) -> bool:
        """Authenticate with TikTok API"""
        try:
            if not Config.TIKTOK_ACCESS_TOKEN:
                logger.warning("TikTok credentials not configured")
                return False
            
            self.access_token = Config.TIKTOK_ACCESS_TOKEN
            self.authenticated = True
            logger.info("TikTok authenticated successfully")
            return True
        
        except Exception as e:
            self.log_error(str(e))
            return False
    
    def post(self, content: Dict) -> Dict:
        """Post to TikTok (requires video file)"""
        if not self.authenticated:
            return {"success": False, "error": "Not authenticated", "mock": True}
        
        try:
            if Config.DRY_RUN:
                logger.info(f"[DRY RUN] Would post to TikTok: {content.get('hook', '')[:100]}")
                return {
                    "success": True,
                    "platform": "tiktok",
                    "post_id": "mock_tiktok_" + str(datetime.now().timestamp()),
                    "dry_run": True
                }
            
            import requests
            
            # In production, would upload video file first
            video_path = content.get("video_path")
            if not video_path:
                return {"success": False, "error": "No video file provided"}
            
            headers = {
                "Authorization": f"Bearer {self.access_token}",
                "Content-Type": "video/mp4"
            }
            
            with open(video_path, 'rb') as f:
                response = requests.post(
                    Config.TIKTOK_VIDEO_UPLOAD_URL,
                    headers=headers,
                    data=f
                )
            
            if response.status_code == 200:
                result = response.json()
                self.log_success(result.get("data", {}).get("video_id"))
                return {
                    "success": True,
                    "platform": "tiktok",
                    "post_id": result.get("data", {}).get("video_id")
                }
            else:
                error = response.json().get("error_description")
                self.log_error(error)
                return {"success": False, "error": error}
        
        except Exception as e:
            self.log_error(str(e))
            return {"success": False, "error": str(e), "platform": "tiktok"}

# ==================== INSTAGRAM ====================

class InstagramIntegration(PlatformBase):
    """Instagram API Integration"""
    
    def __init__(self):
        super().__init__("Instagram")
        self.authenticated = False
        self.authenticate()
    
    def authenticate(self) -> bool:
        """Authenticate with Instagram Graph API"""
        try:
            if not Config.INSTAGRAM_ACCESS_TOKEN:
                logger.warning("Instagram credentials not configured")
                return False
            
            self.access_token = Config.INSTAGRAM_ACCESS_TOKEN
            self.business_account_id = Config.INSTAGRAM_BUSINESS_ACCOUNT_ID
            self.authenticated = True
            logger.info("Instagram authenticated successfully")
            return True
        
        except Exception as e:
            self.log_error(str(e))
            return False
    
    def post(self, content: Dict) -> Dict:
        """Post to Instagram"""
        if not self.authenticated:
            return {"success": False, "error": "Not authenticated", "mock": True}
        
        try:
            if Config.DRY_RUN:
                logger.info(f"[DRY RUN] Would post to Instagram")
                return {
                    "success": True,
                    "platform": "instagram",
                    "post_id": "mock_ig_" + str(datetime.now().timestamp()),
                    "dry_run": True
                }
            
            import requests
            
            # For Reels
            if content.get("type") == "reel" or content.get("platform") == "tiktok":
                url = f"https://graph.instagram.com/v18.0/{self.business_account_id}/media"
                
                payload = {
                    "media_type": "REELS",
                    "video_url": content.get("video_url"),
                    "caption": content.get("caption", ""),
                    "access_token": self.access_token
                }
            else:
                # For carousel or image posts
                url = f"https://graph.instagram.com/v18.0/{self.business_account_id}/media"
                payload = {
                    "media_type": "IMAGE",
                    "image_url": content.get("image_url"),
                    "caption": content.get("caption", ""),
                    "access_token": self.access_token
                }
            
            response = requests.post(url, json=payload)
            
            if response.status_code == 200:
                result = response.json()
                media_id = result.get("id")
                
                # Publish the media
                publish_url = f"https://graph.instagram.com/v18.0/{self.business_account_id}/media_publish"
                publish_response = requests.post(
                    publish_url,
                    json={"creation_id": media_id, "access_token": self.access_token}
                )
                
                if publish_response.status_code == 200:
                    self.log_success(media_id)
                    return {
                        "success": True,
                        "platform": "instagram",
                        "post_id": media_id
                    }
            
            error = response.json().get("error", {}).get("message", "Unknown error")
            self.log_error(error)
            return {"success": False, "error": error}
        
        except Exception as e:
            self.log_error(str(e))
            return {"success": False, "error": str(e), "platform": "instagram"}

# ==================== LINKEDIN ====================

class LinkedInIntegration(PlatformBase):
    """LinkedIn API Integration"""
    
    def __init__(self):
        super().__init__("LinkedIn")
        self.authenticated = False
        self.authenticate()
    
    def authenticate(self) -> bool:
        """Authenticate with LinkedIn API"""
        try:
            if not Config.LINKEDIN_ACCESS_TOKEN:
                logger.warning("LinkedIn credentials not configured")
                return False
            
            self.access_token = Config.LINKEDIN_ACCESS_TOKEN
            self.person_urn = Config.LINKEDIN_PERSON_URN
            self.authenticated = True
            logger.info("LinkedIn authenticated successfully")
            return True
        
        except Exception as e:
            self.log_error(str(e))
            return False
    
    def post(self, content: Dict) -> Dict:
        """Post to LinkedIn"""
        if not self.authenticated:
            return {"success": False, "error": "Not authenticated", "mock": True}
        
        try:
            if Config.DRY_RUN:
                logger.info(f"[DRY RUN] Would post to LinkedIn: {content.get('content', '')[:100]}")
                return {
                    "success": True,
                    "platform": "linkedin",
                    "post_id": "mock_li_" + str(datetime.now().timestamp()),
                    "dry_run": True
                }
            
            import requests
            
            url = "https://api.linkedin.com/v2/ugcPosts"
            
            headers = {
                "Authorization": f"Bearer {self.access_token}",
                "Content-Type": "application/json",
                "X-Restli-Protocol-Version": "2.0.0"
            }
            
            payload = {
                "author": self.person_urn,
                "lifecycleState": "PUBLISHED",
                "specificContent": {
                    "com.linkedin.ugc.UGCPost": {
                        "content": {
                            "com.linkedin.ugc.UGCPost": {
                                "media": []
                            }
                        }
                    }
                },
                "visibility": {
                    "com.linkedin.ugc.UGCPost": {
                        "visibility": "PUBLIC"
                    }
                }
            }
            
            # Add text content
            payload["specificContent"]["com.linkedin.ugc.UGCPost"]["content"]["com.linkedin.ugc.UGCPost"]["shareCommentary"] = {
                "text": content.get("content", "")
            }
            
            response = requests.post(url, json=payload, headers=headers)
            
            if response.status_code == 201:
                post_id = response.headers.get("X-Restli-Id")
                self.log_success(post_id)
                return {
                    "success": True,
                    "platform": "linkedin",
                    "post_id": post_id
                }
            
            error = response.json().get("message", "Unknown error")
            self.log_error(error)
            return {"success": False, "error": error}
        
        except Exception as e:
            self.log_error(str(e))
            return {"success": False, "error": str(e), "platform": "linkedin"}

# ==================== REDDIT ====================

class RedditIntegration(PlatformBase):
    """Reddit API Integration"""
    
    def __init__(self):
        super().__init__("Reddit")
        self.authenticated = False
        self.authenticate()
    
    def authenticate(self) -> bool:
        """Authenticate with Reddit API"""
        try:
            import praw
            
            if not all([Config.REDDIT_CLIENT_ID, Config.REDDIT_CLIENT_SECRET]):
                logger.warning("Reddit credentials not configured")
                return False
            
            self.reddit = praw.Reddit(
                client_id=Config.REDDIT_CLIENT_ID,
                client_secret=Config.REDDIT_CLIENT_SECRET,
                user_agent="ContentBot/1.0 by " + Config.REDDIT_USERNAME,
                username=Config.REDDIT_USERNAME,
                password=Config.REDDIT_PASSWORD
            )
            
            self.authenticated = True
            logger.info("Reddit authenticated successfully")
            return True
        
        except ImportError:
            logger.error("praw not installed")
            return False
        except Exception as e:
            self.log_error(str(e))
            return False
    
    def post(self, content: Dict) -> Dict:
        """Post to Reddit"""
        if not self.authenticated:
            return {"success": False, "error": "Not authenticated", "mock": True}
        
        try:
            if Config.DRY_RUN:
                logger.info(f"[DRY RUN] Would post to Reddit in r/{content.get('subreddit')}")
                return {
                    "success": True,
                    "platform": "reddit",
                    "post_id": "mock_reddit_" + str(datetime.now().timestamp()),
                    "dry_run": True
                }
            
            subreddit_name = content.get("subreddit", "ChatGPT")
            title = content.get("title", "")
            body = content.get("body", "")
            
            subreddit = self.reddit.subreddit(subreddit_name)
            submission = subreddit.submit(title=title, selftext=body)
            
            self.log_success(submission.id)
            
            return {
                "success": True,
                "platform": "reddit",
                "post_id": submission.id,
                "url": submission.url
            }
        
        except Exception as e:
            self.log_error(str(e))
            return {"success": False, "error": str(e), "platform": "reddit"}

# ==================== MEDIUM ====================

class MediumIntegration(PlatformBase):
    """Medium API Integration"""
    
    def __init__(self):
        super().__init__("Medium")
        self.authenticated = False
        self.authenticate()
    
    def authenticate(self) -> bool:
        """Authenticate with Medium API"""
        try:
            if not Config.MEDIUM_API_TOKEN:
                logger.warning("Medium credentials not configured")
                return False
            
            self.api_token = Config.MEDIUM_API_TOKEN
            self.authenticated = True
            logger.info("Medium authenticated successfully")
            return True
        
        except Exception as e:
            self.log_error(str(e))
            return False
    
    def post(self, content: Dict) -> Dict:
        """Post to Medium"""
        if not self.authenticated:
            return {"success": False, "error": "Not authenticated", "mock": True}
        
        try:
            if Config.DRY_RUN:
                logger.info(f"[DRY RUN] Would post to Medium: {content.get('title')}")
                return {
                    "success": True,
                    "platform": "medium",
                    "post_id": "mock_medium_" + str(datetime.now().timestamp()),
                    "dry_run": True
                }
            
            import requests
            
            # Get user profile first
            user_url = "https://api.medium.com/v1/me"
            headers = {"Authorization": f"Bearer {self.api_token}"}
            
            user_response = requests.get(user_url, headers=headers)
            if user_response.status_code != 200:
                raise Exception("Failed to authenticate with Medium")
            
            user_id = user_response.json().get("data", {}).get("id")
            
            # Create publication
            pub_url = f"https://api.medium.com/v1/users/{user_id}/posts"
            
            payload = {
                "title": content.get("title", ""),
                "contentFormat": "html",
                "content": content.get("body", ""),
                "publishStatus": "public",
                "tags": content.get("tags", [])[:5]
            }
            
            response = requests.post(pub_url, json=payload, headers=headers)
            
            if response.status_code == 201:
                post_id = response.json().get("data", {}).get("id")
                self.log_success(post_id)
                return {
                    "success": True,
                    "platform": "medium",
                    "post_id": post_id,
                    "url": response.json().get("data", {}).get("url")
                }
            
            error = response.json().get("errors", [{}])[0].get("message", "Unknown error")
            self.log_error(error)
            return {"success": False, "error": error}
        
        except Exception as e:
            self.log_error(str(e))
            return {"success": False, "error": str(e), "platform": "medium"}

# ==================== EMAIL / MAILCHIMP ====================

class EmailIntegration(PlatformBase):
    """Mailchimp Email Integration"""
    
    def __init__(self):
        super().__init__("Email")
        self.authenticated = False
        self.authenticate()
    
    def authenticate(self) -> bool:
        """Authenticate with Mailchimp API"""
        try:
            import mailchimp_marketing as MailchimpMarketing
            
            if not all([Config.MAILCHIMP_API_KEY, Config.MAILCHIMP_LIST_ID]):
                logger.warning("Mailchimp credentials not configured")
                return False
            
            self.client = MailchimpMarketing.Client()
            self.client.set_config({
                "api_key": Config.MAILCHIMP_API_KEY,
                "server": Config.MAILCHIMP_SERVER
            })
            
            self.authenticated = True
            logger.info("Mailchimp authenticated successfully")
            return True
        
        except ImportError:
            logger.error("mailchimp-marketing not installed")
            return False
        except Exception as e:
            self.log_error(str(e))
            return False
    
    def post(self, content: Dict) -> Dict:
        """Send email campaign"""
        if not self.authenticated:
            return {"success": False, "error": "Not authenticated", "mock": True}
        
        try:
            if Config.DRY_RUN:
                logger.info(f"[DRY RUN] Would send email: {content.get('subject_line')}")
                return {
                    "success": True,
                    "platform": "email",
                    "campaign_id": "mock_email_" + str(datetime.now().timestamp()),
                    "dry_run": True
                }
            
            # Create campaign
            campaign_data = {
                "type": "regular",
                "recipients": {
                    "list_id": Config.MAILCHIMP_LIST_ID
                },
                "settings": {
                    "subject_line": content.get("subject_line", ""),
                    "preview_text": content.get("preheader_text", ""),
                    "title": content.get("title", "Newsletter")
                }
            }
            
            campaign = self.client.campaigns.post(campaign_data)
            campaign_id = campaign.get("id")
            
            # Set email content
            content_data = {
                "html": self._build_html(content),
                "text": content.get("body", "")
            }
            
            self.client.campaigns.set_content(campaign_id, content_data)
            
            # Schedule the campaign
            schedule_data = {
                "schedule_time": content.get("send_time", "2024-01-01T12:00:00")
            }
            
            self.client.campaigns.schedule(campaign_id, schedule_data)
            
            self.log_success(campaign_id)
            
            return {
                "success": True,
                "platform": "email",
                "campaign_id": campaign_id
            }
        
        except Exception as e:
            self.log_error(str(e))
            return {"success": False, "error": str(e), "platform": "email"}
    
    def _build_html(self, content: Dict) -> str:
        """Build HTML email template"""
        html = f"""
        <html>
            <body>
                <h1>{content.get('greeting', 'Hello!')}</h1>
                <p>{content.get('body', '')}</p>
                <p><a href="{content.get('cta_primary_url', '#')}">{content.get('cta_primary', 'Learn More')}</a></p>
                <hr>
                <footer>{content.get('footer', 'Content Bot Newsletter')}</footer>
            </body>
        </html>
        """
        return html

# ==================== PLATFORM MANAGER ====================

class PlatformManager:
    """Manage all platform integrations"""
    
    def __init__(self):
        self.platforms = {
            "twitter": TwitterIntegration(),
            "tiktok": TikTokIntegration(),
            "instagram": InstagramIntegration(),
            "linkedin": LinkedInIntegration(),
            "reddit": RedditIntegration(),
            "medium": MediumIntegration(),
            "email": EmailIntegration()
        }
        
        self.posting_history = []
    
    def post_to_platform(self, platform: str, content: Dict) -> Dict:
        """Post to specific platform"""
        if platform not in self.platforms:
            return {"success": False, "error": f"Unknown platform: {platform}"}
        
        result = self.platforms[platform].post(content)
        
        # Log to history
        self.posting_history.append({
            "platform": platform,
            "timestamp": datetime.now().isoformat(),
            "success": result.get("success"),
            "post_id": result.get("post_id"),
            "error": result.get("error")
        })
        
        return result
    
    def post_to_all(self, content_map: Dict[str, Dict]) -> Dict[str, Dict]:
        """Post to multiple platforms at once"""
        results = {}
        
        for platform, content in content_map.items():
            results[platform] = self.post_to_platform(platform, content)
        
        return results
    
    def get_status(self) -> Dict:
        """Get status of all platforms"""
        return {
            platform: {
                "authenticated": p.authenticated,
                "last_error": p.last_error,
                "last_success": p.last_success
            }
            for platform, p in self.platforms.items()
        }


def quick_test():
    """Test platform integrations"""
    manager = PlatformManager()
    
    print("Platform Integration Status:")
    for platform, status in manager.get_status().items():
        auth = "✓" if status["authenticated"] else "✗"
        print(f"{auth} {platform}")


if __name__ == "__main__":
    quick_test()
