"""
Email List & Campaign Management
Mailchimp and SendGrid integration for growing subscriber lists
"""

import requests
import logging
from datetime import datetime
from typing import Dict, List, Optional
from config import MAILCHIMP_API_KEY, MAILCHIMP_LIST_ID, SENDGRID_API_KEY

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MailchimpManager:
    """Manage email list and campaigns on Mailchimp"""
    
    def __init__(self):
        if not MAILCHIMP_API_KEY:
            logger.warning("Mailchimp API key not configured")
            return
        
        self.api_key = MAILCHIMP_API_KEY
        self.list_id = MAILCHIMP_LIST_ID
        self.server = MAILCHIMP_API_KEY.split('-')[1]
        self.base_url = f"https://{self.server}.api.mailchimp.com/3.0"
        self.headers = {
            "Authorization": f"apikey {self.api_key}",
            "Content-Type": "application/json"
        }
    
    def add_subscriber(self, email: str, name: str = None, 
                       tags: List[str] = None) -> Dict:
        """Add subscriber to list"""
        
        url = f"{self.base_url}/lists/{self.list_id}/members"
        
        data = {
            "email_address": email,
            "status": "subscribed",
            "merge_fields": {
                "FNAME": name.split()[0] if name else "",
                "LNAME": name.split()[-1] if name and len(name.split()) > 1 else ""
            }
        }
        
        if tags:
            data["tags"] = tags
        
        try:
            response = requests.post(url, headers=self.headers, json=data)
            
            if response.status_code in [200, 201]:
                logger.info(f"✓ Subscriber added: {email}")
                return {"success": True, "email": email}
            else:
                logger.error(f"Failed to add subscriber: {response.text}")
                return {"success": False, "error": response.text}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_list_stats(self) -> Dict:
        """Get subscriber list statistics"""
        
        url = f"{self.base_url}/lists/{self.list_id}"
        
        try:
            response = requests.get(url, headers=self.headers)
            
            if response.status_code == 200:
                data = response.json()
                return {
                    "total_subscribers": data.get("stats", {}).get("member_count"),
                    "unsubscribed": data.get("stats", {}).get("unsubscribe_count"),
                    "cleaned": data.get("stats", {}).get("cleaned_count"),
                    "list_name": data.get("name"),
                    "created_date": data.get("date_created")
                }
            else:
                logger.error(f"Failed to get list stats: {response.text}")
                return {}
        except Exception as e:
            logger.error(f"Error getting list stats: {str(e)}")
            return {}
    
    def send_campaign(self, subject: str, content: str, 
                     template_id: str = None) -> Dict:
        """Create and schedule email campaign"""
        
        url = f"{self.base_url}/campaigns"
        
        data = {
            "type": "regular",
            "recipients": {
                "list_id": self.list_id
            },
            "settings": {
                "subject_line": subject,
                "from_name": "Content Bot",
                "reply_to": "noreply@contentbot.com",
                "preview_text": content[:100]
            },
            "content": {
                "html": f"<p>{content.replace(chr(10), '<br>')}</p>"
            }
        }
        
        try:
            response = requests.post(url, headers=self.headers, json=data)
            
            if response.status_code in [200, 201]:
                campaign_id = response.json().get("id")
                logger.info(f"✓ Campaign created: {campaign_id}")
                
                # Send campaign
                send_url = f"{self.base_url}/campaigns/{campaign_id}/actions/send"
                send_response = requests.post(send_url, headers=self.headers)
                
                if send_response.status_code == 204:
                    logger.info(f"✓ Campaign sent: {campaign_id}")
                    return {"success": True, "campaign_id": campaign_id}
                else:
                    return {"success": False, "error": "Failed to send campaign"}
            else:
                logger.error(f"Campaign creation failed: {response.text}")
                return {"success": False, "error": response.text}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_campaigns(self) -> List[Dict]:
        """Get list of campaigns"""
        
        url = f"{self.base_url}/campaigns"
        
        try:
            response = requests.get(url, headers=self.headers)
            
            if response.status_code == 200:
                campaigns = response.json().get("campaigns", [])
                return [
                    {
                        "id": c["id"],
                        "subject": c["settings"]["subject_line"],
                        "status": c["status"],
                        "sent_date": c.get("send_time"),
                        "opens": c.get("report_summary", {}).get("opens"),
                        "clicks": c.get("report_summary", {}).get("clicks")
                    }
                    for c in campaigns
                ]
            else:
                return []
        except Exception as e:
            logger.error(f"Error getting campaigns: {str(e)}")
            return []


