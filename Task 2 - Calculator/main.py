import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLineEdit, QGridLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QIcon
import ast
import os

class Calculator(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Calculator')
        self.setFixedSize(400, 400)

        icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "icon/icon.ico")
        self.setWindowIcon(QIcon(icon_path))

        layout = QVBoxLayout()
        layout.setContentsMargins(20, 0, 20, 0)

        self.secondary_display = QLineEdit()
        self.secondary_display.setFixedHeight(30)
        self.secondary_display.setReadOnly(True)
        layout.addWidget(self.secondary_display)

        self.main_display = QLineEdit()
        self.main_display.setFixedHeight(50)
        self.main_display.setMaxLength(16)
        font = self.main_display.font()
        font.setPointSize(20)
        self.main_display.setFont(font)
        self.main_display.setAlignment(Qt.AlignRight)
        layout.addWidget(self.main_display)

        # Add buttons
        button_grid = QGridLayout()
        buttons = [
            '7', '8', '9', '/',
            '4', '5', '6', '*',
            '1', '2', '3', '-',
            '0', 'C', '=', '+'
        ]

        row, col = 0, 0
        for label in buttons:
            button = QPushButton(label)
            button.setFont(QFont('Segoe UI', 16))
            button.clicked.connect(lambda _, label=label: self.on_button_click(label))
            button_grid.addWidget(button, row, col)
            col += 1
            if col > 3:
                col = 0
                row += 1

        # Add Del button
        del_button = QPushButton('Del')
        del_button.setFont(QFont('Segoe UI', 16))
        del_button.clicked.connect(self.on_del_button_click)
        button_grid.addWidget(del_button, row, col, 1, -1)

        layout.addLayout(button_grid)
        self.setLayout(layout)
    
    def on_button_click(self, label):
        main_text = self.main_display.text()
        secondary_text = self.secondary_display.text()

        if label.isdigit() or (label == '.' and '.' not in main_text):
            self.main_display.setText(main_text + label)
        elif label in ['+', '-', '*', '/']:
            if main_text:
                self.secondary_display.setText(secondary_text + main_text + ' ' + label + ' ')
                self.main_display.clear()
        elif label == '=':
            if main_text and secondary_text:
                try:
                    expression = secondary_text + main_text
                    parsed_expression = ast.parse(expression, mode='eval')
                    
                    result = eval(compile(parsed_expression, filename='', mode='eval'))
                    
                    if len(str(result)) > 16:
                        result = '{:.2e}'.format(result)
                    
                    self.secondary_display.setText('')
                    self.main_display.setText(str(result))
                except Exception:
                    self.secondary_display.setText('Error')
                    self.main_display.clear()

        elif label == 'C':
            self.secondary_display.clear()
            self.main_display.clear()


    def on_del_button_click(self):
        main_text = self.main_display.text()
        self.main_display.setText(main_text[:-1])

def main():
    app = QApplication(sys.argv)
    window = Calculator()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()