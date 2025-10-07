# ============================================================
# X BOT CONFIGURATION
# Edit these settings to customize your bot behavior
# ============================================================

# SEARCH SETTINGS
TARGET_INFLUENCERS = ['BigfoltzVIP', 'HerroCrypto', 'Mrbankstips', 'BlazinHotBets', 'thegaboeth']  # Top gambling influencers
KEYWORD = "(from:BigfoltzVIP OR from:HerroCrypto OR from:Mrbankstips OR from:BlazinHotBets OR from:thegaboeth) (win OR bonus OR slots OR jackpot) filter:videos min_replies:10"  # Fixed "bonu" to "bonus"
MAX_REPLIES = 50  # Increased for more replies per run (be cautious of bans)
REPLY_FILTER_KEYWORDS = ['amazing', 'wow', 'nice', 'fire', 'lfg', 'insane', '🔥', '💰', 'gl', 'good luck', 'lets go', 'yo', 'bro', 'gm', '🤑', '👻', '🎃', 'epic', 'huge', 'win', 'bonus', 'slots', 'jackpot']  # Further expanded to catch more hype replies
MAX_REPLY_LENGTH = 100  # Increased to catch more varied replies

# AFFILIATE SETTINGS
AFFILIATE_LINK = "https://gamba.com/?c=gambaniest&utm_source=x_replier&utm_campaign=gambaniest"  # Affiliate link with UTM

# MODE SETTINGS
DRY_RUN = True  # True = test mode (no posts), False = live
WARM_UP = True  # True = browse to look human

# REPLY GENERATION SETTINGS
REPLY_PROMPT_TEMPLATE = """You are replying to an excited user in a casino tweet thread. Be fun, urgent, and hype with gambling emojis (🎰, 💸, 🤑). Mention specific bonuses like free spins, rakeback, or daily rewards. Keep it 100-150 chars. Do NOT include any links. Always end with a gambling emoji.

Original tweet: {original_tweet}
Replier @{username}: {replier_text}

Your reply:"""

# TIMING SETTINGS (in seconds)
DELAY_BETWEEN_REPLIES_MIN = 60  # Increased min delay for safety with more replies
DELAY_BETWEEN_REPLIES_MAX = 120  # Increased max delay for safety
DRY_RUN_DELAY_MIN = 2  # Min wait in dry run
DRY_RUN_DELAY_MAX = 5  # Max wait in dry run

# NEW: Interval between full bot cycles (for continuous running)
RUN_INTERVAL_SECONDS = 1800  # 30 minutes between runs (adjust as needed)

# OLLAMA SETTINGS
OLLAMA_MODEL = "llama3.2"  # LLM model
OLLAMA_URL = "http://localhost:11434/api/generate"  # Ollama API endpoint
