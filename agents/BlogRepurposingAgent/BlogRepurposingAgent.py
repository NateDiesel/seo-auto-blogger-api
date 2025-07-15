import os
import json
import logging
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for
from typing import Dict
import asyncio
import requests
from requests_oauthlib import OAuth2Session
from apscheduler.schedulers.background import BackgroundScheduler
from keyrings.alt import PlaintextKeyring
keyring.set_keyring(PlaintextKeyring())


# Configure logging
logging.basicConfig(
    filename="blog_repurposing_agent.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Load configuration
CONFIG_FILE = "config.json"
def load_config():
    if not os.path.exists(CONFIG_FILE):
        raise FileNotFoundError(f"Configuration file {CONFIG_FILE} not found.")
    with open(CONFIG_FILE, 'r') as f:
        return json.load(f)

config = load_config()

# OAuth endpoints and credentials
INSTAGRAM_AUTH_URL = "https://api.instagram.com/oauth/authorize"
INSTAGRAM_TOKEN_URL = "https://api.instagram.com/oauth/access_token"
INSTAGRAM_API_BASE = "https://graph.instagram.com/"

FACEBOOK_AUTH_URL = "https://www.facebook.com/v10.0/dialog/oauth"
FACEBOOK_TOKEN_URL = "https://graph.facebook.com/v10.0/oauth/access_token"
FACEBOOK_API_BASE = "https://graph.facebook.com/v10.0/"

TIKTOK_AUTH_URL = "https://open-api.tiktokglobalplatform.com/oauth/authorize"
TIKTOK_TOKEN_URL = "https://open-api.tiktokglobalplatform.com/oauth/token"
TIKTOK_API_BASE = "https://open-api.tiktokglobalplatform.com/"

app = Flask(__name__)

class BlogRepurposingAgent:
    def __init__(self):
        self.instagram_token = keyring.get_password("blog_agent", "instagram_token")
        self.facebook_token = keyring.get_password("blog_agent", "facebook_token")
        self.tiktok_token = keyring.get_password("blog_agent", "tiktok_token")
        self.scheduler = BackgroundScheduler()
        self.scheduler.start()

    def authenticate_instagram(self, client_id: str, client_secret: str, redirect_uri: str):
        oauth = OAuth2Session(client_id, redirect_uri=redirect_uri, scope=["user_profile", "user_media"])
        authorization_url, state = oauth.authorization_url(INSTAGRAM_AUTH_URL)
        return authorization_url

    def handle_instagram_callback(self, client_id: str, client_secret: str, redirect_uri: str, redirect_response: str):
        oauth = OAuth2Session(client_id, redirect_uri=redirect_uri, scope=["user_profile", "user_media"])
        token = oauth.fetch_token(INSTAGRAM_TOKEN_URL, client_secret=client_secret, authorization_response=redirect_response)
        self.instagram_token = token['access_token']
        keyring.set_password("blog_agent", "instagram_token", self.instagram_token)
        logging.info("Authenticated Instagram successfully.")

    def authenticate_facebook(self, client_id: str, client_secret: str, redirect_uri: str):
        oauth = OAuth2Session(client_id, redirect_uri=redirect_uri, scope=["public_profile", "pages_manage_posts"])
        authorization_url, state = oauth.authorization_url(FACEBOOK_AUTH_URL)
        return authorization_url

    def handle_facebook_callback(self, client_id: str, client_secret: str, redirect_uri: str, redirect_response: str):
        oauth = OAuth2Session(client_id, redirect_uri=redirect_uri, scope=["public_profile", "pages_manage_posts"])
        token = oauth.fetch_token(FACEBOOK_TOKEN_URL, client_secret=client_secret, authorization_response=redirect_response)
        self.facebook_token = token['access_token']
        keyring.set_password("blog_agent", "facebook_token", self.facebook_token)
        logging.info("Authenticated Facebook successfully.")

    def authenticate_tiktok(self, client_key: str, client_secret: str, redirect_uri: str):
        oauth = OAuth2Session(client_key, redirect_uri=redirect_uri, scope=["video.upload"])
        authorization_url, state = oauth.authorization_url(TIKTOK_AUTH_URL)
        return authorization_url

    def handle_tiktok_callback(self, client_key: str, client_secret: str, redirect_uri: str, redirect_response: str):
        oauth = OAuth2Session(client_key, redirect_uri=redirect_uri, scope=["video.upload"])
        token = oauth.fetch_token(TIKTOK_TOKEN_URL, client_secret=client_secret, authorization_response=redirect_response)
        self.tiktok_token = token['access_token']
        keyring.set_password("blog_agent", "tiktok_token", self.tiktok_token)
        logging.info("Authenticated TikTok successfully.")

    async def repurpose_blog(self, blog_post: Dict):
        try:
            tasks = []
            title = blog_post['title']
            content = blog_post['content']

            instagram_content = {
                "image": blog_post['image'],
                "caption": f"{title}\n\n{content[:200]}... #ReadMoreOnBlog",
            }
            if self.instagram_token:
                tasks.append(self.post_to_instagram(instagram_content))

            facebook_content = {
                "message": f"{title}\n\n{content[:300]}... Read the full blog here: {blog_post['url']}",
                "link": blog_post['url']
            }
            if self.facebook_token:
                tasks.append(self.post_to_facebook(facebook_content))

            tiktok_content = {
                "video": blog_post['video'],
                "caption": f"{title} \n\n Learn more: {blog_post['url']}"
            }
            if self.tiktok_token:
                tasks.append(self.post_to_tiktok(tiktok_content))

            await asyncio.gather(*tasks)
            logging.info("Repurposed blog content successfully.")
        except Exception as e:
            logging.error(f"Failed to repurpose blog content: {e}")

    async def post_to_instagram(self, content: Dict):
        try:
            url = f"{INSTAGRAM_API_BASE}me/media"
            headers = {"Authorization": f"Bearer {self.instagram_token}"}
            data = {
                "image_url": content["image"],
                "caption": content["caption"],
            }
            response = requests.post(url, headers=headers, data=data)
            response.raise_for_status()
            logging.info(f"Successfully posted to Instagram: {response.json()}.")
        except Exception as e:
            logging.error(f"Failed to post to Instagram: {e}")

    async def post_to_facebook(self, content: Dict):
        try:
            url = f"{FACEBOOK_API_BASE}me/feed"
            headers = {"Authorization": f"Bearer {self.facebook_token}"}
            data = {
                "message": content["message"],
                "link": content["link"],
            }
            response = requests.post(url, headers=headers, data=data)
            response.raise_for_status()
            logging.info(f"Successfully posted to Facebook: {response.json()}.")
        except Exception as e:
            logging.error(f"Failed to post to Facebook: {e}")

    async def post_to_tiktok(self, content: Dict):
        try:
            url = f"{TIKTOK_API_BASE}video/upload"
            headers = {"Authorization": f"Bearer {self.tiktok_token}"}
            files = {"video": open(content["video"], "rb")}
            data = {"caption": content["caption"]}
            response = requests.post(url, headers=headers, files=files, data=data)
            response.raise_for_status()
            logging.info(f"Successfully posted to TikTok: {response.json()}.")
        except Exception as e:
            logging.error(f"Failed to post to TikTok: {e}")

    def schedule_post(self, blog_post: Dict, run_time: datetime):
        self.scheduler.add_job(self.repurpose_blog, 'date', run_date=run_time, args=[blog_post])
        logging.info(f"Scheduled blog post for {run_time}.")

# Flask routes
@app.route('/')
def index():
    return "<h1>Welcome to Blog Repurposing Agent</h1>"

@app.route('/authenticate/instagram')
def authenticate_instagram():
    client_id = config['instagram']['client_id']
    client_secret = config['instagram']['client_secret']
    redirect_uri = config['instagram']['redirect_uri']
    auth_url = agent.authenticate_instagram(client_id, client_secret, redirect_uri)
    return redirect(auth_url)

@app.route('/callback/instagram')
def instagram_callback():
    client_id = config['instagram']['client_id']
    client_secret = config['instagram']['client_secret']
    redirect_uri = config['instagram']['redirect_uri']
    redirect_response = request.url
    agent.handle_instagram_callback(client_id, client_secret, redirect_uri, redirect_response)
    return "Instagram authenticated successfully!"

@app.route('/schedule', methods=['GET', 'POST'])
def schedule():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        image = request.form['image']
        video = request.form['video']
        url = request.form['url']
        post_time = datetime.strptime(request.form['post_time'], "%Y-%m-%d %H:%M:%S")

        blog_post = {
            "title": title,
            "content": content,
            "image": image,
            "video": video,
            "url": url
        }

        agent.schedule_post(blog_post, post_time)
        return "Post scheduled successfully!"

    return '''
    <form method='POST'>
        Title: <input type='text' name='title'><br>
        Content: <textarea name='content'></textarea><br>
        Image URL: <input type='text' name='image'><br>
        Video Path: <input type='text' name='video'><br>
        Blog URL: <input type='text' name='url'><br>
        Post Time (YYYY-MM-DD HH:MM:SS): <input type='text' name='post_time'><br>
        <input type='submit' value='Schedule'>
    </form>
    '''

if __name__ == "__main__":
    agent = BlogRepurposingAgent()
    app.run(debug=True)
