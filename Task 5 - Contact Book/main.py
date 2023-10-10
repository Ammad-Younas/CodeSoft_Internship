import sys
import sqlite3
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QTreeView, QFormLayout, QRadioButton, QDialogButtonBox, QMessageBox, QHeaderView, QFileDialog, QDialog, QListWidget, QListWidgetItem
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QIcon
import os

class ContactApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Contact App')
        self.initUI()
        self.db_conn = sqlite3.connect(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'contacts.db'))
        self.create_table()
        self.display_contacts()

    def initUI(self):

        icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "icon/icon.ico")
        self.setWindowIcon(QIcon(icon_path))

        layout = QVBoxLayout()

        form_layout = QFormLayout()

        self.name_entry = QLineEdit(self)
        self.mobile_entry = QLineEdit(self)

        form_layout.addRow('Name:', self.name_entry)
        form_layout.addRow('Mobile Number:', self.mobile_entry)

        button_layout = QHBoxLayout()
        buttons = ['Add', 'Update', 'Delete', 'Export', 'Search', 'Reset']
        for btn_text in buttons:
            button = QPushButton(btn_text)
            button.clicked.connect(self.onButtonClick)
            button_layout.addWidget(button)

        self.search_entry = QLineEdit(self)
        self.search_entry.setPlaceholderText("Search term")

        self.search_by_name = QRadioButton("Search by Name")
        self.search_by_number = QRadioButton("Search by Number")
        self.search_by_name.setChecked(True)

        self.tree_model = QStandardItemModel()
        self.tree_view = QTreeView(self)
        self.tree_view.setModel(self.tree_model)
        self.tree_view.header().setSectionResizeMode(QHeaderView.Stretch)

        layout.addLayout(form_layout)
        layout.addLayout(button_layout)
        layout.addWidget(self.search_entry)
        layout.addWidget(self.search_by_name)
        layout.addWidget(self.search_by_number)
        layout.addWidget(self.tree_view)

        self.setLayout(layout)

    def create_table(self):
        cursor = self.db_conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS contacts
                          (name TEXT,
                          mobile TEXT)''')
        self.db_conn.commit()

    def onButtonClick(self):
        sender = self.sender().text()
        if sender == 'Add':
            self.add_contact()
        elif sender == 'Update':
            self.update_contact()
        elif sender == 'Delete':
            self.confirm_delete_contact()
        elif sender == 'Export':
            self.export_contacts()
        elif sender == 'Search':
            self.search_contacts()
        elif sender == 'Reset':
            self.display_contacts()

    def add_contact(self):
        name = self.name_entry.text()
        mobile = self.mobile_entry.text()
        if name and mobile:
            cursor = self.db_conn.cursor()
            cursor.execute("INSERT INTO contacts (name, mobile) VALUES (?, ?)", (name, mobile))
            self.db_conn.commit()
            self.display_contacts()
            self.name_entry.clear()
            self.mobile_entry.clear()
        else:
            QMessageBox.warning(self, 'Warning', 'Please enter both name and mobile number.')

    def update_contact(self):
        selected_items = self.tree_view.selectionModel().selectedIndexes()
        if not selected_items:
            QMessageBox.warning(self, 'Warning', 'Please select a contact to update.')
            return
        selected_row = selected_items[0].row()
        selected_contact_name = self.tree_model.item(selected_row, 0).text()
        selected_contact_mobile = self.tree_model.item(selected_row, 1).text()

        dialog = UpdateContactDialog(selected_contact_name, selected_contact_mobile, self)
        if dialog.exec_():
            updated_name, updated_mobile = dialog.get_values()
            if updated_name and updated_mobile:
                cursor = self.db_conn.cursor()
                cursor.execute("UPDATE contacts SET name=?, mobile=? WHERE name=? AND mobile=?", (updated_name, updated_mobile, selected_contact_name, selected_contact_mobile))
                self.db_conn.commit()
                self.display_contacts()

    def confirm_delete_contact(self):
        selected_items = self.tree_view.selectionModel().selectedIndexes()
        if not selected_items:
            QMessageBox.warning(self, 'Warning', 'Please select a contact to delete.')
            return

        reply = QMessageBox.question(self, 'Confirm Deletion', 'Are you sure you want to delete this contact?', 
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.delete_contact()

    def delete_contact(self):
        selected_items = self.tree_view.selectionModel().selectedIndexes()
        selected_row = selected_items[0].row()
        selected_contact_name = self.tree_model.item(selected_row, 0).text()
        selected_contact_mobile = self.tree_model.item(selected_row, 1).text()
        cursor = self.db_conn.cursor()
        cursor.execute("DELETE FROM contacts WHERE name=? AND mobile=?", (selected_contact_name, selected_contact_mobile))
        self.db_conn.commit()
        self.display_contacts()

    def export_contacts(self):
        selected_items = self.tree_view.selectionModel().selectedIndexes()
        selected_rows = [index.row() for index in selected_items]
        export_dialog = ExportDialog(self, selected_rows)
        export_dialog.exec_()

    def search_contacts(self):
        term = self.search_entry.text()
        if term:
            column = 'name' if self.search_by_name.isChecked() else 'mobile'
            cursor = self.db_conn.cursor()
            cursor.execute(f"SELECT * FROM contacts WHERE {column} LIKE ?", (f'%{term}%',))
            results = cursor.fetchall()
            self.show_search_results(results)

    def show_search_results(self, results):
        self.tree_model.clear()
        self.tree_model.setHorizontalHeaderLabels(['Name', 'Mobile Number'])
        for contact in results:
            row = [QStandardItem(contact[0]), QStandardItem(contact[1])]
            self.tree_model.appendRow(row)

    def display_contacts(self):
        self.tree_model.clear()
        self.tree_model.setHorizontalHeaderLabels(['Name', 'Mobile Number'])
        cursor = self.db_conn.cursor()
        cursor.execute("SELECT * FROM contacts")
        contacts = cursor.fetchall()
        for contact in contacts:
            row = [QStandardItem(contact[0]), QStandardItem(contact[1])]
            self.tree_model.appendRow(row)


class UpdateContactDialog(QDialog):
    def __init__(self, name, mobile, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Update Contact')
        self.layout = QFormLayout()

        self.name_entry = QLineEdit(self)
        self.mobile_entry = QLineEdit(self)

        self.name_entry.setText(name)
        self.mobile_entry.setText(mobile)

        self.layout.addRow('Name:', self.name_entry)
        self.layout.addRow('Mobile Number:', self.mobile_entry)

        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)

        self.layout.addWidget(button_box)
        self.setLayout(self.layout)

    def get_values(self):
        return self.name_entry.text(), self.mobile_entry.text()


class ExportDialog(QDialog):
    def __init__(self, parent, selected_rows):
        super().__init__(parent)
        self.setWindowTitle('Export Contacts')
        self.layout = QVBoxLayout()

        self.export_list = QListWidget(self)
        self.export_list.setSelectionMode(QListWidget.MultiSelection)

        self.export_button = QPushButton('Export', self)
        self.export_button.clicked.connect(self.export_contacts)

        self.layout.addWidget(self.export_list)
        self.layout.addWidget(self.export_button)
        self.setLayout(self.layout)

        cursor = parent.db_conn.cursor()
        cursor.execute("SELECT * FROM contacts")
        contacts = cursor.fetchall()
        for index, contact in enumerate(contacts):
            item = QListWidgetItem(f'{contact[0]}: {contact[1]}')
            if index in selected_rows:
                item.setSelected(True)
            self.export_list.addItem(item)

    def export_contacts(self):
        selected_items = self.export_list.selectedIndexes()
        if not selected_items:
            QMessageBox.warning(self, 'Warning', 'Please select contacts to export.')
            return

        filename, _ = QFileDialog.getSaveFileName(self, 'Save Contacts', '', 'VCF Files (*.vcf);;All Files (*)')
        if filename:
            with open(filename, 'w', encoding='utf-8') as vcf_file:
                cursor = self.parent().db_conn.cursor()
                cursor.execute("SELECT * FROM contacts")
                contacts = cursor.fetchall()

                for index in selected_items:
                    contact = contacts[index.row()]
                    name, mobile = contact[0], contact[1]

                    vcf_file.write(f'BEGIN:VCARD\n')
                    vcf_file.write(f'FN:{name}\n')
                    vcf_file.write(f'TEL:{mobile}\n')
                    vcf_file.write(f'END:VCARD\n')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ContactApp()
    window.show()
    sys.exit(app.exec_())
