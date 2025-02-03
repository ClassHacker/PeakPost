import praw
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set up API client
class RedditActivityTracker:
    def __init__(self):
        self.reddit = praw.Reddit(
            client_id=os.getenv("CLIENT_ID"),
            client_secret=os.getenv("CLIENT_SECRET"),
            user_agent=os.getenv("USER_AGENT"),
        )

    # Fetch posts from a subreddit
    def fetch_posts(self, subreddit_name, limit=100):
        subreddit = self.reddit.subreddit(subreddit_name)
        posts = []
    
        for post in subreddit.new(limit=limit):
            posts.append({
                "title": post.title,
                "author": post.author.name if post.author else "Deleted",
                "timestamp": post.created_utc,
                "score": post.score,
                "num_comments": post.num_comments,
            })
        return pd.DataFrame(posts)

    # Analyze activity
    def analyze_activity(self, df):
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')
        df['hour'] = df['timestamp'].dt.hour
        activity_by_hour = df['hour'].value_counts().sort_index()
        return activity_by_hour

    # Improved visualization using Seaborn
    def plot_activity(self, activity_by_hour):
        """
        Plot subreddit activity by hour with an improved visual presentation.
        :param activity_by_hour: Series with activity counts by hour.
        """
        sns.set_style("whitegrid")
        plt.figure(figsize=(10, 5))

        # Create a bar plot with a custom color palette
        bars = plt.bar(activity_by_hour.index, activity_by_hour.values, color=sns.color_palette("coolwarm", len(activity_by_hour)))

        # Add value labels on top of each bar
        for bar in bars:
            plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1, str(bar.get_height()),
                     ha='center', va='bottom', fontsize=10, fontweight='bold')

        # Add labels and title
        plt.xlabel("Hour of the Day", fontsize=12, fontweight='bold')
        plt.ylabel("Number of Posts", fontsize=12, fontweight='bold')
        plt.title("Subreddit Activity by Hour", fontsize=14, fontweight='bold')

        # Set x-axis ticks for better readability
        plt.xticks(range(24), fontsize=10)
        plt.yticks(fontsize=10)

        # Remove unnecessary borders
        sns.despine()

        # Show the plot
        plt.show()

    # Save to CSV
    def save_to_csv(self, df, filename):
        df.to_csv(filename, index=False)
        print(f"Data saved to {filename}")

if __name__ == "__main__":
    # Initialize tracker
    tracker = RedditActivityTracker()

    # Fetch posts from a subreddit
    subreddit_name = "indiasocial"  # Replace with your target subreddit
    posts_df = tracker.fetch_posts(subreddit_name, limit=100)

    # Analyze activity
    activity_by_hour = tracker.analyze_activity(posts_df)

    # Plot activity
    tracker.plot_activity(activity_by_hour)

    # Save data to CSV
    tracker.save_to_csv(posts_df, "subreddit_activity.csv")
