# Google Sheets Templates Pack - Productivity Edition
## Detailed Specifications for 10 Ready-to-Share Templates

---

## TEMPLATE 1: Master Task Manager

### Purpose
All-in-one task management system with priority levels, deadlines, dependencies, and progress tracking.

### Column Structure
| Column | Type | Purpose | Example |
|--------|------|---------|---------|
| A: Task ID | Text | Unique identifier | TASK-001 |
| B: Task Name | Text | What needs to be done | Write quarterly report |
| C: Description | Text | Details about the task | Include Q4 metrics, trends, recommendations |
| D: Category | Dropdown | Task category | Project / Admin / Personal / Meeting |
| E: Priority | Dropdown | Importance level | High / Medium / Low |
| F: Status | Dropdown | Current state | Not Started / In Progress / Blocked / Complete |
| G: Assigned To | Text | Who's responsible | Your name |
| H: Due Date | Date | Deadline | 2024-03-15 |
| I: Days Until Due | Formula | Time remaining | `=H2-TODAY()` |
| J: Start Date | Date | When work begins | 2024-03-01 |
| K: Estimated Hours | Number | Time budget | 8 |
| L: Actual Hours | Number | Time spent | 6.5 |
| M: Progress % | Number | Completion rate | 85% |
| N: Dependencies | Text | Other tasks required first | TASK-003, TASK-005 |
| O: Notes | Text | Additional context | Waiting on client feedback |
| P: Tags | Text | Keywords for filtering | #urgent #client #report |

### Key Formulas

**Color Coding by Status (Conditional Formatting)**
- Not Started = Light gray
- In Progress = Light blue
- Blocked = Light orange
- Complete = Light green
- Overdue = Light red

**Auto-Status Update**
```
IF(M2=1,"Complete",IF(TODAY()>H2,"Overdue",F2))
```

**Overdue Alert**
```
IF(AND(F2<>"Complete",TODAY()>H2),"⚠️ OVERDUE",IF(I2<2,"Due Soon",""))
```

**Week View Priority**
```
FILTER(A:P,F:F="In Progress",I:I<7)
```

### Example Data
```
Task: "Design new landing page"
Category: Project
Priority: High
Status: In Progress
Due: March 20, 2024
Progress: 60%
Dependencies: Content from marketing
Assigned: Sarah
```

### Setup Instructions
1. Copy the template to your Google Drive
2. Update the Category, Priority, and Status dropdowns to your needs
3. Add your task list (import from Asana/Todoist if you have export)
4. Enable conditional formatting: Format → Conditional formatting
5. Set up notification rules on Due Date column
6. Share with your team if needed

### Advanced Features
- **Priority Matrix View:** Create pivot table showing all tasks by Priority × Status
- **Timeline View:** Create Gantt chart using Status and Due Date
- **Team Capacity:** Duplicate "Assigned To" column and count tasks per person
- **Burndown Chart:** Graph Progress % over time to see velocity

### Integration Ideas
- Connect to Google Calendar: Due dates automatically create calendar events
- Send to Slack: Daily digest of "In Progress" tasks
- Zapier automation: New Asana tasks auto-populate this sheet

---

## TEMPLATE 2: Weekly Planner with Time Blocks

### Purpose
Hour-by-hour scheduling system with time blocking for deep work, meetings, and admin tasks.

### Column Structure
| Column | Type | Purpose | Example |
|--------|------|---------|---------|
| A: Time Slot | Time | Hour of day | 8:00 AM - 9:00 AM |
| B: Monday | Text | Activity scheduled | Deep Work: Coding |
| C: Tuesday | Text | Activity scheduled | Team Meeting |
| D: Wednesday | Text | Activity scheduled | Admin Time |
| E: Thursday | Text | Activity scheduled | Client Call |
| F: Friday | Text | Activity scheduled | Weekly Review |
| G: Notes | Text | Context/location | Conference room 3B |
| H: Energy Level | Dropdown | Expected energy | High / Medium / Low |
| I: Task Category | Dropdown | Type of work | Deep Work / Meeting / Admin / Break |
| J: Duration | Time | How long (auto) | 1 hour |
| K: Focus Required | Dropdown | Yes / No / Maybe | Yes |

### Sheet Tabs
1. **Template** - Blank template for new week
2. **Week 1 (3/4-3/8)** - Current week example
3. **Week 2 (3/11-3/15)** - Next week example
4. **Analysis** - Summary stats for the week

### Key Formulas

**Block Category Color Coding**
```
"Deep Work" = Blue
"Meeting" = Orange
"Admin" = Gray
"Break" = Green
```

**Time Block Integrity Check**
```
IF(AND(B2<>"",B2<>"Break"),IF(K2="No","⚠️ Should be break",IF(K2="Yes","✓","")),""
)
```

