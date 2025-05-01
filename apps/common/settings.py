from dotenv import load_dotenv
from pathlib import Path
import os

load_dotenv(dotenv_path=Path(__file__).parent.parent.parent / ".env")

# OpenAI
# OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Anthropic
# ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

# Azure OpenAI
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
AZURE_OPENAI_BASE_URL = os.getenv("AZURE_OPENAI_BASE_URL")
OPENAI_API_VERSION = os.getenv("OPENAI_API_VERSION")

# Debug .env path:
# print(Path(__file__).parent.parent.parent / ".env")