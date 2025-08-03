from flask import Flask, request
import requests
import os

app = Flask(name)
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')  # Токен из Шага 1
CHAT_ID = os.getenv('CHAT_ID')                # ID чата из Шага 2

@app.route('/webhook', methods=['POST'])
def webhook():
    payload = request.json
    event_type = request.headers.get('X-GitHub-Event')

    # Формируем сообщение в зависимости от события
    if event_type == 'push':
        repo_name = payload['repository']['name']
        pusher = payload['pusher']['name']
        branch = payload['ref'].split('/')[-1]
        commit_count = len(payload['commits'])
        message = f"🚀 Новый push в {repo_name} ({branch}) от {pusher}! Коммитов: {commit_count}"
        send_telegram(message)

    return 'OK', 200

def send_telegram(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": text}
    requests.post(url, json=data)

if name == 'main':
    app.run(host='0.0.0.0', port=5000)
