"""
Content Generator - AI-Powered Content Creation
Generates high-quality content for multiple platforms using OpenAI API
"""

import json
import random
from typing import Dict, List, Optional, Tuple
from datetime import datetime
import logging

try:
    from openai import OpenAI
except ImportError:
    print("Warning: OpenAI not installed. Install with: pip install openai")
    OpenAI = None

from config import Config

# Setup logging
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=getattr(logging, Config.LOG_LEVEL),
    format=Config.LOG_FORMAT
)

class ContentGenerator:
    """Generate high-quality content for all platforms"""
    
    def __init__(self):
        """Initialize content generator with OpenAI client"""
        if not Config.OPENAI_API_KEY or Config.OPENAI_API_KEY == "your-openai-key-here":
            logger.warning("OpenAI API key not configured. Content generation will fail.")
            self.client = None
        else:
            self.client = OpenAI(api_key=Config.OPENAI_API_KEY)
        
        self.affiliate_links = Config.AFFILIATE_LINKS
        self.keywords = Config.CONTENT_KEYWORDS
        self.content_styles = Config.CONTENT_STYLES
        self.content_types = Config.CONTENT_TYPES
    
    def generate_tiktok_script(self, topic: Optional[str] = None) -> Dict:
        """Generate TikTok/Reels script (30-60 seconds)"""
        if not self.client:
            return self._generate_mock_tiktok()
        
        try:
            topic = topic or self._select_random_topic()
            style = random.choice(self.content_styles)
            content_type = random.choice(self.content_types)
            
            prompt = f"""Create a viral TikTok/Reels script about {topic} for the AI Tools & Productivity niche.

Requirements:
- Length: 30-60 seconds (300-600 words when spoken)
- Style: {style}
- Type: {content_type}
- Hook: First 3 seconds must be VERY engaging
- Hook examples: "Wait, you can...", "Nobody talks about this...", "This AI tool is insane..."
- Include a call-to-action at the end
- Include 1-2 related affiliate links naturally (from: {', '.join([v['display_name'] for k, v in list(self.affiliate_links.items())[:5]])})
- Use modern slang and conversational tone
- Include visual directions (e.g., [Show tool on screen], [B-roll of results])

Format the response as JSON:
{{
    "hook": "First 3 seconds of script",
    "body": "Main content (30-45 seconds)",
    "cta": "Call to action",
    "affiliate_mention": "How affiliate link is woven in",
    "visual_directions": ["Direction 1", "Direction 2"],
    "background_music_mood": "energetic/calm/inspiring",
    "hashtags": ["#hashtag1", "#hashtag2", ...],
    "keywords": ["keyword1", "keyword2", ...]
}}"""
            
            response = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=1000,
                messages=[{"role": "user", "content": prompt}]
            )
            
            # Parse response
            content = response.content[0].text
            script_data = json.loads(content)
            
            return {
                "platform": "tiktok",
                "type": content_type,
                "topic": topic,
                "length_seconds": 45,
                **script_data,
                "generated_at": datetime.now().isoformat(),
                "ready_to_post": True
            }
        
        except Exception as e:
            logger.error(f"Error generating TikTok script: {e}")
            return self._generate_mock_tiktok()
    
    def generate_twitter_posts(self, count: int = 5) -> List[Dict]:
        """Generate Twitter posts (280 characters, 5 per day)"""
        if not self.client:
            return [self._generate_mock_twitter() for _ in range(count)]
        
        posts = []
        for i in range(count):
            try:
                topic = self._select_random_topic()
                angle = random.choice(["tip", "question", "controversy", "news", "personal_experience"])
                
                prompt = f"""Create a viral Twitter post about {topic} for the AI Tools & Productivity niche.

Requirements:
- Maximum 280 characters
- Angle: {angle}
- Include 1 relevant hashtag
- Optional: include 1 affiliate link naturally if it fits
- Make it memorable, shareable, thought-provoking
- Use emojis if appropriate

Available affiliate links: {', '.join([v['display_name'] for k, v in list(self.affiliate_links.items())[:5]])}

Return ONLY the tweet text, nothing else."""
                
                response = self.client.messages.create(
                    model="claude-3-5-sonnet-20241022",
                    max_tokens=300,
                    messages=[{"role": "user", "content": prompt}]
                )
                
                tweet = response.content[0].text.strip()
                
                posts.append({
                    "platform": "twitter",
                    "content": tweet,
                    "character_count": len(tweet),
                    "topic": topic,
                    "angle": angle,
                    "generated_at": datetime.now().isoformat(),
                    "ready_to_post": True
                })
                
            except Exception as e:
                logger.error(f"Error generating Twitter post {i+1}: {e}")
                posts.append(self._generate_mock_twitter())
        
        return posts
    
    def generate_blog_post(self, topic: Optional[str] = None) -> Dict:
        """Generate full blog post (2000+ words)"""
        if not self.client:
            return self._generate_mock_blog()
        
        try:
            topic = topic or self._select_random_topic()
            
            prompt = f"""Write a comprehensive, SEO-optimized blog post about {topic} in the AI Tools & Productivity niche.

Requirements:
- Length: 2000-3000 words
- Structure: H1 title, intro, 4-6 sections with H2 headers, conclusion
- Include practical tips, examples, case studies
- Naturally integrate 2-3 affiliate links to relevant tools
- Include a "Key Takeaways" section
- Include an email signup CTA
- Include internal linking opportunities
- Use short paragraphs (2-3 sentences)
- Include 1-2 visual descriptions for images
- Focus on: {topic}
- Target audience: Professionals looking to improve productivity with AI

Available tools to mention: {', '.join([v['display_name'] for k, v in list(self.affiliate_links.items())[:10]])}

Return JSON:
{{
    "title": "H1 Title",
    "meta_description": "Meta description for SEO (150 chars)",
    "slug": "url-slug",
    "introduction": "Opening paragraph",
    "sections": [
        {{"header": "H2 Header", "content": "Section content"}},
        ...
    ],
    "key_takeaways": ["Takeaway 1", "Takeaway 2", ...],
    "conclusion": "Closing paragraph with CTA",
    "cta_email": "Email signup CTA text",
    "tags": ["tag1", "tag2", ...],
    "reading_time_minutes": 7
}}"""
            
            response = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=4000,
                messages=[{"role": "user", "content": prompt}]
            )
            
            content = response.content[0].text
            post_data = json.loads(content)
            
            return {
                "platform": "blog",
                "topic": topic,
                "word_count": sum(len(s.get("content", "").split()) for s in post_data.get("sections", [])),
                **post_data,
                "generated_at": datetime.now().isoformat(),
                "ready_to_post": True
            }
        
        except Exception as e:
            logger.error(f"Error generating blog post: {e}")
            return self._generate_mock_blog()
    
    def generate_email_content(self) -> Dict:
        """Generate email newsletter content"""
        if not self.client:
            return self._generate_mock_email()
        
        try:
            email_type = random.choice(["daily_tool", "weekly_roundup", "affiliate_promotion", "tips"])
            
            prompt = f"""Create email newsletter content for {email_type} in the AI Tools & Productivity niche.

Types:
- daily_tool: Feature one AI tool daily with benefits
- weekly_roundup: Best 3 tools from the week
- affiliate_promotion: Promote 2-3 affiliate products naturally
- tips: 5 productivity tips

Requirements:
- Tone: Friendly, conversational, helpful
- Length: 300-500 words
- Include subject line (max 50 chars)
- Include preheader text (max 100 chars)
- Include 1-2 CTAs
- Naturally integrate affiliate links

Available tools: {', '.join([v['display_name'] for k, v in list(self.affiliate_links.items())[:8]])}

Return JSON:
{{
    "subject_line": "Email subject",
    "preheader_text": "Preheader text (shows in inbox)",
    "greeting": "How to greet subscriber",
    "body": "Main email content",
    "cta_primary": "Primary button text + URL",
    "cta_secondary": "Secondary link text + URL",
    "closing": "Sign-off",
    "footer": "Footer info",
    "type": "{email_type}",
    "estimated_read_time": "X minutes"
}}"""
            
            response = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=1500,
                messages=[{"role": "user", "content": prompt}]
            )
            
            content = response.content[0].text
            email_data = json.loads(content)
            
            return {
                "platform": "email",
                "email_type": email_type,
                **email_data,
                "generated_at": datetime.now().isoformat(),
                "ready_to_post": True
            }
        
        except Exception as e:
            logger.error(f"Error generating email content: {e}")
            return self._generate_mock_email()
    
    def generate_linkedin_post(self) -> Dict:
        """Generate LinkedIn professional content"""
        if not self.client:
            return self._generate_mock_linkedin()
        
        try:
            topic = self._select_random_topic()
            
            prompt = f"""Create a professional LinkedIn post about {topic} for professionals in AI/productivity space.

Requirements:
- Length: 300-500 words
- Tone: Professional but personable
- Start with hook question or interesting statement
- Include 1-2 relevant insights
- Include subtle affiliate mention if natural
- End with question to drive engagement
- Include 5-10 relevant hashtags

Available tools to mention: {', '.join([v['display_name'] for k, v in list(self.affiliate_links.items())[:5]])}

Return JSON:
{{
    "content": "Main post content",
    "hook": "Opening line",
    "insights": ["Insight 1", "Insight 2"],
    "engagement_question": "Question to ask readers",
    "hashtags": ["#Hashtag1", "#Hashtag2", ...],
    "affiliate_mention": "Optional affiliate mention"
}}"""
            
            response = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=1000,
                messages=[{"role": "user", "content": prompt}]
            )
            
            content = response.content[0].text
            post_data = json.loads(content)
            
            return {
                "platform": "linkedin",
                "topic": topic,
                **post_data,
                "generated_at": datetime.now().isoformat(),
                "ready_to_post": True
            }
        
        except Exception as e:
            logger.error(f"Error generating LinkedIn post: {e}")
            return self._generate_mock_linkedin()
    
    def generate_reddit_post(self, subreddit: str = "ChatGPT") -> Dict:
        """Generate Reddit post for specified subreddit"""
        if not self.client:
            return self._generate_mock_reddit()
        
        try:
            topic = self._select_random_topic()
            
            prompt = f"""Create an authentic Reddit post for r/{subreddit} about {topic}.

Requirements:
- Tone: Casual, authentic (like a real Redditor)
- Length: 200-400 words
- Start with engaging title (max 300 chars)
- Include specific examples or personal experience
- Include helpful information and discussion
- Very subtle affiliate mention (if any)
- Reddit users hate obvious self-promotion, so NO hard selling
- Include 2-3 follow-up questions for comments

Return JSON:
{{
    "title": "Reddit post title",
    "body": "Post content",
    "tone": "authentic/helpful",
    "discussion_hooks": ["Question 1", "Question 2"],
    "subreddit": "{subreddit}",
    "keywords": ["keyword1", "keyword2"]
}}"""
            
            response = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=1000,
                messages=[{"role": "user", "content": prompt}]
            )
            
            content = response.content[0].text
            post_data = json.loads(content)
            
            return {
                "platform": "reddit",
                "topic": topic,
                **post_data,
                "generated_at": datetime.now().isoformat(),
                "ready_to_post": True
            }
        
        except Exception as e:
            logger.error(f"Error generating Reddit post: {e}")
            return self._generate_mock_reddit()
    
    def _select_random_topic(self) -> str:
        """Select random topic from keywords"""
        return random.choice(self.keywords)
    
    # ==================== MOCK DATA (Fallback) ====================
    
    def _generate_mock_tiktok(self) -> Dict:
        """Mock TikTok script for testing"""
        return {
            "platform": "tiktok",
            "hook": "Wait, this AI tool just saved me 5 hours this week...",
            "body": "Most people don't know about [Tool] but it literally changed how I work...",
            "cta": "Try it free - link in bio",
            "hashtags": ["#AITools", "#Productivity", "#ChatGPT"],
            "generated_at": datetime.now().isoformat()
        }
    
    def _generate_mock_twitter(self) -> Dict:
        """Mock Twitter post for testing"""
        return {
            "platform": "twitter",
            "content": "Just discovered this AI tool that cuts my writing time in half. Game changer 🚀 #ProductivityHacks",
            "generated_at": datetime.now().isoformat()
        }
    
    def _generate_mock_blog(self) -> Dict:
        """Mock blog post for testing"""
        return {
            "platform": "blog",
            "title": "10 AI Tools That Will Transform Your Workflow in 2024",
            "slug": "ai-tools-transform-workflow",
            "sections": [
                {"header": "Why AI Tools Matter", "content": "Content here..."},
                {"header": "Tool #1: ChatGPT Plus", "content": "Content here..."}
            ],
            "word_count": 2500,
            "generated_at": datetime.now().isoformat()
        }
    
    def _generate_mock_email(self) -> Dict:
        """Mock email content for testing"""
        return {
            "platform": "email",
            "subject_line": "The #1 Tool Productivity Experts Are Using",
            "body": "Email content here...",
            "cta_primary": "Learn More",
            "generated_at": datetime.now().isoformat()
        }
    
    def _generate_mock_linkedin(self) -> Dict:
        """Mock LinkedIn post for testing"""
        return {
            "platform": "linkedin",
            "content": "Just helped my team save 10 hours/week with this simple workflow...",
            "hashtags": ["#Productivity", "#AI", "#Leadership"],
            "generated_at": datetime.now().isoformat()
        }
    
    def _generate_mock_reddit(self) -> Dict:
        """Mock Reddit post for testing"""
        return {
            "platform": "reddit",
            "title": "Best AI Tools for Content Creation (2024)",
            "body": "I've been testing AI tools for months...",
            "subreddit": "ChatGPT",
            "generated_at": datetime.now().isoformat()
        }


def quick_test():
    """Quick test of content generator"""
    gen = ContentGenerator()
    
    print("Testing Content Generator...\n")
    
    # Test TikTok
    print("Generating TikTok script...")
    tiktok = gen.generate_tiktok_script()
    print(f"✓ TikTok: {tiktok.get('hook', 'N/A')[:50]}...\n")
    
    # Test Twitter
    print("Generating Twitter post...")
    twitter = gen.generate_twitter_posts(1)
    print(f"✓ Twitter: {twitter[0].get('content', 'N/A')[:50]}...\n")
    
    # Test Blog
    print("Generating blog post...")
    blog = gen.generate_blog_post()
    print(f"✓ Blog: {blog.get('title', 'N/A')}\n")
    
    # Test Email
    print("Generating email...")
    email = gen.generate_email_content()
    print(f"✓ Email: {email.get('subject_line', 'N/A')}\n")
    
    print("✓ All content generation working!")


if __name__ == "__main__":
    quick_test()
