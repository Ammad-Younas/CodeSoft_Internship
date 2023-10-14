import sys
import random
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QHBoxLayout, QPushButton, QLineEdit
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
import os


class RockPaperScissorsGame(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.rounds_played = 0
        self.player_wins_total = 0
        self.computer_wins_total = 0
        self.player_wins = 0
        self.computer_wins = 0

        icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "icon/icon.ico")
        self.setWindowIcon(QIcon(icon_path))

    def initUI(self):
        self.setWindowTitle("Rock Paper Scissors")
        self.setFixedSize(400, 200)

        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)

        self.layout = QVBoxLayout()

        self.vs_layout = QHBoxLayout()
        self.player_label = QLabel("Player: ")
        self.computer_label = QLabel("Computer: ")
        self.vs_layout.addWidget(self.player_label)
        self.vs_layout.addWidget(self.computer_label)
        self.layout.addLayout(self.vs_layout)

        self.buttons_layout = QHBoxLayout()

        self.rock_button = QPushButton("Rock")
        self.rock_button.clicked.connect(lambda: self.play_round("Rock"))

        self.paper_button = QPushButton("Paper")
        self.paper_button.clicked.connect(lambda: self.play_round("Paper"))

        self.scissors_button = QPushButton("Scissors")
        self.scissors_button.clicked.connect(lambda: self.play_round("Scissors"))

        self.buttons_layout.addWidget(self.rock_button)
        self.buttons_layout.addWidget(self.paper_button)
        self.buttons_layout.addWidget(self.scissors_button)

        self.layout.addLayout(self.buttons_layout)

        self.wins_label = QLabel("Wins: ")
        self.layout.addWidget(self.wins_label)

        self.win_show = QLineEdit()
        self.win_show.setReadOnly(True)
        self.win_show.setFocusPolicy(Qt.NoFocus)
        self.layout.addWidget(self.win_show)

        self.reset_button = QPushButton("Reset Game")
        self.reset_button.clicked.connect(self.reset_game)
        self.layout.addWidget(self.reset_button)

        self.centralWidget.setLayout(self.layout)

        self.player_wins = 0

    def play_round(self, player_choice):
        choices = ["Rock", "Paper", "Scissors"]
        computer_choice = random.choice(choices)

        self.player_label.setText(f"Player: {player_choice}")
        self.computer_label.setText(f"Computer: {computer_choice}")

        if player_choice == computer_choice:
            result = "It's a Tie!"
        elif (
            (player_choice == "Rock" and computer_choice == "Scissors")
            or (player_choice == "Paper" and computer_choice == "Rock")
            or (player_choice == "Scissors" and computer_choice == "Paper")
        ):
            result = "Player Wins!"
            self.player_wins += 1
        else:
            result = "Computer Wins!"
            self.computer_wins += 1

        self.rounds_played += 1

        if self.rounds_played == 10:
            final_result = ""
            if self.player_wins > self.computer_wins:
                final_result = "Player Wins!"
                self.player_wins_total += 1
            elif self.player_wins < self.computer_wins:
                final_result = "Computer Wins!"
                self.computer_wins_total += 1
            else:
                final_result = "It's a Tie!"

            self.win_show.setText(f"Final Winner: {final_result}")
            self.win_show.setCursorPosition(0)

            self.rounds_played = 0
            self.player_wins = 0
            self.computer_wins = 0
            self.rock_button.setEnabled(False)
            self.paper_button.setEnabled(False)
            self.scissors_button.setEnabled(False)
        else:
            self.win_show.setText(str(result))
            self.win_show.setCursorPosition(0)


    def reset_game(self):
        self.player_label.setText("Player: ")
        self.computer_label.setText("Computer: ")
        self.win_show.clear()
        self.player_wins = 0
        self.rock_button.setEnabled(True)
        self.paper_button.setEnabled(True)
        self.scissors_button.setEnabled(True)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    game = RockPaperScissorsGame()
    game.show()
    sys.exit(app.exec_())