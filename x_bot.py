from playwright.sync_api import sync_playwright
import time
import json
import os
import requests
import random
from datetime import datetime

# Import configuration
from config import (
    KEYWORD, MAX_REPLIES_PER_CYCLE, DRY_RUN, WARM_UP, SEARCH_TYPE,
    RUN_CONTINUOUSLY, CYCLE_DELAY_MINUTES,
    CHECK_MENTIONS, REPLY_TO_MENTIONS, MAX_MENTION_REPLIES_PER_CYCLE,
    ATTACH_IMAGE, IMAGE_PATH,
    SYSTEM_MESSAGE, INPUT_PROMPT_TEMPLATE,
    OLLAMA_MODEL, OLLAMA_URL,
    DELAY_BETWEEN_REPLIES_MIN, DELAY_BETWEEN_REPLIES_MAX,
    DRY_RUN_DELAY_MIN, DRY_RUN_DELAY_MAX
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
        delay = random.uniform(min_sec, max_sec)
        time.sleep(delay)
    
    def human_like_scroll(self, page):
        scroll_amount = random.randint(100, 500)
        page.evaluate(f"window.scrollBy(0, {scroll_amount})")
        self.random_delay(0.5, 1.5)
    
    def human_like_mouse_move(self, page):
        try:
            x = random.randint(100, 800)
            y = random.randint(100, 600)
            page.mouse.move(x, y)
            self.random_delay(0.2, 0.5)
        except:
            pass
    
    def warm_up_session(self, page):
        print("Warming up session...")
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
        print("Warm-up complete")
    
    def generate_reply(self, tweet_text, username):
        print(f"   Generating AI reply...")
        input_prompt = INPUT_PROMPT_TEMPLATE.format(username=username, tweet_text=tweet_text)
        full_prompt = f"{SYSTEM_MESSAGE}\n\n{input_prompt}"
        
        try:
            response = requests.post(
                self.ollama_url,
                json={
                    "model": self.ollama_model,
                    "prompt": full_prompt,
                    "stream": False
                },
                timeout=30
            )
            
            if response.status_code == 200:
                reply = response.json()["response"].strip()
                if len(reply) > 250:
                    reply = reply.split('.')[0] + '.'
                return reply
            else:
                return "Interesting perspective! Thanks for sharing."
        except Exception as e:
            print(f"   Error calling Ollama: {e}")
            return "Interesting perspective! Thanks for sharing."
    
    def search_keyword(self, page, keyword, search_type="top"):
        print(f"\nSearching for: {keyword} (sorted by {search_type})")
        
        if search_type == "top":
            search_url = f"https://x.com/search?q={keyword}&src=typed_query"
        else:
            search_url = f"https://x.com/search?q={keyword}&src=typed_query&f=live"
        
        page.goto(search_url)
        self.random_delay(2, 4)
        page.wait_for_selector('article[data-testid="tweet"]', timeout=15000)
        self.human_like_scroll(page)
        self.random_delay(1, 2)
        print("Search results loaded")
    
    def get_tweets(self, page, max_tweets=5):
        tweets = []
        tweet_elements = page.locator('article[data-testid="tweet"]').all()
        print(f"Found {len(tweet_elements)} tweets on page")
        
        for tweet in tweet_elements[:max_tweets]:
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
    
    def check_mentions(self, page, max_mentions=10):
        """Check notifications for replies to our posts"""
        print("\nChecking mentions and replies...")
        page.goto("https://x.com/notifications/mentions")
        self.random_delay(2, 4)
        
        try:
            page.wait_for_selector('article[data-testid="tweet"]', timeout=10000)
            self.human_like_scroll(page)
            self.random_delay(1, 2)
            
            mentions = self.get_tweets(page, max_tweets=max_mentions)
            print(f"Found {len(mentions)} mentions/replies")
            return mentions
        except Exception as e:
            print(f"Could not load mentions: {e}")
            return []
    
    def reply_to_tweet(self, page, tweet, dry_run=False, attach_image=False, image_path=None):
        print(f"\n{'='*60}")
        print(f"Processing tweet: {tweet['id']}")
        print(f"   From: {tweet['username']}")
        print(f"   Text: {tweet['text'][:150]}...")
        
        reply_text = self.generate_reply(tweet['text'], tweet['username'])
        print(f"   Generated reply: {reply_text}")
        
        if attach_image and image_path:
            print(f"   Will attach image: {image_path}")
        
        if dry_run:
            print(f"   DRY RUN MODE - Not actually posting!")
            print(f"   Would reply to: {tweet['url']}")
            
            self.replied_tweets['ids'].append(tweet['id'])
            self.replied_tweets['details'][tweet['id']] = {
                'url': tweet['url'],
                'username': tweet['username'],
                'original_text': tweet['text'][:200],
                'our_reply': reply_text,
                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
                'had_image': attach_image,
                'dry_run': True
            }
            self.save_replied_tweets()
            return True
        
        try:
            page.goto(tweet['url'])
            self.random_delay(2, 4)
            self.human_like_mouse_move(page)
            self.human_like_scroll(page)
            
            page.screenshot(path=f"debug_1_tweet_{tweet['id']}.png")
            print(f"   Screenshot 1: Opened tweet")
            
            reply_button = page.locator('[data-testid="reply"]').first
            reply_button.scroll_into_view_if_needed()
            self.random_delay(1, 2)
            self.human_like_mouse_move(page)
            
            reply_button.click()
            self.random_delay(2, 3)
            page.screenshot(path=f"debug_2_reply_opened_{tweet['id']}.png")
            print(f"   Screenshot 2: Reply box opened")
            
            page.wait_for_selector('[data-testid="tweetTextarea_0"]', timeout=10000)
            self.random_delay(1, 2)
            
            if attach_image and image_path:
                if os.path.exists(image_path):
                    print(f"   Uploading image...")
                    try:
                        file_input = page.locator('input[type="file"][accept*="image"]').first
                        file_input.set_input_files(image_path)
                        self.random_delay(2, 4)
                        page.screenshot(path=f"debug_2b_image_uploaded_{tweet['id']}.png")
                        print(f"   Image uploaded successfully")
                    except Exception as e:
                        print(f"   Warning: Could not upload image: {e}")
                else:
                    print(f"   Warning: Image file not found: {image_path}")
            
            textarea = page.locator('[data-testid="tweetTextarea_0"]').first
            textarea.click()
            self.random_delay(0.5, 1)
            
            for char in reply_text:
                page.keyboard.type(char)
                time.sleep(random.uniform(0.05, 0.15))
            
            self.random_delay(2, 3)
            page.screenshot(path=f"debug_3_text_filled_{tweet['id']}.png")
            print(f"   Screenshot 3: Text typed")
            
            self.human_like_mouse_move(page)
            self.random_delay(1, 2)
            
            post_button = page.locator('[data-testid="tweetButton"]').first
            post_button.scroll_into_view_if_needed()
            self.random_delay(0.5, 1)
            post_button.click()
            print(f"   Clicked Post button")
            
            self.random_delay(5, 7)
            page.screenshot(path=f"debug_4_after_post_{tweet['id']}.png")
            
            page_content = page.content().lower()
            
            if "your post was sent" in page_content or "your reply was sent" in page_content:
                print(f"   Reply posted successfully!")
                self.replied_tweets['ids'].append(tweet['id'])
                self.replied_tweets['details'][tweet['id']] = {
                    'url': tweet['url'],
                    'username': tweet['username'],
                    'original_text': tweet['text'][:200],
                    'our_reply': reply_text,
                    'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
                    'had_image': attach_image,
                    'dry_run': False
                }
                self.save_replied_tweets()
                return True
            
            if "this request looks like it might be automated" in page_content:
                print(f"   Blocked: X detected automation")
                return False
            
            if "something went wrong" in page_content and "try again" in page_content:
                print(f"   Error message detected")
                return False
            
            print(f"   No error detected - likely posted successfully")
            self.replied_tweets['ids'].append(tweet['id'])
            self.replied_tweets['details'][tweet['id']] = {
                'url': tweet['url'],
                'username': tweet['username'],
                'original_text': tweet['text'][:200],
                'our_reply': reply_text,
                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
                'had_image': attach_image,
                'dry_run': False
            }
            self.save_replied_tweets()
            return True
            
        except Exception as e:
            print(f"   Error posting reply: {e}")
            page.screenshot(path=f"debug_error_{tweet['id']}.png")
            return False
    
    def run_cycle(self, page, keyword, max_replies, search_type, dry_run, attach_image, image_path):
        """Run one complete cycle: reply to keyword posts, then check mentions"""
        cycle_start = datetime.now()
        print(f"\n{'='*70}")
        print(f"CYCLE START: {cycle_start.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*70}")
        
        # Phase 1: Reply to keyword posts
        print(f"\nPHASE 1: Searching and replying to '{keyword}' posts")
        self.search_keyword(page, keyword, search_type=search_type)
        tweets = self.get_tweets(page, max_tweets=max_replies)
        
        reply_count = 0
        for tweet in tweets:
            if tweet['id'] not in self.replied_tweets['ids']:
                success = self.reply_to_tweet(page, tweet, dry_run=dry_run, attach_image=attach_image, image_path=image_path)
                if success:
                    reply_count += 1
                
                if dry_run:
                    wait_time = random.randint(DRY_RUN_DELAY_MIN, DRY_RUN_DELAY_MAX)
                else:
                    wait_time = random.randint(DELAY_BETWEEN_REPLIES_MIN, DELAY_BETWEEN_REPLIES_MAX)
                print(f"\nWaiting {wait_time} seconds...")
                time.sleep(wait_time)
            else:
                print(f"Skipping {tweet['id']} (already replied)")
        
        print(f"\nPhase 1 complete: Replied to {reply_count} keyword posts")
        
        # Phase 2: Check and reply to mentions
        if CHECK_MENTIONS and REPLY_TO_MENTIONS:
            print(f"\nPHASE 2: Checking mentions and replies")
            mentions = self.check_mentions(page, max_mentions=10)
            
            mention_reply_count = 0
            for mention in mentions:
                if mention['id'] not in self.replied_tweets['ids'] and mention_reply_count < MAX_MENTION_REPLIES_PER_CYCLE:
                    success = self.reply_to_tweet(page, mention, dry_run=dry_run, attach_image=False, image_path=None)
                    if success:
                        mention_reply_count += 1
                    
                    if dry_run:
                        wait_time = random.randint(DRY_RUN_DELAY_MIN, DRY_RUN_DELAY_MAX)
                    else:
                        wait_time = random.randint(DELAY_BETWEEN_REPLIES_MIN, DELAY_BETWEEN_REPLIES_MAX)
                    print(f"\nWaiting {wait_time} seconds...")
                    time.sleep(wait_time)
                else:
                    if mention['id'] in self.replied_tweets['ids']:
                        print(f"Skipping mention {mention['id']} (already replied)")
            
            print(f"\nPhase 2 complete: Replied to {mention_reply_count} mentions")
        
        cycle_end = datetime.now()
        duration = (cycle_end - cycle_start).total_seconds() / 60
        
        print(f"\n{'='*70}")
        print(f"CYCLE COMPLETE")
        print(f"Duration: {duration:.1f} minutes")
        print(f"Total keyword replies: {reply_count}")
        if CHECK_MENTIONS and REPLY_TO_MENTIONS:
            print(f"Total mention replies: {mention_reply_count}")
        print(f"Total activity: {len(self.replied_tweets['ids'])} tweets replied to")
        print(f"{'='*70}")
    
    def run(self):
        if not os.path.exists('x_session.json'):
            print("No x_session.json found!")
            return
        
        print("="*70)
        if DRY_RUN:
            print("X BOT - DRY RUN MODE")
        else:
            print("X BOT - LIVE MODE")
        
        if RUN_CONTINUOUSLY:
            print(f"Continuous mode: {CYCLE_DELAY_MINUTES} min between cycles")
        print("="*70)
        
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
                if WARM_UP and not DRY_RUN:
                    self.warm_up_session(page)
                
                cycle_number = 1
                while True:
                    print(f"\n\n*** CYCLE {cycle_number} ***")
                    
                    self.run_cycle(
                        page=page,
                        keyword=KEYWORD,
                        max_replies=MAX_REPLIES_PER_CYCLE,
                        search_type=SEARCH_TYPE,
                        dry_run=DRY_RUN,
                        attach_image=ATTACH_IMAGE,
                        image_path=IMAGE_PATH
                    )
                    
                    if not RUN_CONTINUOUSLY:
                        print("\nSingle cycle mode - stopping")
                        break
                    
                    # Wait before next cycle
                    wait_minutes = CYCLE_DELAY_MINUTES
                    print(f"\nWaiting {wait_minutes} minutes until next cycle...")
                    print(f"Next cycle will start at: {datetime.now().strftime('%H:%M:%S')}")
                    time.sleep(wait_minutes * 60)
                    
                    cycle_number += 1
                
            except KeyboardInterrupt:
                print("\n\nBot stopped by user (Ctrl+C)")
            except Exception as e:
                print(f"\nError: {e}")
                page.screenshot(path="error_screenshot.png")
            finally:
                browser.close()
                print("\nBot finished")

if __name__ == "__main__":
    bot = XBot()
    bot.run()
