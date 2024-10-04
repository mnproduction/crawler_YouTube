from playwright.sync_api import sync_playwright
from playwright.sync_api import Page, Browser

def run(playwright):
    browser: Browser = playwright.chromium.launch(headless=False)
    page: Page = browser.new_page()
    page.goto("https://www.browserscan.net/")
    page.screenshot(path="./screenshots/example.png")
    browser.close()

with sync_playwright() as playwright:
    run(playwright)