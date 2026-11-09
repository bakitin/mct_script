import os
from dotenv import load_dotenv

load_dotenv()


class Config():
    def __init__(self):
        self.cc=os.getenv("CC")
        self.password=os.getenv("PASSWORD")
        self.gemini_api_key=os.getenv("GEMINI_API_KEY")