**Weekly Summary Stats**
```
Deep Work Hours: COUNTIF(I:I,"Deep Work") * 1
Meeting Hours: COUNTIF(I:I,"Meeting") * 1
Admin Hours: COUNTIF(I:I,"Admin") * 1
Break Hours: COUNTIF(I:I,"Break") * 1
```

**Optimal Time Block Detector**
```
IF(AND(ROWS($A$2:A2)>3,COUNTIF($I$2:I2,"Deep Work")>=3),"✓ Good focus block","")
```

### Example Data
```
8:00-9:00am Monday: "Deep Work: Website redesign" (High energy, Yes focus, Blue)
9:00-10:00am Monday: Break (Green)
10:00-12:00pm Monday: "Team standup + planning" (Medium, No focus, Orange)
1:00-3:00pm Monday: "Deep Work: Code review" (High energy, Yes focus, Blue)
3:00-4:00pm Monday: "Admin: Emails & Slack" (Low energy, No focus, Gray)
4:00-5:00pm Monday: Planning for tomorrow (Medium, Maybe focus, Gray)
```

### Setup Instructions
1. Customize your time slots (7am-10pm example shown, adjust as needed)
2. Input your typical week's fixed commitments first (meetings, recurring events)
3. Block deep work during high-energy hours
4. Add breaks strategically (every 90 min rule)
5. Review Sunday evening and adjust
6. Set phone reminders for transitions

### Advanced Features
- **Calendar Sync:** Pull meetings directly from Google Calendar
- **Energy Tracking:** Log actual energy levels and refine future blocks
- **Context Switching Counter:** Count how many times you switch tasks (minimize!)
- **Ideal vs Actual:** Track planned vs what actually happened

### Integration Ideas
- Zapier to Google Calendar: Each time block creates calendar event
- Daily digest: Email you the day's schedule each morning
- Weekly summary: Calculate deep work hours and identify optimization

---

## TEMPLATE 3: 30-Day Habit Tracker

### Purpose
Simple, visual daily habit tracking with streak counting and trend analysis.

### Column Structure
| Column | Type | Purpose | Example |
|--------|------|---------|---------|
| A: Date | Date | Calendar date | 3/1/2024 |
| B: Day | Text/Formula | Day of week | Monday |
| C-G: Habits | Checkbox | Track 5 habits | Exercise, Meditate, Read, Journal, Sleep |
| H: Total Habits | Formula | How many completed today | 4/5 |
| I: Completion % | Formula | % of habits done | 80% |
| J: Notes | Text | What happened | Skipped exercise due to rain |
| K: Energy Level | Dropdown | How you felt | High / Medium / Low |
| L: Mood | Dropdown | Overall mood | Great / Good / Okay / Rough |

### Extended Structure (by Habit)
For each habit column, create a secondary tracking row showing:
- Current Streak
- Longest Streak
- Completion Rate %
- Best Time of Day
- Notes on what works

### Key Formulas

**Daily Completion %**
```
=COUNTIF(C2:G2,TRUE)/5 * 100
```

**Current Streak (for each habit)**
```
=SUMPRODUCT((C$2:C2<>"")*(C$2:C2=TRUE)*ROW(C$2:C2))/SUMPRODUCT((C$2:C2<>"")*(C$2:C2=TRUE))
=COUNTA(C$2:C2)-SUMPRODUCT(--(C$2:C2=FALSE))
```

**Habit Completion Rate**
```
=COUNTIF(C2:C31,TRUE)/COUNTA(C2:C31)
```

**Correlation: Energy Level vs Habits**
```
=CORREL(I2:I31,K2:K31) [Shows if good days = more habits]
```

**Goal Progress (e.g., 25 days of 30)**
```
=COUNTIFS(I2:I31,">=80%")/30
```

### Example Data
```
Date: March 1
Exercise: ✓
Meditate: ✓
Read: ✗ (ran out of time)
Journal: ✓
Sleep (8hrs): ✓
Daily Total: 4/5 (80%)
Energy: High
Mood: Good
```

### Setup Instructions
1. List your 5 key habits (adjust number if needed)
2. Set 30-day date range (auto-populate with formula)
3. Create simple checkbox system (TRUE/FALSE or ✓/✗)
4. Add daily notes section for context
5. Add weekly summary row every 7 days
6. Print and post, OR check off daily in sheet

### Advanced Features
- **Heat Map:** Color intensity shows streaks (dark = consistent)
- **Best Day Tracking:** Which day of week are you most consistent?
- **Trigger Analysis:** Does energy/mood predict habit completion?
- **Personal Best:** Track longest streaks and total days completed

### Monthly Reflection Prompts
- Which habit was easiest/hardest?
- What blocked you on tough days?
- What would make next month better?
- Which 1 habit should I focus on?

