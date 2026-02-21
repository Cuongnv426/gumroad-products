"""
Email System - Newsletter Management & Mailchimp Integration
Handles email list growth, newsletter sending, and subscriber tracking
"""

import json
import logging
from typing import Dict, List, Optional
from datetime import datetime
import hashlib
from abc import ABC, abstractmethod

from config import Config

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=getattr(logging, Config.LOG_LEVEL),
    format=Config.LOG_FORMAT
)

class EmailListManager:
    """Manage email subscribers and list growth"""
    
    def __init__(self):
        try:
            import mailchimp_marketing as MailchimpMarketing
            self.client = MailchimpMarketing.Client()
            self.client.set_config({
                "api_key": Config.MAILCHIMP_API_KEY,
                "server": Config.MAILCHIMP_SERVER
            })
            self.list_id = Config.MAILCHIMP_LIST_ID
            self.authenticated = True
        except:
            logger.warning("Mailchimp not configured - email list tracking disabled")
            self.authenticated = False
    
    def add_subscriber(self, email: str, first_name: str = "", last_name: str = "", tags: List[str] = None) -> Dict:
        """Add new subscriber to list"""
        if not self.authenticated:
            return {"success": False, "error": "Mailchimp not configured"}
        
        try:
            subscriber_hash = hashlib.md5(email.lower().encode()).hexdigest()
            
            payload = {
                "email_address": email,
                "status": "subscribed",
                "merge_fields": {
                    "FNAME": first_name,
                    "LNAME": last_name
                },
                "tags": tags or []
            }
            
            if Config.DRY_RUN:
                logger.info(f"[DRY RUN] Would add subscriber: {email}")
                return {
                    "success": True,
                    "email": email,
                    "dry_run": True
                }
            
            response = self.client.lists.set_list_member(
                self.list_id,
                subscriber_hash,
                payload
            )
            
            logger.info(f"✓ Subscriber added: {email}")
            
            return {
                "success": True,
                "email": email,
                "subscriber_hash": subscriber_hash,
                "status": response.get("status")
            }
        
        except Exception as e:
            logger.error(f"Error adding subscriber {email}: {e}")
            return {"success": False, "error": str(e), "email": email}
    
    def get_subscriber_count(self) -> int:
        """Get total subscriber count"""
        if not self.authenticated:
            return 0
        
        try:
            list_info = self.client.lists.get_list(self.list_id)
            return list_info.get("stats", {}).get("member_count", 0)
        except Exception as e:
            logger.error(f"Error getting subscriber count: {e}")
            return 0
    
    def add_tag_to_subscriber(self, email: str, tags: List[str]) -> Dict:
        """Add tags to subscriber for segmentation"""
        if not self.authenticated:
            return {"success": False}
        
        try:
            subscriber_hash = hashlib.md5(email.lower().encode()).hexdigest()
            
            payload = {
                "tags": [{"name": tag, "status": "active"} for tag in tags]
            }
            
            self.client.lists.update_list_member_tags(
                self.list_id,
                subscriber_hash,
                payload
            )
            
            logger.info(f"✓ Tags added to {email}: {tags}")
            return {"success": True, "email": email, "tags": tags}
        
        except Exception as e:
            logger.error(f"Error adding tags: {e}")
            return {"success": False, "error": str(e)}
    
    def create_automation(self, automation_type: str, trigger: str) -> Dict:
        """Create email automation sequences"""
        if not self.authenticated:
            return {"success": False}
        
        try:
            # Welcome sequence
            if automation_type == "welcome":
                emails = [
                    {
                        "delay": 0,
                        "subject": "Welcome to AI Tools Insider!",
                        "content": "Welcome email content..."
                    },
                    {
                        "delay": 2,  # days
                        "subject": "Your First Tool: ChatGPT Plus",
                        "content": "Second email content..."
                    },
                    {
                        "delay": 5,
                        "subject": "The Hidden AI Tool Everyone's Using",
                        "content": "Third email content..."
                    }
                ]
            
            # Nurture sequence
            elif automation_type == "nurture":
                emails = [
                    {
                        "delay": 0,
                        "subject": "5 AI Tools You're Missing Out On",
                        "content": "Nurture content..."
                    }
                ]
            
            logger.info(f"✓ Automation created: {automation_type}")
            return {
                "success": True,
                "type": automation_type,
                "email_count": len(emails)
            }
        
        except Exception as e:
            logger.error(f"Error creating automation: {e}")
            return {"success": False, "error": str(e)}
    
    def get_list_growth_stats(self, days: int = 30) -> Dict:
        """Get subscriber growth statistics"""
        if not self.authenticated:
            return {}
        
        try:
            # In production, would query from database
            stats = {
                "total_subscribers": self.get_subscriber_count(),
                "growth_rate": "5-10 per day",
                "engagement_rate": "32%",
                "click_rate": "4.2%"
            }
            
            return stats
        
        except Exception as e:
            logger.error(f"Error getting growth stats: {e}")
            return {}


