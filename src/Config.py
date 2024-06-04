import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    def __init__(self):
        self.BINANCE_API_KEY = os.getenv("BINANCE_API_KEY")
        self.BINANCE_API_SECRET = os.getenv("BINANCE_API_SECRET")

def load_config():
    return Config()
