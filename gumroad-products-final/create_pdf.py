#!/usr/bin/env python3
"""
Generate professional ChatGPT Prompts Library PDF
"""

import os
import sys
from datetime import datetime
from pathlib import Path

# Try to import reportlab and install if needed
try:
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch, cm
    from reportlab.lib.colors import HexColor, white, black
    from reportlab.platypus import (
        SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, 
        PageBreak, Image, KeepTogether, Preformatted
    )
    from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY, TA_RIGHT
except ImportError:
    print("Installing required packages...")
    os.system("python3 -m pip install reportlab -q --user")
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch, cm
    from reportlab.lib.colors import HexColor, white, black
    from reportlab.platypus import (
        SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, 
        PageBreak, Image, KeepTogether, Preformatted
    )
    from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY, TA_RIGHT

# Define professional color scheme
PRIMARY_COLOR = HexColor("#1E3A8A")  # Deep blue
SECONDARY_COLOR = HexColor("#059669")  # Emerald green
ACCENT_COLOR = HexColor("#F59E0B")  # Amber
LIGHT_BG = HexColor("#F0F9FF")  # Light blue
TEXT_COLOR = HexColor("#1F2937")  # Dark gray
BORDER_COLOR = HexColor("#E5E7EB")  # Light gray

