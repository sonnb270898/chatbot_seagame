"""
Setting connect database
"""
import os
from dotenv import load_dotenv

# load all env in .env file
load_dotenv()

MYSQL_PASSWORD = os.environ.get("MYSQL_PASSWORD")
MYSQL_HOST = os.environ.get("MYSQL_HOST")
MYSQL_USER = os.environ.get("MYSQL_USER")
MYSQL_DATABASE = os.environ.get("MYSQL_DATABASE")

FACEBOOK_API_ENDPOINT = os.environ.get("FACEBOOK_API_ENDPOINT")
FACEBOOK_WEBHOOK_VERIFY_TOKEN = os.environ.get("FACEBOOK_WEBHOOK_VERIFY_TOKEN", "rabiloo")
FACEBOOK_TOKEN_PAGE = os.environ.get("FACEBOOK_TOKEN_PAGE")

API_OA_LINK=os.environ.get("API_OA_LINK")
ZALO_TOKEN=os.environ.get("ZALO_TOKEN")
OA_ID=os.environ.get("OA_ID")
SECRET_KEY=os.environ.get("SECRET_KEY")
