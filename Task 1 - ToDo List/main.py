import sys
import os
import sqlite3
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QListWidget, QPushButton, QListWidgetItem, QLineEdit, QDialog,
    QCheckBox, QMessageBox, QLabel
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

class ToDoListApp(QWidget):
    def __init__(self):
        super().__init__()
        self.db_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "todolist.db")
        self.init_db()
        self.load_tasks_from_db()
        self.init_ui()

    def init_db(self):
        self.conn = sqlite3.connect(self.db_file_path)
        self.cursor = self.conn.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY, task TEXT, completed INTEGER DEFAULT 0)")

    def load_tasks_from_db(self):
        self.tasks = []
        self.cursor.execute("SELECT task, completed FROM tasks")
        rows = self.cursor.fetchall()
        for row in rows:
            task, completed = row
            self.tasks.append((task, completed))

    def init_ui(self):
        self.setWindowTitle('To-Do List App')
        self.setGeometry(200, 200, 500, 400)

        self.task_list = QListWidget(self)
        self.add_button = QPushButton('Add Task', self)
        self.update_button = QPushButton('Update Task', self)
        self.delete_button = QPushButton('Delete Task', self)

        icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "icon/icon.ico")
        self.setWindowIcon(QIcon(icon_path))

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.task_list)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.update_button)
        button_layout.addWidget(self.delete_button)

        self.layout.addLayout(button_layout)
        self.setLayout(self.layout)

        self.add_button.clicked.connect(self.add_task_popup)
        self.update_button.clicked.connect(self.update_task_popup)
        self.delete_button.clicked.connect(self.delete_task)

        self.update_task_list()

    def add_task_popup(self):
        popup_dialog = QDialog(self)
        popup_dialog.setWindowTitle('Add Task')
        popup_dialog.setMinimumWidth(300)

        layout = QVBoxLayout()

        task_edit = QLineEdit()
        add_button = QPushButton('Add')

        layout.addWidget(task_edit)
        layout.addWidget(add_button)

        popup_dialog.setLayout(layout)

        def add_task():
            task_text = task_edit.text()
            if task_text:
                self.add_task_to_db(task_text)
                popup_dialog.accept()

        add_button.clicked.connect(add_task)
        popup_result = popup_dialog.exec_()

    def add_task_to_db(self, task_text):
        self.cursor.execute("INSERT INTO tasks (task) VALUES (?)", (task_text,))
        self.conn.commit()
        self.load_tasks_from_db()
        self.update_task_list()

    def update_task_popup(self):
        selected_item = self.task_list.currentItem()
        if selected_item:
            index = self.task_list.row(selected_item)
            old_task, _ = self.tasks[index]

            popup_dialog = QDialog(self)
            popup_dialog.setWindowTitle('Update Task')

            layout = QVBoxLayout()

            task_edit = QLineEdit()
            task_edit.setText(old_task)
            update_button = QPushButton('Update')

            layout.addWidget(task_edit)
            layout.addWidget(update_button)

            popup_dialog.setLayout(layout)

            def update_task():
                new_text = task_edit.text()
                self.update_task_in_db(old_task, new_text)
                popup_dialog.accept()

            update_button.clicked.connect(update_task)
            popup_result = popup_dialog.exec_()
        else:
            QMessageBox.warning(self, 'Warning', 'Please select a task to update.')

    def update_task_in_db(self, old_task, new_task):
        self.cursor.execute("UPDATE tasks SET task = ? WHERE task = ?", (new_task, old_task))
        self.conn.commit()
        self.load_tasks_from_db()
        self.update_task_list()

    def delete_task(self):
        if not self.tasks:
            QMessageBox.warning(self, 'Warning', 'Task list is empty.')
            return

        selected_item = self.task_list.currentItem()
        if selected_item:
            index = self.task_list.row(selected_item)
            task_to_delete, _ = self.tasks[index]
            self.cursor.execute("DELETE FROM tasks WHERE task = ?", (task_to_delete,))
            self.conn.commit()
            del self.tasks[index]
            self.task_list.takeItem(index)
        else:
            QMessageBox.warning(self, 'Warning', 'Please select a task to delete.')

    def update_task_list(self):
        self.task_list.clear()
        self.load_tasks_from_db()
        for task, completed in self.tasks:
            item_widget = QWidget()
            item_layout = QHBoxLayout()
            checkbox = QCheckBox()
            checkbox.setChecked(completed)
            checkbox.stateChanged.connect(lambda state, task=task: self.update_task_completion(task, state))
            label = QLabel(task)

            item_layout.addWidget(checkbox)
            item_layout.addWidget(label)
            item_layout.setAlignment(Qt.AlignLeft)

            item_widget.setLayout(item_layout)
            item = QListWidgetItem()
            item.setSizeHint(item_widget.sizeHint())
            self.task_list.addItem(item)
            self.task_list.setItemWidget(item, item_widget)


    def update_task_completion(self, task, state):
        for index, (t, completed) in enumerate(self.tasks):
            if t == task:
                if completed != state:
                    self.tasks[index] = (task, state)
                    self.cursor.execute("UPDATE tasks SET completed = ? WHERE task = ?", (state, task))
                    self.conn.commit()

def main():
    app = QApplication(sys.argv)
    window = ToDoListApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
