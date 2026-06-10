from flask import Flask, render_template, request
from cipher.caesar import CaesarCipher
from cipher.railfence import RailFenceCipher
from cipher.playfair import PlayFairCipher
from cipher.vigenere import VigenereCipher

app = Flask(__name__)


def render_error(message, back_url, note=None):
    return render_template(
        "error.html",
        message=message,
        back_url=back_url,
        note=note
    )


@app.route("/")
def home():
    return render_template("index.html")


# ===================== CAESAR =====================
@app.route("/caesar")
def caesar():
    return render_template("caesar.html")


@app.route("/encrypt", methods=["POST"])
def caesar_encrypt():
    text = request.form.get("inputPlainText", "")
    key_text = request.form.get("inputKeyPlain", "")

    try:
        key = int(key_text)
        caesar_cipher = CaesarCipher()
        encrypted_text = caesar_cipher.encrypt_text(text, key)

        return render_template(
            "caesar_result.html",
            title="Kết quả mã hóa Caesar",
            text_label="Văn bản gốc",
            input_text=text.upper(),
            key=key,
            result_label="Văn bản mã hóa",
            result=encrypted_text
        )
    except ValueError as error:
        return render_error(error, "/caesar", "Khóa Caesar phải là số nguyên từ 1 đến 25.")


@app.route("/decrypt", methods=["POST"])
def caesar_decrypt():
    text = request.form.get("inputCipherText", "")
    key_text = request.form.get("inputKeyCipher", "")

    try:
        key = int(key_text)
        caesar_cipher = CaesarCipher()
        decrypted_text = caesar_cipher.decrypt_text(text, key)

        return render_template(
            "caesar_result.html",
            title="Kết quả giải mã Caesar",
            text_label="Văn bản mã hóa",
            input_text=text.upper(),
            key=key,
            result_label="Văn bản giải mã",
            result=decrypted_text
        )
    except ValueError as error:
        return render_error(error, "/caesar", "Khóa Caesar phải là số nguyên từ 1 đến 25.")


# ===================== RAIL FENCE =====================
@app.route("/railfence")
def railfence():
    return render_template("railfence.html")


@app.route("/railfence/encrypt", methods=["POST"])
def railfence_encrypt():
    text = request.form.get("inputPlainText", "")
    rails_text = request.form.get("inputRailsPlain", "")

    try:
        rails = int(rails_text)
        railfence_cipher = RailFenceCipher()
        encrypted_text = railfence_cipher.rail_fence_encrypt(text, rails)

        return render_template(
            "railfence_result.html",
            title="Kết quả mã hóa Rail Fence",
            text_label="Văn bản gốc",
            input_text=text,
            key=rails,
            result_label="Văn bản mã hóa",
            result=encrypted_text
        )
    except ValueError as error:
        return render_error(error, "/railfence", "Số rail phải là số nguyên, tối thiểu 2 và không lớn hơn độ dài văn bản.")


@app.route("/railfence/decrypt", methods=["POST"])
def railfence_decrypt():
    text = request.form.get("inputCipherText", "")
    rails_text = request.form.get("inputRailsCipher", "")

    try:
        rails = int(rails_text)
        railfence_cipher = RailFenceCipher()
        decrypted_text = railfence_cipher.rail_fence_decrypt(text, rails)

        return render_template(
            "railfence_result.html",
            title="Kết quả giải mã Rail Fence",
            text_label="Văn bản mã hóa",
            input_text=text,
            key=rails,
            result_label="Văn bản giải mã",
            result=decrypted_text
        )
    except ValueError as error:
        return render_error(error, "/railfence", "Số rail phải là số nguyên, tối thiểu 2 và không lớn hơn độ dài văn bản.")


# ===================== PLAYFAIR =====================
@app.route("/playfair")
def playfair():
    return render_template("playfair.html")


