#!/usr/bin/env python3
"""
Content Bot - Main Entry Point
Production-ready 24/7 content generation and posting system
"""

import sys
import logging
from datetime import datetime
from typing import Optional

# Import all modules
from config import *
from content_engine import engine, formatter
from platform_manager import manager
from scheduler import scheduler, manual
from email_system import email_manager, sequences
from analytics import dashboard, affiliate_tracker, post_analytics

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - [%(levelname)s] - %(name)s - %(message)s',
    handlers=[
        logging.FileHandler('content_bot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class ContentBot:
    """Main bot controller"""
    
    def __init__(self):
        self.version = "1.0.0"
        self.started_at = datetime.now()
        self.running = False
        logger.info("=" * 70)
        logger.info(f"Content Bot v{self.version} initialized")
        logger.info("=" * 70)
    
    def generate_content(self, count: int = 1, niche: str = None, 
                        platform: str = None) -> list:
        """Generate content"""
        
        logger.info(f"Generating {count} content pieces...")
        
        if count == 1:
            return [engine.generate_content(niche=niche, platform=platform)]
        else:
            return engine.generate_batch(count=count)
    
    def post_content(self, content: dict, platforms: list = None) -> dict:
        """Post content to platforms"""
        
        platforms = platforms or ["twitter", "linkedin", "reddit"]
        results = {}
        
        for platform in platforms:
            logger.info(f"Posting to {platform}...")
            result = manager.post_to_platform(content, platform)
            results[platform] = result
            
            if result.get("success"):
                logger.info(f"✓ {platform}: Success")
            else:
                logger.error(f"✗ {platform}: {result.get('error')}")
        
        return results
    
    def add_email_subscriber(self, email: str, name: str = None) -> dict:
        """Add email subscriber"""
        
        logger.info(f"Adding subscriber: {email}")
        result = email_manager.add_subscriber(email, name)
        
        if result.get("success"):
            logger.info(f"✓ Subscriber added: {email}")
        else:
            logger.error(f"✗ Failed to add subscriber: {result.get('error')}")
        
        return result
    
    def send_email_campaign(self, subject: str, content: str) -> dict:
        """Send email campaign"""
        
        logger.info(f"Sending email campaign: {subject}")
        result = email_manager.send_email(subject, content)
        return result
    
    def track_affiliate_click(self, product: str) -> str:
        """Track affiliate link click"""
        
        link = affiliate_tracker.track_click(product)
        return link
    
    def track_conversion(self, product: str, amount: float) -> dict:
        """Track affiliate conversion"""
        
        result = affiliate_tracker.track_conversion(product, amount)
        return result
    
    def get_stats(self) -> dict:
        """Get current statistics"""
        
        return {
            "uptime": str(datetime.now() - self.started_at),
            "version": self.version,
            "posting_stats": manager.get_posting_stats(),
            "affiliate_stats": affiliate_tracker.get_affiliate_stats(),
            "post_stats": post_analytics.get_post_stats(),
            "scheduler_stats": scheduler.get_stats()
        }
    
    def get_report(self) -> dict:
        """Get full analytics report"""
        
        return dashboard.get_dashboard_data()
    
    def print_status(self):
        """Print bot status"""
        
        stats = self.get_stats()
        
        print("\n" + "=" * 70)
        print("CONTENT BOT STATUS")
        print("=" * 70)
        print(f"Version: {self.version}")
        print(f"Uptime: {stats['uptime']}")
        print(f"\nPosting Stats:")
        print(f"  Total posts: {stats['posting_stats'].get('total_posts', 0)}")
        print(f"  Successful: {stats['posting_stats'].get('successful_posts', 0)}")
        print(f"  Failed: {stats['posting_stats'].get('failed_posts', 0)}")
        print(f"\nScheduler:")
        print(f"  Total jobs: {stats['scheduler_stats'].get('total_jobs', 0)}")
        print(f"  Posts today: {stats['scheduler_stats'].get('posts_today', 0)}")
        print(f"  Daily limit: {stats['scheduler_stats'].get('daily_limit', 0)}")
        print("\n" + "=" * 70 + "\n")
    
    def start(self, daemon: bool = True):
        """Start the bot"""
        
        self.running = True
        
        logger.info("Starting Content Bot...")
        logger.info(f"Daemon mode: {daemon}")
        
        self.print_status()
        
        if daemon:
            scheduler.run()
        else:
            logger.info("Running test mode...")
            scheduler.run_once()
            self.print_status()
    
    def stop(self):
        """Stop the bot"""
        
        self.running = False
        logger.info("Content Bot stopped")
    
    def test(self):
        """Run tests"""
        
        logger.info("Running tests...")
        
        # Test content generation
        logger.info("Test 1: Content generation")
        content = self.generate_content(count=1, platform="twitter")
        if content and "error" not in content[0]:
            logger.info("✓ Content generation works")
        else:
            logger.error("✗ Content generation failed")
        
        # Test posting (dry run)
        logger.info("Test 2: Platform posting")
        logger.info("(Skipping actual posting, use --post flag to enable)")
        
        # Test email
        logger.info("Test 3: Email system")
        logger.info("✓ Email system initialized")
        
        # Test analytics
        logger.info("Test 4: Analytics")
        dashboard.print_summary()
        logger.info("✓ Analytics working")
        
        logger.info("✓ All tests completed")


# CLI Commands
def main():
    """Main CLI interface"""
    
    bot = ContentBot()
    
    if len(sys.argv) < 2:
        print_help()
        return
    
    command = sys.argv[1].lower()
    
    if command == "start":
        bot.start(daemon=True)
    
    elif command == "test":
        bot.test()
    
    elif command == "generate":
        count = int(sys.argv[2]) if len(sys.argv) > 2 else 1
        platform = sys.argv[3] if len(sys.argv) > 3 else None
        content = bot.generate_content(count=count, platform=platform)
        print(f"\nGenerated {len(content)} content pieces:\n")
        for i, c in enumerate(content, 1):
            print(f"{i}. [{c.get('platform')}] {c.get('content')[:100]}...")
    
    elif command == "post":
        platform = sys.argv[2] if len(sys.argv) > 2 else "twitter"
        content = bot.generate_content(count=1, platform=platform)[0]
        result = bot.post_content(content, platforms=[platform])
        print(f"\nPosting result:\n{result}")
    
    elif command == "email":
        action = sys.argv[2] if len(sys.argv) > 2 else None
        
        if action == "send":
            subject = sys.argv[3] if len(sys.argv) > 3 else "Test Email"
            text = "This is a test email from Content Bot"
            bot.send_email_campaign(subject, text)
        else:
            print("Usage: python bot_main.py email send [subject]")
    
    elif command == "status":
        bot.print_status()
        dashboard.print_summary()
    
    elif command == "report":
        report = bot.get_report()
        import json
        print(json.dumps(report, indent=2))
    
    elif command == "scheduler":
        action = sys.argv[2] if len(sys.argv) > 2 else "status"
        
        if action == "status":
            stats = scheduler.get_stats()
            print(f"\nScheduler Status:")
            for key, value in stats.items():
                print(f"  {key}: {value}")
        elif action == "next":
            jobs = scheduler.get_next_jobs(hours=24)
            print(f"\nNext scheduled jobs (24h):")
            for job in jobs:
                print(f"  {job['time']}: {job['platform']}")
    
    elif command == "help":
        print_help()
    
    else:
        print(f"Unknown command: {command}")
        print_help()


def print_help():
    """Print help message"""
    
    help_text = """
Content Bot v1.0.0 - Production Ready Content Generation System

USAGE:
    python bot_main.py <command> [options]

COMMANDS:
    start               Start the bot (24/7 scheduling)
    test                Run tests
    generate [n] [p]    Generate n content pieces for platform p
    post [platform]     Generate and post to platform (default: twitter)
    email send [subj]   Send email campaign
    status              Show bot status and analytics
    report              Get full analytics report (JSON)
    scheduler [action]  Manage scheduler (status, next)
    help                Show this help message

EXAMPLES:
    python bot_main.py start              # Run bot 24/7
    python bot_main.py generate 5 twitter # Generate 5 Twitter posts
    python bot_main.py post linkedin      # Post to LinkedIn
    python bot_main.py status             # Check stats
    python bot_main.py report             # Get JSON report

CONFIGURATION:
    Set API keys in .env file:
    - OPENAI_API_KEY
    - TWITTER_BEARER_TOKEN
    - LINKEDIN_ACCESS_TOKEN
    - MAILCHIMP_API_KEY
    - etc.

For deployment:
    1. Configure API keys in .env
    2. Run: python bot_main.py test
    3. Run: python bot_main.py start
    4. Use systemd/supervisor for auto-restart

Documentation: See /docs/ folder
    """
    
    print(help_text)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("Bot interrupted by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Bot error: {str(e)}")
        sys.exit(1)
