#!/usr/bin/env python3
"""
PREMIUM GUMROAD PRODUCTS GENERATOR
Creates professional, conversion-focused digital products
"""

import json
import os
from datetime import datetime

# ============================================================================
# PART 1: CHATGPT PROMPTS LIBRARY DATA
# ============================================================================

PROMPTS_DATA = {
    "library_title": "ChatGPT Prompts Library",
    "library_subtitle": "Professional Prompts for Productivity, Creativity & Growth",
    "version": "1.0 - Premium Edition",
    "publication_date": "2024",
    
    "prompts": [
        {
            "id": 1,
            "title": "Executive Summary Generator",
            "category": "Business",
            "prompt": "Create a concise executive summary for [DOCUMENT/PROJECT]. Include: key objectives, major findings, critical metrics, and recommended next steps. Format as a professional brief suitable for C-level presentation.",
            "use_case": "Sales decks, board reports, project pitches, quarterly reviews",
            "example_input": "A 50-page market research report on AI adoption in retail",
            "example_output": "2-page executive summary with key metrics, trends, and recommendations",
            "pro_tips": [
                "Specify the target audience (CEO, investors, board) for better tone",
                "Ask for specific metrics to include",
                "Request it in PowerPoint format for faster implementation"
            ],
            "customize": "Replace [DOCUMENT/PROJECT] with your specific content. Adjust length by saying '2-page' or '1-paragraph'"
        },
        {
            "id": 2,
            "title": "Content Calendar Strategist",
            "category": "Marketing",
            "prompt": "Design a 90-day content calendar for [PLATFORM/BRAND] targeting [AUDIENCE]. Include content themes, posting frequency, content types (video/blog/carousel/etc), and key dates. Align with [BUSINESS_GOAL].",
            "use_case": "Social media management, blog planning, YouTube scheduling, TikTok strategy",
            "example_input": "Instagram for a fitness coaching brand targeting busy professionals",
            "example_output": "Detailed calendar with daily posts, theme weeks, carousel ideas, and engagement strategies",
            "pro_tips": [
                "Include competitor analysis in your request for better positioning",
                "Ask for analytics-based posting times",
                "Request backup content ideas for flexibility"
            ],
            "customize": "Change platforms (LinkedIn, TikTok, Pinterest), audiences, and business goals to match your brand"
        },
        {
            "id": 3,
            "title": "Email Sequence Copywriter",
            "category": "Marketing",
            "prompt": "Write a [X]-email sequence for [GOAL]: [AUDIENCE]. Each email should: hook them, deliver value, build authority, and include a strong CTA. Focus on [PAIN_POINT] and position [SOLUTION]. Keep subject lines short and curiosity-driven.",
            "use_case": "Lead nurturing, product launches, re-engagement campaigns, webinar sign-ups",
            "example_input": "5-email sequence for productivity app targeting solopreneurs struggling with time management",
            "example_output": "5 complete emails with subject lines, body copy, and conversion tactics",
            "pro_tips": [
                "Test variations of subject lines with A/B mention",
                "Ask for segmentation strategies based on user behavior",
                "Request mobile-optimized formatting"
            ],
            "customize": "Adjust email count, goal, audience segment, and pain points. Add your brand voice details."
        },
        {
            "id": 4,
            "title": "LinkedIn Authority Builder",
            "category": "Personal Branding",
            "prompt": "Create a 30-day LinkedIn content strategy for [YOUR_EXPERTISE]. Generate 30 unique post ideas that position you as an authority in [NICHE]. Include: hook format, content angle, CTA, and optimal posting times. Focus on [TARGET_RESULT].",
            "use_case": "Building thought leadership, consulting lead generation, job hunting, personal brand growth",
            "example_input": "LinkedIn strategy for a sales coach wanting to attract enterprise clients",
            "example_output": "30 post outlines with hooks, angles, CTAs, and growth metrics",
            "pro_tips": [
                "Mix educational, personal stories, and industry insights",
                "Ask for engagement-rate predictions",
                "Request hashtag strategies for reach"
            ],
            "customize": "Replace expertise area, niche, and target result with your specific goals"
        },
        {
            "id": 5,
            "title": "Customer Pain Point Excavator",
            "category": "Market Research",
            "prompt": "Identify the top 10 pain points for [TARGET_AUDIENCE] in [INDUSTRY/CONTEXT]. For each pain point, provide: current solutions they use, why those solutions fail, emotional impact, and how our [PRODUCT/SERVICE] solves it differently.",
            "use_case": "Product development, sales messaging, market positioning, landing page copy",
            "example_input": "Pain points for freelance designers in the agency outsourcing space",
            "example_output": "10 detailed pain points with solutions and messaging angles",
            "pro_tips": [
                "Ask for severity ratings (1-10) for prioritization",
                "Request language/terminology your audience uses",
                "Include willingness-to-pay insights"
            ],
            "customize": "Specify your exact target audience and industry/context for hyper-relevant results"
        },
        {
            "id": 6,
            "title": "Product Launch Blueprint",
            "category": "Business",
            "prompt": "Create a go-to-market plan for [PRODUCT/SERVICE] launching to [AUDIENCE]. Include: pre-launch hype (30 days), launch day activities, post-launch momentum (30 days), PR angles, influencer outreach, and expected sales milestones.",
            "use_case": "SaaS launches, digital product releases, service line launches, course promotions",
            "example_input": "A new productivity app for remote teams launching in Q2",
            "example_output": "90-day launch roadmap with tactics, timelines, and growth projections",
            "pro_tips": [
                "Include budget estimates for ad spend",
                "Ask for influencer pitch templates",
                "Request media list ideas for PR"
            ],
            "customize": "Update product type, target audience, and launch timeline to match your schedule"
        },
        {
            "id": 7,
            "title": "Sales Objection Handler",
            "category": "Sales",
            "prompt": "Generate responses to the top 15 objections for [YOUR_PRODUCT]. For each objection provide: why customers say it, a reframe strategy, proof/evidence, and a specific response script. Tone: [TONE]. Focus on [DECISION_MAKER].",
            "use_case": "Sales training, pitch refinement, objection handling confidence, closing rates improvement",
            "example_input": "Objections for a $5K/month marketing agency service targeting e-commerce brands",
            "example_output": "15 objection responses with scripts and proof points",
            "pro_tips": [
                "Include objections from different buyer personas",
                "Ask for video/email versions of responses",
                "Request follow-up tactics after objection handling"
            ],
            "customize": "List your specific product, target decision-maker, and desired tone"
        },
        {
            "id": 8,
            "title": "Blog Post Outline Master",
            "category": "Content Creation",
            "prompt": "Create a detailed blog post outline for '[POST_TITLE]' targeting [KEYWORD] for [AUDIENCE]. Structure with: compelling intro hook, 5-7 main sections, subheadings, key takeaways, CTA, and internal link suggestions. Aim for [GOAL].",
            "use_case": "Blog strategy, SEO content planning, organic traffic growth, thought leadership",
            "example_input": "Blog post 'How to Implement OKRs Without Failing' for startup founders",
            "example_output": "Detailed outline with H2s, H3s, content angles, and keyword placements",
            "pro_tips": [
                "Include word count recommendations",
                "Ask for competitor analysis insights",
                "Request image/infographic placement ideas"
            ],
            "customize": "Insert your post title, target keyword, audience, and business goal"
        },
        {
            "id": 9,
            "title": "Customer Testimonial Elicitor",
            "category": "Marketing",
            "prompt": "Create a guide for collecting powerful testimonials from [CUSTOMER_SEGMENT]. Generate 12 specific questions that uncover: transformation, specific results, before/after, emotional impact, and buying recommendation. Format responses as case studies for [USE_CASE].",
            "use_case": "Building social proof, case study development, sales page optimization, video testimonials",
            "example_input": "Testimonials from fitness app users for landing page credibility",
            "example_output": "12-question framework + 3 sample case studies with results and quotes",
            "pro_tips": [
                "Ask for video interview scripts",
                "Request permission language for marketing use",
                "Include incentive suggestions for participation"
            ],
            "customize": "Specify your customer segment and intended use of testimonials"
        },
        {
            "id": 10,
            "title": "Personal Brand Bio Creator",
            "category": "Personal Branding",
            "prompt": "Write 5 versions of a professional bio for me: [YOUR_NAME], a [ROLE] specializing in [EXPERTISE]. Versions: 1-sentence, 50-word, 100-word, LinkedIn full, and creative narrative. Highlight [KEY_ACHIEVEMENTS] and position for [TARGET_AUDIENCE].",
            "use_case": "LinkedIn profiles, speaking bios, website About pages, podcast introductions, email signatures",
            "example_input": "Bio for Sarah Chen, marketing strategist specializing in B2B SaaS growth",
            "example_output": "5 bio versions ranging from one sentence to full narrative",
            "pro_tips": [
                "Include personal brand archetype to guide tone",
                "Ask for differentiation from competitors",
                "Request a tagline/elevator pitch"
            ],
            "customize": "Fill in your name, role, expertise, achievements, and target audience"
        },
        {
            "id": 11,
            "title": "Competitor Intelligence Analyzer",
            "category": "Market Research",
            "prompt": "Analyze [COMPETITOR_NAME] and create a competitive intelligence report. Include: their positioning, messaging pillars, customer segments, pricing strategy, content themes, growth tactics, and where they're vulnerable. Format: actionable intelligence for [YOUR_BUSINESS].",
            "use_case": "Market positioning, pricing strategy, messaging differentiation, content ideas, partnership opportunities",
            "example_input": "Analysis of Notion for a competing productivity tool",
            "example_output": "Detailed competitive intelligence with strategic opportunities identified",
            "pro_tips": [
                "Ask for SWOT analysis format",
                "Include their content calendar analysis",
                "Request customer review sentiment analysis"
            ],
            "customize": "Replace competitor name and focus on your specific business context"
        },
        {
            "id": 12,
            "title": "Webinar Funnel Designer",
            "category": "Marketing",
            "prompt": "Design a webinar funnel for [TOPIC] targeting [AUDIENCE]. Create: 1) Registration page copy (headline + subheading), 2) Email sequence (3 pre-webinar), 3) Slide outline (5 main points), 4) Pitch strategy (last 5 minutes), 5) Follow-up sequence (3 emails).",
            "use_case": "Lead generation, product launches, course promotions, consulting sign-ups",
            "example_input": "Webinar 'The Ultimate Guide to Personal Branding' for mid-career professionals",
            "example_output": "Complete funnel blueprint from registration through conversion",
            "pro_tips": [
                "Include A/B testing suggestions",
                "Ask for technical setup recommendations",
                "Request Q&A preparation guide"
            ],
            "customize": "Update topic, audience, and business goal to match your webinar"
        }
    ]
}

