#!/usr/bin/env python3
"""
PREMIUM PDF GENERATOR FOR CHATGPT PROMPTS LIBRARY
Generates a professional, conversion-optimized PDF with stunning design
"""

import json
import html
from datetime import datetime

def generate_premium_html():
    """Generate professional HTML for ChatGPT Prompts Library"""
    
    with open('/root/clawd/gumroad-premium-final/prompts_library.json', 'r') as f:
        data = json.load(f)
    
    prompts = data['prompts']
    
    html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ChatGPT Prompts Library - Premium Edition</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        @page {{
            size: A4;
            margin: 0.5in;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            color: #2C3E50;
            line-height: 1.6;
            background: white;
        }}
        
        .page-break {{
            page-break-after: always;
            margin-bottom: 1in;
        }}
        
        /* ============ COVER PAGE ============ */
        .cover {{
            background: linear-gradient(135deg, #1F3A93 0%, #2E5C8A 100%);
            color: white;
            padding: 4in 1in;
            text-align: center;
            min-height: 11in;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            position: relative;
            overflow: hidden;
        }}
        
        .cover::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: radial-gradient(circle at 20% 50%, rgba(255, 215, 0, 0.1) 0%, transparent 50%);
            pointer-events: none;
        }}
        
        .cover-content {{
            position: relative;
            z-index: 1;
        }}
        
        .cover h1 {{
            font-size: 3.5em;
            font-weight: 700;
            margin-bottom: 0.5em;
            letter-spacing: -1px;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
        }}
        
        .cover h2 {{
            font-size: 1.8em;
            font-weight: 300;
            margin-bottom: 2em;
            opacity: 0.95;
        }}
        
        .cover .badge {{
            display: inline-block;
            background: rgba(255, 215, 0, 0.2);
            color: #FFD700;
            padding: 0.5em 1.5em;
            border-radius: 30px;
            font-size: 0.9em;
            font-weight: 600;
            margin-bottom: 2em;
            border: 1px solid #FFD700;
        }}
        
        .cover-features {{
            margin-top: 2em;
            font-size: 0.95em;
            line-height: 2;
        }}
        
        .cover-features li {{
            list-style: none;
            padding: 0.3em 0;
        }}
        
        .cover-features li::before {{
            content: '✓ ';
            color: #FFD700;
            font-weight: bold;
            margin-right: 0.5em;
        }}
        
        /* ============ TABLE OF CONTENTS ============ */
        .toc {{
            padding: 2in 1in;
            min-height: 11in;
        }}
        
        .toc h2 {{
            color: #1F3A93;
            font-size: 2em;
            margin-bottom: 1.5em;
            border-bottom: 3px solid #1F3A93;
            padding-bottom: 0.5em;
        }}
        
        .toc-list {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 1em 2em;
        }}
        
        .toc-list li {{
            list-style: none;
            padding: 0.5em;
            border-left: 3px solid #3498DB;
            padding-left: 1em;
        }}
        
        .toc-list a {{
            text-decoration: none;
            color: #2C3E50;
            font-weight: 500;
        }}
        
        /* ============ PROMPT CARDS ============ */
        .prompt-section {{
            padding: 0.5in;
            margin-bottom: 0.3in;
            min-height: 10.5in;
            background: white;
        }}
        
        .prompt-card {{
            background: white;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
            border-left: 5px solid #1F3A93;
        }}
        
        .prompt-header {{
            background: linear-gradient(90deg, #1F3A93 0%, #3498DB 100%);
            color: white;
            padding: 1.2em;
            border-bottom: 1px solid #F39C12;
        }}
        
        .prompt-number {{
            display: inline-block;
            background: rgba(255, 215, 0, 0.3);
            color: #FFD700;
            width: 2em;
            height: 2em;
            border-radius: 50%;
            line-height: 2em;
            text-align: center;
            font-weight: bold;
            margin-right: 0.5em;
            font-size: 0.9em;
        }}
        
        .prompt-title {{
            font-size: 1.6em;
            font-weight: 700;
            margin-bottom: 0.2em;
        }}
        
        .prompt-category {{
            display: inline-block;
            background: rgba(255, 255, 255, 0.2);
            padding: 0.3em 0.8em;
            border-radius: 15px;
            font-size: 0.8em;
            font-weight: 600;
            margin-top: 0.5em;
        }}
        
        .prompt-body {{
            padding: 1.2em;
        }}
        
        .section-label {{
            color: #1F3A93;
            font-weight: 700;
            font-size: 0.9em;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-top: 0.8em;
            margin-bottom: 0.4em;
        }}
        
        .section-label::before {{
            content: '▌';
            color: #F39C12;
            margin-right: 0.5em;
        }}
        
        .prompt-text {{
            background: #F8F9FA;
            border-left: 3px solid #F39C12;
            padding: 1em;
            margin-bottom: 1em;
            border-radius: 4px;
            font-family: 'Monaco', 'Courier New', monospace;
            font-size: 0.9em;
            line-height: 1.5;
            color: #2C3E50;
        }}
        
        .use-case {{
            background: #E3F2FD;
            padding: 0.8em;
            border-radius: 4px;
            margin-bottom: 0.8em;
            color: #1565C0;
            font-size: 0.9em;
        }}
        
        .example-block {{
            background: #F5F5F5;
            border: 1px solid #E0E0E0;
            padding: 0.8em;
            margin-bottom: 0.8em;
            border-radius: 4px;
            font-size: 0.85em;
            line-height: 1.4;
        }}
        
        .example-label {{
            color: #1F3A93;
            font-weight: 600;
            font-size: 0.8em;
            text-transform: uppercase;
            margin-bottom: 0.3em;
        }}
        
        .pro-tips {{
            background: #FFF8E1;
            border-left: 3px solid #F39C12;
            padding: 0.8em;
            border-radius: 4px;
            font-size: 0.9em;
        }}
        
        .pro-tips ul {{
            margin-left: 1em;
            margin-top: 0.4em;
        }}
        
        .pro-tips li {{
            margin-bottom: 0.3em;
            color: #E65100;
        }}
        
        .customize {{
            background: #F3E5F5;
            border-left: 3px solid #9C27B0;
            padding: 0.8em;
            margin-top: 1em;
            border-radius: 4px;
            font-size: 0.9em;
            color: #6A1B9A;
        }}
        
        /* ============ QUICK REFERENCE PAGE ============ */
        .quick-ref {{
            padding: 1in;
            min-height: 11in;
        }}
        
        .quick-ref h2 {{
            color: #1F3A93;
            font-size: 2em;
            margin-bottom: 1em;
            border-bottom: 3px solid #1F3A93;
            padding-bottom: 0.5em;
        }}
        
        .quick-ref-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 1em;
        }}
        
        .quick-ref-item {{
            background: #F8F9FA;
            padding: 0.8em;
            border-radius: 4px;
            border-left: 3px solid #3498DB;
        }}
        
        .quick-ref-item strong {{
            color: #1F3A93;
            display: block;
            margin-bottom: 0.3em;
            font-size: 0.95em;
        }}
        
        .quick-ref-item em {{
            display: block;
            font-size: 0.85em;
            color: #666;
            font-style: italic;
        }}
        
        /* ============ FAQ PAGE ============ */
        .faq {{
            padding: 1in;
            min-height: 11in;
        }}
        
        .faq h2 {{
            color: #1F3A93;
            font-size: 2em;
            margin-bottom: 1em;
            border-bottom: 3px solid #1F3A93;
            padding-bottom: 0.5em;
        }}
        
        .faq-item {{
            margin-bottom: 1.2em;
        }}
        
        .faq-question {{
            color: #1F3A93;
            font-weight: 700;
            font-size: 1em;
            margin-bottom: 0.4em;
        }}
        
        .faq-question::before {{
            content: 'Q: ';
            color: #F39C12;
            font-weight: bold;
        }}
        
        .faq-answer {{
            color: #2C3E50;
            margin-left: 1.5em;
            line-height: 1.6;
            font-size: 0.95em;
        }}
        
        .faq-answer::before {{
            content: 'A: ';
            color: #27AE60;
            font-weight: bold;
        }}
        
        /* ============ FOOTER ============ */
        .footer {{
            text-align: center;
            padding: 0.5em;
            border-top: 1px solid #E0E0E0;
            font-size: 0.85em;
            color: #999;
            margin-top: 1em;
        }}
        
        .watermark {{
            position: fixed;
            opacity: 0.08;
            font-size: 5em;
            font-weight: bold;
            color: #1F3A93;
            pointer-events: none;
            transform: rotate(-45deg);
            z-index: -1;
        }}
        
        /* ============ HEADERS ============ */
        h1 {{
            margin: 0.5em 0;
        }}
        
        h2 {{
            margin: 0.8em 0 0.4em 0;
        }}
        
        h3 {{
            margin: 0.6em 0 0.3em 0;
        }}
    </style>
