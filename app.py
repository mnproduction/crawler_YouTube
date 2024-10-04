from crawlers.firecrawl.firecrawler import scrape_data, save_raw_data, format_data, save_formatted_data
from datetime import datetime
from utils.logger import Logger

logger = Logger(__name__)

def main():
    url = 'https://trends.google.com/trends/explore?gprop=youtube'
    try:
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        raw_data = scrape_data(url)
        save_raw_data(raw_data, timestamp)
        formatted_data = format_data(raw_data, fields=['place', 'trend', 'popularity growth'])
        save_formatted_data(formatted_data, timestamp)
    except Exception as e:
        logger.error(f"Error: {e}")

if __name__ == "__main__":
    main()