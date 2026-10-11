import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify
from ollama import Client

load_dotenv()

app = Flask(__name__)

client = Client(host=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"))
MODEL = os.getenv("OLLAMA_MODEL", "llama3.2:1b")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get('message', '')

    try:
        response = client.chat(model=MODEL, messages=[
            {'role': 'user', 'content': user_message},
        ])
        reply = response.message.content
    except Exception as e:
        reply = f"Error: {e}"

    return jsonify({'reply': reply})

if __name__ == '__main__':
    app.run(debug=True)