# Prompt data structure
prompts_data = {
    "CATEGORY 1: TASK MANAGEMENT & TODO": [
        {
            "title": "Smart Task Breakdown Prompt",
            "prompt": '"I have this task: [TASK]. Break it down into 5-7 specific, actionable subtasks that I can realistically complete today. For each subtask, estimate the time needed and difficulty level (easy/medium/hard). Format as a numbered checklist I can use immediately."',
            "use_case": "Breaking large projects into manageable daily chunks",
            "example": "Input: 'Write a quarterly business report'\nOutput: 1. Gather Q4 sales data (30 min) - Easy | 2. Compile customer feedback summary (45 min) - Medium | 3. Create charts/visuals (60 min) - Medium",
            "tips": "Be specific about the main task. The more detail you provide, the better the breakdown will be."
        },
        {
            "title": "Priority Matrix Generator",
            "prompt": '"I have these 8 tasks to do this week: [LIST TASKS]. Use the Eisenhower Matrix (urgent/important) to categorize them. Show me which I should do first, which I should schedule, which I should delegate, and which I should eliminate. Explain your reasoning for each."',
            "use_case": "Deciding what to focus on when overwhelmed",
            "example": "Input: Email clients, fix website bug, plan vacation, call dentist, learn new software, attend meeting, social media post, grocery shopping\nOutput: DO FIRST: Fix bug, Call dentist | SCHEDULE: Plan vacation, Learn software",
            "tips": "List all tasks competing for your attention. The matrix will show you what's truly important vs just urgent."
        },
        {
            "title": "Task Blocker Solver",
            "prompt": '"I\'m stuck on this task: [DESCRIBE BLOCKER]. What\'s preventing me from moving forward? Give me 3 specific, actionable steps to overcome this blocker right now. For each step, explain why it works and what result I should expect."',
            "use_case": "Getting unstuck when you don't know what to do",
            "example": "Input: Need to write client proposal but keep procrastinating\nOutput: Step 1: Write rough outline (5 min) | Step 2: Set timer 25 min, write intro only | Step 3: Read aloud, fix gaps",
            "tips": "Be honest about what's blocking you. Fear, perfectionism, and unclear expectations are common."
        },
        {
            "title": "Daily Planning Template Generator",
            "prompt": '"Create a detailed plan for my tomorrow using this info: [SCHEDULE OVERVIEW, MAIN GOALS]. Include: 1) Time blocks for each task, 2) Break times, 3) Backup/flex time, 4) Success metrics for the day, 5) One thing that would make tomorrow \'successful\'. Format it for easy reading."',
            "use_case": "Planning the perfect productive day",
            "example": "Input: 8am meeting, finish report, 3 client calls, exercise\nOutput: Detailed hour-by-hour schedule with breaks and backup time",
            "tips": "Provide your existing commitments and main goals. Include energy level changes throughout your day."
        },
        {
            "title": "Recurring Task Automation Checker",
            "prompt": '"I do these tasks repeatedly: [LIST RECURRING TASKS]. For each one, tell me: 1) Can it be automated? 2) What tool would work best? 3) How much time would I save per month? 4) Implementation steps. Focus on quick wins I can set up this week."',
            "use_case": "Finding easy automations to free up time",
            "example": "Input: Send weekly emails, Create notes, Invoice clients, Social reminders\nOutput: IFTTT for emails (5 hrs/mo), Otter.ai for notes (8 hrs/mo), Stripe invoicing (4 hrs/mo)",
            "tips": "Focus on tasks you do more than twice per month. Even small automations add up to hours saved."
        },
        {
            "title": "Parallel Task Organizer",
            "prompt": '"I need to juggle these [NUMBER] tasks: [LIST THEM]. Which can I do in parallel? Which must be sequential? Create a workflow showing dependencies and optimal scheduling. Include realistic timelines."',
            "use_case": "Managing multiple projects at once",
            "example": "Input: 3 dependent tasks vs 3 independent tasks\nOutput: Sequential flowchart showing overlaps, timeline, critical path analysis",
            "tips": "Identify dependencies clearly. Some tasks can overlap to save time significantly."
        },
        {
            "title": "Task Estimation Calibrator",
            "prompt": '"I estimated these tasks would take [TIMES] but they usually take [ACTUAL TIMES]. Show me the pattern in my estimations. Then give me a personal formula to estimate more accurately going forward. Include: 1) My bias (over/under estimating), 2) Adjustment multiplier, 3) 3 ways to estimate better."',
            "use_case": "Getting better at time estimates",
            "example": "Input: Est 1hr→Actual 2hrs, Est 2hrs→Actual 3.5hrs\nOutput: Shows 1.5-1.75x multiplier pattern, suggests 15% buffer, time-boxing technique",
            "tips": "Track your estimates vs actual times for 2+ weeks before using this prompt."
        },
        {
            "title": "Context Switching Reducer",
            "prompt": '"I context switch between [LIST TASKS/APPS]. This kills my productivity. Analyze my typical day and create a schedule that: 1) Batches similar tasks, 2) Minimizes app switching, 3) Protects deep work time, 4) Still handles urgent items. Show the before/after impact."',
            "use_case": "Eliminating productivity killers",
            "example": "Input: Jump between emails, Slack, coding, meetings\nOutput: Batch emails 3x daily, Slack in 2 blocks, 2hr coding blocks, meetings in afternoon",
            "tips": "List every app/task you switch between. The goal is 2-3 context switches per day max."
        },
        {
            "title": "Completed Tasks Analyzer",
            "prompt": '"Over the past [WEEK/MONTH], I completed these tasks: [LIST]. What patterns do you see? Which tasks gave me the most energy? Which drained me? What should I do more/less of? How should I adjust next period?"',
            "use_case": "Learning from what actually happened",
            "example": "Input: List of 20 completed tasks from past week\nOutput: Energy patterns, high-impact vs low-impact work, recommendations for next week",
            "tips": "Include small tasks too. You'll be surprised what actually energizes vs drains you."
        },
        {
            "title": "Task Refusal Decision Maker",
            "prompt": '"Someone asked me to do this: [TASK DESCRIPTION]. Should I say yes or no? Evaluate: 1) Strategic fit (aligned with my goals?), 2) Energy/time cost, 3) Opportunity cost (what does it prevent?), 4) Who really needs this (is it actually urgent?). Give me a clear YES/NO with reasoning I can use to respond."',
            "use_case": "Protecting your time with confidence",
            "example": "Input: Manager asked to lead new initiative on top of current work\nOutput: Decision framework showing fit, costs, alternatives, confidence level",
            "tips": "Use this when you're unsure. The structure helps you say no professionally."
        }
    ],
    
    "CATEGORY 2: TIME MANAGEMENT & SCHEDULING": [
        {
            "title": "Weekly Time Audit Creator",
            "prompt": '"Here\'s my current weekly schedule: [DESCRIBE YOUR WEEK]. Create a detailed audit showing: 1) Time spent in each activity category, 2) Energy levels throughout the week, 3) Bottlenecks/conflicts, 4) Wasted time, 5) Opportunities to reclaim time. Give me 3 high-impact changes."',
            "use_case": "Understanding where your time actually goes",
            "example": "Input: 30 hrs meetings, 20 hrs coding, 10 hrs admin, scattered breaks\nOutput: Pie chart analysis, energy map, 3 changes like 'batch meetings into 2 days'",
            "tips": "Track your week honestly. Most people are surprised what takes their time."
        },
        {
            "title": "Time Block Template Designer",
            "prompt": '"Design the perfect weekly time block schedule for someone who: [YOUR ROLE/CONSTRAINTS]. Include: 1) Deep work blocks, 2) Meeting blocks, 3) Admin time, 4) Buffer time, 5) Recovery time. Optimize for when my energy is highest. Make it a template I can reuse."',
            "use_case": "Creating your ideal weekly structure",
            "example": "Input: Software engineer, prefer mornings for coding, 5-8 meetings/week\nOutput: Hour-by-hour template Monday-Friday with optimal scheduling",
            "tips": "Protect your peak energy time fiercely. Everything else should work around it."
        },
        {
            "title": "Meeting Impact Analyzer",
            "prompt": '"I have these meetings scheduled: [LIST MEETINGS]. For each, tell me: 1) Is it necessary? 2) What\'s the real purpose? 3) Who actually needs to attend? 4) How long should it really be? 5) Could it be async instead? Recommend how to consolidate/eliminate."',
            "use_case": "Reducing meeting bloat",
            "example": "Input: 15 meetings across the week, varying lengths and purposes\nOutput: Shows which are essential, can be shortened, can be combined, can be async",
            "tips": "Many meetings don't need to exist or can be emails instead. This prompt shows you which."
        },
        {
            "title": "Urgent vs Important Distinguisher",
            "prompt": '"Something came up that feels urgent: [DESCRIBE IT]. Help me distinguish: 1) Is it actually urgent or just feels that way? 2) If I ignore it for 4 hours, what happens? 3) What\'s the real deadline? 4) Should I interrupt current work? 5) What\'s the best response? Give me confidence in my decision."',
            "use_case": "Resisting false urgency",
            "example": "Input: Client email asking for quick update\nOutput: Shows how to test urgency, likely deadline, best response strategy",
            "tips": "The 4-hour rule: if nothing bad happens if you wait 4 hours, it's not urgent."
        },
        {
            "title": "Energy-Based Schedule Optimizer",
            "prompt": '"My energy levels throughout the day: [DESCRIBE YOUR PATTERN]. Create a schedule that: 1) Puts hardest tasks in peak energy times, 2) Uses low-energy times for easy/mindless work, 3) Protects focus time when you\'re sharpest, 4) Schedules breaks strategically. Make it specific and actionable for my tomorrow."',
            "use_case": "Working WITH your natural rhythm, not against it",
            "example": "Input: Sharp 6-11am, slump 1-3pm, recover 4-5pm\nOutput: Detailed schedule with hard coding 7-11am, admin 1-3pm, meetings 4-5pm",
            "tips": "Track your energy for a week first. Everyone's rhythm is different."
        },
        {
            "title": "Calendar Blocking Guide",
            "prompt": '"Show me how to properly time-block my calendar for [YOUR WORK TYPE]. Include: 1) Deep work blocks (size, frequency), 2) Meeting buffering (how much space between meetings), 3) Admin time blocks (how often, how long), 4) Break rules (frequency, duration), 5) Template I can copy. Add defensive tactics to protect these blocks."',
            "use_case": "Creating a calendar that actually works",
            "example": "Input: Creative work that needs long focus periods\nOutput: Specific block sizes, protection strategies, calendar template",
            "tips": "Defensive tactics: Mark blocks as 'busy', set auto-decline for conflicting meetings, etc."
        },
        {
            "title": "Deadline Reverse Planner",
            "prompt": '"I have a [PROJECT] due on [DATE]. Today is [TODAY]. Work backward from the deadline and create: 1) Key milestones/checkpoints, 2) When each major piece must be done, 3) Buffer time built in, 4) What I should start THIS WEEK, 5) Warning signs I\'m off track. Give me the timeline as a calendar view."',
            "use_case": "Never missing deadlines with breathing room",
            "example": "Input: Website launch in 8 weeks from today\nOutput: Week-by-week breakdown with milestones and buffer built in",
            "tips": "Add buffer time equal to 20-30% of total project time."
        },
        {
            "title": "Batch Processing Maximizer",
            "prompt": '"I do these types of tasks frequently: [LIST TASK TYPES]. Create a batching strategy that: 1) Groups similar tasks together, 2) Shows optimal batch size and frequency, 3) Reduces context switching, 4) Minimizes setup/tear-down time, 5) Gives me a specific weekly schedule. Calculate time saved."',
            "use_case": "Dramatic productivity gains from batching",
            "example": "Input: Emails, social posts, client calls, admin work\nOutput: Batching schedule, time saved calculations, weekly template",
            "tips": "Batching can save 5-10 hours per week by reducing context switching."
        },
        {
            "title": "Break Optimization Protocol",
            "prompt": '"I take [CURRENT BREAKS] but still get burned out. Design an optimal break strategy: 1) When to take breaks (based on focus science), 2) Break length (based on task type), 3) What to do during breaks (to actually recover), 4) When to take longer breaks, 5) Weekly schedule. Make it sustainable."',
            "use_case": "Better recovery = higher productivity = less burnout",
            "example": "Input: Currently grab random breaks when exhausted\nOutput: Break science, specific timings, recovery activities, weekly rhythm",
            "tips": "Take breaks BEFORE you're exhausted. Preventive breaks work better than reactive ones."
        },
        {
            "title": "Time Reclamation Action Plan",
            "prompt": '"I want to reclaim [NUMBER] hours per week. Analyze my current schedule and identify: 1) Time being wasted, 2) Tasks that can be delegated, 3) Meetings that can be cut, 4) Processes that can be streamlined, 5) Specific actions with time reclaimed for each. Prioritize by ease vs impact."',
            "use_case": "Finding 5-10 hours of free time without working harder",
            "example": "Input: Want to reclaim 5 hours/week for deep work\nOutput: Specific cuts/changes with hours recovered, prioritized action plan",
            "tips": "Focus on the highest-impact, easiest wins first."
        }
    ],
    
    "CATEGORY 3: PRODUCTIVITY SYSTEMS & PLANNING": [
        {
            "title": "GTD Workflow Setup Assistant",
            "prompt": '"I want to implement Getting Things Done (GTD) for [YOUR CONTEXT]. Create a custom system that: 1) Capture process (how to capture all your tasks/ideas), 2) Clarify process (how to decide if each task is actionable), 3) Organize categories (what you need to track), 4) Review cadence (daily/weekly rhythms), 5) Tools recommendation. Make it specific to my life."',
            "use_case": "Implementing GTD without overwhelm",
            "example": "Input: Freelance consultant with personal + business tasks\nOutput: Custom GTD system with categories, review rhythm, tools",
            "tips": "GTD works best when you adapt it to your life, not the other way around."
        },
        {
            "title": "Second Brain Setup Guide",
            "prompt": '"I want to build a second brain using [TOOL] to capture: [WHAT YOU WANT TO TRACK]. Create: 1) Structure/folder hierarchy, 2) Capture process (how notes get in), 3) Tagging/organization system, 4) Review process (how you find things), 5) Integration with my tools, 6) Daily/weekly rituals. Make it ready to implement today."',
            "use_case": "Organizing all your knowledge and reducing mental load",
            "example": "Input: Notion-based second brain for business ideas, articles, and learnings\nOutput: Folder structure, capture flow, review system, implementation checklist",
            "tips": "Start simple. You can always add complexity later."
        },
        {
            "title": "Goal Setting Framework Creator",
            "prompt": '"Help me set [NUMBER] goals for [TIMEFRAME] that are actually achievable. Create: 1) Clear goal definition for each, 2) Why it matters (motivation), 3) Key milestones (progress markers), 4) Potential obstacles and solutions, 5) Success metrics (how I\'ll measure it), 6) Weekly actions to get there. Format as a trackable plan."',
            "use_case": "Setting goals that you'll actually achieve",
            "example": "Input: 3 goals for Q1: fitness, learning, business\nOutput: SMART goals with full tracking framework and weekly actions",
            "tips": "Focus on 3-5 goals max. More than that and none of them get attention."
        }
    ]
}

