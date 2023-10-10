import sys
import random
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QMessageBox
from PyQt5.QtGui import QIcon
import os

class RockPaperScissorsGame(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.user_score = 0
        self.comp_score = 0
        self.rounds_played = 0
        self.rounds_to_play = 10

        self.setFixedSize(300, 300)

        icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "icon/icon.ico")
        self.setWindowIcon(QIcon(icon_path))

        self.result_label = QLabel('')
        self.score_label = QLabel('User: 0 - Computer: 0')

        rock_button = QPushButton('Rock', self)
        rock_button.clicked.connect(lambda: self.on_choice_selected('rock'))

        paper_button = QPushButton('Paper', self)
        paper_button.clicked.connect(lambda: self.on_choice_selected('paper'))

        scissors_button = QPushButton('Scissors', self)
        scissors_button.clicked.connect(lambda: self.on_choice_selected('scissors'))

        layout = QVBoxLayout()
        layout.addWidget(rock_button)
        layout.addWidget(paper_button)
        layout.addWidget(scissors_button)
        layout.addWidget(self.result_label)
        layout.addWidget(self.score_label)

        self.setLayout(layout)
        self.setWindowTitle('Rock-Paper-Scissors Game')
        self.play_round()

    def computer_choice(self):
        choices = ['rock', 'paper', 'scissors']
        return random.choice(choices)

    def determine_winner(self, user_choice, comp_choice):
        if user_choice == comp_choice:
            return 'It\'s a tie!'
        elif (user_choice == 'rock' and comp_choice == 'scissors') or \
             (user_choice == 'paper' and comp_choice == 'rock') or \
             (user_choice == 'scissors' and comp_choice == 'paper'):
            self.user_score += 1
            return 'You win!'
        else:
            self.comp_score += 1
            return 'Computer wins!'

    def play_round(self):
        if self.rounds_played < self.rounds_to_play:
            self.rounds_played += 1
            self.user_choice = None
            self.comp_choice = None
            self.result_label.setText('')
        else:
            self.show_result()

    def on_choice_selected(self, choice):
        self.user_choice = choice
        self.comp_choice = self.computer_choice()
        winner = self.determine_winner(self.user_choice, self.comp_choice)
        self.result_label.setText(f'Your choice: {self.user_choice.capitalize()}\n'
                                  f'Computer\'s choice: {self.comp_choice.capitalize()}\n'
                                  f'Result: {winner}')
        self.score_label.setText(f'User: {self.user_score} - Computer: {self.comp_score}')
        self.play_round()

    def show_result(self):
        result_message = f'Game Over! You: {self.user_score} - Computer: {self.comp_score}\n'
        if self.user_score > self.comp_score:
            result_message += 'You win!'
        elif self.user_score < self.comp_score:
            result_message += 'Computer wins!'
        else:
            result_message += 'It\'s a tie!'
        QMessageBox.information(self, 'Game Over', result_message)
        sys.exit()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    game = RockPaperScissorsGame()
    sys.exit(app.exec_())
