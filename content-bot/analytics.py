"""
Analytics - Track metrics, revenue, and optimize content
Monitor engagement, affiliate clicks, earnings, and A/B test results
"""

import json
import logging
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from collections import defaultdict
import sqlite3

from config import Config

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=getattr(logging, Config.LOG_LEVEL),
    format=Config.LOG_FORMAT
)

class AnalyticsDB:
    """SQLite database for analytics tracking"""
    
    def __init__(self, db_path: str = None):
        self.db_path = db_path or f"{Config.DATA_PATH}/analytics.db"
        self.init_db()
    
    def init_db(self):
        """Initialize database tables"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Posts table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS posts (
                    id INTEGER PRIMARY KEY,
                    platform TEXT,
                    content_type TEXT,
                    topic TEXT,
                    post_id TEXT,
                    posted_at TIMESTAMP,
                    views INTEGER DEFAULT 0,
                    likes INTEGER DEFAULT 0,
                    comments INTEGER DEFAULT 0,
                    shares INTEGER DEFAULT 0,
                    engagement_rate REAL DEFAULT 0
                )
            """)
            
            # Affiliate clicks table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS affiliate_clicks (
                    id INTEGER PRIMARY KEY,
                    platform TEXT,
                    post_id TEXT,
                    affiliate_link TEXT,
                    tool_name TEXT,
                    clicked_at TIMESTAMP,
                    user_id TEXT,
                    conversion INTEGER DEFAULT 0,
                    revenue REAL DEFAULT 0
                )
            """)
            
            # Email subscribers table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS email_subscribers (
                    id INTEGER PRIMARY KEY,
                    email TEXT UNIQUE,
                    first_name TEXT,
                    last_name TEXT,
                    subscribed_at TIMESTAMP,
                    status TEXT,
                    last_engaged TIMESTAMP
                )
            """)
            
            # Revenue table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS revenue (
                    id INTEGER PRIMARY KEY,
                    date DATE,
                    platform TEXT,
                    affiliate_clicks INTEGER,
                    affiliate_revenue REAL,
                    email_signups INTEGER,
                    email_revenue REAL,
                    adsense_revenue REAL,
                    total_revenue REAL
                )
            """)
            
            conn.commit()
            conn.close()
            
            logger.info("Analytics database initialized")
        except Exception as e:
            logger.error(f"Error initializing analytics DB: {e}")
    
    def log_post(self, platform: str, content_type: str, topic: str, post_id: str):
        """Log a post"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO posts (platform, content_type, topic, post_id, posted_at)
                VALUES (?, ?, ?, ?, ?)
            """, (platform, content_type, topic, post_id, datetime.now()))
            
            conn.commit()
            conn.close()
            
            logger.info(f"Logged post: {platform} - {post_id}")
        except Exception as e:
            logger.error(f"Error logging post: {e}")
    
    def log_affiliate_click(self, platform: str, post_id: str, affiliate_link: str, 
                           tool_name: str, user_id: str = None):
        """Log affiliate click"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO affiliate_clicks (platform, post_id, affiliate_link, tool_name, user_id, clicked_at)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (platform, post_id, affiliate_link, tool_name, user_id or "anonymous", datetime.now()))
            
            conn.commit()
            conn.close()
            
            logger.info(f"Logged affiliate click: {tool_name} via {platform}")
        except Exception as e:
            logger.error(f"Error logging affiliate click: {e}")
    
    def log_email_signup(self, email: str, first_name: str = "", last_name: str = ""):
        """Log email signup"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT OR REPLACE INTO email_subscribers (email, first_name, last_name, subscribed_at, status)
                VALUES (?, ?, ?, ?, ?)
            """, (email, first_name, last_name, datetime.now(), "active"))
            
            conn.commit()
            conn.close()
            
            logger.info(f"Logged email signup: {email}")
        except Exception as e:
            logger.error(f"Error logging email signup: {e}")
    
    def get_daily_stats(self, date: str = None) -> Dict:
        """Get daily statistics"""
        date = date or datetime.now().strftime("%Y-%m-%d")
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Posts created today
            cursor.execute("""
                SELECT COUNT(*), platform FROM posts 
                WHERE DATE(posted_at) = ? 
                GROUP BY platform
            """, (date,))
            
            posts_by_platform = {row[1]: row[0] for row in cursor.fetchall()}
            
            # Affiliate clicks today
            cursor.execute("""
                SELECT COUNT(*), SUM(COALESCE(revenue, 0)) FROM affiliate_clicks 
                WHERE DATE(clicked_at) = ?
            """, (date,))
            
            affiliate_data = cursor.fetchone()
            affiliate_clicks = affiliate_data[0] if affiliate_data else 0
            affiliate_revenue = affiliate_data[1] if affiliate_data and affiliate_data[1] else 0
            
            # Email signups today
            cursor.execute("""
                SELECT COUNT(*) FROM email_subscribers 
                WHERE DATE(subscribed_at) = ?
            """, (date,))
            
            email_signups = cursor.fetchone()[0] if cursor.fetchone() else 0
            
            conn.close()
            
            return {
                "date": date,
                "posts_created": sum(posts_by_platform.values()),
                "posts_by_platform": posts_by_platform,
                "affiliate_clicks": affiliate_clicks,
                "affiliate_revenue": affiliate_revenue,
                "email_signups": email_signups,
                "email_revenue": email_signups * Config.REVENUE_MULTIPLIERS.get("email_signup", 1.0)
            }
        
        except Exception as e:
            logger.error(f"Error getting daily stats: {e}")
            return {}
    
    def get_weekly_stats(self) -> Dict:
        """Get weekly statistics"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            week_ago = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
            today = datetime.now().strftime("%Y-%m-%d")
            
            # Posts this week
            cursor.execute("""
                SELECT COUNT(*) FROM posts 
                WHERE DATE(posted_at) BETWEEN ? AND ?
            """, (week_ago, today))
            
            posts_count = cursor.fetchone()[0] if cursor.fetchone() else 0
            
            # Affiliate revenue this week
            cursor.execute("""
                SELECT SUM(COALESCE(revenue, 0)) FROM affiliate_clicks 
                WHERE DATE(clicked_at) BETWEEN ? AND ?
            """, (week_ago, today))
            
            affiliate_revenue = cursor.fetchone()[0] if cursor.fetchone() else 0
            
            # Email signups this week
            cursor.execute("""
                SELECT COUNT(*) FROM email_subscribers 
                WHERE DATE(subscribed_at) BETWEEN ? AND ?
            """, (week_ago, today))
            
            email_signups = cursor.fetchone()[0] if cursor.fetchone() else 0
            
            conn.close()
            
            return {
                "period": "last_7_days",
                "posts": posts_count,
                "affiliate_revenue": f"${affiliate_revenue:.2f}" if affiliate_revenue else "$0.00",
                "email_signups": email_signups,
                "email_revenue": f"${email_signups * Config.REVENUE_MULTIPLIERS.get('email_signup', 1.0):.2f}",
                "total_revenue": f"${(affiliate_revenue or 0) + (email_signups * Config.REVENUE_MULTIPLIERS.get('email_signup', 1.0)):.2f}"
            }
        
        except Exception as e:
            logger.error(f"Error getting weekly stats: {e}")
            return {}
    
    def get_monthly_stats(self) -> Dict:
        """Get monthly statistics"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            month_ago = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
            today = datetime.now().strftime("%Y-%m-%d")
            
            # Posts this month
            cursor.execute("""
                SELECT COUNT(*) FROM posts 
                WHERE DATE(posted_at) BETWEEN ? AND ?
            """, (month_ago, today))
            
            posts_count = cursor.fetchone()[0] if cursor.fetchone() else 0
            
            # Revenue breakdown
            cursor.execute("""
                SELECT SUM(COALESCE(revenue, 0)) FROM affiliate_clicks 
                WHERE DATE(clicked_at) BETWEEN ? AND ?
            """, (month_ago, today))
            
            affiliate_revenue = cursor.fetchone()[0] if cursor.fetchone() else 0
            
            # Email revenue
            cursor.execute("""
                SELECT COUNT(*) FROM email_subscribers 
                WHERE DATE(subscribed_at) BETWEEN ? AND ?
            """, (month_ago, today))
            
            email_signups = cursor.fetchone()[0] if cursor.fetchone() else 0
            
            conn.close()
            
            email_revenue = email_signups * Config.REVENUE_MULTIPLIERS.get("email_signup", 1.0)
            total = (affiliate_revenue or 0) + email_revenue
            
            return {
                "period": "last_30_days",
                "posts": posts_count,
                "affiliate_clicks": "See daily breakdown",
                "affiliate_revenue": f"${affiliate_revenue:.2f}" if affiliate_revenue else "$0.00",
                "email_signups": email_signups,
                "email_revenue": f"${email_revenue:.2f}",
                "total_revenue": f"${total:.2f}",
                "daily_average": f"${total / 30:.2f}"
            }
        
        except Exception as e:
            logger.error(f"Error getting monthly stats: {e}")
            return {}


