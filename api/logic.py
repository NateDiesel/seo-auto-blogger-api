import re

def slugify(text: str) -> str:
    return re.sub(r'\W+', '-', text.lower()).strip('-')

def generate_blog_post(topic: str, style: str, length: str) -> dict:
    title = topic.title()
    slug = slugify(title)
    tags = [word for word in topic.split() if word.lower() not in {"the", "is", "a", "of", "in", "on"}]

    intro = f"Welcome to our {style} article on {topic}.\n\n"
    body = "In this article, we’ll explore the implications of this topic in detail.\n\n" * (2 if length == "short" else 4)
    outro = "Thanks for reading! Be sure to follow us for more insights.\n"

    return {
        "title": title,
        "slug": slug,
        "tags": tags,
        "content": intro + body + outro
    }
