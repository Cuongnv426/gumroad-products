"""
Analytics & Revenue Tracking
Track posts, engagement, and affiliate earnings
"""

import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List
from collections import defaultdict
from config import AFFILIATE_COMMISSION_RATES, AFFILIATE_LINKS

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AffiliateTracker:
    """Track affiliate link clicks and conversions"""
    
    def __init__(self):
        self.clicks = []
        self.conversions = []
        self.earnings = []
        
    def track_click(self, affiliate_product: str, utm_source: str = "content-bot") -> str:
        """Track affiliate link click"""
        
        if affiliate_product not in AFFILIATE_LINKS:
            logger.warning(f"Unknown affiliate product: {affiliate_product}")
            return None
        
        link = AFFILIATE_LINKS[affiliate_product]
        
        click_data = {
            "product": affiliate_product,
            "link": link,
            "timestamp": datetime.now().isoformat(),
            "utm_source": utm_source
        }
        
        self.clicks.append(click_data)
        logger.info(f"✓ Tracked click: {affiliate_product}")
        
        return link
    
    def track_conversion(self, affiliate_product: str, sale_amount: float) -> Dict:
        """Track successful affiliate conversion"""
        
        commission_rate = AFFILIATE_COMMISSION_RATES.get(affiliate_product, 0.15)
        commission = sale_amount * commission_rate
        
        conversion_data = {
            "product": affiliate_product,
            "sale_amount": sale_amount,
            "commission_rate": commission_rate,
            "commission": commission,
            "timestamp": datetime.now().isoformat()
        }
        
        self.conversions.append(conversion_data)
        self.earnings.append(conversion_data)
        
        logger.info(f"✓ Conversion: {affiliate_product} - ${commission:.2f}")
        
        return {
            "product": affiliate_product,
            "earnings": commission
        }
    
    def get_affiliate_stats(self) -> Dict:
        """Get affiliate statistics"""
        
        stats = {
            "total_clicks": len(self.clicks),
            "total_conversions": len(self.conversions),
            "total_earnings": sum(e.get("commission", 0) for e in self.earnings),
            "by_product": {}
        }
        
        for product in AFFILIATE_LINKS:
            product_clicks = sum(1 for c in self.clicks if c["product"] == product)
            product_conversions = sum(1 for c in self.conversions if c["product"] == product)
            product_earnings = sum(e.get("commission", 0) for e in self.earnings 
                                  if e["product"] == product)
            
            stats["by_product"][product] = {
                "clicks": product_clicks,
                "conversions": product_conversions,
                "earnings": product_earnings,
                "conversion_rate": (product_conversions / product_clicks * 100) 
                                  if product_clicks > 0 else 0
            }
        
        return stats


class PostAnalytics:
    """Track post performance metrics"""
    
    def __init__(self):
        self.posts = []
        self.engagement = defaultdict(lambda: {
            "likes": 0, "comments": 0, "shares": 0, "views": 0
        })
        
    def log_post(self, post_id: str, platform: str, content_id: str) -> Dict:
        """Log a posted piece of content"""
        
        post_data = {
            "post_id": post_id,
            "platform": platform,
            "content_id": content_id,
            "timestamp": datetime.now().isoformat(),
            "status": "active"
        }
        
        self.posts.append(post_data)
        logger.info(f"✓ Post logged: {platform} - {post_id}")
        
        return post_data
    
    def log_engagement(self, post_id: str, engagement_type: str, count: int = 1):
        """Log engagement metric (likes, comments, shares)"""
        
        if engagement_type not in ["likes", "comments", "shares", "views"]:
            logger.warning(f"Unknown engagement type: {engagement_type}")
            return
        
        self.engagement[post_id][engagement_type] += count
        logger.info(f"✓ Engagement: {post_id} - {engagement_type} +{count}")
    
    def get_post_stats(self, platform: str = None) -> Dict:
        """Get post statistics"""
        
        stats = {
            "total_posts": len(self.posts),
            "by_platform": defaultdict(lambda: {"posts": 0, "engagement": {}}),
            "total_engagement": {
                "likes": sum(e["likes"] for e in self.engagement.values()),
                "comments": sum(e["comments"] for e in self.engagement.values()),
                "shares": sum(e["shares"] for e in self.engagement.values()),
                "views": sum(e["views"] for e in self.engagement.values())
            }
        }
        
        for post in self.posts:
            p = post["platform"]
            stats["by_platform"][p]["posts"] += 1
            
            if post["post_id"] in self.engagement:
                eng = self.engagement[post["post_id"]]
                stats["by_platform"][p]["engagement"] = {
                    "likes": stats["by_platform"][p]["engagement"].get("likes", 0) + eng["likes"],
                    "comments": stats["by_platform"][p]["engagement"].get("comments", 0) + eng["comments"],
                    "shares": stats["by_platform"][p]["engagement"].get("shares", 0) + eng["shares"],
                }
        
        return dict(stats)
    
    def get_best_posts(self, top_n: int = 5) -> List[Dict]:
        """Get top performing posts"""
        
        ranked = sorted(
            self.posts,
            key=lambda p: sum(self.engagement[p["post_id"]].values()),
            reverse=True
        )
        
        return ranked[:top_n]


