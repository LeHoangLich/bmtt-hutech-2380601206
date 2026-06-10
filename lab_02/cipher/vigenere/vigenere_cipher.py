from string import ascii_letters


class VigenereCipher:
    def __init__(self):
        pass

    def validate_text(self, text, text_name="Văn bản"):
        if text is None or str(text).strip() == "":
            raise ValueError(f"{text_name} không được để trống")
        return str(text)

    def validate_key(self, key):
        if key is None or str(key).strip() == "":
            raise ValueError("Khóa không được để trống")
        key = str(key).replace(" ", "").upper()

        if not key.isascii() or not key.isalpha():
            raise ValueError("Khóa chỉ được chứa chữ cái A-Z")
        return key

    def vigenere_encrypt(self, plain_text, key):
        plain_text = self.validate_text(plain_text, "Văn bản cần mã hóa")
        key = self.validate_key(key)

        encrypted_text = ""
        key_index = 0

        for char in plain_text:
            if char in ascii_letters:
                key_shift = ord(key[key_index % len(key)]) - ord("A")

                if char.isupper():
                    encrypted_text += chr((ord(char) - ord("A") + key_shift) % 26 + ord("A"))
                else:
                    encrypted_text += chr((ord(char) - ord("a") + key_shift) % 26 + ord("a"))

                key_index += 1
            else:
                encrypted_text += char

        return encrypted_text

    def vigenere_decrypt(self, encrypted_text, key):
        encrypted_text = self.validate_text(encrypted_text, "Văn bản cần giải mã")
        key = self.validate_key(key)

        decrypted_text = ""
        key_index = 0

        for char in encrypted_text:
            if char in ascii_letters:
                key_shift = ord(key[key_index % len(key)]) - ord("A")

                if char.isupper():
                    decrypted_text += chr((ord(char) - ord("A") - key_shift) % 26 + ord("A"))
                else:
                    decrypted_text += chr((ord(char) - ord("a") - key_shift) % 26 + ord("a"))

                key_index += 1
            else:
                decrypted_text += char

        return decrypted_text