def create_pdf():
    """Generate professional PDF"""
    output_path = "/root/clawd/gumroad-products-final/ChatGPT-Prompts-Library.pdf"
    
    # Create document
    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        rightMargin=0.75*inch,
        leftMargin=0.75*inch,
        topMargin=0.75*inch,
        bottomMargin=0.75*inch
    )
    
    # Create styles
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=28,
        textColor=PRIMARY_COLOR,
        spaceAfter=6,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    subtitle_style = ParagraphStyle(
        'Subtitle',
        parent=styles['Normal'],
        fontSize=14,
        textColor=TEXT_COLOR,
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName='Helvetica'
    )
    
    category_style = ParagraphStyle(
        'Category',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=white,
        spaceAfter=12,
        spaceBeforeFont=12,
        fontName='Helvetica-Bold',
        backColor=PRIMARY_COLOR,
        leftIndent=12,
        rightIndent=12,
        topPadding=8,
        bottomPadding=8
    )
    
    prompt_title_style = ParagraphStyle(
        'PromptTitle',
        parent=styles['Heading3'],
        fontSize=12,
        textColor=PRIMARY_COLOR,
        spaceAfter=6,
        fontName='Helvetica-Bold'
    )
    
    label_style = ParagraphStyle(
        'Label',
        parent=styles['Normal'],
        fontSize=9,
        textColor=SECONDARY_COLOR,
        spaceAfter=3,
        fontName='Helvetica-Bold'
    )
    
    content_style = ParagraphStyle(
        'Content',
        parent=styles['Normal'],
        fontSize=9,
        textColor=TEXT_COLOR,
        spaceAfter=6,
        leading=12,
        fontName='Helvetica'
    )
    
    # Build PDF content
    story = []
    
    # Cover page
    story.append(Spacer(1, 1.5*inch))
    story.append(Paragraph("ChatGPT PROMPTS LIBRARY", title_style))
    story.append(Spacer(1, 0.2*inch))
    story.append(Paragraph("Productivity Edition", subtitle_style))
    story.append(Spacer(1, 0.3*inch))
    
    cover_text = ParagraphStyle(
        'CoverText',
        parent=styles['Normal'],
        fontSize=11,
        textColor=TEXT_COLOR,
        spaceAfter=12,
        alignment=TA_CENTER,
        leading=16
    )
    story.append(Paragraph("50 Ready-to-Use ChatGPT Prompts<br/>for Maximum Productivity", cover_text))
    story.append(Spacer(1, 0.5*inch))
    
    story.append(Paragraph(f"<font color='#059669'><b>Version 1.0</b></font><br/>{datetime.now().strftime('%B %Y')}", 
                          ParagraphStyle('Date', parent=styles['Normal'], alignment=TA_CENTER, fontSize=10)))
    
    story.append(PageBreak())
    
    # Table of contents
    story.append(Paragraph("TABLE OF CONTENTS", title_style))
    story.append(Spacer(1, 0.2*inch))
    
    toc_items = [
        ("Category 1: Task Management & TODO", "Prompts 1-10"),
        ("Category 2: Time Management & Scheduling", "Prompts 11-20"),
        ("Category 3: Productivity Systems & Planning", "Prompts 21-30"),
        ("Category 4: Automation & Workflow Optimization", "Prompts 31-40"),
        ("Category 5: Goal Setting & Progress Tracking", "Prompts 41-50"),
    ]
    
    toc_style = ParagraphStyle(
        'TOC',
        parent=styles['Normal'],
        fontSize=11,
        textColor=TEXT_COLOR,
        spaceAfter=8,
        leading=14
    )
    
    for category, prompts in toc_items:
        story.append(Paragraph(f"<b>{category}</b> — {prompts}", toc_style))
    
    story.append(Spacer(1, 0.3*inch))
    story.append(Paragraph("Quick Reference: Top 10 Most-Used Prompts", ParagraphStyle('Heading', parent=styles['Heading3'], fontSize=12, textColor=PRIMARY_COLOR)))
    story.append(Spacer(1, 0.1*inch))
    
    top_10 = [
        "Priority Matrix (#2) - Eisenhower decision making",
        "Weekly Audit (#11) - Understanding your time",
        "Quarterly Goals (#41) - Strategic planning",
        "Time Blocking (#12) - Perfect schedule design",
        "Weekly Review (#25) - Reflection and tracking",
        "Procrastination Override (#27) - Getting unstuck",
        "Email Workflow (#32) - Inbox management",
        "Urgent vs Important (#14) - Decision confidence",
        "Task Blocker Solver (#3) - Breaking through blocks",
        "Retrospective (#50) - Learning and growth",
    ]
    
    for item in top_10:
        story.append(Paragraph(f"• {item}", content_style))
    
    story.append(PageBreak())
    
    # Prompts content
    prompt_counter = 1
    for category, prompts in prompts_data.items():
        story.append(Paragraph(category, category_style))
        story.append(Spacer(1, 0.15*inch))
        
        for prompt in prompts:
            story.append(Paragraph(f"{prompt_counter}. {prompt['title']}", prompt_title_style))
            
            story.append(Paragraph("<b>Prompt:</b>", label_style))
            story.append(Paragraph(prompt['prompt'], content_style))
            
            story.append(Paragraph("<b>Use Case:</b>", label_style))
            story.append(Paragraph(prompt['use_case'], content_style))
            
            story.append(Paragraph("<b>Example:</b>", label_style))
            story.append(Paragraph(prompt['example'], content_style))
            
            story.append(Paragraph("<b>Pro Tip:</b>", label_style))
            story.append(Paragraph(prompt['tips'], content_style))
            
            story.append(Spacer(1, 0.15*inch))
            
            prompt_counter += 1
        
        story.append(PageBreak())
    
    # Back matter
    story.append(Spacer(1, 0.3*inch))
    story.append(Paragraph("HOW TO USE THIS LIBRARY", category_style))
    story.append(Spacer(1, 0.15*inch))
    
    how_to_items = [
        ("<b>Step 1: Find Your Challenge</b> — Look for a prompt matching your current situation",),
        ("<b>Step 2: Copy the Prompt</b> — Use the exact text provided",),
        ("<b>Step 3: Fill in Brackets</b> — Replace [BRACKETS] with your specific information",),
        ("<b>Step 4: Paste into ChatGPT</b> — Get custom, actionable output",),
        ("<b>Step 5: Iterate and Refine</b> — Ask follow-up questions for deeper insights",),
    ]
    
    for item in how_to_items:
        story.append(Paragraph(item[0], content_style))
        story.append(Spacer(1, 0.08*inch))
    
    story.append(Spacer(1, 0.2*inch))
    story.append(Paragraph("BEST PRACTICES", category_style))
    story.append(Spacer(1, 0.15*inch))
    
    best_practices = [
        "Be specific with your information — detail enables better answers",
        "Go deep — don't settle for the first answer, ask follow-ups",
        "Iterate — run the same prompt monthly to track progress",
        "Personalize — modify prompts to match your language and style",
        "Experiment — try different prompts for the same challenge",
    ]
    
    for practice in best_practices:
        story.append(Paragraph(f"✓ {practice}", content_style))
        story.append(Spacer(1, 0.08*inch))
    
    # Build PDF
    doc.build(story)
    print(f"✅ PDF created: {output_path}")
    return output_path

if __name__ == "__main__":
    create_pdf()
