from playwright.sync_api import sync_playwright

def run(playwright):
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()

    # Open new page
    page = context.new_page()

    # Go to http://www.iwencai.com/unifiedwap/
    page.goto("http://www.iwencai.com/unifiedwap/")

    # Go to http://www.iwencai.com/unifiedwap/home/index
    page.goto("http://www.iwencai.com/unifiedwap/home/index")

    # Click :nth-match(:text("登录"), 2)
    page.click(":nth-match(:text(\"登录\"), 2)")

    # Close page
    page.close()

    # ---------------------
    context.close()
    browser.close()

with sync_playwright() as playwright:
    run(playwright)