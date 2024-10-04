import json
import os

from firecrawl import FirecrawlApp
from openai import OpenAI
import pandas as pd

from settings.config import config
from utils.logger import Logger

logger = Logger(__name__)


def scrape_data(url):
    app = FirecrawlApp(api_key=config.FIRE_CRAWL_API_KEY)

    scraped_data = app.scrape_url(url)

    if 'markdown' in scraped_data:
        logger.debug("Scraped data successfully")
        return scraped_data['markdown']
    else:
        logger.error("Markdown key not found in scraped data")
        raise KeyError("Markdown key not found in scraped data")

def save_raw_data(raw_data, timestamp, output_folder='data/firecrawl/raw'):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    raw_output_path = os.path.join(output_folder, f"raw_data_{timestamp}.md")
    with open(raw_output_path, 'w', encoding='utf-8') as file:
        file.write(raw_data)
        logger.info(f"Raw data saved to {raw_output_path}")
    
def format_data(raw_data, fields=None):
    client = OpenAI(api_key=config.OPENAI_API_KEY)

    if fields is None:
        fields = ['place', 'trend', 'popularity growth']

    system_message = f"""You are an intelligent text extraction and conversion assistant. Your task is to extract structured information from the given text and convert it into JSON format. The JSON should contain only the structured data, extracted from the text, with no additional commentary, explanations, or extraneous information. You could encounter cases where you cant find the data for a particular field, or the data will be in foreign language. Please process the following text and provide the output in pure JSON format with no words before or after the JSON:"""

    user_message = f"Extract the following information from the provided text: \nPage content:\n\n{raw_data}\n\nInformation to extract: {fields}"

    response = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        response_format={ "type": "json_object" },
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message}
        ]
    )

    if response and response.choices:
        formatted_data = response.choices[0].message.content.strip()
        try:
            parsed_json = json.loads(formatted_data)
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON: {e}")
            logger.error(f"Formatted data: {formatted_data}")
            raise ValueError("The formatted data could not be decoded into JSON")
        
        return parsed_json
    else:
        raise ValueError("The OpenAI response did not contain the expected choices data")

def save_formatted_data(formatted_data, timestamp, output_folder='data/firecrawl/formatted'):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    formatted_output_path = os.path.join(output_folder, f"formatted_data_{timestamp}.json")
    with open(formatted_output_path, 'w', encoding='utf-8') as file:
        json.dump(formatted_data, file, indent=4)
        logger.info(f"Formatted data saved to {formatted_output_path}")
    
    if isinstance(formatted_data, dict) and len(formatted_data) == 1:
        key = next(iter(formatted_data))
        formatted_data = formatted_data[key]
    
    df = pd.DataFrame(formatted_data)
    
    excel_output_path = os.path.join(output_folder, f"formatted_data_{timestamp}.xlsx")
    df.to_excel(excel_output_path, index=False)
    logger.info(f"Formatted data saved to {excel_output_path}")


