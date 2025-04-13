from flask import Flask, render_template, request
import random
import string

app = Flask(__name__)

def generate_key():
    letters = list(string.ascii_lowercase)
    shuffled = letters[:]
    random.shuffle(shuffled)
    return dict(zip(letters, shuffled))

def encrypt(text, keymap):
    result = ''
    for char in text:
        if char.lower() in keymap:
            new_char = keymap[char.lower()]
            result += new_char.upper() if char.isupper() else new_char
        else:
            result += char
    return result

def decrypt(text, keymap):
    reversed_key = {v: k for k, v in keymap.items()}
    result = ''
    for char in text:
        if char.lower() in reversed_key:
            new_char = reversed_key[char.lower()]
            result += new_char.upper() if char.isupper() else new_char
        else:
            result += char
    return result

@app.route("/", methods=["GET", "POST"])
def index():
    result = ''
    plaintext = ''
    keymap_str = ''
    keymap = generate_key()  # default key on load

    if request.method == "POST":
        action = request.form.get("action")
        plaintext = request.form.get("plaintext", "")
        keymap_str = request.form.get("keymap", "")
        try:
            keymap = dict(item.split(":") for item in keymap_str.replace(" ", "").split(",") if ":" in item)
        except:
            result = "Invalid key format!"
        else:
            if action == "encrypt":
                result = encrypt(plaintext, keymap)
            elif action == "decrypt":
                result = decrypt(plaintext, keymap)

    # Format keymap back to string
    keymap_str = ', '.join(f'{k}:{v}' for k, v in keymap.items())

    return render_template("index.html", plaintext=plaintext, keymap=keymap_str, result=result)

if __name__ == "__main__":
    app.run(debug=True)
