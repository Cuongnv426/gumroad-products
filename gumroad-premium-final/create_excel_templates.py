#!/usr/bin/env python3
"""
PREMIUM GOOGLE SHEETS TEMPLATES GENERATOR
Creates 10 beautifully designed spreadsheet templates
Uses CSV format (can be imported to Google Sheets)
"""

import csv
import os
import json

def create_task_manager():
    """Master Task Manager - Color-coded by priority"""
    return {
        'name': 'Master Task Manager',
        'headers': ['Task ID', 'Task Name', 'Category', 'Priority', 'Status', 'Assigned To', 'Start Date', 'Due Date', 'Progress %', 'Notes'],
        'sample_data': [
            ['TK001', 'Q1 Strategic Planning', 'Business', 'High', 'In Progress', 'Sarah', '2024-01-01', '2024-01-31', '75', 'Quarterly planning session'],
            ['TK002', 'Website Redesign', 'Projects', 'High', 'Blocked', 'John', '2024-01-05', '2024-02-15', '40', 'Waiting on design approval'],
            ['TK003', 'Email Campaign Launch', 'Marketing', 'Medium', 'In Progress', 'Emma', '2024-01-08', '2024-01-20', '60', 'Copywriting in progress'],
            ['TK004', 'Team Meeting Prep', 'Admin', 'Medium', 'Not Started', 'Sarah', '2024-01-15', '2024-01-17', '0', 'Agenda needed'],
            ['TK005', 'Client Presentation', 'Sales', 'High', 'Completed', 'Mike', '2024-01-01', '2024-01-10', '100', 'Great feedback received'],
            ['TK006', 'Documentation Update', 'Admin', 'Low', 'Not Started', 'Alex', '2024-01-10', '2024-02-28', '0', 'Can be scheduled later'],
        ]
    }

