from flask import Flask, request, render_template_string
from flask_cors import CORS
from pynput.keyboard import Controller, Key
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
CORS(app)
keyboard = Controller()

@app.route('/')
def index():
    ip = os.getenv('LAPTOP_IP', '0.0.0.0')
    with open('keyboard.html', 'r', encoding='utf-8') as f:
        html = f.read().replace('{{IP}}', ip)
    return render_template_string(html)

@app.route('/key', methods=['POST'])
def press_key():
    data = request.get_json()
    key = data.get('key', '')
    key_type = data.get('type', 'char')

    if not key:
        return 'Missing key', 400

    if key_type == 'text':
        # Paste or text chunk — type all at once
        for ch in key:
            if ch == '\n':
                keyboard.press(Key.enter)
                keyboard.release(Key.enter)
            else:
                keyboard.press(ch)
                keyboard.release(ch)
    elif key == 'backspace':
        keyboard.press(Key.backspace)
        keyboard.release(Key.backspace)
    else:
        keyboard.press(key)
        keyboard.release(key)

    return 'OK', 200

if __name__ == '__main__':
    laptop_ip = os.getenv('LAPTOP_IP', '0.0.0.0')
    app.run(host=laptop_ip, port=5000)
