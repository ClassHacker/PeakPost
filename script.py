import praw
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set up API client
reddit = praw.Reddit(
    client_id=os.getenv("CLIENT_ID"),
    client_secret=os.getenv("CLIENT_SECRET"),
    username=os.getenv("USERNAME"),
    password=os.getenv("PASSWORD"),
    user_agent=os.getenv("USER_AGENT"),
)

# Fetch basic information from a subreddit
subreddit = reddit.subreddit("developersIndia")
print(f"Subreddit: {subreddit.display_name}")
print(f"Active users: {subreddit.active_user_count}")