# ============================================================================
# PART 2: GOOGLE SHEETS TEMPLATES SPECIFICATIONS
# ============================================================================

SHEETS_TEMPLATES = {
    "1_master_task_manager": {
        "name": "Master Task Manager",
        "description": "Central hub for all tasks with priority levels, progress tracking, and deadline management",
        "color_scheme": {
            "header": "#1F3A93",
            "high_priority": "#E74C3C",
            "medium_priority": "#F39C12",
            "low_priority": "#27AE60",
            "completed": "#BDC3C7",
            "accent": "#3498DB"
        },
        "features": [
            "Color-coded priority levels (High/Medium/Low)",
            "Progress slider (0-100%)",
            "Deadline tracking with automatic formatting",
            "Status indicators (Not Started/In Progress/Blocked/Completed)",
            "Task owner assignment",
            "Category filtering",
            "Summary dashboard showing completion rate"
        ]
    },
    "2_weekly_planner": {
        "name": "Weekly Planner",
        "description": "Visual weekly schedule with time blocks, activity types, and daily focus areas",
        "color_scheme": {
            "work": "#3498DB",
            "personal": "#9B59B6",
            "health": "#E74C3C",
            "learning": "#F39C12",
            "leisure": "#1ABC9C"
        },
        "features": [
            "Mon-Sun layout with hourly time blocks",
            "Color-coded activity types with icons",
            "Focus hours highlighting (deep work time)",
            "Weekly habits tracker sidebar",
            "Mini dashboard with time allocation chart",
            "Notes section for weekly goals",
            "Productivity score calculation"
        ]
    },
    "3_30day_habit_tracker": {
        "name": "30-Day Habit Tracker",
        "description": "Track daily habits with visual progress indicators and streak counting",
        "features": [
            "30-day grid with checkbox visualization",
            "Streak counter (current & longest)",
            "Habit categories with icons",
            "Completion percentage by week",
            "Progress bar visualization",
            "Motivation quotes rotating daily",
            "Habit success rate history",
            "Weekly summary with insights"
        ]
    },
    "4_project_manager": {
        "name": "Project Manager",
        "description": "Comprehensive project tracking with Gantt visualization and team assignments",
        "features": [
            "Project overview dashboard",
            "Task list with dependencies",
            "Gantt-style timeline visualization",
            "Team member assignments",
            "Priority and status tracking",
            "Budget tracking by task",
            "Resource allocation chart",
            "Project completion percentage",
            "Risk/issues log"
        ]
    },
    "5_budget_tracker": {
        "name": "Budget Tracker",
        "description": "Income and expense tracking with visual analytics and category breakdown",
        "color_scheme": {
            "income": "#27AE60",
            "expenses": "#E74C3C",
            "savings": "#3498DB"
        },
        "features": [
            "Income vs expenses monthly chart",
            "Category-wise expense breakdown pie chart",
            "Budget vs actual comparison",
            "Savings rate calculation",
            "Recurring expenses tracking",
            "Cash flow forecast",
            "Monthly trends visualization",
            "Category limits and alerts"
        ]
    },
    "6_time_blocker": {
        "name": "Time Blocker",
        "description": "Detailed time blocking schedule with focus hours and activity tracking",
        "features": [
            "15-minute time block precision",
            "Color-coded activity blocks",
            "Focus hours highlighted in bold",
            "Daily focus theme",
            "Time tracking for actual hours spent",
            "Break reminders built-in",
            "Weekly time audit summary",
            "Focus score tracking"
        ]
    },
    "7_goal_tracker": {
        "name": "Goal Tracker",
        "description": "SMART goal setting with milestone tracking and progress visualization",
        "features": [
            "SMART goal template (Specific, Measurable, Achievable, Relevant, Time-bound)",
            "Milestone checkpoints",
            "Progress percentage visualization",
            "Key results sub-tracking",
            "Weekly check-in prompts",
            "Obstacle identification",
            "Accountability partner tracking",
            "Goal success/failure analysis"
        ]
    },
    "8_content_calendar": {
        "name": "Content Calendar",
        "description": "Multi-platform content planning with status indicators and performance metrics",
        "features": [
            "Platform selection (Instagram/Facebook/LinkedIn/TikTok/YouTube/Blog)",
            "Content type indicators (Video/Carousel/Quote/Educational/Promotional)",
            "Publishing schedule",
            "Status tracking (Idea/Draft/Scheduled/Published)",
            "Performance metrics (Likes/Comments/Shares/Views)",
            "Caption preview",
            "Hashtag management",
            "Monthly content matrix"
        ]
    },
    "9_daily_journal": {
        "name": "Daily Journal",
        "description": "Reflective journaling with mood tracking and gratitude logging",
        "features": [
            "Mood tracker with emoji visualization",
            "Daily gratitude log (3 things)",
            "Reflection prompts rotating daily",
            "Energy level tracking (1-10)",
            "Win of the day section",
            "Lessons learned capture",
            "Tomorrow's focus area",
            "Sentiment analysis over time",
            "Monthly insights summary"
        ]
    },
    "10_affiliate_tracker": {
        "name": "Affiliate Tracker",
        "description": "Commission tracking, earnings analysis, and affiliate partnership performance",
        "features": [
            "Affiliate program tracking",
            "Commission rate monitoring",
            "Monthly earnings calculator",
            "Performance metrics (clicks/conversions/revenue)",
            "Payout schedule tracking",
            "Growth rate visualization",
            "Top performing programs ranking",
            "Revenue forecast by program",
            "Action items for underperformers"
        ]
    }
}

# ============================================================================
# PART 3: SAVE DATA
# ============================================================================

def save_data():
    os.makedirs('/root/clawd/gumroad-premium-final', exist_ok=True)
    
    # Save prompts data
    with open('/root/clawd/gumroad-premium-final/prompts_library.json', 'w') as f:
        json.dump(PROMPTS_DATA, f, indent=2)
    
    # Save sheets templates spec
    with open('/root/clawd/gumroad-premium-final/sheets_templates_spec.json', 'w') as f:
        json.dump(SHEETS_TEMPLATES, f, indent=2)
    
    print("✅ Data files saved successfully")
    print(f"   - {len(PROMPTS_DATA['prompts'])} premium ChatGPT prompts")
    print(f"   - {len(SHEETS_TEMPLATES)} Google Sheets templates")

if __name__ == '__main__':
    save_data()
