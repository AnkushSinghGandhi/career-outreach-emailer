import os

# --- Automation & Depth Settings ---
RUN_OUTREACH_AUTO = True
RUN_FOLLOWUP_AUTO = False
RUN_BOUNCE_CHECK_AUTO = False
RUN_REPLY_CHECK_AUTO = False
CHECK_DAYS_BACK = 20

# --- General Configuration ---
EMAIL_ADDRESS = os.environ.get("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD")

ATTACHMENT_PATH = "resume.pdf"
LINKS = "\nhttps://warriorwhocodes.com\nhttps://www.linkedin.com/in/ankushsinghgandhi"

# --- Initial Outreach Settings ---
INITIAL_LIMIT = 100
INITIAL_MIN_DELAY = 60
INITIAL_MAX_DELAY = 250

INITIAL_SUBJECTS = [
    "Application for Python/Backend Developer Role",
    "Exploring Python Backend Opportunities",
    "Regarding Python Backend Position",
    "Interest in Python Developer Openings",
    "Application: Python Backend Engineer",
    "Inquiry About Python Developer Roles",
    "Potential Fit for Python Backend Position",
    "Profile for Python/Backend Developer"
]

INITIAL_OPENINGS = [
    "I hope you're doing well.",
    "Hope you're having a great day.",
    "Hope you're doing great.",
    "I hope everything is going well on your end.",
    "Hope you're staying productive and healthy.",
    "Trust you're doing well.",
    "Hope this message finds you well.",
    "I appreciate you taking a moment to read this.",
    "Thank you for your time.",
    "Hope you're having a productive week."
]

INITIAL_SIGNATURES = [
    "Best regards,\nAnkush Singh Gandhi\n+91-95296-39652",
    "Warm regards,\nAnkush Singh Gandhi\n+91-95296-39652",
    "Sincerely,\nAnkush Singh Gandhi\n+91-95296-39652",
    "Thank you,\nAnkush Singh Gandhi\n+91-95296-39652",
    "Best,\nAnkush\n+91-95296-39652",
    "Regards,\nAnkush\n+91-95296-39652",
]

INITIAL_BODY_TEMPLATE = """
Hi {first_name},

{opening}

I’m reaching out to explore opportunities for Python Backend roles within your organization or network. 
I have 2+ years of experience working with Flask, Django, REST APIs, MySQL, MongoDB, Redis, and cloud deployments — 
with strong focus on scalable backend systems and performance optimization.

I understand you may not be hiring immediately, but I would appreciate the opportunity to connect or 
be considered for future openings. I genuinely believe my backend engineering experience can be a strong fit 
for fast-growing teams.

Thank you for your time. Happy to provide any additional information.

{signature}
{links}
"""

# --- Follow-up Settings ---
FOLLOWUP_LIMIT = 40
FOLLOWUP_MIN_DELAY = 40
FOLLOWUP_MAX_DELAY = 60

FOLLOWUP_SUBJECTS = [
    "Following up on my previous email",
    "Quick follow-up on my application",
    "Checking in regarding my earlier message",
    "Just circling back on my application",
    "Wanted to follow up on my previous note",
]

FOLLOWUP_OPENERS = [
    "Hope you’re doing well.",
    "Hope your day is going great.",
    "I hope you're having a productive week.",
    "Hope everything is going smoothly on your side.",
    "I hope you’re doing well and staying healthy.",
]

FOLLOWUP_BODY_VARIANTS = [
    """
I wanted to quickly follow up on my earlier message regarding potential Python/Backend Developer opportunities.

I understand things can get busy, so I just wanted to check in and see if you had a chance to review my previous email. 
I’m still very interested in any backend roles involving Python, Django, Flask, REST APIs, or database work.

If you need any additional details from my side, I’d be happy to share them.
""",

    """
Just following up on my previous email about backend roles.  
I know schedules get packed, so I thought I’d circle back to see if you had a moment to review my application.

I remain excited about opportunities involving Python, API development, and scalable backend systems.
If there's anything more you need, feel free to let me know.
""",

    """
I'm checking in regarding my earlier note about Python backend opportunities.

I understand hiring timelines vary, so no rush — just wanted to ensure my previous email didn't get missed.  
I’m still very much interested and open to discussing how my experience in Python, Django, Flask, and databases aligns with your team’s needs.
""",

    """
Reaching out again to follow up on my previous message.

I know you receive many emails, so I wanted to check in politely. I’m still actively exploring opportunities that involve backend engineering, API development, and Python-based systems.
If there's any update or next step you'd recommend, I’d appreciate hearing from you.
"""
]

FOLLOWUP_SIGNATURES = [
    """
Best regards,  
Ankush Singh Gandhi  
https://warriorwhocodes.com  
""",

    """
Warm regards,  
Ankush  
https://warriorwhocodes.com  
""",

    """
Thanks and regards,  
Ankush Singh  
https://warriorwhocodes.com  
""",

    """
Sincerely,  
Ankush  
Backend Developer  
https://warriorwhocodes.com  
""",
]

FOLLOWUP_BODY_TEMPLATE = "Hi {first_name},\n\n{opener}\n{body}\n{signature}"
