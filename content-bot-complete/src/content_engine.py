"""
AI Content Generation Engine
Powered by ChatGPT for creating diverse, engaging content
"""

import openai
import random
import json
import logging
from datetime import datetime
from typing import Dict, List, Optional
from config import OPENAI_API_KEY, NICHES, GPT_MODEL, MAX_TOKENS, TEMPERATURE

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

openai.api_key = OPENAI_API_KEY


class ContentEngine:
    """Generate AI-powered content for multiple platforms"""
    
    def __init__(self):
        self.model = GPT_MODEL
        self.max_tokens = MAX_TOKENS
        self.temperature = TEMPERATURE
        self.content_history = []
        
    def generate_content(self, niche: str = None, platform: str = None, 
                        include_affiliate: bool = True) -> Dict:
        """
        Generate content for a specific platform/niche
        
        Args:
            niche: AI_TOOLS, PRODUCTIVITY, BUSINESS, TECH
            platform: twitter, instagram, linkedin, etc
            include_affiliate: Add affiliate links to content
            
        Returns:
            Dict with generated content and metadata
        """
        
        if not niche:
            niche = random.choice(list(NICHES.keys()))
        
        niche_data = NICHES.get(niche, NICHES["AI_TOOLS"])
        keywords = ", ".join(niche_data["keywords"][:3])
        
        prompt = self._build_prompt(niche, platform, keywords)
        
        try:
            logger.info(f"Generating content for {platform} ({niche})")
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": f"You are an expert content creator specializing in {niche}. "
                                 f"Create engaging, unique content with tone: {niche_data['tone']}"
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=self.max_tokens,
                temperature=self.temperature,
            )
            
            content_text = response.choices[0].message.content.strip()
            
            # Build the result
            result = {
                "id": datetime.now().isoformat(),
                "niche": niche,
                "platform": platform,
                "content": content_text,
                "hashtags": " ".join(niche_data["hashtags"]),
                "created_at": datetime.now().isoformat(),
                "status": "generated",
                "usage": {
                    "prompt_tokens": response.usage.prompt_tokens,
                    "completion_tokens": response.usage.completion_tokens,
                    "total_tokens": response.usage.total_tokens
                }
            }
            
            # Check for duplicates
            if not self._is_duplicate(result["content"]):
                self.content_history.append(result)
                logger.info(f"✓ Content generated: {len(content_text)} chars")
                return result
            else:
                logger.warning("Duplicate content detected, regenerating...")
                return self.generate_content(niche, platform, include_affiliate)
                
        except Exception as e:
            logger.error(f"Error generating content: {str(e)}")
            return {
                "error": str(e),
                "status": "failed"
            }
    
    def generate_batch(self, count: int = 5, include_all_platforms: bool = True) -> List[Dict]:
        """
        Generate multiple content pieces
        
        Args:
            count: Number of pieces to generate
            include_all_platforms: Generate for all platforms or random
            
        Returns:
            List of generated content
        """
        
        generated = []
        platforms = ["twitter", "instagram", "linkedin", "tiktok", "reddit", "medium"]
        niches = list(NICHES.keys())
        
        for i in range(count):
            niche = random.choice(niches)
            platform = random.choice(platforms)
            content = self.generate_content(niche, platform)
            if "error" not in content:
                generated.append(content)
        
        logger.info(f"✓ Generated {len(generated)}/{count} content pieces")
        return generated
    
    def _build_prompt(self, niche: str, platform: str, keywords: str) -> str:
        """Build optimized prompt for content generation"""
        
        platform_instructions = {
            "twitter": "Create a tweet (under 280 chars) that's engaging and shareable. Include a call-to-action.",
            "instagram": "Create an Instagram caption (200-300 chars) with emojis and engagement hooks.",
            "linkedin": "Create a professional LinkedIn post about {keywords} that encourages discussion.",
            "tiktok": "Create a viral TikTok script idea (100-200 words) with trending elements.",
            "reddit": "Create a Reddit post discussing {keywords} that would do well in r/productivity or similar.",
            "medium": "Create an article outline (300+ words) for Medium about {keywords}.",
            "email": "Create an engaging email subject line and first paragraph about {keywords}."
        }
        
        instruction = platform_instructions.get(platform, "Create engaging content")
        
        prompt = f"""
        {instruction}
        
        Focus on: {keywords}
        Niche: {niche}
        
        Requirements:
        - Original and unique
        - Action-oriented
        - Facts-based but conversational
        - Include a hook in the first line
        - Make it shareable
        
        Content:
        """
        
        return prompt
    
    def _is_duplicate(self, content: str, threshold: float = 0.85) -> bool:
        """Check if content is too similar to previous content"""
        
        if not self.content_history:
            return False
        
        # Simple similarity check (can be enhanced with ML)
        for prev in self.content_history[-10:]:  # Check last 10
            prev_content = prev.get("content", "")
            similarity = self._similarity_score(content, prev_content)
            if similarity > threshold:
                return True
        
        return False
    
    @staticmethod
    def _similarity_score(s1: str, s2: str) -> float:
        """Calculate similarity between two strings (0-1)"""
        
        words1 = set(s1.lower().split())
        words2 = set(s2.lower().split())
        
        if not words1 or not words2:
            return 0.0
        
        intersection = len(words1 & words2)
        union = len(words1 | words2)
        
        return intersection / union if union > 0 else 0.0


