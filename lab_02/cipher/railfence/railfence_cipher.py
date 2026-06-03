class RailFenceCipher:
    def __init__(self):
        pass

    def validate_input(self, text, num_rails):
        if text is None or str(text).strip() == "":
            raise ValueError("Văn bản không được để trống")

        try:
            num_rails = int(num_rails)
        except (ValueError, TypeError):
            raise ValueError("Số rail phải là số nguyên")

        if isinstance(num_rails, bool):
            raise ValueError("Số rail phải là số nguyên")

        if num_rails < 2:
            raise ValueError("Số rail phải lớn hơn hoặc bằng 2")

        if num_rails > len(str(text).strip()):
            raise ValueError("Số rail không được lớn hơn độ dài văn bản")

        return str(text), num_rails

    def rail_fence_encrypt(self, plain_text, num_rails):
        plain_text, num_rails = self.validate_input(plain_text, num_rails)

        rails = [[] for _ in range(num_rails)]
        rail_index = 0
        direction = 1

        for char in plain_text:
            rails[rail_index].append(char)

            if rail_index == 0:
                direction = 1
            elif rail_index == num_rails - 1:
                direction = -1

            rail_index += direction

        cipher_text = "".join("".join(rail) for rail in rails)
        return cipher_text

    def rail_fence_decrypt(self, cipher_text, num_rails):
        cipher_text, num_rails = self.validate_input(cipher_text, num_rails)

        rail_lengths = [0] * num_rails
        rail_index = 0
        direction = 1

        for _ in range(len(cipher_text)):
            rail_lengths[rail_index] += 1

            if rail_index == 0:
                direction = 1
            elif rail_index == num_rails - 1:
                direction = -1

            rail_index += direction

        rails = []
        start = 0

        for length in rail_lengths:
            rails.append(list(cipher_text[start:start + length]))
            start += length

        plain_text = ""
        rail_index = 0
        direction = 1

        for _ in range(len(cipher_text)):
            plain_text += rails[rail_index].pop(0)

            if rail_index == 0:
                direction = 1
            elif rail_index == num_rails - 1:
                direction = -1

            rail_index += direction

        return plain_text