def create_weekly_planner():
    """Weekly Planner - Visual time blocks"""
    return {
        'name': 'Weekly Planner',
        'headers': ['Time', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
        'sample_data': [
            ['6:00 AM', 'Workout', 'Workout', 'Workout', 'Workout', 'Workout', 'Rest', 'Rest'],
            ['7:00 AM', 'Breakfast', 'Breakfast', 'Breakfast', 'Breakfast', 'Breakfast', 'Brunch', 'Brunch'],
            ['8:00 AM', 'Deep Work', 'Deep Work', 'Deep Work', 'Deep Work', 'Deep Work', 'Personal', 'Personal'],
            ['9:00 AM', 'Deep Work', 'Deep Work', 'Deep Work', 'Deep Work', 'Deep Work', 'Personal', 'Personal'],
            ['10:00 AM', 'Meetings', 'Deep Work', 'Meetings', 'Deep Work', 'Meetings', 'Personal', 'Leisure'],
            ['11:00 AM', 'Meetings', 'Email', 'Meetings', 'Email', 'Planning', 'Social', 'Leisure'],
            ['12:00 PM', 'Lunch', 'Lunch', 'Lunch', 'Lunch', 'Lunch', 'Social', 'Lunch'],
            ['1:00 PM', 'Focused Work', 'Focused Work', 'Focused Work', 'Focused Work', 'Focused Work', 'Activities', 'Leisure'],
            ['2:00 PM', 'Focused Work', 'Focused Work', 'Focused Work', 'Focused Work', 'Focused Work', 'Activities', 'Leisure'],
            ['3:00 PM', 'Admin/Email', 'Admin/Email', 'Admin/Email', 'Admin/Email', 'Admin/Email', 'Shopping', 'Prep'],
            ['4:00 PM', 'Collaboration', 'Collaboration', 'Collaboration', 'Collaboration', 'Buffer', 'Shopping', 'Prep'],
            ['5:00 PM', 'Wrap-up', 'Wrap-up', 'Wrap-up', 'Wrap-up', 'Wrap-up', 'Dinner', 'Dinner'],
            ['6:00 PM', 'Personal', 'Personal', 'Personal', 'Personal', 'Personal', 'Entertainment', 'Entertainment'],
        ]
    }

def create_habit_tracker():
    """30-Day Habit Tracker - Progress bars"""
    habits = ['Morning Exercise', 'Read 30min', 'Meditation', 'Drink Water', 'Journal', 'Learn Something']
    headers = ['Habit'] + [f'Day {i+1}' for i in range(30)]
    sample_data = []
    for habit in habits:
        row = [habit] + ['✓' if i % (5-len(habit)%4) == 0 else '○' for i in range(30)]
        sample_data.append(row)
    
    return {
        'name': '30-Day Habit Tracker',
        'headers': headers,
        'sample_data': sample_data
    }

def create_project_manager():
    """Project Manager - Gantt visualization"""
    return {
        'name': 'Project Manager',
        'headers': ['Task', 'Owner', 'Start', 'End', 'Duration (days)', 'Status', 'Priority', '% Complete', 'Dependencies'],
        'sample_data': [
            ['Discovery & Planning', 'Sarah', '2024-01-01', '2024-01-15', '14', 'Completed', 'High', '100', 'None'],
            ['Design Mockups', 'Alex', '2024-01-08', '2024-01-31', '23', 'In Progress', 'High', '65', 'Discovery'],
            ['Frontend Development', 'Mike', '2024-01-20', '2024-02-28', '39', 'In Progress', 'High', '40', 'Design'],
            ['Backend API Dev', 'John', '2024-01-20', '2024-02-20', '31', 'In Progress', 'High', '55', 'Discovery'],
            ['QA & Testing', 'Emma', '2024-02-15', '2024-02-28', '13', 'Not Started', 'Medium', '0', 'Development'],
            ['Content Creation', 'Tom', '2024-01-15', '2024-02-10', '26', 'In Progress', 'Medium', '70', 'None'],
            ['Launch & Deploy', 'Sarah', '2024-03-01', '2024-03-05', '4', 'Not Started', 'Critical', '0', 'QA'],
        ]
    }

def create_budget_tracker():
    """Budget Tracker - Income vs Expenses"""
    return {
        'name': 'Budget Tracker',
        'headers': ['Date', 'Category', 'Description', 'Amount', 'Type', 'Status'],
        'sample_data': [
            ['2024-01-01', 'Salary', 'Monthly Salary', '5000', 'Income', 'Received'],
            ['2024-01-02', 'Utilities', 'Electric Bill', '150', 'Expense', 'Paid'],
            ['2024-01-03', 'Groceries', 'Weekly Groceries', '120', 'Expense', 'Paid'],
            ['2024-01-05', 'Freelance', 'Consulting Project', '1500', 'Income', 'Received'],
            ['2024-01-07', 'Rent', 'Monthly Rent', '1200', 'Expense', 'Paid'],
            ['2024-01-10', 'Dining', 'Restaurants', '85', 'Expense', 'Paid'],
            ['2024-01-12', 'Entertainment', 'Streaming Services', '45', 'Expense', 'Paid'],
            ['2024-01-15', 'Bonus', 'Performance Bonus', '800', 'Income', 'Received'],
            ['2024-01-20', 'Healthcare', 'Medical Checkup', '200', 'Expense', 'Paid'],
            ['2024-01-25', 'Shopping', 'Clothing', '150', 'Expense', 'Pending'],
        ]
    }

def create_time_blocker():
    """Time Blocker - Detailed time blocks"""
    return {
        'name': 'Time Blocker',
        'headers': ['Time', 'Activity', 'Duration (min)', 'Type', 'Focus Level', 'Completed', 'Notes'],
        'sample_data': [
            ['6:00-6:30', 'Morning Routine', '30', 'Personal', 'Low', 'Yes', 'Meditation & breakfast'],
            ['6:30-7:00', 'Exercise', '30', 'Health', 'High', 'Yes', 'Morning workout'],
            ['8:00-10:00', 'Deep Work - Project A', '120', 'Work', 'Critical', 'Yes', 'No interruptions'],
            ['10:00-10:15', 'Break', '15', 'Break', 'Low', 'Yes', 'Coffee break'],
            ['10:15-12:00', 'Deep Work - Project B', '105', 'Work', 'Critical', 'In Progress', 'Focused coding'],
            ['12:00-1:00', 'Lunch & Social', '60', 'Break', 'Low', 'Yes', 'Team lunch'],
            ['1:00-2:30', 'Meetings', '90', 'Work', 'Medium', 'In Progress', 'Client calls'],
            ['2:30-3:00', 'Email & Admin', '30', 'Admin', 'Low', 'No', 'Batch processing'],
            ['3:00-4:30', 'Learning & Growth', '90', 'Development', 'High', 'No', 'Course module'],
            ['4:30-5:00', 'Daily Review', '30', 'Planning', 'Medium', 'No', 'Next day prep'],
        ]
    }

def create_goal_tracker():
    """Goal Tracker - SMART goals"""
    return {
        'name': 'Goal Tracker',
        'headers': ['Goal', 'Category', 'SMART Goal', 'Target', 'Current Progress', 'Deadline', 'Status', 'Owner'],
        'sample_data': [
            ['Increase Sales Revenue', 'Business', 'Increase revenue by 30% YoY', '30% increase', '12% to date', '2024-12-31', 'On Track', 'Sales Team'],
            ['Improve Customer Satisfaction', 'Customer', 'Achieve 95% NPS score', '95', '88 current', '2024-06-30', 'On Track', 'Operations'],
            ['Launch New Product', 'Product', 'Launch 2 new features', '2 features', '1 launched', '2024-03-31', 'On Track', 'Product Team'],
            ['Team Development', 'People', 'Complete certifications for 80% of team', '8 of 10', '3 completed', '2024-09-30', 'In Progress', 'HR'],
            ['Cost Optimization', 'Finance', 'Reduce operating costs by 20%', '20% reduction', '8% savings', '2024-12-31', 'On Track', 'Finance'],
            ['Market Expansion', 'Strategic', 'Enter 2 new markets', '2 markets', '0 entered', '2024-08-31', 'Planning', 'Strategy'],
        ]
    }

def create_content_calendar():
    """Content Calendar - Multi-platform"""
    return {
        'name': 'Content Calendar',
        'headers': ['Date', 'Platform', 'Content Type', 'Title', 'Status', 'Scheduled Time', 'Engagement Goal'],
        'sample_data': [
            ['2024-01-15', 'Instagram', 'Carousel', 'Top 5 Productivity Tips', 'Published', '9:00 AM', '500 likes'],
            ['2024-01-15', 'LinkedIn', 'Article', 'Future of Remote Work', 'Scheduled', '10:00 AM', '200 shares'],
            ['2024-01-16', 'TikTok', 'Video', '60-second Success Story', 'Draft', '6:00 PM', '10K views'],
            ['2024-01-16', 'Blog', 'Post', 'Deep Dive: AI Tools', 'Published', 'Evergreen', 'Organic traffic'],
            ['2024-01-17', 'YouTube', 'Tutorial', 'How to Use Our Platform', 'In Production', '2:00 PM', '500 views'],
            ['2024-01-17', 'Twitter', 'Thread', 'Daily productivity insights', 'Scheduled', '8:00 AM', '100 RTs'],
            ['2024-01-18', 'Instagram', 'Reel', 'Behind the scenes', 'Draft', '7:00 PM', '300 likes'],
        ]
    }

def create_daily_journal():
    """Daily Journal - Mood tracking"""
    return {
        'name': 'Daily Journal',
        'headers': ['Date', 'Mood', 'Energy Level', 'Gratitude 1', 'Gratitude 2', 'Gratitude 3', 'Win of the Day', 'Lesson Learned'],
        'sample_data': [
            ['2024-01-14', '😊 Happy', '9/10', 'Great team collaboration', 'Morning coffee', 'Supportive family', 'Completed project milestone', 'Listen more than talk'],
            ['2024-01-13', '😌 Content', '7/10', 'Good health', 'Exercise done', 'Learning new skill', 'Solved difficult problem', 'Ask for help when needed'],
            ['2024-01-12', '😔 Tired', '4/10', 'Still have a job', 'Supportive friends', 'Warm bed', 'Pushed through challenges', 'Rest is productive'],
            ['2024-01-11', '🤗 Excited', '8/10', 'New opportunity', 'My creativity', 'Client appreciation', 'Won new contract', 'Enthusiasm is contagious'],
            ['2024-01-10', '😊 Happy', '8/10', 'My achievements', 'Team celebration', 'Family dinner', 'Shipped new feature', 'Celebrate small wins'],
        ]
    }

def create_affiliate_tracker():
    """Affiliate Tracker - Commission tracking"""
    return {
        'name': 'Affiliate Tracker',
        'headers': ['Program', 'Commission Rate', 'Clicks (Month)', 'Conversions', 'Revenue', 'Payout Status', 'Growth Rate'],
        'sample_data': [
            ['AppOne', '15%', '450', '45', '$675', 'Pending', '+12%'],
            ['WebTool Pro', '20%', '320', '32', '$960', 'Paid', '+8%'],
            ['CloudSoft', '10%', '680', '51', '$510', 'Pending', '+25%'],
            ['SaaS Platform', '25%', '210', '21', '$1,050', 'Paid', '+5%'],
            ['DataTools', '18%', '390', '35', '$630', 'Pending', '+18%'],
            ['MarketingHub', '12%', '560', '45', '$540', 'Paid', '+3%'],
        ]
    }

# Generate all templates
templates = [
    create_task_manager(),
    create_weekly_planner(),
    create_habit_tracker(),
    create_project_manager(),
    create_budget_tracker(),
    create_time_blocker(),
    create_goal_tracker(),
    create_content_calendar(),
    create_daily_journal(),
    create_affiliate_tracker(),
]

# Create directory
os.makedirs('/root/clawd/gumroad-premium-final/templates', exist_ok=True)

# Save as CSV files
for i, template in enumerate(templates, 1):
    filename = f"/root/clawd/gumroad-premium-final/templates/{i:02d}_{template['name'].replace(' ', '_').lower()}.csv"
    
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(template['headers'])
        for row in template['sample_data']:
            writer.writerow(row)
    
    print(f"✅ {template['name']} - {filename}")

print(f"\n✅ All 10 templates created!")
print("   📊 Can be imported to Google Sheets via File > Import")