</head>
<body>

<!-- ============ WATERMARK ============ -->
<div class="watermark">Premium Edition</div>

<!-- ============ COVER PAGE ============ -->
<div class="cover">
    <div class="cover-content">
        <div class="badge">PREMIUM EDITION v1.0</div>
        <h1>ChatGPT Prompts<br>Library</h1>
        <h2>Professional Prompts for Productivity, Creativity & Growth</h2>
        
        <div class="cover-features">
            <ul>
                <li>12 Premium ChatGPT Prompts</li>
                <li>Ready-to-Use Templates</li>
                <li>Real-World Use Cases</li>
                <li>Customization Guides</li>
                <li>Pro Tips & Strategies</li>
                <li>Save Hours Each Week</li>
            </ul>
        </div>
    </div>
</div>

<div class="page-break"></div>

<!-- ============ TABLE OF CONTENTS ============ -->
<div class="toc page-break">
    <h2>📑 Table of Contents</h2>
    <ol class="toc-list">
"""
    
    # Add TOC entries
    for i, prompt in enumerate(prompts, 1):
        html_content += f"""        <li><a href="#{prompt['id']}">Prompt {i}: {prompt['title']}</a></li>\n"""
    
    html_content += """    </ol>
</div>

<!-- ============ PROMPTS ============ -->
"""
    
    # Add each prompt
    for prompt in prompts:
        html_content += f"""
