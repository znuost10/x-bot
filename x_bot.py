from playwright.sync_api import sync_playwright
import time
import json
import os
import requests
import random

# Import configuration
from config import (
    KEYWORD, MAX_REPLIES, DRY_RUN, WARM_UP,
    REPLY_PROMPT_TEMPLATE, OLLAMA_MODEL, OLLAMA_URL,
    DELAY_BETWEEN_REPLIES_MIN, DELAY_BETWEEN_REPLIES_MAX,
    DRY_RUN_DELAY_MIN, DRY_RUN_DELAY_MAX,
    REPLY_FILTER_KEYWORDS, MAX_REPLY_LENGTH, AFFILIATE_LINK
)

class XBot:
    def __init__(self):
        self.replied_tweets = self.load_replied_tweets()
        self.ollama_url = OLLAMA_URL
        self.ollama_model = OLLAMA_MODEL
    
    def load_replied_tweets(self):
        if os.path.exists('replied_tweets.json'):
            with open('replied_tweets.json', 'r') as f:
                data = json.load(f)
                if isinstance(data, list):
                    return {'ids': data, 'details': {}}
                return data
        return {'ids': [], 'details': {}}
    
    def save_replied_tweets(self):
        with open('replied_tweets.json', 'w') as f:
            json.dump(self.replied_tweets, f, indent=2)
    
    def random_delay(self, min_sec=1, max_sec=3):
        """Add random human-like delay"""
        delay = random.uniform(min_sec, max_sec)
        time.sleep(delay)
    
    def human_like_scroll(self, page):
        """Simulate human scrolling behavior"""
        scroll_amount = random.randint(100, 500)
        page.evaluate(f"window.scrollBy(0, {scroll_amount})")
        self.random_delay(0.5, 1.5)
    
    def human_like_mouse_move(self, page):
        """Simulate random mouse movements"""
        try:
            x = random.randint(100, 800)
            y = random.randint(100, 600)
            page.mouse.move(x, y)
            self.random_delay(0.2, 0.5)
        except:
            pass
    
    def warm_up_session(self, page):
        """Make the session look human by browsing first"""
        print("🔥 Warming up session (looking human)...")
        
        page.goto("https://x.com/home")
        self.random_delay(2, 4)
        
        for _ in range(random.randint(2, 4)):
            self.human_like_scroll(page)
            self.human_like_mouse_move(page)
        
        try:
            tweets = page.locator('article[data-testid="tweet"]').all()
            if tweets and len(tweets) > 0:
                random_tweet = random.choice(tweets[:5])
                random_tweet.scroll_into_view_if_needed()
                self.random_delay(1, 2)
        except:
            pass
        
        page.goto("https://x.com/notifications")
        self.random_delay(2, 3)
        self.human_like_scroll(page)
        
        print("✓ Warm-up complete")
    
    def generate_reply(self, original_tweet, replier_text, username):
        """Use Ollama to generate a contextual reply"""
        print(f"   🤖 Generating AI reply...")
        
        # Use prompt from config file
        prompt = REPLY_PROMPT_TEMPLATE.format(
            original_tweet=original_tweet[:200],
            replier_text=replier_text,
            username=username,
            affiliate_link=AFFILIATE_LINK
        )
        
        try:
            response = requests.post(
                self.ollama_url,
                json={
                    "model": self.ollama_model,
                    "prompt": prompt,
                    "stream": False
                },
                timeout=30
            )
            
            if response.status_code == 200:
                reply = response.json()["response"].strip()
                if len(reply) > 200:
                    reply = reply.split('.')[0] + '.'
                # Randomly include affiliate link (70% chance)
                if random.random() < 0.7 and AFFILIATE_LINK not in reply:
                    reply = reply.rstrip('.') + f" {AFFILIATE_LINK} 18+ | Gamble responsibly."
                return reply
            else:
                return f"Love the energy, @{username}! Grab 50 free spins: {AFFILIATE_LINK} 18+ | Gamble responsibly."
                
        except Exception as e:
            print(f"   ⚠️ Error calling Ollama: {e}")
            return f"Love the energy, @{username}! Grab 50 free spins: {AFFILIATE_LINK} 18+ | Gamble responsibly."
    
    def search_keyword(self, page, keyword):
        print(f"\n🔍 Searching for: {keyword}")
        search_url = f"https://x.com/search?q={keyword}&src=typed_query&f=live"
        page.goto(search_url)
        self.random_delay(2, 4)
        page.wait_for_selector('article[data-testid="tweet"]', timeout=15000)
        self.human_like_scroll(page)
        self.random_delay(1, 2)
        print("✓ Search results loaded")
    
    def get_tweets(self, page):
        tweets = []
        tweet_elements = page.locator('article[data-testid="tweet"]').all()
        print(f"📊 Found {len(tweet_elements)} tweets on page")
        
        for tweet in tweet_elements[:3]:  # Limit to top 3 posts
            try:
                link = tweet.locator('a[href*="/status/"]').first
                href = link.get_attribute('href')
                
                if href and '/status/' in href:
                    tweet_id = href.split('/status/')[-1].split('?')[0]
                    
                    text_element = tweet.locator('[data-testid="tweetText"]').first
                    tweet_text = text_element.inner_text() if text_element.count() > 0 else ""
                    
                    username_element = tweet.locator('[data-testid="User-Name"]').first
                    username_text = username_element.inner_text() if username_element.count() > 0 else ""
                    
                    username = username_text.split('\n')[0] if username_text else ""
                    
                    if tweet_text:
                        tweets.append({
                            'id': tweet_id,
                            'text': tweet_text,
                            'username': username,
                            'url': f"https://x.com{href}"
                        })
            except Exception as e:
                continue
        
        return tweets
    
    def get_thread_replies(self, page, tweet_url, original_tweet):
        """Fetch replies to a tweet and filter for excited users"""
        print(f"   📋 Loading replies for {tweet_url}")
        page.goto(tweet_url)
        self.random_delay(2, 4)
        
        # Scroll to load more replies
        for _ in range(3):  # Scroll 3 times to load ~20-50 replies
            self.human_like_scroll(page)
            self.random_delay(1, 2)
        
        replies = []
        reply_elements = page.locator('article[data-testid="tweet"]').all()
        print(f"   📊 Found {len(reply_elements)} replies in thread")
        
        for reply in reply_elements:
            try:
                link = reply.locator('a[href*="/status/"]').first
                href = link.get_attribute('href')
                
                if href and '/status/' in href:
                    reply_id = href.split('/status/')[-1].split('?')[0]
                    
                    text_element = reply.locator('[data-testid="tweetText"]').first
                    reply_text = text_element.inner_text() if text_element.count() > 0 else ""
                    
                    username_element = reply.locator('[data-testid="User-Name"]').first
                    username_text = username_element.inner_text() if username_element.count() > 0 else ""
                    
                    username = username_text.split('\n')[0] if username_text else ""
                    
                    # Filter: Short, excited replies
                    if (reply_text and len(reply_text) <= MAX_REPLY_LENGTH and
                        any(keyword.lower() in reply_text.lower() for keyword in REPLY_FILTER_KEYWORDS)):
                        replies.append({
                            'id': reply_id,
                            'text': reply_text,
                            'username': username,
                            'url': f"https://x.com{href}",
                            'original_tweet': original_tweet,
                            'original_tweet_id': tweet_url.split('/status/')[-1].split('?')[0]
                        })
            except Exception as e:
                continue
        
        return replies[:2]  # Limit to 2 replies per thread
    
    def reply_to_tweet(self, page, reply_data, dry_run=False):
        print(f"\n{'='*60}")
        print(f"📝 Processing reply: {reply_data['id']} (to original {reply_data['original_tweet_id']})")
        print(f"   From: {reply_data['username']}")
        print(f"   Text: {reply_data['text']}")
        
        reply_text = self.generate_reply(
            original_tweet=reply_data['original_tweet'],
            replier_text=reply_data['text'],
            username=reply_data['username']
        )
        print(f"   💬 Generated reply: {reply_text}")
        
        if dry_run:
            print(f"   🧪 DRY RUN MODE - Not actually posting!")
            print(f"   🔗 Would reply to: {reply_data['url']}")
            
            self.replied_tweets['ids'].append(reply_data['id'])
            self.replied_tweets['details'][reply_data['id']] = {
                'url': reply_data['url'],
                'username': reply_data['username'],
                'original_tweet_id': reply_data['original_tweet_id'],
                'original_text': reply_data['text'][:200],
                'parent_tweet': reply_data['original_tweet'][:200],
                'our_reply': reply_text,
                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
                'dry_run': True
            }
            self.save_replied_tweets()
            return True
        
        try:
            page.goto(reply_data['url'])
            self.random_delay(2, 4)
            self.human_like_mouse_move(page)
            self.human_like_scroll(page)
            
            page.screenshot(path=f"debug_1_reply_{reply_data['id']}.png")
            print(f"   📸 Screenshot 1: Opened reply")
            
            reply_button = page.locator('[data-testid="reply"]').first
            reply_button.scroll_into_view_if_needed()
            self.random_delay(1, 2)
            self.human_like_mouse_move(page)
            
            reply_button.click()
            self.random_delay(2, 3)
            page.screenshot(path=f"debug_2_reply_opened_{reply_data['id']}.png")
            print(f"   📸 Screenshot 2: Reply box opened")
            
            page.wait_for_selector('[data-testid="tweetTextarea_0"]', timeout=10000)
            self.random_delay(1, 2)
            
            textarea = page.locator('[data-testid="tweetTextarea_0"]').first
            textarea.click()
            self.random_delay(0.5, 1)
            
            for char in reply_text:
                page.keyboard.type(char)
                time.sleep(random.uniform(0.05, 0.15))
            
            self.random_delay(2, 3)
            page.screenshot(path=f"debug_3_text_filled_{reply_data['id']}.png")
            print(f"   📸 Screenshot 3: Text typed naturally")
            
            self.human_like_mouse_move(page)
            self.random_delay(1, 2)
            
            post_button = page.locator('[data-testid="tweetButton"]').first
            post_button.scroll_into_view_if_needed()
            self.random_delay(0.5, 1)
            post_button.click()
            print(f"   🖱️ Clicked Post button")
            
            self.random_delay(5, 7)
            page.screenshot(path=f"debug_4_after_post_{reply_data['id']}.png")
            print(f"   📸 Screenshot 4: After clicking post")
            
            page_content = page.content().lower()
            
            if "automated" in page_content or "spam" in page_content:
                print(f"   ❌ Still detected as automated!")
                return False
            
            if "something went wrong" in page_content:
                print(f"   ⚠️ Error message detected!")
                return False
            
            print(f"   ✅ Reply posted successfully!")
            print(f"   🔗 Original reply: {reply_data['url']}")
            
            self.replied_tweets['ids'].append(reply_data['id'])
            self.replied_tweets['details'][reply_data['id']] = {
                'url': reply_data['url'],
                'username': reply_data['username'],
                'original_tweet_id': reply_data['original_tweet_id'],
                'original_text': reply_data['text'][:200],
                'parent_tweet': reply_data['original_tweet'][:200],
                'our_reply': reply_text,
                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
                'dry_run': False
            }
            self.save_replied_tweets()
            return True
            
        except Exception as e:
            print(f"   ❌ Error posting reply: {e}")
            page.screenshot(path=f"debug_error_{reply_data['id']}.png")
            return False
    
    def run(self, keyword, max_replies=6, warm_up=True, dry_run=False):
        if not os.path.exists('x_session.json'):
            print("❌ No x_session.json found!")
            return
        
        print("="*60)
        if dry_run:
            print("🧪 Starting X Bot in DRY RUN Mode (No Actual Posts)")
        else:
            print("🚀 Starting X Bot with Anti-Detection (LIVE MODE)")
        print("="*60)
        
        with sync_playwright() as p:
            browser = p.chromium.launch(
                headless=True,
                args=[
                    '--disable-blink-features=AutomationControlled',
                    '--disable-dev-shm-usage',
                    '--no-sandbox'
                ]
            )
            
            context = browser.new_context(
                storage_state="x_session.json",
                viewport={'width': 1920, 'height': 1080},
                user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                locale='en-US',
                timezone_id='America/New_York'
            )
            
            page = context.new_page()
            
            try:
                if warm_up and not dry_run:
                    self.warm_up_session(page)
                
                self.search_keyword(page, keyword)
                
                tweets = self.get_tweets(page)
                print(f"\n📋 Found {len(tweets)} influencer tweets")
                
                reply_count = 0
                for tweet in tweets:
                    if reply_count >= max_replies:
                        break
                    
                    # Get replies to this tweet
                    replies = self.get_thread_replies(page, tweet['url'], tweet['text'])
                    print(f"\n📋 Found {len(replies)} target replies for tweet {tweet['id']}")
                    
                    for reply in replies:
                        if reply['id'] not in self.replied_tweets['ids'] and reply_count < max_replies:
                            success = self.reply_to_tweet(page, reply, dry_run=dry_run)
                            if success:
                                reply_count += 1
                            
                            if reply_count < max_replies:
                                if dry_run:
                                    wait_time = random.randint(DRY_RUN_DELAY_MIN, DRY_RUN_DELAY_MAX)
                                else:
                                    wait_time = random.randint(DELAY_BETWEEN_REPLIES_MIN, DELAY_BETWEEN_REPLIES_MAX)
                                print(f"\n⏳ Waiting {wait_time} seconds before next reply...")
                                time.sleep(wait_time)
                        else:
                            if reply['id'] in self.replied_tweets['ids']:
                                print(f"⏭️  Skipping {reply['id']} (already replied)")
                
                print("\n" + "="*60)
                if reply_count == 0:
                    print("✓ No new replies to target!")
                else:
                    if dry_run:
                        print(f"🧪 DRY RUN: Generated {reply_count} replies (not posted)")
                    else:
                        print(f"✅ Successfully posted {reply_count} replies")
                print("="*60)
                
                print("\n📊 REPLY HISTORY:")
                print(f"Total replies recorded: {len(self.replied_tweets['ids'])}")
                if self.replied_tweets['details']:
                    print("\nRecent replies:")
                    for reply_id, details in list(self.replied_tweets['details'].items())[-5:]:
                        dry_run_marker = " [DRY RUN]" if details.get('dry_run', False) else " [POSTED]"
                        print(f"\n  Reply ID: {reply_id}{dry_run_marker}")
                        print(f"  To: {details['username']} (Original: {details['original_tweet_id']})")
                        print(f"  URL: {details['url']}")
                        print(f"  Time: {details['timestamp']}")
                        print(f"  Our reply: {details['our_reply'][:100]}...")
                
            except Exception as e:
                print(f"\n❌ Error: {e}")
                page.screenshot(path="error_screenshot.png")
            
            finally:
                browser.close()
                print("\n🏁 Bot finished running")

if __name__ == "__main__":
    bot = XBot()
    bot.run(keyword=KEYWORD, max_replies=MAX_REPLIES, warm_up=WARM_UP, dry_run=DRY_RUN)
