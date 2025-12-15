import os
from dotenv import load_dotenv
load_dotenv()

class Config:
    MONGODB_URI = os.getenv('MONGODB_URI')
    TWITTER_BEARER = os.getenv('TWITTER_BEARER_TOKEN')
    REDDIT_ID = os.getenv('REDDIT_CLIENT_ID')
    REDDIT_SECRET = os.getenv('REDDIT_CLIENT_SECRET')
    REDDIT_AGENT = 'TrendDetector/1.0'
    
    KEYWORDS = ['AI', 'ML', 'data science', 'python', 'tech']
