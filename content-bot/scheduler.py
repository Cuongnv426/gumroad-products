"""
Scheduler - Post content at optimal times
Manages scheduling, queuing, and timing for all platforms
"""

import json
import logging
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import pytz
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import schedule
import time

from config import Config
from content_generator import ContentGenerator
from platform_integrations import PlatformManager

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=getattr(logging, Config.LOG_LEVEL),
    format=Config.LOG_FORMAT
)

class PostScheduler:
    """Manage content posting schedule"""
    
    def __init__(self):
        self.scheduler = BackgroundScheduler(timezone=Config.TIMEZONE)
        self.content_gen = ContentGenerator()
        self.platform_manager = PlatformManager()
        
        self.post_queue = []
        self.posted_today = {}
        self.schedule_config = Config.POSTING_SCHEDULE
        
        logger.info("PostScheduler initialized")
    
    def start(self):
        """Start the scheduler"""
        try:
            self._schedule_all_posts()
            self.scheduler.start()
            logger.info("✓ Scheduler started successfully")
            return True
        except Exception as e:
            logger.error(f"Failed to start scheduler: {e}")
            return False
    
    def stop(self):
        """Stop the scheduler"""
        try:
            self.scheduler.shutdown()
            logger.info("Scheduler stopped")
            return True
        except Exception as e:
            logger.error(f"Failed to stop scheduler: {e}")
            return False
    
    def _schedule_all_posts(self):
        """Schedule posts for all platforms"""
        logger.info("Scheduling all platform posts...")
        
        # Twitter - 5x per day
        if self.schedule_config["twitter"]["enabled"]:
            for time_slot in self.schedule_config["twitter"]["times"]:
                self._schedule_cron_job(
                    self._post_twitter,
                    time_slot,
                    "twitter"
                )
                logger.info(f"Twitter scheduled at {time_slot}")
        
        # TikTok - 2x per day
        if self.schedule_config["tiktok"]["enabled"]:
            for time_slot in self.schedule_config["tiktok"]["times"]:
                self._schedule_cron_job(
                    self._post_tiktok,
                    time_slot,
                    "tiktok"
                )
                logger.info(f"TikTok scheduled at {time_slot}")
        
        # Instagram - 2x per day (mirror TikTok)
        if self.schedule_config["instagram"]["enabled"]:
            for time_slot in self.schedule_config["instagram"]["times"]:
                self._schedule_cron_job(
                    self._post_instagram,
                    time_slot,
                    "instagram"
                )
                logger.info(f"Instagram scheduled at {time_slot}")
        
        # LinkedIn - 2x per day
        if self.schedule_config["linkedin"]["enabled"]:
            for time_slot in self.schedule_config["linkedin"]["times"]:
                self._schedule_cron_job(
                    self._post_linkedin,
                    time_slot,
                    "linkedin"
                )
                logger.info(f"LinkedIn scheduled at {time_slot}")
        
        # Reddit - 2x per day
        if self.schedule_config["reddit"]["enabled"]:
            for time_slot in self.schedule_config["reddit"]["times"]:
                self._schedule_cron_job(
                    self._post_reddit,
                    time_slot,
                    "reddit"
                )
                logger.info(f"Reddit scheduled at {time_slot}")
        
        # Medium - 2x per week (Wed, Sun)
        if self.schedule_config["medium"]["enabled"]:
            for day_num in self.schedule_config["medium"]["days"]:
                self._schedule_cron_job_weekly(
                    self._post_medium,
                    day_num,
                    "08:00",  # Morning time
                    "medium"
                )
                logger.info(f"Medium scheduled for day {day_num}")
        
        # Email - 3x per week (Tue, Thu, Sat)
        if self.schedule_config["email"]["enabled"]:
            for day_num in self.schedule_config["email"]["days"]:
                self._schedule_cron_job_weekly(
                    self._post_email,
                    day_num,
                    self.schedule_config["email"]["time"],
                    "email"
                )
                logger.info(f"Email scheduled for day {day_num}")
        
        logger.info("✓ All posts scheduled")
    
    def _schedule_cron_job(self, func, time_str: str, platform: str):
        """Schedule a daily cron job at specific time"""
        hour, minute = map(int, time_str.split(":"))
        
        trigger = CronTrigger(hour=hour, minute=minute, timezone=Config.TIMEZONE)
        self.scheduler.add_job(
            func,
            trigger=trigger,
            id=f"{platform}_{time_str}",
            name=f"Post to {platform} at {time_str}",
            replace_existing=True
        )
    
    def _schedule_cron_job_weekly(self, func, day_of_week: int, time_str: str, platform: str):
        """Schedule a weekly cron job"""
        hour, minute = map(int, time_str.split(":"))
        
        trigger = CronTrigger(
            day_of_week=day_of_week,
            hour=hour,
            minute=minute,
            timezone=Config.TIMEZONE
        )
        self.scheduler.add_job(
            func,
            trigger=trigger,
            id=f"{platform}_day{day_of_week}",
            name=f"Post to {platform} on day {day_of_week}",
            replace_existing=True
        )
    
    # ==================== POSTING FUNCTIONS ====================
    
    def _post_twitter(self):
        """Generate and post to Twitter"""
        try:
            logger.info("Posting to Twitter...")
            posts = self.content_gen.generate_twitter_posts(1)
            
            if posts:
                result = self.platform_manager.post_to_platform("twitter", posts[0])
                self._log_post(result)
        except Exception as e:
            logger.error(f"Twitter posting failed: {e}")
    
    def _post_tiktok(self):
        """Generate and post to TikTok"""
        try:
            logger.info("Posting to TikTok...")
            script = self.content_gen.generate_tiktok_script()
            
            # In production, would generate video from script
            result = self.platform_manager.post_to_platform("tiktok", script)
            self._log_post(result)
        except Exception as e:
            logger.error(f"TikTok posting failed: {e}")
    
    def _post_instagram(self):
        """Post to Instagram (Reels)"""
        try:
            logger.info("Posting to Instagram...")
            script = self.content_gen.generate_tiktok_script()
            
            content = {
                "type": "reel",
                "caption": script.get("body", ""),
                "hashtags": script.get("hashtags", [])
            }
            
            result = self.platform_manager.post_to_platform("instagram", content)
            self._log_post(result)
        except Exception as e:
            logger.error(f"Instagram posting failed: {e}")
    
    def _post_linkedin(self):
        """Generate and post to LinkedIn"""
        try:
            logger.info("Posting to LinkedIn...")
            post = self.content_gen.generate_linkedin_post()
            
            content = {
                "content": post.get("content", "")
            }
            
            result = self.platform_manager.post_to_platform("linkedin", content)
            self._log_post(result)
        except Exception as e:
            logger.error(f"LinkedIn posting failed: {e}")
    
    def _post_reddit(self):
        """Generate and post to Reddit"""
        try:
            logger.info("Posting to Reddit...")
            subreddit = "ChatGPT"  # Default, can be randomized
            post = self.content_gen.generate_reddit_post(subreddit)
            
            result = self.platform_manager.post_to_platform("reddit", post)
            self._log_post(result)
        except Exception as e:
            logger.error(f"Reddit posting failed: {e}")
    
    def _post_medium(self):
        """Generate and post to Medium"""
        try:
            logger.info("Posting to Medium...")
            blog_post = self.content_gen.generate_blog_post()
            
            content = {
                "title": blog_post.get("title", ""),
                "body": blog_post.get("body", ""),
                "tags": blog_post.get("tags", [])
            }
            
            result = self.platform_manager.post_to_platform("medium", content)
            self._log_post(result)
        except Exception as e:
            logger.error(f"Medium posting failed: {e}")
    
    def _post_email(self):
        """Generate and send email"""
        try:
            logger.info("Sending email...")
            email_content = self.content_gen.generate_email_content()
            
            result = self.platform_manager.post_to_platform("email", email_content)
            self._log_post(result)
        except Exception as e:
            logger.error(f"Email sending failed: {e}")
    
    def _log_post(self, result: Dict):
        """Log posting result"""
        platform = result.get("platform")
        success = result.get("success")
        
        if success:
            logger.info(f"✓ {platform.upper()}: Post successful (ID: {result.get('post_id')})")
        else:
            logger.error(f"✗ {platform.upper()}: Post failed - {result.get('error')}")
    
    def get_next_posts(self, hours: int = 24) -> List[Dict]:
        """Get scheduled posts for next N hours"""
        next_time = datetime.now(pytz.timezone(Config.TIMEZONE)) + timedelta(hours=hours)
        
        upcoming = []
        for job in self.scheduler.get_jobs():
            if job.next_run_time and job.next_run_time <= next_time:
                upcoming.append({
                    "job_id": job.id,
                    "platform": job.args[0] if job.args else "unknown",
                    "scheduled_time": job.next_run_time.isoformat(),
                    "name": job.name
                })
        
        return sorted(upcoming, key=lambda x: x["scheduled_time"])
    
    def get_status(self) -> Dict:
        """Get scheduler status"""
        return {
            "running": self.scheduler.running,
            "jobs_count": len(self.scheduler.get_jobs()),
            "jobs": [
                {
                    "id": job.id,
                    "name": job.name,
                    "next_run": job.next_run_time.isoformat() if job.next_run_time else None
                }
                for job in self.scheduler.get_jobs()
            ],
            "timezone": Config.TIMEZONE
        }

