
# SEO Auto Blogger API 🚀

A FastAPI-powered backend that generates SEO-optimized blog posts using LLMs like OpenAI or OpenRouter. Designed for automation, repurposing, and high-volume content creation for bloggers, marketers, and publishers.

---

## ✨ Features

- 🔁 Repurpose topics into fresh blog content
- 🔍 SEO-friendly formatting and structure
- 🧠 GPT-style prompt logic (OpenAI or OpenRouter ready)
- ⚙️ Built with FastAPI (async, production-grade)
- 💡 Simple API interface for integrations

---

## 🚀 Quickstart

```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
uvicorn api.main:app --reload --port 8000
```

---

## 🔧 Example Request

**POST** `/generate-blog`

```json
{
  "topic": "AI tools for bloggers",
  "style": "educational",
  "length": "short"
}
```

**Response**
```json
{
  "blog_post": "AI tools have transformed how bloggers create content..."
}
```

---

## 🧪 Sample Use Cases

- Repurpose newsletters into blog posts
- Auto-generate content from product updates
- SEO-fresh blog refresh for evergreen topics

---

## 🧠 Tech Stack

- Python 3.10+
- FastAPI
- Pydantic
- Optional: OpenAI or OpenRouter LLM API

---

## 📂 Project Structure

```
.
├── api/
│   ├── main.py          # FastAPI app
│   ├── logic.py         # Blog generation logic
├── requirements.txt
├── README.md
```

---

## 👔 Recruiter Notes

This app demonstrates:
- Clean backend API design
- Prompt engineering integration
- Real-world async application with FastAPI
- SEO content automation logic

Feel free to clone, test, or deploy.

Built by [Nathan Bentley](https://github.com/NateDiesel)