@app.route("/playfair/encrypt", methods=["POST"])
def playfair_encrypt():
    text = request.form.get("inputPlainText", "")
    key = request.form.get("inputKeyPlain", "")
    playfair_cipher = PlayFairCipher()

    try:
        clean_text = playfair_cipher.validate_text(text, "Văn bản cần mã hóa")
        clean_key = playfair_cipher.validate_key(key)
        matrix = playfair_cipher.create_playfair_matrix(clean_key)
        encrypted_text = playfair_cipher.playfair_encrypt(clean_text, matrix)

        return render_template(
            "playfair_result.html",
            title="Kết quả mã hóa Playfair",
            text_label="Văn bản gốc",
            input_text=clean_text,
            key=clean_key,
            matrix=matrix,
            result_label="Văn bản mã hóa",
            result=encrypted_text
        )
    except ValueError as error:
        return render_error(
            error,
            "/playfair",
            "Ràng buộc Playfair: khóa và văn bản chỉ dùng chữ cái A-Z, không dùng tiếng Việt có dấu. Chữ J sẽ được thay bằng I. Ma trận phải là 5x5, gồm đủ 25 chữ cái A-Z và không có J."
        )


@app.route("/playfair/decrypt", methods=["POST"])
def playfair_decrypt():
    text = request.form.get("inputCipherText", "")
    key = request.form.get("inputKeyCipher", "")
    playfair_cipher = PlayFairCipher()

    try:
        clean_text = playfair_cipher.validate_cipher_text(text)
        clean_key = playfair_cipher.validate_key(key)
        matrix = playfair_cipher.create_playfair_matrix(clean_key)
        decrypted_text = playfair_cipher.playfair_decrypt(clean_text, matrix)

        return render_template(
            "playfair_result.html",
            title="Kết quả giải mã Playfair",
            text_label="Văn bản mã hóa",
            input_text=clean_text,
            key=clean_key,
            matrix=matrix,
            result_label="Văn bản giải mã",
            result=decrypted_text
        )
    except ValueError as error:
        return render_error(
            error,
            "/playfair",
            "Ràng buộc Playfair: văn bản mã hóa phải có độ dài chẵn sau khi bỏ khoảng trắng. Khóa và văn bản chỉ dùng chữ cái A-Z, không dùng tiếng Việt có dấu."
        )


# ===================== VIGENERE =====================
@app.route("/vigenere")
def vigenere():
    return render_template("vigenere.html")


@app.route("/vigenere/encrypt", methods=["POST"])
def vigenere_encrypt():
    text = request.form.get("inputPlainText", "")
    key = request.form.get("inputKeyPlain", "")
    vigenere_cipher = VigenereCipher()

    try:
        encrypted_text = vigenere_cipher.vigenere_encrypt(text, key)

        return render_template(
            "vigenere_result.html",
            title="Kết quả mã hóa Vigenere",
            text_label="Văn bản gốc",
            input_text=text,
            key=key.upper(),
            result_label="Văn bản mã hóa",
            result=encrypted_text
        )
    except ValueError as error:
        return render_error(error, "/vigenere", "Khóa Vigenere chỉ được chứa chữ cái A-Z, không dùng số, ký tự đặc biệt hoặc tiếng Việt có dấu.")


@app.route("/vigenere/decrypt", methods=["POST"])
def vigenere_decrypt():
    text = request.form.get("inputCipherText", "")
    key = request.form.get("inputKeyCipher", "")
    vigenere_cipher = VigenereCipher()

    try:
        decrypted_text = vigenere_cipher.vigenere_decrypt(text, key)

        return render_template(
            "vigenere_result.html",
            title="Kết quả giải mã Vigenere",
            text_label="Văn bản mã hóa",
            input_text=text,
            key=key.upper(),
            result_label="Văn bản giải mã",
            result=decrypted_text
        )
    except ValueError as error:
        return render_error(error, "/vigenere", "Khóa Vigenere chỉ được chứa chữ cái A-Z, không dùng số, ký tự đặc biệt hoặc tiếng Việt có dấu.")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050, debug=True)