### Integration Ideas
- Daily check-in: Send yourself a form each morning to submit habits
- Weekly report: Automated email showing weekly completion
- Slack reminder: Daily message to remind you to log habits

---

## TEMPLATE 4: Project Manager (Tasks + Timeline + Owner)

### Purpose
Comprehensive project tracking with task dependencies, timeline visualization, and team assignment.

### Column Structure
| Column | Type | Purpose | Example |
|--------|------|---------|---------|
| A: Phase | Dropdown | Project phase | Planning / Design / Build / Test / Launch |
| B: Task # | Text | Unique ID | 1.1, 1.2, 2.1 |
| C: Task Name | Text | What to do | Create wireframes |
| D: Description | Text | Details | Desktop + mobile versions |
| E: Owner | Text | Who leads | Design team |
| F: Team Members | Text | All involved | Sarah, Mike, Lisa |
| G: Status | Dropdown | Current state | Not Started / In Progress / Blocked / Review / Complete |
| H: Priority | Dropdown | Importance | Critical / High / Medium / Low |
| I: Start Date | Date | When beginning | 3/4/2024 |
| J: Due Date | Date | Deadline | 3/15/2024 |
| K: Days Remaining | Formula | Time left | =J2-TODAY() |
| L: % Complete | Number | Progress | 75% |
| M: Estimate Hours | Number | Budget | 40 |
| N: Actual Hours | Number | Spent | 32 |
| O: Dependencies | Text | Tasks needed first | 1.1, 1.3 |
| P: Blockers | Text | What's stopping progress | Waiting on client feedback |
| Q: Notes | Text | Additional info | On track for launch |

### Sheet Tabs
1. **Gantt Chart View** - Timeline visualization
2. **By Owner** - Tasks grouped by person
3. **By Status** - Progress view
4. **Timeline** - Start/Due dates with visual bar
5. **Risk Log** - Potential issues and mitigations

### Key Formulas

**Timeline Bar (Gantt Style)**
```
Create a bar from Start Date to Due Date with color based on Status
=REPT("█",INT((J2-I2)/3))
```

**On-Track Assessment**
```
=IF(AND(L2>=(TODAY()-I2)/(J2-I2)*100,G2<>"Complete"),"✓ On Track","⚠️ Behind")
```

**Days Until Deadline**
```
=IF(J2<TODAY(),"⚠️ OVERDUE",IF(J2-TODAY()<=3,"Due Soon!",J2-TODAY()&" days"))
```

**Team Workload (by owner)**
```
=SUMIF(E:E,"Sarah") [Counts tasks assigned to Sarah]
=SUMIF(E:E,"Sarah",N:N) [Sums hours for Sarah]
```

**Predecessor Block**
```
=IF(COUNTIF(O2,"1.1")>0,IF(INDEX(G:G,MATCH("1.1",B:B,0))="Complete","Ready","Blocked"),IF(INDEX(G:G,MATCH(VALUE(LEFT(O2,FIND(",",O2)-1)),B:B,0))="Complete","Ready","Blocked"))
```

**Critical Path Identifier**
```
=IF(AND(H2="Critical",K2<5),"🚨 CRITICAL DEADLINE","")
```

### Example Data
```
Phase: Design
Task: 2.1 - Create high-fidelity mockups
Owner: Sarah Chen
Team: Sarah, Mike (feedback)
Status: In Progress (60%)
Start: 3/6/2024
Due: 3/13/2024
Hours: Est 25, Actual 18
Blockers: None
Dependencies: Task 1.5 (wireframes - complete)
```

### Setup Instructions
1. Break project into phases
2. List all tasks with clear owners
3. Set start and due dates
4. Link dependencies (what needs to happen first)
5. Estimate hours for each task
6. Share with team and assign permissions
7. Update status weekly

### Advanced Features
- **Critical Path Analysis:** Which tasks matter most for deadline?
- **Resource Planning:** Who's overloaded? Who has capacity?
- **Risk Dashboard:** Blockers and dependencies in one view
- **Burndown Chart:** Visual progress toward completion

### Weekly Status Meeting Template
- Red/Yellow/Green status for each phase
- What's blocking progress?
- This week's priorities
- Next week's risks
- Help needed

---

## TEMPLATE 5: Budget Tracker (Income + Expenses)

### Purpose
Track all income and expenses with categories, monthly summaries, and financial insights.

### Column Structure - INCOME Sheet
| Column | Type | Purpose | Example |
|--------|------|---------|---------|
| A: Date | Date | Transaction date | 3/5/2024 |
| B: Income Source | Text | Where money came from | Client project |
| C: Category | Dropdown | Income type | Project / Salary / Passive / Other |
| D: Description | Text | Details | Web redesign project |
| E: Amount | Currency | How much | $2,500 |
| F: Status | Dropdown | Received / Pending / Invoiced | Received |
| G: Invoice # | Text | Reference | INV-2024-015 |
| H: Notes | Text | Additional context | Final payment |

