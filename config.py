import os
from dotenv import load_dotenv

load_dotenv()


class Config():
    def __init__(self):
        self.cc=os.getenv("CC")
        self.password=os.getenv("PASSWORD")