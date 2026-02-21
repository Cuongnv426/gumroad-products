"""
Multi-Platform Posting Manager
Handles posting to Twitter, Instagram, LinkedIn, TikTok, Reddit, Medium, Email
"""

import tweepy
import requests
import praw
import logging
from datetime import datetime
from typing import Dict, List, Optional
from config import (
    TWITTER_API_KEY, TWITTER_API_SECRET, TWITTER_ACCESS_TOKEN, 
    TWITTER_ACCESS_TOKEN_SECRET, TWITTER_BEARER_TOKEN,
    TIKTOK_ACCESS_TOKEN, INSTAGRAM_ACCESS_TOKEN, LINKEDIN_ACCESS_TOKEN,
    REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, REDDIT_USERNAME, REDDIT_PASSWORD,
    MAILCHIMP_API_KEY, SENDGRID_API_KEY, MEDIUM_TOKEN, MAX_RETRIES, RETRY_DELAY
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

import time


class PlatformManager:
    """Unified interface for posting to multiple platforms"""
    
    def __init__(self):
        self.post_history = []
        self._init_twitter()
        self._init_reddit()
        
    def _init_twitter(self):
        """Initialize Twitter/X API client"""
        try:
            auth = tweepy.OAuthHandler(TWITTER_API_KEY, TWITTER_API_SECRET)
            auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)
            self.twitter_api = tweepy.API(auth)
            self.twitter_client = tweepy.Client(
                bearer_token=TWITTER_BEARER_TOKEN,
                consumer_key=TWITTER_API_KEY,
                consumer_secret=TWITTER_API_SECRET,
                access_token=TWITTER_ACCESS_TOKEN,
                access_token_secret=TWITTER_ACCESS_TOKEN_SECRET
            )
            logger.info("✓ Twitter API initialized")
        except Exception as e:
            logger.warning(f"Twitter API init failed: {e}")
            self.twitter_api = None
            self.twitter_client = None
    
    def _init_reddit(self):
        """Initialize Reddit API client"""
        try:
            self.reddit = praw.Reddit(
                client_id=REDDIT_CLIENT_ID,
                client_secret=REDDIT_CLIENT_SECRET,
                user_agent="ContentBot/1.0",
                username=REDDIT_USERNAME,
                password=REDDIT_PASSWORD
            )
            logger.info("✓ Reddit API initialized")
        except Exception as e:
            logger.warning(f"Reddit API init failed: {e}")
            self.reddit = None
    
    def post_to_platform(self, content: Dict, platform: str, retry: int = 0) -> Dict:
        """
        Post content to specified platform
        
        Args:
            content: Content dict with 'content' key
            platform: twitter, instagram, linkedin, tiktok, reddit, medium, email
            retry: Current retry attempt
            
        Returns:
            Result dict with success/error status
        """
        
        result = {
            "platform": platform,
            "content_id": content.get("id"),
            "timestamp": datetime.now().isoformat(),
            "success": False
        }
        
        try:
            if platform == "twitter":
                result.update(self.post_twitter(content))
            elif platform == "instagram":
                result.update(self.post_instagram(content))
            elif platform == "linkedin":
                result.update(self.post_linkedin(content))
            elif platform == "tiktok":
                result.update(self.post_tiktok(content))
            elif platform == "reddit":
                result.update(self.post_reddit(content))
            elif platform == "medium":
                result.update(self.post_medium(content))
            elif platform == "email":
                result.update(self.post_email(content))
            else:
                result["error"] = f"Unknown platform: {platform}"
            
            self.post_history.append(result)
            return result
            
        except Exception as e:
            logger.error(f"Error posting to {platform}: {str(e)}")
            
            # Retry logic
            if retry < MAX_RETRIES:
                logger.info(f"Retrying {platform} (attempt {retry + 1}/{MAX_RETRIES})")
                time.sleep(RETRY_DELAY)
                return self.post_to_platform(content, platform, retry + 1)
            else:
                result["error"] = str(e)
                result["failed_retries"] = MAX_RETRIES
                self.post_history.append(result)
                return result
    
    def post_twitter(self, content: Dict) -> Dict:
        """Post to Twitter"""
        if not self.twitter_client:
            return {"error": "Twitter API not initialized"}
        
        text = content["content"][:280]
        if content.get("hashtags"):
            hashtags = " " + content["hashtags"]
            text = (text + hashtags)[:280]
        
        try:
            response = self.twitter_client.create_tweet(text=text)
            logger.info(f"✓ Posted to Twitter: {response.data['id']}")
            return {
                "success": True,
                "post_id": response.data['id'],
                "url": f"https://twitter.com/i/web/status/{response.data['id']}"
            }
        except Exception as e:
            return {"error": str(e)}
    
    def post_instagram(self, content: Dict) -> Dict:
        """Post to Instagram (requires image - placeholder)"""
        # Instagram API requires image media
        # This is a placeholder for integration
        
        logger.warning("Instagram posting requires image media - feature requires enhancement")
        return {
            "error": "Instagram posting requires image uploads",
            "note": "Can be integrated with image generation"
        }
    
    def post_linkedin(self, content: Dict) -> Dict:
        """Post to LinkedIn"""
        
        if not LINKEDIN_ACCESS_TOKEN:
            return {"error": "LinkedIn token not configured"}
        
        headers = {
            "Authorization": f"Bearer {LINKEDIN_ACCESS_TOKEN}",
            "X-Requested-With": "XMLHttpRequest",
            "Content-Type": "application/json"
        }
        
        data = {
            "content": {
                "contentEntities": [
                    {
                        "entityLocation": "DESCRIPTION",
                        "attributes": []
                    }
                ],
                "title": content["content"][:100]
            },
            "distribution": {
                "feedDistribution": "MAIN_FEED",
                "targetEntities": [],
                "thirdPartyDistributionChannels": []
            },
            "lifecycleState": "PUBLISHED",
            "origin": "FEED",
            "specificContent": {
                "com.linkedin.ugc.UGCPost": {
                    "shareMediaCategory": "ARTICLE",
                    "shareCommentary": {
                        "attributes": [],
                        "text": content["content"]
                    },
                    "media": []
                }
            },
            "visibility": {
                "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
            }
        }
        
        try:
            response = requests.post(
                "https://api.linkedin.com/v2/ugcPosts",
                headers=headers,
                json=data
            )
            
            if response.status_code in [200, 201]:
                logger.info(f"✓ Posted to LinkedIn")
                return {
                    "success": True,
                    "post_id": response.json().get("id"),
                }
            else:
                return {"error": f"LinkedIn API error: {response.text}"}
        except Exception as e:
            return {"error": str(e)}
    
    def post_tiktok(self, content: Dict) -> Dict:
        """Post to TikTok (requires video - placeholder)"""
        
        logger.warning("TikTok posting requires video content - feature requires enhancement")
        return {
            "error": "TikTok posting requires video uploads",
            "note": "Can be integrated with video generation"
        }
    
    def post_reddit(self, content: Dict) -> Dict:
        """Post to Reddit"""
        
        if not self.reddit:
            return {"error": "Reddit API not initialized"}
        
        try:
            # Get first subreddit from config or use default
            subreddit_name = "test"  # Use appropriate subreddit
            
            # Create title from content
            title = content["content"][:300]
            
            # Post to subreddit
            subreddit = self.reddit.subreddit(subreddit_name)
            submission = subreddit.submit(
                title=title,
                selftext=content["content"],
                send_replies=True
            )
            
            logger.info(f"✓ Posted to Reddit: {submission.url}")
            return {
                "success": True,
                "post_id": submission.id,
                "url": submission.url
            }
        except Exception as e:
            return {"error": str(e)}
    
    def post_medium(self, content: Dict) -> Dict:
        """Post to Medium"""
        
        if not MEDIUM_TOKEN:
            return {"error": "Medium token not configured"}
        
        headers = {
            "Authorization": f"Bearer {MEDIUM_TOKEN}",
            "Content-Type": "application/json"
        }
        
        # Get current user's ID first
        try:
            user_response = requests.get(
                "https://api.medium.com/v1/me",
                headers=headers
            )
            
            if user_response.status_code != 200:
                return {"error": "Failed to get Medium user"}
            
            user_id = user_response.json()["data"]["id"]
            
            # Create article
            article_data = {
                "title": content["content"][:100],
                "contentFormat": "html",
                "content": f"<p>{content['content']}</p>",
                "publishStatus": "public"
            }
            
            response = requests.post(
                f"https://api.medium.com/v1/users/{user_id}/posts",
                headers=headers,
                json=article_data
            )
            
            if response.status_code in [200, 201]:
                logger.info(f"✓ Posted to Medium")
                return {
                    "success": True,
                    "post_id": response.json().get("data", {}).get("id")
                }
            else:
                return {"error": f"Medium API error: {response.text}"}
        except Exception as e:
            return {"error": str(e)}
    
    def post_email(self, content: Dict) -> Dict:
        """Send email to list (via Mailchimp or SendGrid)"""
        
        if MAILCHIMP_API_KEY:
            return self._post_mailchimp(content)
        elif SENDGRID_API_KEY:
            return self._post_sendgrid(content)
        else:
            return {"error": "Email API not configured"}
    
    def _post_mailchimp(self, content: Dict) -> Dict:
        """Post via Mailchimp"""
        from config import MAILCHIMP_LIST_ID, EMAIL_FROM, EMAIL_FROM_NAME
        
        if not MAILCHIMP_LIST_ID:
            return {"error": "Mailchimp list ID not configured"}
        
        # Extract Mailchimp API server from key (e.g., "us1")
        server = MAILCHIMP_API_KEY.split('-')[1]
        
        # Split content for email format
        lines = content["content"].split("\n")
        subject = lines[0] if lines else "Check This Out!"
        body = "\n".join(lines[1:]) if len(lines) > 1 else content["content"]
        
        headers = {
            "Authorization": f"apikey {MAILCHIMP_API_KEY}",
            "Content-Type": "application/json"
        }
        
        data = {
            "type": "regular",
            "recipients": {
                "list_id": MAILCHIMP_LIST_ID
            },
            "settings": {
                "subject_line": subject,
                "from_name": EMAIL_FROM_NAME,
                "reply_to": EMAIL_FROM,
                "preview_text": body[:100]
            },
            "content": {
                "html": f"<p>{body.replace(chr(10), '<br>')}</p>"
            }
        }
        
        try:
            response = requests.post(
                f"https://{server}.api.mailchimp.com/3.0/campaigns",
                headers=headers,
                json=data
            )
            
            if response.status_code in [200, 201]:
                campaign_id = response.json().get("id")
                logger.info(f"✓ Email campaign created: {campaign_id}")
                return {
                    "success": True,
                    "campaign_id": campaign_id
                }
            else:
                return {"error": f"Mailchimp error: {response.text}"}
        except Exception as e:
            return {"error": str(e)}
    
    def _post_sendgrid(self, content: Dict) -> Dict:
        """Post via SendGrid"""
        from config import EMAIL_FROM, EMAIL_FROM_NAME
        
        from sendgrid import SendGridAPIClient
        from sendgrid.helpers.mail import Mail
        
        try:
            lines = content["content"].split("\n")
            subject = lines[0] if lines else "Check This Out!"
            body = "\n".join(lines[1:]) if len(lines) > 1 else content["content"]
            
            message = Mail(
                from_email=(EMAIL_FROM, EMAIL_FROM_NAME),
                to_emails="contact@example.com",  # Replace with actual email list
                subject=subject,
                html_content=f"<p>{body}</p>"
            )
            
            sg = SendGridAPIClient(SENDGRID_API_KEY)
            response = sg.send(message)
            
            logger.info(f"✓ Email sent via SendGrid: {response.status_code}")
            return {
                "success": True,
                "status_code": response.status_code
            }
        except Exception as e:
            return {"error": str(e)}
    
    def post_batch(self, contents: List[Dict], platforms: List[str] = None) -> List[Dict]:
        """Post multiple contents to multiple platforms"""
        
        results = []
        
        for content in contents:
            for platform in (platforms or ["twitter", "linkedin", "reddit"]):
                result = self.post_to_platform(content, platform)
                results.append(result)
        
        logger.info(f"✓ Batch posting complete: {len(results)} posts")
        return results
    
    def get_posting_stats(self) -> Dict:
        """Get stats on posts made"""
        
        stats = {
            "total_posts": len(self.post_history),
            "successful_posts": sum(1 for p in self.post_history if p.get("success")),
            "failed_posts": sum(1 for p in self.post_history if not p.get("success")),
            "by_platform": {}
        }
        
        for post in self.post_history:
            platform = post.get("platform")
            if platform not in stats["by_platform"]:
                stats["by_platform"][platform] = {"success": 0, "failed": 0}
            
            if post.get("success"):
                stats["by_platform"][platform]["success"] += 1
            else:
                stats["by_platform"][platform]["failed"] += 1
        
        return stats


# Initialize manager
manager = PlatformManager()

if __name__ == "__main__":
    print("Platform Manager initialized")
    print(f"Post history: {manager.post_history}")