### Column Structure - EXPENSES Sheet
| Column | Type | Purpose | Example |
|--------|------|---------|---------|
| A: Date | Date | Expense date | 3/7/2024 |
| B: Category | Dropdown | Expense type | Software / Equipment / Marketing / Meals |
| C: Subcategory | Dropdown | More specific | Adobe Subscription |
| D: Description | Text | What it was | Monthly Adobe Creative Cloud |
| E: Amount | Currency | Cost | $54.99 |
| F: Vendor | Text | Who you paid | Adobe |
| G: Payment Method | Dropdown | How paid | Credit Card / Bank Transfer / Cash |
| H: Deductible | Checkbox | Tax deductible? | ✓ |
| I: Project Billable | Text | Can bill to client? | Project XYZ |
| J: Receipts | URL | Link to receipt | https://receipt.pdf |
| K: Notes | Text | Additional info | Annual plan renewal |

### Sheet Tabs
1. **Income** - All revenue
2. **Expenses** - All costs
3. **Summary** - Monthly totals and comparisons
4. **By Category** - Spending breakdown
5. **Trends** - Income/expense trends over time
6. **Invoicing** - Track billable expenses

### Key Formulas

**Monthly Income Total**
```
=SUMIFS(E:E,A:A,">="&DATE(2024,3,1),A:A,"<"&DATE(2024,4,1))
```

**Monthly Expense Total by Category**
```
=SUMIFS(E:E,B:B,"Software",A:A,">="&DATE(2024,3,1),A:A,"<"&DATE(2024,4,1))
```

**Income vs Expenses**
```
=SUMIF(A:A,MONTH(TODAY()))-SUMIF(B:B,MONTH(TODAY()))
```

**Profit Margin %**
```
=((Income - Expenses) / Income) * 100
```

**Deductible Expenses Total**
```
=SUMIFS(E:E,H:H,TRUE,A:A,">="&DATE(2024,1,1),A:A,"<"&DATE(2024,12,31))
```

**Monthly Comparison Growth**
```
=((Current Month - Previous Month) / Previous Month) * 100
```

**Cash Flow Forecast**
```
Next 3 months income minus upcoming committed expenses
=SUMIFS(Income,Date,">="&TODAY(),Date,"<"&TODAY()+90)-SUMIFS(Expenses,Date,">="&TODAY(),Date,"<"&TODAY()+90)
```

### Example Data
```
INCOME:
Date: 3/5/2024
Source: Client project
Category: Project
Amount: $2,500
Status: Received

EXPENSE:
Date: 3/7/2024
Category: Software
Item: Adobe Subscription
Amount: $54.99
Deductible: Yes
```

### Monthly Summary Section
```
Total Income: $8,500
Total Expenses: $1,200
Gross Profit: $7,300
Profit Margin: 85.9%

By Category:
Software: $342
Equipment: $200
Marketing: $400
Meals: $158
```

### Setup Instructions
1. Create two main sheets: Income and Expenses
2. Set up dropdown categories for your business
3. Log transactions daily or weekly (automate with Zapier if possible)
4. Create Summary sheet with monthly totals
5. Review monthly for insights
6. Use for tax planning and financial decisions

### Advanced Features
- **Revenue Forecasting:** Predict next quarter based on trends
- **Expense Ratio Analysis:** What % of income goes to each category?
- **Seasonal Patterns:** Does income fluctuate by season?
- **Customer Profitability:** Which clients make you the most?

### Tax Prep Helper
Automatically calculates deductible expenses for tax season

---

## TEMPLATE 6: Time Blocker (Weekly Schedule)

### Purpose
Simple visual weekly schedule showing how time is allocated across different activity types.

### Column Structure
| Column | Type | Purpose | Example |
|--------|------|---------|---------|
| A: Time | Time | Hour slot | 8:00 AM |
| B-H: Days | Text | Activity for that time | Deep Work, Meeting, Admin, Break |
| I: Total Deep Work | Formula | Sum of deep work | 15 hours |
| J: Total Meetings | Formula | Sum of meetings | 8 hours |
| K: Total Admin | Formula | Sum of admin | 5 hours |
| L: Total Break | Formula | Sum of breaks | 5 hours |

### Color Coding System
- **Blue** = Deep Work (focus required)
- **Orange** = Meetings
- **Gray** = Admin/Email
- **Green** = Break/Lunch
- **Yellow** = Buffer time
- **Red** = Do Not Schedule (protect this)

### Key Formulas

**Activity Category Summary**
```
Deep Work Hours: =COUNTIF(B2:H50,"Deep Work")
Meeting Hours: =COUNTIF(B2:H50,"Meeting")
Admin Hours: =COUNTIF(B2:H50,"Admin")
Break Hours: =COUNTIF(B2:H50,"Break")
```

