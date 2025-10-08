# ============================================================
# X CASINO BOT CONFIGURATION
# ============================================================

# AFFILIATE SETTINGS
AFFILIATE_LINK = "https://gamba.com?c=beastaura"  # CHANGE THIS to your tracked link
CASINO_NAME = "Gamba"  # The casino you're promoting

# SEARCH STRATEGY POOL
# Bot will pick from these using weighted random selection
STRATEGY_POOL = [
    "best online casino",
    "casino bonus",
    "slots online",
    "need casino recommendation",
    "casino withdrawal problems",
    "crypto casino",
    "online gambling",
    "sports betting casino"
]

# SAFETY LIMITS (Safe Mode)
MAX_REPLIES_PER_HOUR = 20
MAX_REPLIES_PER_DAY = 100
ACCOUNT_COOLDOWN_DAYS = 7  # Don't reply to same account within X days
MAX_CONSECUTIVE_FAILURES = 3  # Pause bot after X failures

# CONTENT FILTERS
# Bot will skip tweets containing these words
BLACKLIST_KEYWORDS = [
    "addiction",
    "gambling addiction",
    "quit gambling",
    "gambling problem",
    "help me stop",
    "gamble responsibly",
    "self-exclude"
]

# Bot will skip these accounts
BLACKLIST_ACCOUNTS = [
    # Add accounts to avoid, e.g. "verified_news_account"
]

# SCORING WEIGHTS (how bot picks best tweet to reply to)
SCORE_RELEVANCE = 40  # How relevant to casino topic
SCORE_ENGAGEMENT = 20  # Existing likes/replies on tweet
SCORE_RECENCY = 15  # How recent (< 6 hours)
SCORE_QUESTION = 15  # Is it a question?
SCORE_LOW_FOLLOWERS = 10  # Low follower count (< 5k)

# LEARNING SYSTEM
INITIAL_STRATEGY_WEIGHT = 10  # Starting weight for all strategies
WEIGHT_BOOST_LIKE = 5  # Weight increase if our reply gets liked
WEIGHT_BOOST_REPLY = 10  # Weight increase if our reply gets replied to
WEIGHT_BOOST_RETWEET = 15  # Weight increase if our reply gets retweeted
WEIGHT_PENALTY_NO_ENGAGEMENT = -2  # Weight decrease if no engagement

# TIMING SETTINGS
SLEEP_MIN_SECONDS = 60  # Minimum wait between replies (1 minute)
SLEEP_MAX_SECONDS = 180  # Maximum wait between replies (3 minutes)

# MODE SETTINGS
DRY_RUN = True  # True = test mode (no actual posts), False = live posting
WARM_UP = True  # True = browse normally first to look human (only affects first run)

# REPLY GENERATION SETTINGS
REPLY_PROMPT_TEMPLATE = """You are a helpful member of the online casino community. Someone just posted about casinos/gambling. Write a natural, friendly reply (1-2 sentences, under 200 characters) that:
1. Responds directly to what they said
2. Naturally recommends {casino_name} with this link: {affiliate_link}
3. Sounds like a real person sharing their experience
4. Is not salesy or spammy

Tweet from @{{username}}: {{tweet_text}}

Your reply (include the link naturally):"""

# OLLAMA SETTINGS
OLLAMA_MODEL = "llama3.2"  # Which LLM model to use
OLLAMA_URL = "http://localhost:11434/api/generate"  # Ollama API endpoint

# ADVANCED SETTINGS
MAX_TWEET_AGE_HOURS = 24  # Only reply to tweets newer than this
MAX_CANDIDATES_TO_FETCH = 20  # How many tweets to fetch per search
MIN_LEARNING_SAMPLES = 20  # How many replies before weight adjustment kicks in