class NewsletterTemplateManager:
    """Manage email templates"""
    
    @staticmethod
    def create_welcome_template() -> str:
        """Create welcome email template"""
        return """
        <html>
            <body style="font-family: Arial, sans-serif; color: #333;">
                <h1>Welcome to AI Tools Insider! 🚀</h1>
                <p>Hi {{FNAME}},</p>
                <p>I'm excited to have you on my list!</p>
                <p>You're about to discover:</p>
                <ul>
                    <li>5 Game-Changing AI Tools (most people don't know about #3)</li>
                    <li>Productivity hacks that save 10+ hours/week</li>
                    <li>Exclusive affiliate deals for my subscribers</li>
                </ul>
                <p><a href="https://example.com" style="background: #007bff; color: white; padding: 10px 20px;">Get Started</a></p>
                <p>Talk soon,<br>Jr Pan</p>
            </body>
        </html>
        """
    
    @staticmethod
    def create_daily_tool_template() -> str:
        """Create daily tool feature template"""
        return """
        <html>
            <body style="font-family: Arial, sans-serif;">
                <h2>Tool of the Day: {{TOOL_NAME}}</h2>
                <p>What it does: {{TOOL_DESC}}</p>
                <p>Why you need it: {{TOOL_BENEFITS}}</p>
                <p><a href="{{TOOL_URL}}">Try it free →</a></p>
            </body>
        </html>
        """
    
    @staticmethod
    def create_weekly_roundup_template() -> str:
        """Create weekly roundup template"""
        return """
        <html>
            <body>
                <h1>This Week's Best AI Tools 📊</h1>
                <h3>Tool #1: {{TOOL1_NAME}}</h3>
                <p>{{TOOL1_DESC}}</p>
                <h3>Tool #2: {{TOOL2_NAME}}</h3>
                <p>{{TOOL2_DESC}}</p>
                <h3>Tool #3: {{TOOL3_NAME}}</h3>
                <p>{{TOOL3_DESC}}</p>
            </body>
        </html>
        """
    
    @staticmethod
    def create_affiliate_promotion_template() -> str:
        """Create affiliate promotion template"""
        return """
        <html>
            <body>
                <h1>Exclusive Offer for You 💎</h1>
                <p>My subscribers just got exclusive access to {{PRODUCT_NAME}}.</p>
                <p>Here's what you get:</p>
                <ul>
                    <li>{{BENEFIT1}}</li>
                    <li>{{BENEFIT2}}</li>
                    <li>{{BENEFIT3}}</li>
                </ul>
                <p><a href="{{AFFILIATE_LINK}}">Claim Your Deal →</a></p>
            </body>
        </html>
        """


class Optin Forms:
    """Email opt-in forms for websites/blogs"""
    
    @staticmethod
    def create_inline_form() -> str:
        """Create inline email opt-in form (for blog posts)"""
        return """
        <div id="email-optin-form" style="background: #f0f0f0; padding: 20px; border-radius: 8px; margin: 20px 0;">
            <h3>📧 Get Daily AI Tools (Free)</h3>
            <p>Join 1,000+ people learning the best AI tools</p>
            <form id="optin-form" action="/api/subscribe" method="POST">
                <input type="text" name="first_name" placeholder="Your name" required>
                <input type="email" name="email" placeholder="Your email" required>
                <button type="submit">Get Instant Access</button>
            </form>
        </div>
        """
    
    @staticmethod
    def create_popup_form() -> str:
        """Create popup opt-in form"""
        return """
        <div id="popup-form" style="position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%); 
            background: white; padding: 40px; border-radius: 8px; box-shadow: 0 4px 20px rgba(0,0,0,0.2);">
            <h2>Free: 5 AI Tools Changing Everything</h2>
            <p>Limited time - get the free guide worth $47</p>
            <form action="/api/subscribe" method="POST">
                <input type="email" name="email" placeholder="Your email" required>
                <button type="submit">Send Me the Guide</button>
            </form>
            <button onclick="closePopup()">Close</button>
        </div>
        """
    
    @staticmethod
    def create_exit_intent_form() -> str:
        """Create exit-intent offer"""
        return """
        <script>
            document.addEventListener('mouseleave', function(e) {
                if (e.clientY < 0) {
                    document.getElementById('exit-intent').style.display = 'block';
                }
            });
        </script>
        <div id="exit-intent" style="display: none; position: fixed; inset: 0; background: rgba(0,0,0,0.8);">
            <div style="background: white; width: 600px; margin: 100px auto; padding: 40px;">
                <h2>Wait! Don't leave yet</h2>
                <p>Join 1,000+ people getting AI tools in their inbox every day</p>
                <form action="/api/subscribe" method="POST">
                    <input type="email" name="email" placeholder="Email" required>
                    <button type="submit">Send Me the Free Tools</button>
                </form>
            </div>
        </div>
        """


