import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from ui.playfair import Ui_MainWindow
import requests

class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushEncrypt.clicked.connect(self.call_api_encrypt)
        self.ui.pushDecrypt.clicked.connect(self.call_api_decrypt)
        self.ui.pushCreateMatrix.clicked.connect(self.call_api_create_matrix)

    def validate_key(self):
        key = self.ui.textKey.toPlainText()
        if not key.isalpha():
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowTitle("Invalid Key")
            msg.setText("Khóa chỉ được chứa chữ cái A-Z, không dùng số, ký tự đặc biệt hoặc tiếng Việt có dấu.")
            msg.exec_()
            return False
        return True
    
    def call_api_encrypt(self):
        if not self.validate_key():
            return
        url = "http://127.0.0.1:5000/api/playfair/encrypt"
        payload = {
            "plain_text": self.ui.textPlainText.toPlainText(),
            "key": self.ui.textKey.toPlainText()
        }
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                self.ui.textCipherText.setText(data["encrypted_text"])

                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText("Mã hóa thành công!")
                msg.exec_()
            else:
                print("Error while calling API")
        except requests.exceptions.RequestException as e:
            print("Error: %s" % e.message)

    def call_api_decrypt(self):
        url = "http://127.0.0.1:5000/api/playfair/decrypt"
        payload = {
            "cipher_text": self.ui.textCipherText.toPlainText(),
            "key": self.ui.textKey.toPlainText()
        }
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                self.ui.textPlainText.setText(data["decrypted_text"])

                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText("Giải mã thành công!")
                msg.exec_()
            else:
                print("Error while calling API")
        except requests.exceptions.RequestException as e:
            print("Error: %s" % e.message)

    def call_api_create_matrix(self):
        url = "http://127.0.0.1:5000/api/playfair/creatematrix"
        payload = {
            "key": self.ui.textKey.toPlainText()
        }
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                matrix = data["playfair_matrix"]
                # Format 5x5 matrix as string for display
                matrix_str = "\n".join(" ".join(row) for row in matrix)
                self.ui.textMatrix.setText(matrix_str)

                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText("Tạo ma trận thành công!")
                msg.exec_()
            else:
                print("Error while calling API")
        except requests.exceptions.RequestException as e:
            print("Error: %s" % e.message)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