class ContentFormatter:
    """Format content for specific platforms"""
    
    @staticmethod
    def format_twitter(content: Dict) -> str:
        """Format for Twitter (280 char limit)"""
        text = content["content"][:280]
        hashtags = " " + content.get("hashtags", "")
        return (text + hashtags)[:280]
    
    @staticmethod
    def format_instagram(content: Dict) -> str:
        """Format for Instagram with emojis and caption"""
        return content["content"] + "\n\n" + content.get("hashtags", "")
    
    @staticmethod
    def format_linkedin(content: Dict) -> str:
        """Format for LinkedIn (professional)"""
        return content["content"] + "\n\n" + content.get("hashtags", "")
    
    @staticmethod
    def format_tiktok(content: Dict) -> str:
        """Format for TikTok"""
        return content["content"] + "\n\n" + content.get("hashtags", "")
    
    @staticmethod
    def format_reddit(content: Dict) -> str:
        """Format for Reddit"""
        return content["content"] + "\n\n" + content.get("hashtags", "")
    
    @staticmethod
    def format_medium(content: Dict) -> str:
        """Format for Medium (long form)"""
        return content["content"]
    
    @staticmethod
    def format_email(content: Dict) -> tuple:
        """Format for email (subject, body)"""
        lines = content["content"].split("\n")
        subject = lines[0] if lines else "Check This Out!"
        body = "\n".join(lines[1:]) if len(lines) > 1 else content["content"]
        return (subject, body)
    
    @classmethod
    def format_for_platform(cls, content: Dict, platform: str) -> str:
        """Universal formatter"""
        
        formatters = {
            "twitter": cls.format_twitter,
            "instagram": cls.format_instagram,
            "linkedin": cls.format_linkedin,
            "tiktok": cls.format_tiktok,
            "reddit": cls.format_reddit,
            "medium": cls.format_medium,
            "email": cls.format_email,
        }
        
        formatter = formatters.get(platform, lambda x: x["content"])
        return formatter(content)


# Initialize engine
engine = ContentEngine()
formatter = ContentFormatter()

if __name__ == "__main__":
    # Test content generation
    print("Testing Content Engine...")
    
    # Generate single content
    content = engine.generate_content(niche="AI_TOOLS", platform="twitter")
    print(f"\nGenerated Content:\n{content}\n")
    
    # Generate batch
    batch = engine.generate_batch(count=3)
    print(f"Batch generated: {len(batch)} items\n")
    
    # Test formatting
    if batch:
        formatted = formatter.format_for_platform(batch[0], "twitter")
        print(f"Formatted for Twitter:\n{formatted}")
