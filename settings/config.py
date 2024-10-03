# settings/config.py

DOWNLOADER_MIDDLEWARES = {
    'scrapy_playwright.middleware.ScrapyPlaywrightDownloadHandler': 800,
}

TWISTED_REACTOR = 'twisted.internet.asyncioreactor.AsyncioSelectorReactor'

PLAYWRIGHT_BROWSER_TYPE = 'chromium'
PLAYWRIGHT_LAUNCH_OPTIONS = {
    'headless': True,
    'args': [
        '--no-sandbox',
        '--disable-setuid-sandbox',
        '--disable-dev-shm-usage',
        '--disable-blink-features=AutomationControlled'
    ]
}