class SendGridManager:
    """Manage email via SendGrid"""
    
    def __init__(self):
        if not SENDGRID_API_KEY:
            logger.warning("SendGrid API key not configured")
            return
        
        self.api_key = SENDGRID_API_KEY
    
    def add_contact(self, email: str, name: str = None) -> Dict:
        """Add contact to SendGrid"""
        
        url = "https://api.sendgrid.com/v3/marketing/contacts"
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "contacts": [
                {
                    "email": email,
                    "first_name": name.split()[0] if name else "",
                    "last_name": name.split()[-1] if name and len(name.split()) > 1 else ""
                }
            ]
        }
        
        try:
            response = requests.put(url, headers=headers, json=data)
            
            if response.status_code in [200, 201, 202]:
                logger.info(f"✓ Contact added to SendGrid: {email}")
                return {"success": True, "email": email}
            else:
                logger.error(f"Failed to add contact: {response.text}")
                return {"success": False, "error": response.text}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def send_email(self, to_email: str, subject: str, content: str) -> Dict:
        """Send email via SendGrid"""
        
        from sendgrid import SendGridAPIClient
        from sendgrid.helpers.mail import Mail
        
        try:
            message = Mail(
                from_email=("noreply@contentbot.com", "Content Bot"),
                to_emails=to_email,
                subject=subject,
                html_content=f"<p>{content.replace(chr(10), '<br>')}</p>"
            )
            
            sg = SendGridAPIClient(self.api_key)
            response = sg.send(message)
            
            if response.status_code in [200, 202]:
                logger.info(f"✓ Email sent to {to_email}")
                return {"success": True, "status": response.status_code}
            else:
                return {"success": False, "error": f"Status {response.status_code}"}
        except Exception as e:
            return {"success": False, "error": str(e)}


class EmailSequences:
    """Pre-built email sequences for conversions"""
    
    @staticmethod
    def welcome_sequence() -> List[Dict]:
        """Welcome email sequence (3 emails)"""
        
        return [
            {
                "day": 0,
                "subject": "Welcome to Content Bot! 🚀",
                "content": """
                Hi there!

                Thanks for subscribing! I'm thrilled to have you here.

                Here's what you'll get:
                • Daily AI tips and tricks
                • Content marketing strategies
                • Tools & resources to automate your work
                • Exclusive affiliate deals (save money!)

                Check out these amazing tools:
                [ChatGPT] [Notion] [Zapier]

                Can't wait to help you level up!

                Best,
                Content Bot
                """
            },
            {
                "day": 2,
                "subject": "The #1 Tool That Changed My Content Game",
                "content": """
                Hi!

                Two days in - how are you liking the tips so far?

                I wanted to share something that's a game-changer for content creators:
                ChatGPT

                With ChatGPT, you can:
                ✓ Generate blog post ideas in seconds
                ✓ Draft entire articles
                ✓ Create social media captions
                ✓ Brainstorm marketing angles

                [Get started with ChatGPT →]

                Thousands of creators use it. You should too.

                - Bot
                """
            },
            {
                "day": 5,
                "subject": "Your free resource guide is ready 📚",
                "content": """
                Hey!

                I've put together a guide: "The Content Creator's Toolkit"

                It includes:
                • 50 content ideas you can post today
                • The 7 best AI tools for creators
                • A complete posting schedule template
                • Affiliate link best practices

                [Download your free guide →]

                See you inside!
                """
            }
        ]
    
    @staticmethod
    def nurture_sequence() -> List[Dict]:
        """Customer nurture sequence"""
        
        return [
            {
                "subject": "5 Ways to Make Money as a Content Creator",
                "content": "Email content about monetization..."
            },
            {
                "subject": "The Secret to Going Viral (Hint: It's Not Luck)",
                "content": "Email content about viral strategies..."
            },
            {
                "subject": "Upgrade Your Workflow [Limited Time Offer]",
                "content": "Email content with special offers..."
            }
        ]


class EmailManager:
    """Unified email management"""
    
    def __init__(self):
        self.mailchimp = MailchimpManager() if MAILCHIMP_API_KEY else None
        self.sendgrid = SendGridManager() if SENDGRID_API_KEY else None
    
    def add_subscriber(self, email: str, name: str = None, 
                       tags: List[str] = None) -> Dict:
        """Add subscriber to email list"""
        
        if self.mailchimp:
            return self.mailchimp.add_subscriber(email, name, tags)
        elif self.sendgrid:
            return self.sendgrid.add_contact(email, name)
        else:
            return {"error": "Email service not configured"}
    
    def send_email(self, subject: str, content: str) -> Dict:
        """Send email campaign"""
        
        if self.mailchimp:
            return self.mailchimp.send_campaign(subject, content)
        else:
            return {"error": "Email service not configured"}
    
    def get_list_stats(self) -> Dict:
        """Get email list statistics"""
        
        if self.mailchimp:
            return self.mailchimp.get_list_stats()
        else:
            return {}


# Initialize managers
mailchimp = MailchimpManager()
sendgrid = SendGridManager()
email_manager = EmailManager()
sequences = EmailSequences()

if __name__ == "__main__":
    print("Email System initialized")
    print(f"Mailchimp configured: {MAILCHIMP_API_KEY is not None}")
    print(f"SendGrid configured: {SENDGRID_API_KEY is not None}")
