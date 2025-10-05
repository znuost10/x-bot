# ============================================================
# X BOT CONFIGURATION
# Edit these settings to customize your bot behavior
# ============================================================

# SEARCH SETTINGS
KEYWORD = "artificial intelligence"  # What to search for on X
MAX_REPLIES = 5  # How many tweets to reply to per run

# MODE SETTINGS
DRY_RUN = True  # True = test mode (no actual posts), False = live posting
WARM_UP = True  # True = browse normally first to look human

# REPLY GENERATION SETTINGS
REPLY_PROMPT_TEMPLATE = """You are replying to a tweet. Write a brief, natural, friendly reply (1-2 sentences max, under 200 characters). Be conversational and relevant to what they said. Don't use hashtags. Sound human and authentic.

Tweet from @{username}: {tweet_text}

Your reply:"""

# Alternative prompt templates (uncomment to use):

# PROFESSIONAL TONE
# REPLY_PROMPT_TEMPLATE = """Write a professional, insightful reply to this tweet (1-2 sentences, under 200 characters). Be thoughtful and add value.
#
# Tweet from @{username}: {tweet_text}
#
# Your reply:"""

# CASUAL/FUN TONE
# REPLY_PROMPT_TEMPLATE = """Write a casual, friendly reply to this tweet (1-2 sentences, under 200 characters). Be enthusiastic and relatable. Use occasional emojis.
#
# Tweet from @{username}: {tweet_text}
#
# Your reply:"""

# EXPERT/EDUCATIONAL TONE
# REPLY_PROMPT_TEMPLATE = """Write an expert reply that adds valuable insight (2-3 sentences, under 250 characters). Share knowledge or ask a thoughtful question.
#
# Tweet from @{username}: {tweet_text}
#
# Your reply:"""

# TIMING SETTINGS (in seconds)
DELAY_BETWEEN_REPLIES_MIN = 30  # Minimum wait between replies (live mode)
DELAY_BETWEEN_REPLIES_MAX = 60  # Maximum wait between replies (live mode)
DRY_RUN_DELAY_MIN = 2  # Minimum wait in dry run mode
DRY_RUN_DELAY_MAX = 5  # Maximum wait in dry run mode

# OLLAMA SETTINGS
OLLAMA_MODEL = "llama3.2"  # Which LLM model to use
OLLAMA_URL = "http://localhost:11434/api/generate"  # Ollama API endpoint
