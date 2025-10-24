import os
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# Make API key accessible throughout the application
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise EnvironmentError("OPENAI_API_KEY not found. Please create a .env file and add your key.")