class RevenueCalculator:
    """Calculate total revenue from multiple streams"""
    
    def __init__(self):
        self.affiliate_tracker = AffiliateTracker()
        self.post_analytics = PostAnalytics()
        
    def get_revenue_summary(self, days: int = 7) -> Dict:
        """Get revenue summary for period"""
        
        affiliate_stats = self.affiliate_tracker.get_affiliate_stats()
        post_stats = self.post_analytics.get_post_stats()
        
        summary = {
            "period_days": days,
            "period_start": (datetime.now() - timedelta(days=days)).isoformat(),
            "revenue_streams": {
                "affiliate_commissions": affiliate_stats["total_earnings"],
                "sponsored_posts": 0,  # Can be integrated
                "email_signups": 0,  # Can be integrated
                "digital_products": 0  # Can be integrated
            },
            "total_revenue": affiliate_stats["total_earnings"],
            "metrics": {
                "total_posts": post_stats["total_posts"],
                "total_engagement": post_stats["total_engagement"],
                "affiliate_conversions": affiliate_stats["total_conversions"]
            }
        }
        
        return summary
    
    def get_daily_revenue(self) -> Dict:
        """Get today's revenue"""
        
        today_str = datetime.now().strftime("%Y-%m-%d")
        today_earnings = [
            e.get("commission", 0) for e in self.affiliate_tracker.earnings
            if e["timestamp"].startswith(today_str)
        ]
        
        return {
            "date": today_str,
            "total": sum(today_earnings),
            "conversions": len(today_earnings),
            "average_per_conversion": sum(today_earnings) / len(today_earnings) 
                                       if today_earnings else 0
        }
    
    def get_revenue_forecast(self) -> Dict:
        """Forecast revenue for month"""
        
        daily = self.get_daily_revenue()
        projected_monthly = daily["total"] * 30
        
        return {
            "daily_average": daily["total"],
            "projected_monthly": projected_monthly,
            "projected_annual": projected_monthly * 12
        }
    
    def get_full_report(self) -> Dict:
        """Get complete analytics report"""
        
        return {
            "timestamp": datetime.now().isoformat(),
            "affiliate_stats": self.affiliate_tracker.get_affiliate_stats(),
            "post_stats": self.post_analytics.get_post_stats(),
            "revenue_summary": self.get_revenue_summary(days=7),
            "daily_revenue": self.get_daily_revenue(),
            "forecast": self.get_revenue_forecast(),
            "top_posts": self.post_analytics.get_best_posts(top_n=5)
        }


class AnalyticsDashboard:
    """Dashboard for monitoring bot performance"""
    
    def __init__(self):
        self.calculator = RevenueCalculator()
    
    def get_dashboard_data(self) -> Dict:
        """Get all data for dashboard display"""
        
        report = self.calculator.get_full_report()
        
        dashboard = {
            "status": "running",
            "timestamp": report["timestamp"],
            "key_metrics": {
                "total_revenue": report["revenue_summary"]["total_revenue"],
                "daily_revenue": report["daily_revenue"]["total"],
                "monthly_projection": report["forecast"]["projected_monthly"],
                "posts_made": report["post_stats"]["total_posts"],
                "conversions": report["affiliate_stats"]["total_conversions"]
            },
            "detailed_report": report
        }
        
        return dashboard
    
    def export_json(self, filepath: str = "analytics.json"):
        """Export analytics to JSON"""
        
        data = self.get_dashboard_data()
        
        with open(filepath, "w") as f:
            json.dump(data, f, indent=2)
        
        logger.info(f"✓ Analytics exported to {filepath}")
        return filepath
    
    def print_summary(self):
        """Print analytics summary to console"""
        
        data = self.get_dashboard_data()
        metrics = data["key_metrics"]
        
        print("\n" + "=" * 60)
        print("CONTENT BOT ANALYTICS SUMMARY")
        print("=" * 60)
        print(f"\nTODAY'S PERFORMANCE:")
        print(f"  Revenue: ${metrics['daily_revenue']:.2f}")
        print(f"  Posts Made: {metrics['posts_made']}")
        print(f"  Conversions: {metrics['conversions']}")
        print(f"\nPROJECTIONS:")
        print(f"  Monthly Revenue: ${metrics['monthly_projection']:.2f}")
        print(f"  Annual Revenue: ${metrics['monthly_projection'] * 12:.2f}")
        print("\n" + "=" * 60 + "\n")


# Initialize analytics
affiliate_tracker = AffiliateTracker()
post_analytics = PostAnalytics()
revenue_calculator = RevenueCalculator()
dashboard = AnalyticsDashboard()

if __name__ == "__main__":
    print("Analytics system initialized")
    
    # Test tracking
    affiliate_tracker.track_click("chatgpt")
    affiliate_tracker.track_conversion("chatgpt", 100.00)
    
    post_analytics.log_post("post_123", "twitter", "content_456")
    post_analytics.log_engagement("post_123", "likes", 50)
    
    # Print summary
    dashboard.print_summary()
