"""
Content Bot - Main Orchestrator
Runs 24/7 and manages all content generation, posting, and analytics
"""

import json
import logging
import time
import signal
import sys
from typing import Dict, Optional
from datetime import datetime, timedelta
import os

# Import all modules
from config import Config
from content_generator import ContentGenerator
from platform_integrations import PlatformManager
from scheduler import PostScheduler
from email_system import EmailListManager, NewsletterTemplateManager
from analytics import DashboardGenerator, AnalyticsDB

# Setup logging
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=getattr(logging, Config.LOG_LEVEL),
    format=Config.LOG_FORMAT,
    handlers=[
        logging.FileHandler(f"{Config.LOG_PATH}/bot.log"),
        logging.StreamHandler()
    ]
)

class ContentBot:
    """Main Content Bot - Orchestrates all operations"""
    
    def __init__(self):
        logger.info("Initializing Content Bot...")
        
        # Initialize components
        self.content_gen = ContentGenerator()
        self.platform_manager = PlatformManager()
        self.scheduler = PostScheduler()
        self.email_manager = EmailListManager()
        self.analytics = DashboardGenerator()
        
        self.running = False
        self.stats = {
            "startup_time": datetime.now().isoformat(),
            "posts_generated": 0,
            "posts_published": 0,
            "total_errors": 0
        }
        
        logger.info("✓ Content Bot initialized successfully")
    
    def start(self):
        """Start the bot"""
        logger.info("=" * 60)
        logger.info("🤖 CONTENT BOT STARTING")
        logger.info("=" * 60)
        
        try:
            self.running = True
            
            # Setup signal handlers
            signal.signal(signal.SIGINT, self._signal_handler)
            signal.signal(signal.SIGTERM, self._signal_handler)
            
            # Check configuration
            self._check_configuration()
            
            # Start scheduler
            if self.scheduler.start():
                logger.info("✓ Scheduler started")
            else:
                logger.warning("⚠ Scheduler failed to start - manual generation only")
            
            # Show platform status
            self._show_platform_status()
            
            # Generate initial content
            logger.info("Generating initial content...")
            self._generate_daily_content()
            
            # Start monitoring loop
            logger.info("✓ Bot is now running!")
            logger.info(f"Check logs at: {Config.LOG_PATH}")
            logger.info(f"Check dashboard at: {Config.DATA_PATH}/dashboard.html")
            
            self._run_monitoring_loop()
        
        except Exception as e:
            logger.error(f"Fatal error: {e}")
            self.stop()
    
    def stop(self):
        """Stop the bot"""
        logger.info("\n" + "=" * 60)
        logger.info("🛑 CONTENT BOT SHUTTING DOWN")
        logger.info("=" * 60)
        
        self.running = False
        
        try:
            self.scheduler.stop()
            logger.info("✓ Scheduler stopped")
        except:
            pass
        
        # Generate final report
        self._generate_status_report()
        
        logger.info("✓ Content Bot stopped gracefully")
        sys.exit(0)
    
    def _signal_handler(self, sig, frame):
        """Handle shutdown signals"""
        logger.info(f"\nReceived signal {sig}")
        self.stop()
    
    def _check_configuration(self):
        """Check if required APIs are configured"""
        logger.info("Checking configuration...")
        
        issues = []
        
        # Check OpenAI
        if Config.OPENAI_API_KEY == "your-openai-key-here" or not Config.OPENAI_API_KEY:
            issues.append("⚠ OpenAI API key not configured")
        
        # Check platform APIs
        if not Config.TWITTER_API_KEY:
            issues.append("⚠ Twitter API not configured")
        if not Config.TIKTOK_ACCESS_TOKEN:
            issues.append("⚠ TikTok API not configured")
        if not Config.MAILCHIMP_API_KEY:
            issues.append("⚠ Mailchimp not configured")
        
        if issues:
            logger.warning("Configuration warnings:")
            for issue in issues:
                logger.warning(f"  {issue}")
            logger.warning("Bot will continue with available platforms")
        else:
            logger.info("✓ All APIs configured")
    
    def _show_platform_status(self):
        """Show status of all platforms"""
        logger.info("Platform Status:")
        status = self.platform_manager.get_status()
        
        for platform, info in status.items():
            status_icon = "✓" if info["authenticated"] else "✗"
            logger.info(f"  {status_icon} {platform.upper()}: {('Authenticated' if info['authenticated'] else 'Not configured')}")
    
    def _generate_daily_content(self):
        """Generate daily content batch"""
        logger.info("Generating daily content batch...")
        
        try:
            daily_content = {
                "generated_at": datetime.now().isoformat(),
                "content": {}
            }
            
            # TikTok scripts (2)
            logger.info("  - Generating 2 TikTok scripts...")
            daily_content["content"]["tiktok"] = [
                self.content_gen.generate_tiktok_script() for _ in range(2)
            ]
            self.stats["posts_generated"] += 2
            
            # Twitter posts (5)
            logger.info("  - Generating 5 Twitter posts...")
            daily_content["content"]["twitter"] = self.content_gen.generate_twitter_posts(5)
            self.stats["posts_generated"] += 5
            
            # LinkedIn posts (2)
            logger.info("  - Generating 2 LinkedIn posts...")
            daily_content["content"]["linkedin"] = [
                self.content_gen.generate_linkedin_post() for _ in range(2)
            ]
            self.stats["posts_generated"] += 2
            
            # Reddit posts (2)
            logger.info("  - Generating 2 Reddit posts...")
            daily_content["content"]["reddit"] = [
                self.content_gen.generate_reddit_post() for _ in range(2)
            ]
            self.stats["posts_generated"] += 2
            
            # Email (1)
            logger.info("  - Generating 1 email...")
            daily_content["content"]["email"] = self.content_gen.generate_email_content()
            self.stats["posts_generated"] += 1
            
            # Blog post (1-2 per week)
            if datetime.now().weekday() in [2, 6]:  # Wednesday, Sunday
                logger.info("  - Generating blog post...")
                daily_content["content"]["blog"] = self.content_gen.generate_blog_post()
                self.stats["posts_generated"] += 1
            
            # Save to file
            queue_file = f"{Config.DATA_PATH}/queue-{datetime.now().strftime('%Y-%m-%d')}.json"
            os.makedirs(Config.DATA_PATH, exist_ok=True)
            
            with open(queue_file, 'w') as f:
                json.dump(daily_content, f, indent=2)
            
            logger.info(f"✓ Generated {self.stats['posts_generated']} pieces of content")
            logger.info(f"  Saved to: {queue_file}")
        
        except Exception as e:
            logger.error(f"Error generating daily content: {e}")
            self.stats["total_errors"] += 1
    
    def _run_monitoring_loop(self):
        """Run continuous monitoring loop"""
        check_interval = Config.CHECK_INTERVAL_MINUTES * 60
        
        logger.info(f"Monitoring loop started (check every {Config.CHECK_INTERVAL_MINUTES} minutes)")
        
        while self.running:
            try:
                current_time = datetime.now()
                
                # Every hour: Check and show status
                if current_time.minute == 0:
                    self._show_hourly_status()
                
                # Every day at midnight: Generate new content
                if current_time.hour == 0 and current_time.minute == 0:
                    self._generate_daily_content()
                
                # Every 6 hours: Update dashboard
                if current_time.hour % 6 == 0 and current_time.minute == 0:
                    self._update_dashboard()
                
                # Sleep before next check
                time.sleep(check_interval)
            
            except KeyboardInterrupt:
                break
            except Exception as e:
                logger.error(f"Error in monitoring loop: {e}")
                self.stats["total_errors"] += 1
                time.sleep(60)
    
    def _show_hourly_status(self):
        """Show hourly status"""
        logger.info(f"\n--- Hourly Status Check ({datetime.now().strftime('%H:%M:%S')}) ---")
        logger.info(f"Posts generated today: {self.stats['posts_generated']}")
        logger.info(f"Posts published: {self.stats['posts_published']}")
        logger.info(f"Errors: {self.stats['total_errors']}")
        
        # Show next scheduled posts
        next_posts = self.scheduler.get_next_posts(hours=3)
        if next_posts:
            logger.info("Next 3 hours of posts:")
            for post in next_posts[:5]:
                logger.info(f"  - {post['platform']}: {post['scheduled_time']}")
    
    def _update_dashboard(self):
        """Update analytics dashboard"""
        try:
            logger.info("Updating analytics dashboard...")
            self.analytics.export_dashboard_html()
            logger.info("✓ Dashboard updated")
        except Exception as e:
            logger.error(f"Error updating dashboard: {e}")
    
    def _generate_status_report(self):
        """Generate final status report"""
        logger.info("\n" + "=" * 60)
        logger.info("📊 FINAL STATUS REPORT")
        logger.info("=" * 60)
        
        uptime = datetime.now() - datetime.fromisoformat(self.stats["startup_time"])
        
        logger.info(f"Uptime: {uptime}")
        logger.info(f"Posts Generated: {self.stats['posts_generated']}")
        logger.info(f"Posts Published: {self.stats['posts_published']}")
        logger.info(f"Errors: {self.stats['total_errors']}")
        
        # Get analytics
        try:
            daily_stats = self.analytics.db.get_daily_stats()
            affiliate_stats = self.analytics.affiliate.get_affiliate_stats()
            
            logger.info(f"\nToday's Revenue: {daily_stats.get('affiliate_revenue', 0)}")
            logger.info(f"Affiliate Clicks: {affiliate_stats.get('total_clicks', 0)}")
            logger.info(f"Email Signups: {daily_stats.get('email_signups', 0)}")
        except:
            pass
        
        logger.info("=" * 60)
    
    def generate_content_batch(self, count: int = 20) -> Dict:
        """Generate a batch of content for manual posting"""
        logger.info(f"Generating batch of {count} pieces of content...")
        
        batch = {
            "generated_at": datetime.now().isoformat(),
            "items": []
        }
        
        for i in range(count):
            content_type = ["twitter", "tiktok", "linkedin", "reddit"][i % 4]
            
            if content_type == "twitter":
                content = self.content_gen.generate_twitter_posts(1)[0]
            elif content_type == "tiktok":
                content = self.content_gen.generate_tiktok_script()
            elif content_type == "linkedin":
                content = self.content_gen.generate_linkedin_post()
            else:
                content = self.content_gen.generate_reddit_post()
            
            batch["items"].append(content)
        
        logger.info(f"✓ Generated {count} pieces of content")
        return batch
    
    def get_status(self) -> Dict:
        """Get current bot status"""
        return {
            "running": self.running,
            "startup_time": self.stats["startup_time"],
            "posts_generated": self.stats["posts_generated"],
            "posts_published": self.stats["posts_published"],
            "errors": self.stats["total_errors"],
            "scheduler_status": self.scheduler.get_status(),
            "platform_status": self.platform_manager.get_status()
        }
    
    def post_manually(self, platform: str, content: Dict) -> Dict:
        """Manually post content to a platform"""
        logger.info(f"Manually posting to {platform}...")
        
        result = self.platform_manager.post_to_platform(platform, content)
        
        if result.get("success"):
            self.stats["posts_published"] += 1
            logger.info(f"✓ Post successful: {result.get('post_id')}")
        else:
            self.stats["total_errors"] += 1
            logger.error(f"✗ Post failed: {result.get('error')}")
        
        return result


