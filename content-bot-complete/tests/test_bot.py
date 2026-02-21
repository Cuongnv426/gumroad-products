#!/usr/bin/env python3
"""
Content Bot Test Suite
Comprehensive tests for all components
"""

import sys
import unittest
from io import StringIO
import logging

# Setup test logging
logging.basicConfig(level=logging.INFO)

class TestContentEngine(unittest.TestCase):
    """Test content generation"""
    
    def setUp(self):
        from content_engine import ContentEngine
        self.engine = ContentEngine()
    
    def test_initialization(self):
        """Test engine initializes"""
        self.assertIsNotNone(self.engine)
        self.assertEqual(self.engine.model, "gpt-3.5-turbo")
    
    def test_content_history(self):
        """Test content history tracking"""
        self.assertEqual(len(self.engine.content_history), 0)
    
    def test_similarity_score(self):
        """Test similarity calculation"""
        score = self.engine._similarity_score(
            "This is a test",
            "This is a test"
        )
        self.assertEqual(score, 1.0)
        
        score = self.engine._similarity_score(
            "Hello world",
            "Goodbye world"
        )
        self.assertLess(score, 1.0)


class TestConfigSettings(unittest.TestCase):
    """Test configuration"""
    
    def setUp(self):
        from config import NICHES, AFFILIATE_LINKS, POSTING_SCHEDULE
        self.niches = NICHES
        self.affiliate_links = AFFILIATE_LINKS
        self.schedule = POSTING_SCHEDULE
    
    def test_niches_configured(self):
        """Test niches are configured"""
        self.assertGreater(len(self.niches), 0)
        self.assertIn("AI_TOOLS", self.niches)
    
    def test_affiliate_links_configured(self):
        """Test affiliate links are configured"""
        self.assertGreater(len(self.affiliate_links), 0)
        self.assertIn("chatgpt", self.affiliate_links)
    
    def test_schedule_configured(self):
        """Test schedule is configured"""
        self.assertGreater(len(self.schedule), 0)
        self.assertTrue(self.schedule["twitter"]["enabled"])


class TestAnalytics(unittest.TestCase):
    """Test analytics system"""
    
    def setUp(self):
        from analytics import AffiliateTracker, PostAnalytics
        self.affiliate = AffiliateTracker()
        self.posts = PostAnalytics()
    
    def test_affiliate_tracker_init(self):
        """Test affiliate tracker initializes"""
        self.assertEqual(len(self.affiliate.clicks), 0)
        self.assertEqual(len(self.affiliate.conversions), 0)
    
    def test_track_affiliate_click(self):
        """Test tracking affiliate click"""
        link = self.affiliate.track_click("chatgpt")
        self.assertIsNotNone(link)
        self.assertEqual(len(self.affiliate.clicks), 1)
    
    def test_post_analytics_init(self):
        """Test post analytics initializes"""
        self.assertEqual(len(self.posts.posts), 0)


class TestEmailSystem(unittest.TestCase):
    """Test email system"""
    
    def setUp(self):
        from email_system import EmailSequences
        self.sequences = EmailSequences()
    
    def test_welcome_sequence(self):
        """Test welcome sequence templates"""
        sequence = self.sequences.welcome_sequence()
        self.assertEqual(len(sequence), 3)
        self.assertEqual(sequence[0]["day"], 0)
    
    def test_sequence_has_content(self):
        """Test sequences have content"""
        sequence = self.sequences.welcome_sequence()
        for email in sequence:
            self.assertIn("subject", email)
            self.assertIn("content", email)


class TestScheduler(unittest.TestCase):
    """Test scheduler"""
    
    def setUp(self):
        from scheduler import ContentScheduler
        self.scheduler = ContentScheduler()
    
    def test_scheduler_init(self):
        """Test scheduler initializes"""
        self.assertGreater(self.scheduler.job_count, 0)
    
    def test_scheduler_has_jobs(self):
        """Test scheduler has scheduled jobs"""
        jobs = self.scheduler.schedule.get_jobs()
        self.assertGreater(len(jobs), 0)
    
    def test_get_next_jobs(self):
        """Test getting next scheduled jobs"""
        jobs = self.scheduler.get_next_jobs(hours=24)
        self.assertIsInstance(jobs, list)


class TestIntegration(unittest.TestCase):
    """Integration tests"""
    
    def test_imports_work(self):
        """Test all modules import successfully"""
        try:
            from config import *
            from content_engine import ContentEngine
            from platform_manager import PlatformManager
            from scheduler import ContentScheduler
            from email_system import EmailManager
            from analytics import AffiliateTracker, RevenueCalculator
            print("✓ All imports successful")
        except ImportError as e:
            self.fail(f"Import failed: {e}")
    
    def test_bot_initialization(self):
        """Test bot can initialize"""
        try:
            from bot_main import ContentBot
            bot = ContentBot()
            self.assertIsNotNone(bot)
            self.assertEqual(bot.version, "1.0.0")
            print("✓ Bot initialized successfully")
        except Exception as e:
            self.fail(f"Bot initialization failed: {e}")


def run_tests():
    """Run all tests"""
    
    print("\n" + "=" * 70)
    print("CONTENT BOT - TEST SUITE")
    print("=" * 70 + "\n")
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test classes
    suite.addTests(loader.loadTestsFromTestCase(TestContentEngine))
    suite.addTests(loader.loadTestsFromTestCase(TestConfigSettings))
    suite.addTests(loader.loadTestsFromTestCase(TestAnalytics))
    suite.addTests(loader.loadTestsFromTestCase(TestEmailSystem))
    suite.addTests(loader.loadTestsFromTestCase(TestScheduler))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegration))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    print(f"Tests run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print("=" * 70 + "\n")
    
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(run_tests())
