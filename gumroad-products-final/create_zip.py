#!/usr/bin/env python3
import zipfile
import os
from pathlib import Path

output_path = "/root/clawd/gumroad-products-final/Gumroad-Products-Complete.zip"
source_dir = "/root/clawd/gumroad-products-final"

# Files to include
files = [
    "ChatGPT-Prompts-Library.html",
    "01-Master-Task-Manager.csv",
    "02-Weekly-Planner.csv",
    "03-30-Day-Habit-Tracker.csv",
    "04-Project-Manager.csv",
    "05-Budget-Tracker.csv",
    "06-Time-Blocker.csv",
    "07-Goal-Tracker.csv",
    "08-Content-Calendar.csv",
    "09-Daily-Journal.csv",
    "10-Affiliate-Income-Tracker.csv",
    "QUICK-START-GUIDE.txt",
    "GOOGLE-SHEETS-SETUP-GUIDE.txt",
    "GUMROAD-UPLOAD-GUIDE.txt",
]

with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zf:
    for file in files:
        file_path = os.path.join(source_dir, file)
        if os.path.exists(file_path):
            zf.write(file_path, arcname=file)
            print(f"✓ Added: {file}")
    
    # Create a README for the ZIP
    readme = """PRODUCTIVITY BUNDLE - COMPLETE

This ZIP contains everything you need to transform your productivity.

CONTENTS:
=========

ChatGPT Prompts Library (HTML format - open in any web browser):
  - ChatGPT-Prompts-Library.html (50 ready-to-use prompts)

Google Sheets Templates (CSV format - import to Google Sheets):
  1. 01-Master-Task-Manager.csv
  2. 02-Weekly-Planner.csv
  3. 03-30-Day-Habit-Tracker.csv
  4. 04-Project-Manager.csv
  5. 05-Budget-Tracker.csv
  6. 06-Time-Blocker.csv
  7. 07-Goal-Tracker.csv
  8. 08-Content-Calendar.csv
  9. 09-Daily-Journal.csv
  10. 10-Affiliate-Income-Tracker.csv

Guides (Text format):
  - QUICK-START-GUIDE.txt (30-minute setup plan)
  - GOOGLE-SHEETS-SETUP-GUIDE.txt (detailed template instructions)
  - GUMROAD-UPLOAD-GUIDE.txt (if you want to sell your own version)

GETTING STARTED:
================

1. START HERE: Open QUICK-START-GUIDE.txt
2. THEN: Open ChatGPT-Prompts-Library.html in your web browser
3. TRY: Use the Priority Matrix prompt (#2) with your tasks
4. IMPORT: Bring the CSV files into Google Sheets
5. SETUP: Follow GOOGLE-SHEETS-SETUP-GUIDE.txt for your first template

QUICK WINS (Next 30 minutes):
============================

1. Try Priority Matrix (#2) - Instant clarity on priorities (5 min)
2. Set up Weekly Planner - Plan your perfect week (20 min)  
3. Start one habit - Pick your easiest habit (2 min setup)

This bundle is worth $100+ but you got it for one price.

Questions? Everything is covered in the guides.

Ready? Let's go! 🚀
"""
    
    zf.writestr("README.txt", readme)
    print(f"✓ Added: README.txt")

print(f"\n✅ ZIP file created: {output_path}")
size = os.path.getsize(output_path) / (1024*1024)
print(f"   Size: {size:.2f} MB")
print(f"   Files: {len(files) + 1}")