class ManualScheduler:
    """Manual scheduler using simple schedule library (for testing)"""
    
    def __init__(self):
        self.content_gen = ContentGenerator()
        self.platform_manager = PlatformManager()
        self.running = False
    
    def schedule_daily_generation(self):
        """Schedule daily content generation"""
        schedule.every().day.at("00:00").do(self.generate_daily_content)
    
    def generate_daily_content(self):
        """Generate content for the day"""
        try:
            logger.info("Generating daily content...")
            
            daily_content = {
                "tiktok": self.content_gen.generate_tiktok_script(),
                "twitter": self.content_gen.generate_twitter_posts(5),
                "linkedin": self.content_gen.generate_linkedin_post(),
                "reddit": self.content_gen.generate_reddit_post(),
                "email": self.content_gen.generate_email_content()
            }
            
            # Save to queue
            with open(f"{Config.DATA_PATH}/queue-{datetime.now().strftime('%Y-%m-%d')}.json", 'w') as f:
                json.dump(daily_content, f, indent=2)
            
            logger.info("✓ Daily content generated and queued")
            return daily_content
        
        except Exception as e:
            logger.error(f"Error generating daily content: {e}")
            return {}
    
    def run_pending(self):
        """Check and run pending scheduled tasks"""
        schedule.run_pending()
    
    def run_loop(self, check_interval_seconds: int = 60):
        """Run scheduler loop"""
        self.running = True
        logger.info("Manual scheduler running...")
        
        try:
            while self.running:
                self.run_pending()
                time.sleep(check_interval_seconds)
        except KeyboardInterrupt:
            logger.info("Scheduler stopped")
            self.running = False


def quick_test():
    """Test scheduler"""
    print("Testing Scheduler...\n")
    
    scheduler = PostScheduler()
    
    print("Scheduler Status:")
    status = scheduler.get_status()
    print(f"Jobs scheduled: {status['jobs_count']}")
    print("\nNext posts (next 24h):")
    
    upcoming = scheduler.get_next_posts(24)
    for post in upcoming[:5]:
        print(f"  - {post['platform']}: {post['scheduled_time']}")
    
    print("\n✓ Scheduler test complete")


if __name__ == "__main__":
    quick_test()
