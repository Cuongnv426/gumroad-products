"""
24/7 Content Scheduling System
Automatically generates and posts content at optimal times
"""

import schedule
import time
import logging
from datetime import datetime, timedelta
from typing import List, Dict
from content_engine import engine, formatter
from platform_manager import manager
from config import POSTING_SCHEDULE, POSTS_PER_DAY

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class ContentScheduler:
    """Schedule and execute automated content posting"""
    
    def __init__(self):
        self.schedule = schedule.Scheduler()
        self.job_count = 0
        self.posts_today = 0
        self.last_reset = datetime.now().date()
        self.posting_log = []
        self._setup_schedule()
        
    def _setup_schedule(self):
        """Configure all posting schedules for all platforms"""
        
        logger.info("Setting up posting schedule...")
        
        for platform, config in POSTING_SCHEDULE.items():
            if not config.get("enabled"):
                logger.info(f"Skipping disabled platform: {platform}")
                continue
            
            times = config.get("times", [])
            
            for post_time in times:
                self.schedule.every().day.at(post_time).do(
                    self.job_post_to_platform,
                    platform=platform
                )
                self.job_count += 1
                logger.info(f"✓ Scheduled {platform} at {post_time}")
        
        logger.info(f"✓ {self.job_count} jobs scheduled")
    
    def job_post_to_platform(self, platform: str):
        """Job to generate and post content to a platform"""
        
        try:
            logger.info(f"[{platform.upper()}] Starting post job...")
            
            # Reset daily counter at midnight
            if datetime.now().date() > self.last_reset:
                self.posts_today = 0
                self.last_reset = datetime.now().date()
            
            # Check if we've hit daily limit
            if self.posts_today >= POSTS_PER_DAY:
                logger.warning(f"Daily post limit reached ({POSTS_PER_DAY})")
                return
            
            # Generate content
            content = engine.generate_content(platform=platform)
            
            if "error" in content:
                logger.error(f"Content generation failed: {content['error']}")
                return
            
            # Format for platform
            formatted_content = formatter.format_for_platform(content, platform)
            content["formatted"] = formatted_content
            
            # Post to platform
            result = manager.post_to_platform(content, platform)
            
            if result.get("success"):
                self.posts_today += 1
                self.posting_log.append({
                    "timestamp": datetime.now().isoformat(),
                    "platform": platform,
                    "success": True,
                    "post_id": result.get("post_id")
                })
                logger.info(f"✓ Successfully posted to {platform}")
            else:
                logger.error(f"Failed to post to {platform}: {result.get('error')}")
                self.posting_log.append({
                    "timestamp": datetime.now().isoformat(),
                    "platform": platform,
                    "success": False,
                    "error": result.get("error")
                })
        
        except Exception as e:
            logger.error(f"Job error for {platform}: {str(e)}")
    
    def run(self):
        """Main scheduler loop - run forever"""
        
        logger.info("=" * 60)
        logger.info("Content Bot Scheduler Started")
        logger.info(f"Total jobs: {self.job_count}")
        logger.info(f"Posts per day limit: {POSTS_PER_DAY}")
        logger.info("=" * 60)
        
        while True:
            try:
                self.schedule.run_pending()
                time.sleep(60)  # Check every minute
            except KeyboardInterrupt:
                logger.info("Scheduler stopped by user")
                break
            except Exception as e:
                logger.error(f"Scheduler error: {str(e)}")
                time.sleep(60)
    
    def run_once(self):
        """Run all jobs once (for testing)"""
        
        logger.info("Running all jobs once...")
        
        for job in self.schedule.get_jobs():
            job.do()
        
        logger.info("All jobs completed")
    
    def get_next_jobs(self, hours: int = 24) -> List[Dict]:
        """Get upcoming scheduled jobs"""
        
        jobs = []
        now = datetime.now()
        future = now + timedelta(hours=hours)
        
        for job in self.schedule.get_jobs():
            job_time = job.at_time if hasattr(job, 'at_time') else None
            if job_time:
                job_hour, job_min = map(int, str(job_time).split(':'))
                job_datetime = now.replace(
                    hour=job_hour, 
                    minute=job_min, 
                    second=0
                )
                
                if now <= job_datetime <= future:
                    jobs.append({
                        "time": job_datetime.isoformat(),
                        "platform": str(job.job_func.keywords.get("platform", "unknown"))
                    })
        
        return sorted(jobs, key=lambda x: x["time"])
    
    def get_stats(self) -> Dict:
        """Get scheduler statistics"""
        
        today_logs = [p for p in self.posting_log 
                     if p["timestamp"].startswith(datetime.now().strftime("%Y-%m-%d"))]
        
        return {
            "total_jobs": self.job_count,
            "posts_today": self.posts_today,
            "daily_limit": POSTS_PER_DAY,
            "posts_remaining": max(0, POSTS_PER_DAY - self.posts_today),
            "successful_posts": sum(1 for p in today_logs if p.get("success")),
            "failed_posts": sum(1 for p in today_logs if not p.get("success")),
            "last_reset": self.last_reset.isoformat(),
            "recent_posts": self.posting_log[-10:] if self.posting_log else []
        }


# Initialize scheduler
scheduler = ContentScheduler()


class ManualScheduler:
    """Manual scheduling for testing and one-off posts"""
    
    @staticmethod
    def post_now(platform: str = None, niche: str = None):
        """Generate and post content immediately"""
        
        logger.info(f"Posting immediately to {platform}...")
        
        content = engine.generate_content(niche=niche, platform=platform)
        
        if "error" in content:
            logger.error(f"Generation failed: {content['error']}")
            return content
        
        result = manager.post_to_platform(content, platform)
        logger.info(f"Post result: {result}")
        return result
    
    @staticmethod
    def generate_batch_now(count: int = 5) -> List[Dict]:
        """Generate a batch of content immediately"""
        
        logger.info(f"Generating {count} content pieces...")
        return engine.generate_batch(count=count)
    
    @staticmethod
    def post_batch_now(contents: List[Dict], platforms: List[str] = None):
        """Post a batch to specified platforms"""
        
        logger.info(f"Posting batch to {platforms}...")
        return manager.post_batch(contents, platforms)


manual = ManualScheduler()


if __name__ == "__main__":
    import sys
    
    # Run mode selection
    if len(sys.argv) > 1:
        mode = sys.argv[1]
        
        if mode == "run":
            scheduler.run()
        elif mode == "test":
            logger.info("Running test...")
            scheduler.run_once()
        elif mode == "stats":
            print(scheduler.get_stats())
        elif mode == "next":
            print("Next jobs (24h):")
            for job in scheduler.get_next_jobs():
                print(f"  {job['time']}: {job['platform']}")
        else:
            print("Usage: python scheduler.py [run|test|stats|next]")
    else:
        # Default: run scheduler
        scheduler.run()
