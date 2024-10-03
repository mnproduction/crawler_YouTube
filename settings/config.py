# settings/config.py

import os

class Config:
    def __init__(self):
        self.FIRE_CRAWL_API_KEY = os.getenv("FIRE_CRAWL_API_KEY")
        self.OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

        self.DEBUG_STATE_CONSOLE = True
        self.DEBUG_STATE_FILE = False


config = Config()