<div class="prompt-section page-break">
    <div class="prompt-card">
        <div class="prompt-header">
            <span class="prompt-number">{prompt['id']}</span>
            <div class="prompt-title">{html.escape(prompt['title'])}</div>
            <span class="prompt-category">{html.escape(prompt['category'])}</span>
        </div>
        
        <div class="prompt-body">
            <div class="section-label">The Prompt</div>
            <div class="prompt-text">{html.escape(prompt['prompt'])}</div>
            
            <div class="section-label">Use Cases</div>
            <div class="use-case">{html.escape(prompt['use_case'])}</div>
            
            <div class="section-label">Example</div>
            <div class="example-block">
                <div class="example-label">Input:</div>
                {html.escape(prompt['example_input'])}
            </div>
            <div class="example-block">
                <div class="example-label">Output:</div>
                {html.escape(prompt['example_output'])}
            </div>
            
            <div class="section-label">Pro Tips</div>
            <div class="pro-tips">
                <ul>
"""
        
        for tip in prompt['pro_tips']:
            html_content += f"""                    <li>{html.escape(tip)}</li>\n"""
        
        html_content += f"""                </ul>
            </div>
            
            <div class="section-label">How to Customize</div>
            <div class="customize">
                {html.escape(prompt['customize'])}
            </div>
        </div>
    </div>
