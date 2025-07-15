import os
import datetime
import xml.etree.ElementTree as ET
from fastapi import FastAPI
from fastapi.responses import FileResponse

app = FastAPI()

RSS_FEED_FILE = "rss_feed.xml"
BLOG_POSTS_DIR = "blog_posts"  # Directory where generated posts are stored
SITE_URL = "https://yourdomain.com"  # Update this with your actual domain

# Ensure the blog posts directory exists
os.makedirs(BLOG_POSTS_DIR, exist_ok=True)

def create_rss_feed():
    """Generates or updates the RSS feed with the latest blog posts."""
    rss = ET.Element("rss", version="2.0")
    channel = ET.SubElement(rss, "channel")
    ET.SubElement(channel, "title").text = "AI Auto-Blogger RSS Feed"
    ET.SubElement(channel, "link").text = SITE_URL
    ET.SubElement(channel, "description").text = "Automated blog posts from AI Auto-Blogger SaaS"
    
    # Loop through blog posts and add them to RSS feed
    for filename in sorted(os.listdir(BLOG_POSTS_DIR), reverse=True):
        if filename.endswith(".txt"):  # Assuming blog posts are stored as text files
            with open(os.path.join(BLOG_POSTS_DIR, filename), "r", encoding="utf-8") as f:
                content = f.read()
            
            item = ET.SubElement(channel, "item")
            ET.SubElement(item, "title").text = filename.replace(".txt", "")
            ET.SubElement(item, "link").text = f"{SITE_URL}/blog/{filename.replace('.txt', '')}"
            ET.SubElement(item, "description").text = content[:200] + "..."  # Short preview
            ET.SubElement(item, "pubDate").text = datetime.datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")
    
    # Save RSS feed
    tree = ET.ElementTree(rss)
    tree.write(RSS_FEED_FILE, encoding="utf-8", xml_declaration=True)
    print(f"Updated RSS feed: {RSS_FEED_FILE}")

def add_blog_post(title, content):
    """Saves a new blog post and updates the RSS feed."""
    filename = f"{title.replace(' ', '_').lower()}.txt"
    with open(os.path.join(BLOG_POSTS_DIR, filename), "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Blog post saved: {filename}")
    create_rss_feed()  # Update RSS feed with new post

@app.get("/rss.xml")
def serve_rss_feed():
    """Serves the generated RSS feed as an endpoint."""
    return FileResponse(RSS_FEED_FILE, media_type="application/rss+xml")

if __name__ == "__main__":
    create_rss_feed()  # Run this script to generate/update RSS feed