**Deep Work Blocks Checker**
```
=IF(COUNTIF(B2:B8,"Deep Work")>=2,"✓ Good deep work block",IF(COUNTIF(B2:B8,"Deep Work")=1,"Okay - single block",IF(COUNTIF(B2:B8,"Deep Work")=0,"⚠️ No deep work!")))
```

**Meeting Free Days Indicator**
```
=IF(COUNTIF(B2:H50,"Meeting")=0,"Meeting-free day! ✓","")
```

**Context Switch Counter**
```
=SUMPRODUCT((B2:H50<>B1:H49)*(B2:H50<>"")) [Counts transitions]
```

### Example Data
```
MONDAY:
8:00-9:00: Deep Work (Code review)
9:00-10:00: Meeting (Team standup)
10:00-12:00: Deep Work (Feature development)
12:00-1:00: Break (Lunch)
1:00-3:00: Deep Work (Testing)
3:00-3:30: Break (Stretch)
3:30-4:30: Admin (Emails, Slack)
4:30-5:00: Planning

Total: 7 hours deep work, 1 hour meetings, 1 hour admin, 1 hour breaks
```

### Setup Instructions
1. Fill in your 9am-5pm (adjust as needed)
2. Block in recurring meetings first
3. Identify your high-energy hours
4. Schedule deep work in those hours
5. Batch admin/email times
6. Include breaks (every 90-120 min)
7. Use conditional formatting for colors

### Optimization Checklist
- [ ] Minimum 2-3 hour deep work blocks?
- [ ] Meetings batched on certain days?
- [ ] High-energy work in peak hours?
- [ ] Breaks scheduled (not skipped)?
- [ ] Context switches minimized?
- [ ] Do Not Disturb time protected?

---

## TEMPLATE 7: Goal Tracker (SMART Goals + Progress)

### Purpose
Track SMART goals with monthly milestones, progress indicators, and success criteria.

### Column Structure
| Column | Type | Purpose | Example |
|--------|------|---------|---------|
| A: Goal ID | Text | Unique ID | G-2024-001 |
| B: Goal Title | Text | Main goal | Launch online course |
| C: Category | Dropdown | Type | Business / Health / Learning / Personal |
| D: Timeframe | Text | Duration | Q1 2024 (3 months) |
| E: SMART Breakdown | Text | Specific/Measurable | 50+ students, $5k revenue |
| F: Current Status | Dropdown | Progress | On Track / At Risk / Off Track / Complete |
| G: % Progress | Number | Completion | 45% |
| H: Key Metric 1 | Text | Main measurement | Course module completion |
| I: Target for Metric 1 | Text | Goal amount | 5 modules by 3/31 |
| J: Current Metric 1 | Number | Today's value | 3 modules |
| K: Success Criteria | Text | How you know it's done | All modules complete, 50+ students |
| L: Milestones | Text | Sub-goals | Module 1 (Feb), Module 2 (Feb), etc |
| M: Progress Notes | Text | Updates | Modules 1-3 complete, on schedule |
| N: Blockers | Text | What's in the way | Need video editor |
| O: Next Action | Text | Immediate next step | Schedule video recording |
| P: Owner | Text | Who leads | You |

### Sheet Tabs
1. **Active Goals** - Current quarter goals
2. **Completed Goals** - Finished goals with results
3. **Monthly Milestones** - Breakdown by month
4. **Goal Reflection** - Review and lessons learned
5. **Next Quarter Planning** - Future goals

### Key Formulas

**Progress Indicator**
```
=IF(G2>=ROUNDUP(ROW()/ROWS(GOAL)*100),IF(G2>100,"✓ Complete!","✓ On Track"),"⚠️ Falling Behind")
```

**Days to Goal Deadline**
```
Assumes 3-month goals, adjust for your timeline
=IF(TODAY()>DATE(YEAR(TODAY()),MONTH(TODAY())+3,DAY(TODAY())),"⏰ OVERDUE",DATE(YEAR(TODAY()),MONTH(TODAY())+3,DAY(TODAY()))-TODAY())
```

**Monthly Milestone Check**
```
Milestone Date should be on track for goal completion by deadline
=IF(TODAY()>DATE(YEAR(TODAY()),MONTH(TODAY())+1,1),"Check March milestone","Track to February milestone")
```

**How-Many-Days-Left Calculator**
```
Considering 3-month quarters: =DATEDIF(TODAY(),DATE(YEAR(TODAY()),MONTH(TODAY())+3,1),"D")
```