class PerformanceAnalytics:
    """Analyze content performance and A/B testing"""
    
    def __init__(self):
        self.db = AnalyticsDB()
        self.performance_data = {}
    
    def track_engagement(self, post_id: str, views: int, likes: int, comments: int, shares: int):
        """Track engagement metrics for a post"""
        if views > 0:
            engagement_rate = ((likes + comments + shares) / views) * 100
        else:
            engagement_rate = 0
        
        self.performance_data[post_id] = {
            "views": views,
            "likes": likes,
            "comments": comments,
            "shares": shares,
            "engagement_rate": engagement_rate,
            "tracked_at": datetime.now().isoformat()
        }
        
        logger.info(f"Tracked engagement for {post_id}: {engagement_rate:.2f}% engagement rate")
    
    def get_top_performing_content(self, limit: int = 5) -> List[Dict]:
        """Get top performing posts"""
        sorted_posts = sorted(
            self.performance_data.items(),
            key=lambda x: x[1].get("engagement_rate", 0),
            reverse=True
        )
        
        return [
            {
                "post_id": post_id,
                **data
            }
            for post_id, data in sorted_posts[:limit]
        ]
    
    def get_content_by_topic(self, topic: str) -> List[Dict]:
        """Get all content for a specific topic"""
        # Query database for content by topic
        try:
            conn = sqlite3.connect(self.db.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT post_id, platform, views, likes, comments, shares 
                FROM posts 
                WHERE topic = ?
            """, (topic,))
            
            results = [
                {
                    "post_id": row[0],
                    "platform": row[1],
                    "views": row[2],
                    "likes": row[3],
                    "comments": row[4],
                    "shares": row[5]
                }
                for row in cursor.fetchall()
            ]
            
            conn.close()
            return results
        
        except Exception as e:
            logger.error(f"Error getting content by topic: {e}")
            return []
    
    def get_platform_performance(self) -> Dict[str, Dict]:
        """Compare performance across platforms"""
        try:
            conn = sqlite3.connect(self.db.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT platform, 
                       COUNT(*) as posts,
                       ROUND(AVG(views), 0) as avg_views,
                       ROUND(AVG(engagement_rate), 2) as avg_engagement,
                       SUM(likes) as total_likes
                FROM posts
                GROUP BY platform
            """)
            
            results = {}
            for row in cursor.fetchall():
                results[row[0]] = {
                    "posts": row[1],
                    "avg_views": row[2],
                    "avg_engagement": row[3],
                    "total_likes": row[4]
                }
            
            conn.close()
            return results
        
        except Exception as e:
            logger.error(f"Error getting platform performance: {e}")
            return {}


