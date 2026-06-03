from flask import Flask, render_template, request
from cipher.caesar import CaesarCipher
from cipher.railfence import RailFenceCipher
from cipher.playfair import PlayFairCipher
from cipher.vigenere import VigenereCipher

app = Flask(__name__)


def only_letters(text):
    return "".join(char for char in text.upper() if char.isalpha())


@app.route("/")
def home():
    return render_template('index.html')


@app.route("/caesar")
def caesar():
    return render_template('caesar.html')


@app.route("/encrypt", methods=['POST'])
def caesar_encrypt():
    text = request.form['inputPlainText']
    key = int(request.form['inputKeyPlain'])
    caesar_cipher = CaesarCipher()
    encrypted_text = caesar_cipher.encrypt_text(text, key)
    return f"text: {text}<br/>key: {key}<br/>encrypted text: {encrypted_text}"


@app.route("/decrypt", methods=['POST'])
def caesar_decrypt():
    text = request.form['inputCipherText']
    key = int(request.form['inputKeyCipher'])
    caesar_cipher = CaesarCipher()
    decrypted_text = caesar_cipher.decrypt_text(text, key)
    return f"text: {text}<br/>key: {key}<br/>decrypted text: {decrypted_text}"


@app.route("/railfence")
def railfence():
    return render_template('railfence.html')


@app.route("/railfence/encrypt", methods=['POST'])
def railfence_encrypt():
    text = request.form['inputPlainText']
    rails = int(request.form['inputRailsPlain'])
    railfence_cipher = RailFenceCipher()
    try:
        encrypted_text = railfence_cipher.rail_fence_encrypt(text, rails)
        return f"text: {text}<br/>rails: {rails}<br/>encrypted text: {encrypted_text}"
    except ValueError as error:
        return f"Error: {error}"


@app.route("/railfence/decrypt", methods=['POST'])
def railfence_decrypt():
    text = request.form['inputCipherText']
    rails = int(request.form['inputRailsCipher'])
    railfence_cipher = RailFenceCipher()
    try:
        decrypted_text = railfence_cipher.rail_fence_decrypt(text, rails)
        return f"text: {text}<br/>rails: {rails}<br/>decrypted text: {decrypted_text}"
    except ValueError as error:
        return f"Error: {error}"


@app.route("/playfair")
def playfair():
    return render_template('playfair.html')


@app.route("/playfair/encrypt", methods=['POST'])
def playfair_encrypt():
    text = only_letters(request.form['inputPlainText'])
    key = only_letters(request.form['inputKeyPlain'])
    if not text or not key:
        return "Error: Plain text and key must contain letters."
    playfair_cipher = PlayFairCipher()
    matrix = playfair_cipher.create_playfair_matrix(key)
    encrypted_text = playfair_cipher.playfair_encrypt(text, matrix)
    return f"text: {text}<br/>key: {key}<br/>encrypted text: {encrypted_text}"


@app.route("/playfair/decrypt", methods=['POST'])
def playfair_decrypt():
    text = only_letters(request.form['inputCipherText'])
    key = only_letters(request.form['inputKeyCipher'])
    if not text or not key:
        return "Error: Cipher text and key must contain letters."
    playfair_cipher = PlayFairCipher()
    matrix = playfair_cipher.create_playfair_matrix(key)
    decrypted_text = playfair_cipher.playfair_decrypt(text, matrix)
    return f"text: {text}<br/>key: {key}<br/>decrypted text: {decrypted_text}"


@app.route("/vigenere")
def vigenere():
    return render_template('vigenere.html')


@app.route("/vigenere/encrypt", methods=['POST'])
def vigenere_encrypt():
    text = request.form['inputPlainText']
    key = request.form['inputKeyPlain']
    vigenere_cipher = VigenereCipher()
    try:
        encrypted_text = vigenere_cipher.vigenere_encrypt(text, key)
        return f"text: {text}<br/>key: {key}<br/>encrypted text: {encrypted_text}"
    except ValueError as error:
        return f"Error: {error}"


@app.route("/vigenere/decrypt", methods=['POST'])
def vigenere_decrypt():
    text = request.form['inputCipherText']
    key = request.form['inputKeyCipher']
    vigenere_cipher = VigenereCipher()
    try:
        decrypted_text = vigenere_cipher.vigenere_decrypt(text, key)
        return f"text: {text}<br/>key: {key}<br/>decrypted text: {decrypted_text}"
    except ValueError as error:
        return f"Error: {error}"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050, debug=True)