### Example Data
```
Goal: Launch online course
Category: Business
Timeframe: Q1 2024
SMART Details:
- Specific: Create 5-module course on ChatGPT prompting
- Measurable: Enroll 50+ students
- Achievable: Have template, audience ready
- Relevant: Core to business
- Time-bound: By March 31, 2024

Metrics:
- Modules completed: 3 of 5 (60%)
- Students enrolled: 15 of 50 (30%)
- Revenue: $2,500 of $5,000 goal (50%)

Status: On Track
Progress: 47%

Milestones:
- Feb 15: Modules 1-2 complete
- Feb 28: Modules 3-4 complete
- Mar 15: Module 5 complete
- Mar 30: 50 students enrolled

Blockers: Need better video editing
Next: Hire video editor this week
```

### Review Questions (Monthly)
1. Am I on track? (compare current progress to milestone)
2. What's blocking progress?
3. Do I need to adjust the goal or timeline?
4. What's one thing I can do this week to move forward?
5. Do I still want this goal?

### Setup Instructions
1. Identify 3-5 goals for the quarter
2. Make each one SMART
3. Break into monthly milestones
4. Identify your key metric to track
5. Set weekly check-in time (Friday works well)
6. Update progress weekly
7. Monthly deep review

---

## TEMPLATE 8: Content Calendar (Social Media Planning)

### Purpose
Plan and track social media content across platforms with scheduling dates and performance metrics.

### Column Structure
| Column | Type | Purpose | Example |
|--------|------|---------|---------|
| A: Date | Date | Publish date | 3/15/2024 |
| B: Platform | Dropdown | Where posting | LinkedIn / Twitter / Instagram / TikTok |
| C: Content Type | Dropdown | Type | Tip / Story / Behind-the-scenes / Educational |
| D: Topic/Theme | Text | Main subject | ChatGPT productivity hack |
| E: Content Summary | Text | What you'll post | 3 ChatGPT prompts for emails |
| F: Hashtags | Text | Keywords | #ChatGPT #Productivity #Writing |
| G: Media | Text | Image/video | Link to file |
| H: Content Status | Dropdown | Stage | Draft / Scheduled / Published / Archived |
| I: Engagement Target | Text | Who you want | Entrepreneurs / Content creators |
| J: Call-to-Action | Text | What to ask | "Save this for later" / "Comment below" |
| K: Schedule Time | Time | Post time | 9:00 AM |
| L: Impressions | Number | Views | 2,500 |
| M: Engagement | Number | Likes + comments | 150 |
| N: Engagement Rate | Formula | % engaged | 6% |
| O: Shares/Saves | Number | Reshares | 45 |
| P: Notes | Text | Ideas/observations | Performed better than expected |

### Sheet Tabs
1. **Content Calendar** - Month view of all posts
2. **By Platform** - What you're posting where
3. **Performance** - Which posts do well
4. **Analytics** - Trends over time
5. **Content Ideas** - Backlog of future posts
6. **Monthly Summary** - Performance review

### Key Formulas

**Engagement Rate**
```
=IF(L2>0,((M2+O2)/L2)*100,0)
```

**Best-Performing Content**
```
=FILTER(E:E,N:N=MAX(N:N)) [Shows highest engagement posts]
```

**Weekly Content Balance**
```
Count each content type per week to ensure variety
=COUNTIFS(A:A,">="&DATE(2024,3,11),A:A,"<"&DATE(2024,3,18),C:C,"Tip")
```

**Platform Distribution**
```
=COUNTIF(B:B,"LinkedIn") [Shows how many LinkedIn posts]
```

**Monthly Impressions Total**
```
=SUMIFS(L:L,A:A,">="&DATE(2024,3,1),A:A,"<"&DATE(2024,4,1))
```

### Example Data
```
Date: March 15, 2024
Platform: LinkedIn
Type: Educational tip
Topic: ChatGPT email automation
Content: "3 ChatGPT prompts for writing emails faster..."
CTA: "Save this for your email templates"
Scheduled Time: 9:00 AM
Status: Published

Results:
Impressions: 2,500
Engagement (likes+comments): 180
Engagement Rate: 7.2%
Shares: 45
```

### Monthly Themes (Example Plan)
```
Week 1: Tips & Tricks (Monday, Wednesday, Friday)
Week 2: Tutorials (Tuesday) + Behind-the-scenes (Thursday)
Week 3: Educational deep-dive (Monday) + User stories (Wednesday)
Week 4: Review highlights (Monday) + Community spotlight (Wednesday)
```

### Content Batching Strategy
1. Pick monthly theme
2. Brainstorm 12-15 ideas
3. Create all content (images/videos/captions)
4. Schedule across month
5. Review performance
6. Refine next month

### Setup Instructions
1. List your platforms
2. Decide posting frequency per platform
3. Create content buckets (Tips, Stories, Educational, etc.)
4. Map out one month as template
5. Batch create content in chunks
6. Schedule in advance
7. Track performance to optimize

---

## TEMPLATE 9: Daily Reflection/Journal Log

