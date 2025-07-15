FROM python:3.9-slim

WORKDIR /app

COPY . .
COPY config.json /app/config.json

RUN pip install flask requests keyring apscheduler requests_oauthlib keyrings.alt

EXPOSE 5000

CMD ["python", "BlogRepurposingAgent.py"]
