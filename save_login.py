from playwright.sync_api import sync_playwright
import time

def save_login_session():
    with sync_playwright() as p:
        # Launch browser
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        
        print("Opening X.com...")
        print("Please log in manually in the browser window.")
        print("After you're logged in and see your timeline, come back here and press Enter...")
        
        page.goto("https://x.com/login")
        
        # Wait for you to log in manually
        input("\nPress Enter after you've logged in successfully...")
        
        # Save the login session
        context.storage_state(path="x_session.json")
        print("\n✓ Login session saved to x_session.json!")
        print("You can now upload this file to RunPod.")
        
        browser.close()

if __name__ == "__main__":
    save_login_session()
