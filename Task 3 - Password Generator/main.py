import sys
import string
import random
import pyperclip
from PyQt5.QtWidgets import QApplication, QWidget, QComboBox, QTextEdit, QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox
from PyQt5.QtGui import QFont, QIcon
import os

class PasswordGenerator(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Password Generator')
        self.setFixedSize(640, 400)

        icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "icon/icon.ico")
        self.setWindowIcon(QIcon(icon_path))

        self.passwordOptionsComboBox = QComboBox(self)
        self.passwordOptionsComboBox.setFixedHeight(30)
        self.passwordOptionsComboBox.addItems(["Select password difficulty", "Only Upper Case", "Only Lower Case", "Only Digits",
                                                 "Only Characters", "Upper Case + Lower Case", "Upper Case + Digits",
                                                 "Upper Case + Characters", "Lower Case + Digits",
                                                 "Lower Case + Characters", "Digits + Characters",
                                                 "Upper Case + Lower Case + Digits",
                                                 "Upper Case + Lower Case + Characters",
                                                 "Upper Case + Lower Case + Digits + Characters"])
        self.passwordOptionsComboBox.setFont(QFont("Segoe UI", 9))

        self.passwordLengthComboBox = QComboBox(self)
        self.passwordLengthComboBox.setFixedHeight(30)
        self.passwordLengthComboBox.setFont(QFont("Segoe UI", 9))

        self.passwordLengthComboBox.addItem("Select Length")
        self.passwordLengthComboBox.setCurrentIndex(0)

        self.outputTextEdit = QTextEdit()
        self.outputTextEdit.setReadOnly(True)

        self.generateButton = QPushButton('Generate')
        self.copyButton = QPushButton('Copy')
        self.clearButton = QPushButton('Clear')

        self.generateButton.setFont(QFont("Segoe UI", 11))
        self.copyButton.setFont(QFont("Segoe UI", 11))
        self.clearButton.setFont(QFont("Segoe UI", 11))

        buttonLayout = QHBoxLayout()
        buttonLayout.addWidget(self.generateButton)
        buttonLayout.addWidget(self.copyButton)
        buttonLayout.addWidget(self.clearButton)

        self.generateButton.clicked.connect(self.generatePassword)
        self.copyButton.clicked.connect(self.copyPassword)
        self.clearButton.clicked.connect(self.clearPassword)

        self.copyButton.setEnabled(False)
        self.clearButton.setEnabled(False)

        layout = QVBoxLayout()
        optionsLayout = QHBoxLayout()
        optionsLayout.addWidget(self.passwordOptionsComboBox)
        optionsLayout.addWidget(self.passwordLengthComboBox)
        layout.addLayout(optionsLayout)
        layout.addWidget(self.outputTextEdit)
        layout.addLayout(buttonLayout)

        self.setLayout(layout)

        self.passwordOptionsComboBox.currentIndexChanged.connect(self.forDifficultySelection)

    def forDifficultySelection(self):
        selected_option = self.passwordOptionsComboBox.currentText()
        if selected_option == "Select password difficulty":
            self.passwordLengthComboBox.clear()
        else:
            options = {
                "Only Upper Case": string.ascii_uppercase,
                "Only Lower Case": string.ascii_lowercase,
                "Only Digits": string.digits,
                "Only Characters": string.punctuation,
                "Upper Case + Lower Case": string.ascii_uppercase + string.ascii_lowercase,
                "Upper Case + Digits": string.ascii_uppercase + string.digits,
                "Upper Case + Characters": string.ascii_uppercase + string.punctuation,
                "Lower Case + Digits": string.ascii_lowercase + string.digits,
                "Lower Case + Characters": string.ascii_lowercase + string.punctuation,
                "Digits + Characters": string.digits + string.punctuation,
                "Upper Case + Lower Case + Digits": string.ascii_uppercase + string.ascii_lowercase + string.digits,
                "Upper Case + Lower Case + Characters": string.ascii_uppercase + string.ascii_lowercase + string.punctuation,
                "Upper Case + Lower Case + Digits + Characters": string.ascii_uppercase + string.ascii_lowercase + string.digits + string.punctuation
            }
            self.passwordLengthComboBox.clear()
            self.passwordLengthComboBox.addItems([str(i) for i in range(1, len(options[selected_option]) + 1)])


    def generatePassword(self):
        selected_option = self.passwordOptionsComboBox.currentText()
        if selected_option == "Select password difficulty":
            QMessageBox.warning(self, 'Warning!', 'Select Password Difficulty Level')
        else:
            try:
                password_length = int(self.passwordLengthComboBox.currentText())
                options = {
                    "Only Upper Case": string.ascii_uppercase,
                    "Only Lower Case": string.ascii_lowercase,
                    "Only Digits": string.digits,
                    "Only Characters": string.punctuation,
                    "Upper Case + Lower Case": string.ascii_uppercase + string.ascii_lowercase,
                    "Upper Case + Digits": string.ascii_uppercase + string.digits,
                    "Upper Case + Characters": string.ascii_uppercase + string.punctuation,
                    "Lower Case + Digits": string.ascii_lowercase + string.digits,
                    "Lower Case + Characters": string.ascii_lowercase + string.punctuation,
                    "Digits + Characters": string.digits + string.punctuation,
                    "Upper Case + Lower Case + Digits": string.ascii_uppercase + string.ascii_lowercase + string.digits,
                    "Upper Case + Lower Case + Characters": string.ascii_uppercase + string.ascii_lowercase + string.punctuation,
                    "Upper Case + Lower Case + Digits + Characters": string.ascii_uppercase + string.ascii_lowercase + string.digits + string.punctuation
                }
                generated_password = ''.join(random.choice(options[selected_option]) for _ in range(password_length))
                self.outputTextEdit.setPlainText(generated_password)
                self.copyButton.setEnabled(True)
                self.clearButton.setEnabled(True)
            except ValueError:
                QMessageBox.warning(self, 'Warning!', 'Invalid Password Length')

    def copyPassword(self):
        generated_password = self.outputTextEdit.toPlainText()
        pyperclip.copy(generated_password)
        QMessageBox.information(self, 'Info!', 'Copied!')

    def clearPassword(self):
        self.passwordOptionsComboBox.setCurrentIndex(0)
        self.passwordLengthComboBox.clear()
        self.passwordLengthComboBox.addItem("Select Length")
        self.passwordLengthComboBox.setCurrentIndex(0)
        self.outputTextEdit.clear()
        self.generateButton.setEnabled(True)
        self.copyButton.setEnabled(False)
        self.clearButton.setEnabled(False)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = PasswordGenerator()
    window.show()
    sys.exit(app.exec_())
