from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv('.env'))
import os

api_url = os.environ.get('API_URL')