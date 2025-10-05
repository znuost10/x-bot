from playwright.sync_api import sync_playwright
import time
import json
import os
import requests

class XBot:
    def __init__(self):
        self.replied_tweets = self.load_replied_tweets()
        self.ollama_url = "http://localhost:11434/api/generate"
    
    def load_replied_tweets(self):
        if os.path.exists('replied_tweets.json'):
            with open('replied_tweets.json', 'r') as f:
                return json.load(f)
        return []
    
    def save_replied_tweets(self):
        with open('replied_tweets.json', 'w') as f:
            json.dump(self.replied_tweets, f)
    
    def generate_reply(self, tweet_text, username):
        """Use Ollama to generate a contextual reply"""
        print(f"   🤖 Generating AI reply...")
        
        prompt = f"""You are replying to a tweet. Write a brief, natural, friendly reply (1-2 sentences max, under 200 characters). Be conversational and relevant to what they said. Don't use hashtags.

Tweet from @{username}: {tweet_text}

Your reply:"""
        
        try:
            response = requests.post(
                self.ollama_url,
                json={
                    "model": "llama3.2",
                    "prompt": prompt,
                    "stream": False
                },
                timeout=30
            )
            
            if response.status_code == 200:
                reply = response.json()["response"].strip()
                # Take only first sentence if too long
                if len(reply) > 250:
                    reply = reply.split('.')[0] + '.'
                return reply
            else:
                print(f"   ⚠️ Ollama error, using fallback reply")
                return "Interesting perspective! Thanks for sharing."
                
        except Exception as e:
            print(f"   ⚠️ Error calling Ollama: {e}")
            return "Interesting perspective! Thanks for sharing."
    
    def search_keyword(self, page, keyword):
        print(f"\n🔍 Searching for: {keyword}")
        search_url = f"https://x.com/search?q={keyword}&src=typed_query&f=live"
        page.goto(search_url)
        page.wait_for_selector('article[data-testid="tweet"]', timeout=15000)
        time.sleep(2)
        print("✓ Search results loaded")
    
    def get_tweets(self, page):
        tweets = []
        tweet_elements = page.locator('article[data-testid="tweet"]').all()
        print(f"📊 Found {len(tweet_elements)} tweets on page")
        
        for tweet in tweet_elements[:10]:  # Check more tweets
            try:
                link = tweet.locator('a[href*="/status/"]').first
                href = link.get_attribute('href')
                
                if href and '/status/' in href:
                    tweet_id = href.split('/status/')[-1].split('?')[0]
                    
                    text_element = tweet.locator('[data-testid="tweetText"]').first
                    tweet_text = text_element.inner_text() if text_element.count() > 0 else ""
                    
                    username_element = tweet.locator('[data-testid="User-Name"]').first
                    username_text = username_element.inner_text() if username_element.count() > 0 else ""
                    
                    # Extract just the @username
                    username = username_text.split('\n')[0] if username_text else ""
                    
                    if tweet_text:  # Only add if there's actual text
                        tweets.append({
                            'id': tweet_id,
                            'text': tweet_text,
                            'username': username,
                            'url': f"https://x.com{href}"
                        })
            except Exception as e:
                continue
        
        return tweets
    
    def reply_to_tweet(self, page, tweet):
        print(f"\n{'='*60}")
        print(f"📝 Processing tweet: {tweet['id']}")
        print(f"   From: {tweet['username']}")
        print(f"   Text: {tweet['text'][:150]}...")
        
        # Generate AI reply
        reply_text = self.generate_reply(tweet['text'], tweet['username'])
        print(f"   💬 Generated reply: {reply_text}")
        
        try:
            # Go to tweet
            page.goto(tweet['url'])
            time.sleep(2)
            
            # Click reply button
            reply_button = page.locator('[data-testid="reply"]').first
            reply_button.click()
            time.sleep(1)
            
            # Wait for reply box and fill it
            page.wait_for_selector('[data-testid="tweetTextarea_0"]', timeout=10000)
            page.fill('[data-testid="tweetTextarea_0"]', reply_text)
            time.sleep(2)
            
            # Post reply
            page.click('[data-testid="tweetButton"]')
            time.sleep(3)
            
            print(f"   ✅ Reply posted successfully!")
            
            # Save as replied
            self.replied_tweets.append(tweet['id'])
            self.save_replied_tweets()
            return True
            
        except Exception as e:
            print(f"   ❌ Error posting reply: {e}")
            return False
    
    def run(self, keyword, max_replies=3):
        # Check for session file
        if not os.path.exists('x_session.json'):
            print("❌ No x_session.json found!")
            print("You need to upload your session file from your local machine.")
            return
        
        print("="*60)
        print("🚀 Starting X Bot with AI Replies")
        print("="*60)
        
        with sync_playwright() as p:
            # Launch in headless mode for server
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(storage_state="x_session.json")
            page = context.new_page()
            
            try:
                print("✓ Using saved login session")
                page.goto("https://x.com/home", timeout=30000)
                time.sleep(3)
                
                # Search for keyword
                self.search_keyword(page, keyword)
                
                # Get tweets
                tweets = self.get_tweets(page)
                print(f"\n📋 Found {len(tweets)} tweets with content")
                
                # Reply to new tweets
                reply_count = 0
                for tweet in tweets:
                    if tweet['id'] not in self.replied_tweets and reply_count < max_replies:
                        success = self.reply_to_tweet(page, tweet)
                        if success:
                            reply_count += 1
                        # Wait between replies to seem human
                        time.sleep(8)
                    else:
                        if tweet['id'] in self.replied_tweets:
                            print(f"⏭️  Skipping {tweet['id']} (already replied)")
                
                print("\n" + "="*60)
                if reply_count == 0:
                    print("✓ No new tweets to reply to!")
                else:
                    print(f"✅ Successfully replied to {reply_count} tweets")
                print("="*60)
                
            except Exception as e:
                print(f"\n❌ Error: {e}")
                page.screenshot(path="error_screenshot.png")
                print("Screenshot saved to error_screenshot.png")
            
            finally:
                browser.close()
                print("\n🏁 Bot finished running")

if __name__ == "__main__":
    bot = XBot()
    
    # Configure what to search for and how many replies
    KEYWORD = "artificial intelligence"  # Change this to whatever you want
    MAX_REPLIES = 3  # Number of tweets to reply to
    
    bot.run(keyword=KEYWORD, max_replies=MAX_REPLIES)