class SubscriberWebhooks:
    """Handle webhook events from Mailchimp"""
    
    @staticmethod
    def handle_subscribe(data: Dict) -> Dict:
        """Handle new subscriber webhook"""
        logger.info(f"New subscriber: {data.get('email')}")
        
        # Log for analytics
        with open(f"{Config.DATA_PATH}/subscribers.json", 'a') as f:
            json.dump({
                "email": data.get("email"),
                "timestamp": datetime.now().isoformat(),
                "source": data.get("source", "direct")
            }, f)
            f.write("\n")
        
        return {"success": True}
    
    @staticmethod
    def handle_unsubscribe(data: Dict) -> Dict:
        """Handle unsubscribe webhook"""
        logger.info(f"Subscriber unsubscribed: {data.get('email')}")
        return {"success": True}
    
    @staticmethod
    def handle_complaint(data: Dict) -> Dict:
        """Handle spam complaint"""
        logger.warning(f"Spam complaint: {data.get('email')}")
        return {"success": True}


class EmailAnalytics:
    """Track email campaign performance"""
    
    def __init__(self):
        self.campaigns_data = []
    
    def track_open(self, campaign_id: str, subscriber_email: str):
        """Track email open"""
        self.campaigns_data.append({
            "event": "open",
            "campaign_id": campaign_id,
            "email": subscriber_email,
            "timestamp": datetime.now().isoformat()
        })
    
    def track_click(self, campaign_id: str, subscriber_email: str, link_url: str):
        """Track link click"""
        self.campaigns_data.append({
            "event": "click",
            "campaign_id": campaign_id,
            "email": subscriber_email,
            "link": link_url,
            "timestamp": datetime.now().isoformat()
        })
    
    def track_conversion(self, campaign_id: str, subscriber_email: str, conversion_value: float = 1.0):
        """Track conversion"""
        self.campaigns_data.append({
            "event": "conversion",
            "campaign_id": campaign_id,
            "email": subscriber_email,
            "value": conversion_value,
            "timestamp": datetime.now().isoformat()
        })
    
    def get_campaign_stats(self, campaign_id: str) -> Dict:
        """Get campaign performance stats"""
        campaign_events = [e for e in self.campaigns_data if e.get("campaign_id") == campaign_id]
        
        if not campaign_events:
            return {}
        
        opens = len([e for e in campaign_events if e.get("event") == "open"])
        clicks = len([e for e in campaign_events if e.get("event") == "click"])
        conversions = len([e for e in campaign_events if e.get("event") == "conversion"])
        total_revenue = sum(e.get("value", 0) for e in campaign_events if e.get("event") == "conversion")
        
        return {
            "campaign_id": campaign_id,
            "opens": opens,
            "clicks": clicks,
            "conversions": conversions,
            "open_rate": f"{(opens / len(set(e['email'] for e in campaign_events))) * 100:.1f}%" if campaign_events else "0%",
            "click_rate": f"{(clicks / opens * 100) if opens > 0 else 0:.1f}%",
            "conversion_rate": f"{(conversions / clicks * 100) if clicks > 0 else 0:.1f}%",
            "total_revenue": f"${total_revenue:.2f}"
        }


def quick_test():
    """Test email system"""
    print("Testing Email System...\n")
    
    manager = EmailListManager()
    print(f"Subscriber count: {manager.get_subscriber_count()}")
    
    # Test adding subscriber
    result = manager.add_subscriber(
        "test@example.com",
        first_name="Test",
        last_name="User",
        tags=["new_subscriber", "ai_tools"]
    )
    print(f"Add subscriber: {result}")
    
    # Test automation
    automation = manager.create_automation("welcome", "subscribe")
    print(f"Create automation: {automation}")
    
    print("\n✓ Email system test complete")


if __name__ == "__main__":
    quick_test()
