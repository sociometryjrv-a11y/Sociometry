# =============================
# Sociometry Dashboard (CBSE Safe Version)
# =============================

from flask import Flask, jsonify
import tweepy
import praw
import requests

app = Flask(__name__)

# ========== TWITTER SETUP ==========
TWITTER_CONSUMER_KEY = "jANGglQtUl2ImigwMNh1HDivS"
TWITTER_CONSUMER_SECRET = "SceIJ04Jq4SAFaPBG7AzxDZu3XB1NIMOASHZ7KIDU2OUpjtIDy"
TWITTER_ACCESS_TOKEN = "1983927793743446016-65kcuWhv3ECwXjIzIlizcZwRAe3Z9A"
TWITTER_ACCESS_SECRET = "dhrhsKJZPS6p7g543kRpM7rdMZx0td5xKYWwZKvtoxpiZ"

auth = tweepy.OAuth1UserHandler(
    TWITTER_CONSUMER_KEY,
    TWITTER_CONSUMER_SECRET,
    TWITTER_ACCESS_TOKEN,
    TWITTER_ACCESS_SECRET
)
twitter_api = tweepy.API(auth)

# ========== REDDIT SETUP ==========
reddit = praw.Reddit(
    client_id="YOUR_REDDIT_CLIENT_ID",
    client_secret="YOUR_REDDIT_SECRET",
    user_agent="cbse-sociometry"
)

# ========== FACEBOOK + INSTAGRAM ==========
FB_ACCESS_TOKEN = "YOUR_FB_GRAPH_API_TOKEN"
IG_USER_ID = "YOUR_IG_USER_ID"
FB_USER_ID = "YOUR_FB_USER_ID"

# ========== LINKEDIN (SIMULATED) ==========
LINKEDIN_NAME = "Demo LinkedIn"
LINKEDIN_FOLLOWERS = 1200
LINKEDIN_FOLLOWING = 320
LINKEDIN_PIC = "https://via.placeholder.com/100"

@app.route("/api/followers")
def get_followers():
    data = {}

    # ===== Twitter =====
    try:
        user = twitter_api.get_user(screen_name="Twitter")
        data["Twitter"] = {
            "followers": user.followers_count,
            "following": user.friends_count,
            "profile_pic": user.profile_image_url_https
        }
    except Exception as e:
        data["Twitter"] = {"error": str(e)}

    # ===== Reddit =====
    try:
        subreddit = reddit.subreddit("technology")
        data["Reddit"] = {
            "followers": subreddit.subscribers,
            "following": 0,
            "profile_pic": "https://www.redditstatic.com/avatars/defaults/v2/avatar_default_5.png"
        }
    except Exception as e:
        data["Reddit"] = {"error": str(e)}

    # ===== Instagram =====
    try:
        ig_url = f"https://graph.facebook.com/v18.0/{IG_USER_ID}?fields=followers_count,follows_count,profile_picture_url&access_token={FB_ACCESS_TOKEN}"
        response = requests.get(ig_url).json()
        data["Instagram"] = {
            "followers": response.get("followers_count", 0),
            "following": response.get("follows_count", 0),
            "profile_pic": response.get("profile_picture_url", "")
        }
    except Exception as e:
        data["Instagram"] = {"error": str(e)}

    # ===== Facebook =====
    try:
        fb_url = f"https://graph.facebook.com/v18.0/{FB_USER_ID}?fields=followers_count,picture&access_token={FB_ACCESS_TOKEN}"
        response = requests.get(fb_url).json()
        data["Facebook"] = {
            "followers": response.get("followers_count", 0),
            "following": 0,
            "profile_pic": response.get("picture", {}).get("data", {}).get("url", "")
        }
    except Exception as e:
        data["Facebook"] = {"error": str(e)}

    # ===== LinkedIn (Simulated) =====
    data["LinkedIn"] = {
        "followers": LINKEDIN_FOLLOWERS,
        "following": LINKEDIN_FOLLOWING,
        "profile_pic": LINKEDIN_PIC
    }

    return jsonify(data)

@app.route("/api/trends")
def get_trends():
    trends_data = {
        "Twitter": ["#AI", "#Python", "#CBSE2025"],
        "Instagram": ["#Reels", "#ViralNow", "#Explore"],
        "Facebook": ["#Live", "#Videos", "#Friends"],
        "Reddit": ["r/technology", "r/funny", "r/worldnews"],
        "LinkedIn": ["#Jobs", "#Networking", "#CareerGrowth"]
    }
    return jsonify(trends_data)