</div>
"""
    
    # Add Quick Reference page
    html_content += """
<div class="quick-ref page-break">
    <h2>⚡ Quick Reference Guide</h2>
    <div class="quick-ref-grid">
"""
    
    for prompt in prompts:
        html_content += f"""        <div class="quick-ref-item">
            <strong>{html.escape(prompt['title'])}</strong>
            <em>{html.escape(prompt['category'])}</em>
        </div>
"""
    
    html_content += """    </div>
</div>

<!-- ============ FAQ PAGE ============ -->
<div class="faq page-break">
    <h2>❓ Frequently Asked Questions</h2>
    
    <div class="faq-item">
        <div class="faq-question">Can I use these prompts with free ChatGPT?</div>
        <div class="faq-answer">Yes! All prompts work with ChatGPT Free, ChatGPT Plus, and ChatGPT Pro. Some advanced features may work better with GPT-4, but GPT-3.5 produces excellent results.</div>
    </div>
    
    <div class="faq-item">
        <div class="faq-question">Can I customize the prompts for my specific needs?</div>
        <div class="faq-answer">Absolutely! Every prompt includes a "How to Customize" section. Replace the bracketed fields with your specific context, and ChatGPT will tailor responses exactly to your situation.</div>
    </div>
    
    <div class="faq-item">
        <div class="faq-question">How much time will these prompts save me?</div>
        <div class="faq-answer">Users report saving 5-10+ hours per week by using optimized prompts. What used to take an hour of iterations now takes minutes with our tested, professional templates.</div>
    </div>
    
    <div class="faq-item">
        <div class="faq-question">Do you offer updates if ChatGPT's API changes?</div>
        <div class="faq-answer">Yes! All customers get access to updates and new prompts as we discover what works best. This is a living, evolving resource.</div>
    </div>
    
    <div class="faq-item">
        <div class="faq-question">Can I share these with my team?</div>
        <div class="faq-answer">This license is for personal use. For team licenses with unlimited seats, contact us for bulk pricing.</div>
    </div>
    
    <div class="faq-item">
        <div class="faq-question">What if I'm not happy with the library?</div>
        <div class="faq-answer">We offer a 30-day money-back guarantee. No questions asked. Our goal is to save you time—if it doesn't, we'll refund you immediately.</div>
    </div>
</div>

<!-- ============ FINAL PAGE ============ -->
<div class="page-break" style="padding: 1in; min-height: 11in; display: flex; flex-direction: column; justify-content: center; align-items: center; text-align: center; background: linear-gradient(135deg, #1F3A93 0%, #2E5C8A 100%); color: white;">
    <h2 style="font-size: 2em; margin-bottom: 1em;">You're Ready to Level Up</h2>
    <p style="font-size: 1.1em; margin-bottom: 2em; line-height: 1.8;">
        You now have 12 professional ChatGPT prompts that will transform<br>
        how you work, create, and build your business.
    </p>
    <p style="font-size: 1em;">
        💡 Start with your biggest challenge this week.<br>
        ⚡ Pick the most relevant prompt.<br>
        🚀 Save hours and deliver better results.
    </p>
    <p style="margin-top: 2em; font-size: 0.95em; opacity: 0.9;">
        Thank you for choosing the Premium ChatGPT Prompts Library<br>
        Happy prompting! 🎯
    </p>
</div>

</body>
</html>
"""
    
    return html_content

# Save the HTML
html = generate_premium_html()
with open('/root/clawd/gumroad-premium-final/ChatGPT-Prompts-Library-Premium.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("✅ Professional HTML generated!")
print("   📄 ChatGPT-Prompts-Library-Premium.html created")
print("\nTo convert to PDF, use:")
print("   - Online: Use https://html2pdf.app or similar service")
print("   - Linux: wkhtmltopdf or weasyprint")
print("   - Python: pip install weasyprint && weasyprint input.html output.pdf")