### Purpose
Daily journaling and reflection with mood tracking, gratitude, and lesson capture.

### Column Structure
| Column | Type | Purpose | Example |
|--------|------|---------|---------|
| A: Date | Date | Day | 3/15/2024 |
| B: Day of Week | Text | Day | Friday |
| C: Mood Morning | Dropdown | How woke up | Great / Good / Neutral / Rough |
| D: Mood Evening | Dropdown | How ending day | Great / Good / Neutral / Rough |
| E: Energy Level | Dropdown | Physical energy | High / Medium / Low |
| F: Focus Quality | Dropdown | Ability to focus | Excellent / Good / Okay / Poor |
| G: Gratitude 1 | Text | Thankful for | Morning coffee |
| H: Gratitude 2 | Text | Thankful for | Productive meeting |
| I: Gratitude 3 | Text | Thankful for | Good weather |
| J: Top 3 Wins | Text | Accomplishments | 1) Finished report 2) Gym 3) Great call |
| K: Challenge of Day | Text | Main obstacle | Interrupted by urgent email |
| L: How I Handled It | Text | Response | Blocked email time after 4pm |
| M: Lesson Learned | Text | Key insight | Protecting focus time helps |
| N: People Appreciated | Text | Who helped | Sarah, Mike, John |
| O: One Thing Better | Text | If redoing day | Would plan morning better |
| P: Tomorrow Priority | Text | Main focus | Finish analysis |
| Q: Notes/Journal | Text | Free form | Longer thoughts, feelings |

### Sheet Tabs
1. **Daily Log** - Day-by-day entries
2. **Weekly Review** - Weekly patterns
3. **Monthly Insights** - Monthly trends
4. **Lessons Learned** - Extracting wisdom
5. **Gratitude Tracker** - Patterns of appreciation

### Key Formulas

**Mood Trend (Weekly)**
```
Average mood for the week
=AVERAGE(IF(MONTH(A:A)=MONTH(TODAY()),IF(WEEK(A:A)=WEEK(TODAY()),IF(C:C="Great",4,IF(C:C="Good",3,IF(C:C="Neutral",2,1))))))
```

**Energy Correlation**
```
Does mood match energy level?
=COUNTIFS(C:C,"Great",E:E,"High") [Days you felt great + high energy]
```

**Wins Count**
```
=COUNTA(J:J) [Total wins recorded]
```

**Weekly Gratitude Count**
```
=COUNTA(G:G)+COUNTA(H:H)+COUNTA(I:I) [Total things grateful for]
```

**Challenge Pattern Recognition**
```
=COUNTIF(K:K,"*email*") [How often email interruptions occurred]
```

### Example Entry
```
Date: March 15, 2024 (Friday)
Morning Mood: Good
Evening Mood: Great
Energy: High
Focus: Excellent

Gratitudes:
1. Completed challenging project
2. Great lunch with Sarah
3. Clear blue sky

Top 3 Wins:
1. Finished analysis report (delivered 1 day early)
2. Had productive 1-on-1 with team member
3. Completed daily habits (exercise, meditation, journaling)

Challenge: Interruptions from Slack messages
How handled: Set "Do Not Disturb" 2-4pm
Lesson: Protecting focus time is critical

Tomorrow's Priority: Present findings to stakeholders

People to appreciate: Sarah (feedback), Coach (accountability)

Overall reflection: Felt productive and energized when I protected focus time. Need to continue this pattern.
```

### Setup Instructions
1. Create daily rows (month view, or year if detail)
2. Set reminder to fill out each evening (10 minutes)
3. Keep answers short (2-3 sentences max)
4. Do weekly review (30 minutes)
5. Monthly reflection (1 hour)
6. Annual review (look back at year)

### Weekly Review Template
```
Week of March 11-15:
- Overall mood trend: Improving (3.2/4)
- Energy pattern: Good except Tuesday
- Biggest wins: Project completion, focus time
- Main challenges: Email management
- This week's lessons: Setting boundaries works
- Next week: Double down on focus blocks
- Someone to thank: Team for support
```

---

## TEMPLATE 10: Affiliate/Income Tracker

### Purpose
Track affiliate partnerships, commission rates, sales, and earnings by platform and partner.

