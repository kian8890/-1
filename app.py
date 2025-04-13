from flask import Flask, render_template, request
import os
import random
import string

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret123'

def generate_key():
    letters = list(string.ascii_lowercase)
    shuffled = letters[:]
    random.shuffle(shuffled)
    return dict(zip(letters, shuffled))

def parse_key_string(key_str):
    key_map = {}
    pairs = key_str.lower().split(',')
    for pair in pairs:
        if ':' in pair:
            k, v = pair.split(':')
            key_map[k.strip()] = v.strip()
    return key_map

def mono_cipher(text, key_map):
    result = ""
    for char in text:
        if char.isalpha():
            if char.islower():
                result += key_map.get(char, char)
            else:
                result += key_map.get(char.lower(), char).upper()
        else:
            result += char
    return result

@app.route('/', methods=['GET', 'POST'])
def index():
    plaintext = ''
    keymap = ''
    result = ''
    key_dict = generate_key()
    keymap = ', '.join(f"{k}:{v}" for k, v in key_dict.items())

    if request.method == 'POST':
        plaintext = request.form.get('plaintext', '')
        keymap = request.form.get('keymap', '')
        try:
            key_dict = parse_key_string(keymap)
            result = mono_cipher(plaintext, key_dict)
        except Exception as e:
            result = f"⚠️ Error in key format: {e}"

    return render_template('index.html', plaintext=plaintext, keymap=keymap, result=result)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
