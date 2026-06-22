import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
INPUT_FILE = os.getenv("INPUT_FILE", "data/input.xlsx")
OUTPUT_FILE = os.getenv("OUTPUT_FILE", "data/output.xlsx")
MODEL = os.getenv("MODEL", "gpt-4o-mini")
USE_OPENAI = os.getenv("USE_OPENAI", "false").lower() == "true"

OPENAI_INPUT_PRICE_PER_1M = float(
    os.getenv("OPENAI_INPUT_PRICE_PER_1M", "0.15")
)

OPENAI_OUTPUT_PRICE_PER_1M = float(
    os.getenv("OPENAI_OUTPUT_PRICE_PER_1M", "0.60")
)

USE_WEB_SEARCH = os.getenv("USE_WEB_SEARCH", "false").lower() == "true"
SEARCH_PROVIDER = os.getenv("SEARCH_PROVIDER", "mock")
SERPER_API_KEY = os.getenv("SERPER_API_KEY", "")
CACHE_DIR = os.getenv("CACHE_DIR", "cache")

print(f"INPUT_FILE = {INPUT_FILE}")
print(f"USE_OPENAI = {USE_OPENAI}")
print(f"USE_WEB_SEARCH = {USE_WEB_SEARCH}")
print(f"SEARCH_PROVIDER = {SEARCH_PROVIDER}")