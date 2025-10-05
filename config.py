# ============================================================
# X BOT CONFIGURATION
# ============================================================

# SEARCH SETTINGS
KEYWORD = "onlyfans"
SEARCH_TYPE = "top"
MAX_REPLIES_PER_CYCLE = 5  # Reply to top 5 posts per cycle

# CONTINUOUS MODE
RUN_CONTINUOUSLY = True  # True = runs in loop, False = runs once
CYCLE_DELAY_MINUTES = 10  # Wait time between cycles

# ENGAGEMENT SETTINGS
CHECK_MENTIONS = True  # Check for replies to your posts
REPLY_TO_MENTIONS = True  # Reply to people who replied to you
MAX_MENTION_REPLIES_PER_CYCLE = 3  # Reply to max 3 mentions per cycle

# IMAGE SETTINGS
ATTACH_IMAGE = True
IMAGE_PATH = "/root/x-bot/reply_image.jpg"

# MODE SETTINGS
DRY_RUN = True  # Set to False for live posting
WARM_UP = True

# REPLY GENERATION SETTINGS
SYSTEM_MESSAGE = """You are a (young sexy girl, barely legal, literacy of a high school dropout) horny and fowl mouth OnlyFans model. Reply with one short, sexy line to give men boners. Keep it suggestive, explicit, <80 chars. (USE THE DON'T REFER TO YOURSELF IN THE THIRD PERSON, DON'T INCLUDE PARENTHESIS)"""

INPUT_PROMPT_TEMPLATE = """You are a sexy female responding to males, use a one-liner reply to this post, emojis welcome, <80 chars (EXCLUDE PARENTHESIS):"""

# TIMING SETTINGS (in seconds)
DELAY_BETWEEN_REPLIES_MIN = 30
DELAY_BETWEEN_REPLIES_MAX = 60
DRY_RUN_DELAY_MIN = 2
DRY_RUN_DELAY_MAX = 5

# OLLAMA SETTINGS
OLLAMA_MODEL = "roxas/moethida"
OLLAMA_URL = "http://localhost:11434/api/generate"
