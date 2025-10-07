# ============================================================
# X BOT CONFIGURATION
# Edit these settings to customize your bot behavior
# ============================================================

# SEARCH SETTINGS
TARGET_INFLUENCERS = ['BigfoltzVIP', 'HerroCrypto', 'Mrbankstips', 'BlazinHotBets', 'thegaboeth']  # Top gambling influencers
KEYWORD = "(from:BigfoltzVIP OR from:HerroCrypto OR from:Mrbankstips OR from:BlazinHotBets OR from:thegaboeth) (win OR bonus OR slots OR jackpot) filter:videos min_replies:10"  # Target video posts with replies
MAX_REPLIES = 6  # Max 2 replies per thread, 3 threads
REPLY_FILTER_KEYWORDS = ['amazing', 'wow', 'nice', 'fire', 'lfg', 'insane', '🔥', '💰']  # Excited replier keywords
MAX_REPLY_LENGTH = 50  # Max chars for replier tweets to target

# AFFILIATE SETTINGS
AFFILIATE_LINK = "https://gamba.com/?c=gambaniest&utm_source=x_replier&utm_campaign=gambaniest"  # Affiliate link with UTM

# MODE SETTINGS
DRY_RUN = True  # True = test mode (no posts), False = live
WARM_UP = True  # True = browse to look human

# REPLY GENERATION SETTINGS
REPLY_PROMPT_TEMPLATE = """You are replying to an excited user in a casino tweet thread. Be fun, urgent, mention bonuses (e.g., free spins, rakeback), include {affiliate_link}, end with '18+ | Gamble responsibly'. Keep it under 200 chars.

Original tweet: {original_tweet}
Replier @{username}: {replier_text}

Your reply:"""

# TIMING SETTINGS (in seconds)
DELAY_BETWEEN_REPLIES_MIN = 30  # Min wait between replies (live mode)
DELAY_BETWEEN_REPLIES_MAX = 60  # Max wait between replies (live mode)
DRY_RUN_DELAY_MIN = 2  # Min wait in dry run
DRY_RUN_DELAY_MAX = 5  # Max wait in dry run

# OLLAMA SETTINGS
OLLAMA_MODEL = "llama3.2"  # LLM model
OLLAMA_URL = "http://localhost:11434/api/generate"  # Ollama API endpoint