class AffiliateTracker:
    """Track affiliate link clicks and conversions"""
    
    def __init__(self):
        self.db = AnalyticsDB()
        self.clicks = defaultdict(int)
        self.conversions = defaultdict(int)
        self.revenue = defaultdict(float)
    
    def track_click(self, affiliate_link: str, tool_name: str, platform: str, post_id: str):
        """Track affiliate link click"""
        self.clicks[tool_name] += 1
        self.db.log_affiliate_click(platform, post_id, affiliate_link, tool_name)
        
        logger.info(f"Affiliate click tracked: {tool_name}")
    
    def track_conversion(self, tool_name: str, revenue: float):
        """Track affiliate conversion and revenue"""
        self.conversions[tool_name] += 1
        self.revenue[tool_name] += revenue
        
        logger.info(f"Affiliate conversion: {tool_name} - ${revenue:.2f}")
    
    def get_affiliate_stats(self) -> Dict:
        """Get affiliate performance statistics"""
        try:
            conn = sqlite3.connect(self.db.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT tool_name, COUNT(*) as clicks, SUM(COALESCE(revenue, 0)) as revenue
                FROM affiliate_clicks
                GROUP BY tool_name
                ORDER BY clicks DESC
            """)
            
            stats = {}
            total_clicks = 0
            total_revenue = 0
            
            for row in cursor.fetchall():
                tool_name = row[0]
                clicks = row[1]
                revenue = row[2] or 0
                
                stats[tool_name] = {
                    "clicks": clicks,
                    "revenue": f"${revenue:.2f}",
                    "conversion_rate": "N/A"
                }
                
                total_clicks += clicks
                total_revenue += revenue
            
            conn.close()
            
            return {
                "by_tool": stats,
                "total_clicks": total_clicks,
                "total_revenue": f"${total_revenue:.2f}",
                "average_revenue_per_click": f"${total_revenue / total_clicks:.2f}" if total_clicks > 0 else "$0.00"
            }
        
        except Exception as e:
            logger.error(f"Error getting affiliate stats: {e}")
            return {}


class DashboardGenerator:
    """Generate analytics dashboard"""
    
    def __init__(self):
        self.db = AnalyticsDB()
        self.performance = PerformanceAnalytics()
        self.affiliate = AffiliateTracker()
    
    def generate_daily_report(self) -> Dict:
        """Generate daily analytics report"""
        daily_stats = self.db.get_daily_stats()
        
        report = {
            "period": "Today",
            "timestamp": datetime.now().isoformat(),
            **daily_stats,
            "affiliate_stats": self.affiliate.get_affiliate_stats(),
            "top_performing": self.performance.get_top_performing_content(3)
        }
        
        return report
    
    def generate_weekly_report(self) -> Dict:
        """Generate weekly analytics report"""
        weekly_stats = self.db.get_weekly_stats()
        platform_stats = self.performance.get_platform_performance()
        
        report = {
            "period": "This Week",
            "timestamp": datetime.now().isoformat(),
            **weekly_stats,
            "platform_breakdown": platform_stats,
            "top_tools": list(self.affiliate.get_affiliate_stats().get("by_tool", {}).items())[:5]
        }
        
        return report
    
    def generate_monthly_report(self) -> Dict:
        """Generate monthly analytics report"""
        monthly_stats = self.db.get_monthly_stats()
        
        report = {
            "period": "This Month",
            "timestamp": datetime.now().isoformat(),
            **monthly_stats,
            "revenue_forecast": self._forecast_revenue()
        }
        
        return report
    
    def _forecast_revenue(self) -> Dict:
        """Forecast monthly revenue based on current trends"""
        daily_stats = self.db.get_daily_stats()
        
        avg_daily_revenue = float(daily_stats.get("affiliate_revenue", 0)) + \
                          daily_stats.get("email_revenue", 0)
        
        month_forecast = avg_daily_revenue * 30
        
        return {
            "forecast_daily": f"${avg_daily_revenue:.2f}",
            "forecast_monthly": f"${month_forecast:.2f}",
            "forecast_yearly": f"${month_forecast * 12:.2f}"
        }
    
    def export_dashboard_html(self, filename: str = None) -> str:
        """Export dashboard as HTML"""
        filename = filename or f"{Config.DATA_PATH}/dashboard.html"
        
        daily = self.generate_daily_report()
        weekly = self.generate_weekly_report()
        monthly = self.generate_monthly_report()
        
        html = f"""
        <html>
            <head>
                <title>Content Bot Analytics Dashboard</title>
                <style>
                    body {{ font-family: Arial, sans-serif; margin: 20px; }}
                    .section {{ background: #f5f5f5; padding: 20px; margin: 10px 0; border-radius: 8px; }}
                    .metric {{ display: inline-block; margin: 10px 20px; }}
                    h1, h2 {{ color: #333; }}
                    .value {{ font-size: 28px; font-weight: bold; color: #4CAF50; }}
                </style>
            </head>
            <body>
                <h1>📊 Content Bot Analytics Dashboard</h1>
                <p>Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                
                <div class="section">
                    <h2>Today</h2>
                    <div class="metric">
                        <div>Posts Created</div>
                        <div class="value">{daily.get('posts_created', 0)}</div>
                    </div>
                    <div class="metric">
                        <div>Affiliate Clicks</div>
                        <div class="value">{daily.get('affiliate_clicks', 0)}</div>
                    </div>
                    <div class="metric">
                        <div>Email Signups</div>
                        <div class="value">{daily.get('email_signups', 0)}</div>
                    </div>
                </div>
                
                <div class="section">
                    <h2>This Week</h2>
                    <div class="metric">
                        <div>Revenue</div>
                        <div class="value">{weekly.get('total_revenue', '$0.00')}</div>
                    </div>
                    <div class="metric">
                        <div>Email Growth</div>
                        <div class="value">{weekly.get('email_signups', 0)}</div>
                    </div>
                </div>
                
                <div class="section">
                    <h2>This Month</h2>
                    <div class="metric">
                        <div>Total Revenue</div>
                        <div class="value">{monthly.get('total_revenue', '$0.00')}</div>
                    </div>
                    <div class="metric">
                        <div>Posts</div>
                        <div class="value">{monthly.get('posts', 0)}</div>
                    </div>
                </div>
            </body>
        </html>
        """
        
        with open(filename, 'w') as f:
            f.write(html)
        
        logger.info(f"Dashboard exported to {filename}")
        return html


def quick_test():
    """Test analytics system"""
    print("Testing Analytics System...\n")
    
    db = AnalyticsDB()
    dashboard = DashboardGenerator()
    
    print("Daily Report:")
    daily = dashboard.generate_daily_report()
    print(json.dumps(daily, indent=2, default=str))
    
    print("\n✓ Analytics system test complete")


if __name__ == "__main__":
    quick_test()