### Column Structure
| Column | Type | Purpose | Example |
|--------|------|---------|---------|
| A: Partner/Platform | Text | Affiliate program | Amazon Associates |
| B: Program Type | Dropdown | Relationship | Affiliate / Referral / Partner / Sponsorship |
| C: Commission % | Number | Rate per sale | 5% |
| D: Status | Dropdown | Active / Inactive / Pending | Active |
| E: Signup Date | Date | When joined | 1/15/2024 |
| F: Promo Link | Text | Your unique link | amzn.to/my-link-1 |
| G: Monthly Clicks | Number | Traffic sent | 450 |
| H: Click Rate | Formula | % of impressions | 2.1% |
| I: Monthly Sales | Number | Revenue generated | $1,250 |
| J: Commission Earned | Formula | Money paid | $62.50 |
| K: Payment Status | Dropdown | Paid / Pending / Unpaid | Paid |
| L: Last Payment | Date | When paid | 3/1/2024 |
| M: YTD Earnings | Formula | Year to date | $425.75 |
| N: Promotion Method | Text | How you promote | Email list, Blog, Social |
| O: Best Performer | Checkbox | Top earner? | ✓ |
| P: Notes | Text | Context | Good audience fit |

### Sheet Tabs
1. **Active Partners** - Current affiliate programs
2. **Performance** - Best earners, click rates
3. **Monthly Summary** - Total earnings by month
4. **Promotion Tracking** - Which methods work best
5. **Pipeline** - Pending partnerships

### Key Formulas

**Monthly Commission**
```
=I2*(C2/100)
```

**YTD (Year-to-Date) Total**
```
=SUMIFS(J:J,A:A,"Amazon Associates",E:E,">="&DATE(2024,1,1))
```

**Top Earners**
```
=FILTER(A:A,J:J=MAX(J:J))
```

**Conversion Rate**
```
=IF(G2>0,I2/G2,0) [Sales / Clicks]
```

**Projected Annual (if 12 months)**
```
=IF(MONTH(TODAY())>0,(J2/MONTH(TODAY()))*12,J2)
```

**Partner Tier Status**
```
=IF(M2>5000,"Tier 3 - Gold",IF(M2>2500,"Tier 2 - Silver","Tier 1 - Bronze"))
```

### Example Data
```
Partner: Amazon Associates
Type: Affiliate
Commission: 5%
Status: Active

Monthly Performance (March):
Clicks sent: 450
Sales generated: $1,250
Commission earned: $62.50

YTD Total: $425.75
Promotion Method: Blog recommendations + email

Notes: Strong performer, good fit with audience
```

### Platform Breakdown (Example)
```
Amazon Associates: $425 YTD
Skillshare: $180 YTD
ConvertKit: $95 YTD
AppSumo: $210 YTD
Total: $910 YTD

Best performer: Amazon (46.8% of total)
Most potential: ConvertKit (can grow)
```

### Setup Instructions
1. List all affiliate programs you're part of
2. Enter commission rates and signup dates
3. Get your unique promo links
4. Decide promotion strategy (blog, email, social)
5. Log traffic/clicks monthly
6. Record sales and commissions
7. Review monthly to optimize partnerships

### Optimization Insights
- Which partners have best conversion rates?
- Which promotion methods drive most sales?
- Which partners should you promote more?
- Are there gaps in your affiliate coverage?

### Promotion Batching
```
Email list: Mention Amazon + Skillshare
Blog posts: Link 2-3 relevant products
Social media: Highlight top earners monthly
Newsletter: Feature new partnership
```

---

## QUICK START GUIDE

### Getting Started (Next 30 Minutes)
1. Choose 1 template to start with
2. Copy to Google Drive
3. Customize column names to your language/style
4. Add your first week/month of data
5. Set up one conditional formatting rule
6. Test a formula

### Best Practices
- **Update weekly** - Stale data = useless
- **Simple first** - Add complexity after you're comfortable
- **Share carefully** - Only share what others need to see
- **Archive old data** - Keep sheets focused on current period
- **Test formulas** - In a test row before applying to all

### Integration Opportunities (with Zapier)
- Google Forms → Template (auto-populate)
- Gmail → Templates (log important emails)
- Calendar events → Time Blocker (auto-schedule)
- Slack messages → Daily Journal (auto-capture)
- Email reminders for weekly review

### Customization Ideas
- Add your company logo (top of sheets)
- Change colors to match your brand
- Add your timezone (for time-based formulas)
- Link to other sheets (reference formulas)
- Create a dashboard tab that summarizes all templates

### Common Questions

**Q: Can I use these on mobile?**
A: Yes, Google Sheets is mobile-friendly. Desktop is better for editing, but viewing/updating on phone works.

**Q: Can I share with my team?**
A: Yes! Set permissions (view/edit/comment) for each sheet. Some templates work better for teams (Project Manager, Goal Tracker).

**Q: How do I sync data between templates?**
A: Use VLOOKUP or INDEX/MATCH formulas to pull data from one template to another.

**Q: How often should I update?**
A: Daily for habit tracking, weekly for others. Monthly review of all templates.

---

**Version:** 1.0  
**Format:** Google Sheets (copy and use)  
**Difficulty Level:** Beginner-friendly with optional advanced features  
**Time to Setup:** 15-30 minutes per template  
**Maintenance:** 10-30 minutes per week depending on usage
