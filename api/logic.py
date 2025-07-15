from flask import Flask, render_template, request, jsonify
import requests
from bs4 import BeautifulSoup
import re
import time

app = Flask(__name__)

def fetch_blog_content(url):
    """Fetches the title and content from a given blog URL."""
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        title = soup.title.string if soup.title else "No Title Found"
        paragraphs = soup.find_all('p')
        content = '\n'.join([p.get_text() for p in paragraphs[:5]])  # Fetching first 5 paragraphs
        return title, content
    except Exception as e:
        return "Error fetching blog title", "Error fetching blog content"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/fetch_content', methods=['POST'])
def fetch_content():
    data = request.get_json()
    blog_url = data.get('blog_url')
    if not re.match(r'^(http|https)://', blog_url):
        return jsonify({"error": "Invalid URL format."})
    
    title, content = fetch_blog_content(blog_url)
    return jsonify({"title": title, "content": content})

@app.route('/repurpose', methods=['POST'])
def repurpose():
    data = request.form
    title = data.get('title')
    content = data.get('content')
    platforms = data.getlist('platforms')
    
    # Simulating content repurposing delay
    time.sleep(2)
    
    repurposed_content = {}
    for platform in platforms:
        repurposed_content[platform] = f"[Optimized for {platform}] {content[:250]}..."
    
    return jsonify(repurposed_content)

if __name__ == '__main__':
    app.run(debug=True)