# ==================== CLI INTERFACE ====================

def print_menu():
    """Print CLI menu"""
    print("\n" + "=" * 60)
    print("🤖 CONTENT BOT - INTERACTIVE MENU")
    print("=" * 60)
    print("1. Start bot (24/7 auto-posting)")
    print("2. Generate content batch (manual)")
    print("3. Show current status")
    print("4. View analytics dashboard")
    print("5. Test platform connections")
    print("6. Generate sample content")
    print("7. Exit")
    print("=" * 60)


def main():
    """Main entry point"""
    print("\n" + "=" * 60)
    print("🚀 CONTENT BOT - AI TOOLS & PRODUCTIVITY")
    print("Production-Ready Content Generation & Posting")
    print("=" * 60)
    
    # Initialize bot
    bot = ContentBot()
    
    if len(sys.argv) > 1:
        # Command line mode
        command = sys.argv[1].lower()
        
        if command == "start":
            bot.start()
        elif command == "generate":
            count = int(sys.argv[2]) if len(sys.argv) > 2 else 10
            batch = bot.generate_content_batch(count)
            print(json.dumps(batch, indent=2, default=str))
        elif command == "status":
            status = bot.get_status()
            print(json.dumps(status, indent=2, default=str))
        elif command == "test":
            bot._check_configuration()
            bot._show_platform_status()
        else:
            print("Unknown command. Use: start, generate, status, test")
    else:
        # Interactive mode
        while True:
            print_menu()
            choice = input("Select option (1-7): ").strip()
            
            if choice == "1":
                bot.start()
            
            elif choice == "2":
                try:
                    count = int(input("How many pieces of content? (default: 10): ") or "10")
                    batch = bot.generate_content_batch(count)
                    print(f"\n✓ Generated {count} pieces of content")
                    print(f"Saved to: {Config.DATA_PATH}")
                except ValueError:
                    print("Invalid number")
            
            elif choice == "3":
                status = bot.get_status()
                print("\n" + json.dumps(status, indent=2, default=str))
            
            elif choice == "4":
                print(f"\nDashboard: {Config.DATA_PATH}/dashboard.html")
                bot._update_dashboard()
            
            elif choice == "5":
                print("\nTesting platform connections...")
                bot._check_configuration()
                bot._show_platform_status()
            
            elif choice == "6":
                print("\nGenerating sample content samples...")
                print("1. TikTok Script")
                print(json.dumps(bot.content_gen.generate_tiktok_script(), indent=2, default=str)[:500])
                print("\n2. Twitter Post")
                print(json.dumps(bot.content_gen.generate_twitter_posts(1), indent=2, default=str)[:500])
            
            elif choice == "7":
                print("\nGoodbye!")
                break
            
            else:
                print("Invalid option")


if __name__ == "__main__":
    main()
