class PlayFairCipher:
    def __init__(self):
        self.alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"  # Không có J

    def remove_spaces(self, value):
        return "".join(str(value).split())

    def validate_key(self, key):
        if key is None or str(key).strip() == "":
            raise ValueError("Khóa không được để trống.")

        key = self.remove_spaces(key).upper()

        if not key.isascii() or not key.isalpha():
            raise ValueError(
                "Khóa chỉ được chứa chữ cái A-Z, không dùng số, ký tự đặc biệt hoặc tiếng Việt có dấu."
            )

        return key.replace("J", "I")

    def validate_text(self, text, text_name="Văn bản"):
        if text is None or str(text).strip() == "":
            raise ValueError(f"{text_name} không được để trống.")

        text = self.remove_spaces(text).upper()

        if not text.isascii() or not text.isalpha():
            raise ValueError(
                f"{text_name} chỉ được chứa chữ cái A-Z, không dùng số, ký tự đặc biệt hoặc tiếng Việt có dấu."
            )

        return text.replace("J", "I")

    def validate_matrix(self, matrix):
        if matrix is None:
            raise ValueError("Ma trận Playfair không được để trống.")

        if not isinstance(matrix, list) or len(matrix) != 5:
            raise ValueError("Ma trận Playfair phải là danh sách 5 dòng.")

        letters = []

        for row in matrix:
            if not isinstance(row, list) or len(row) != 5:
                raise ValueError("Mỗi dòng trong ma trận Playfair phải có đúng 5 ký tự.")

            for char in row:
                if not isinstance(char, str) or len(char) != 1:
                    raise ValueError("Mỗi phần tử trong ma trận Playfair phải là 1 ký tự.")

                char = char.upper()

                if char == "J":
                    raise ValueError("Ma trận Playfair không được chứa chữ J.")

                if char not in self.alphabet:
                    raise ValueError("Ma trận Playfair chỉ được chứa chữ cái A-Z, bỏ chữ J.")

                letters.append(char)

        if len(set(letters)) != 25:
            raise ValueError("Ma trận Playfair không được chứa ký tự trùng lặp.")

        if set(letters) != set(self.alphabet):
            raise ValueError("Ma trận Playfair phải chứa đủ 25 chữ cái A-Z, không có J.")

        return matrix

    def create_playfair_matrix(self, key):
        key = self.validate_key(key)

        matrix_letters = []

        for char in key:
            if char not in matrix_letters:
                matrix_letters.append(char)

        for char in self.alphabet:
            if char not in matrix_letters:
                matrix_letters.append(char)

        matrix = []

        for i in range(0, 25, 5):
            matrix.append(matrix_letters[i:i + 5])

        return matrix

    def find_letter_coords(self, matrix, letter):
        self.validate_matrix(matrix)

        letter = letter.upper().replace("J", "I")

        if letter not in self.alphabet:
            raise ValueError(f"Ký tự '{letter}' không tồn tại trong bảng chữ cái Playfair.")

        for row in range(5):
            for col in range(5):
                if matrix[row][col] == letter:
                    return row, col

        raise ValueError(f"Ký tự '{letter}' không tồn tại trong ma trận Playfair.")

    def prepare_plain_text(self, plain_text):
        plain_text = self.validate_text(plain_text, "Văn bản cần mã hóa")

        pairs = []
        i = 0

        while i < len(plain_text):
            first = plain_text[i]

            if i + 1 < len(plain_text):
                second = plain_text[i + 1]

                if first == second:
                    pairs.append(first + "X")
                    i += 1
                else:
                    pairs.append(first + second)
                    i += 2
            else:
                pairs.append(first + "X")
                i += 1

        return pairs

    def validate_cipher_text(self, cipher_text):
        cipher_text = self.validate_text(cipher_text, "Văn bản cần giải mã")

        if len(cipher_text) % 2 != 0:
            raise ValueError("Văn bản mã hóa Playfair phải có độ dài chẵn.")

        return cipher_text

    def playfair_encrypt(self, plain_text, matrix):
        self.validate_matrix(matrix)

        pairs = self.prepare_plain_text(plain_text)
        encrypted_text = ""

        for pair in pairs:
            row1, col1 = self.find_letter_coords(matrix, pair[0])
            row2, col2 = self.find_letter_coords(matrix, pair[1])

            if row1 == row2:
                encrypted_text += matrix[row1][(col1 + 1) % 5]
                encrypted_text += matrix[row2][(col2 + 1) % 5]

            elif col1 == col2:
                encrypted_text += matrix[(row1 + 1) % 5][col1]
                encrypted_text += matrix[(row2 + 1) % 5][col2]

            else:
                encrypted_text += matrix[row1][col2]
                encrypted_text += matrix[row2][col1]

        return encrypted_text

    def playfair_decrypt(self, cipher_text, matrix):
        self.validate_matrix(matrix)

        cipher_text = self.validate_cipher_text(cipher_text)
        decrypted_text = ""

        for i in range(0, len(cipher_text), 2):
            pair = cipher_text[i:i + 2]

            row1, col1 = self.find_letter_coords(matrix, pair[0])
            row2, col2 = self.find_letter_coords(matrix, pair[1])

            if row1 == row2:
                decrypted_text += matrix[row1][(col1 - 1) % 5]
                decrypted_text += matrix[row2][(col2 - 1) % 5]

            elif col1 == col2:
                decrypted_text += matrix[(row1 - 1) % 5][col1]
                decrypted_text += matrix[(row2 - 1) % 5][col2]

            else:
                decrypted_text += matrix[row1][col2]
                decrypted_text += matrix[row2][col1]

        return decrypted_text