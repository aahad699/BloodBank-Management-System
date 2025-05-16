from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QFormLayout, QLineEdit, 
                             QPushButton, QLabel, QMessageBox, QHBoxLayout, QSizePolicy)
from PyQt5.QtCore import Qt
import hashlib

class LoginDialog(QDialog):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.setWindowTitle("Login")
        self.setModal(True)
        self.setMinimumSize(400, 300)
        self.user_data = None
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(15)
        
        title_label = QLabel("Blood Bank Management System")
        title_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #c0392b;")
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)
        
        layout.addSpacing(20)

        form_layout = QFormLayout()
        form_layout.setSpacing(12)
        form_layout.setLabelAlignment(Qt.AlignRight)
        form_layout.setFormAlignment(Qt.AlignHCenter)

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter username")
        self.username_input.setMinimumWidth(250)
        
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setMinimumWidth(250)

        form_layout.addRow("Username:", self.username_input)
        form_layout.addRow("Password:", self.password_input)
        
        layout.addLayout(form_layout)
        layout.addSpacing(25)

        button_layout = QHBoxLayout()
        
        self.login_button = QPushButton("Login")
        self.login_button.setMinimumWidth(120)
        self.login_button.clicked.connect(self.authenticate)
        
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.setMinimumWidth(120)
        self.cancel_button.clicked.connect(self.close)

        button_layout.addStretch()
        button_layout.addWidget(self.login_button)
        button_layout.addSpacing(15)
        button_layout.addWidget(self.cancel_button)
        button_layout.addStretch()

        layout.addLayout(button_layout)
        layout.addStretch()
        
        self.setLayout(layout)
        self.adjustSize()

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def authenticate(self):
        try:
            username = self.username_input.text().strip()
            password = self.password_input.text().strip()

            if not username or not password:
                QMessageBox.warning(self, "Warning", "Both fields are required")
                return False

            if not self.db.connection.is_connected():
                QMessageBox.critical(self, "Error", "Database connection lost")
                return False

            query = """
            SELECT a.Admin_ID, a.Admin_Name, a.Email, a.Password, 
                   bb.BB_Name, bb.BloodBank_ID
            FROM admin a
            LEFT JOIN blood_bank bb ON a.BloodBank_ID = bb.BloodBank_ID
            WHERE a.Username = %s AND a.Is_Active = TRUE
            """
            result = self.db.execute_query(query, (username,), fetch=True)

            if not result:
                QMessageBox.warning(self, "Login Failed", "Invalid credentials")
                return False

            stored_password = result[0]['Password']
            if self.hash_password(password) != stored_password:
                QMessageBox.warning(self, "Login Failed", "Invalid credentials")
                return False

            update_query = "UPDATE admin SET Last_Login = NOW() WHERE Admin_ID = %s"
            self.db.execute_query(update_query, (result[0]['Admin_ID'],))

            self.user_data = result[0]
            self.accept()
            return True

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Login failed: {str(e)}")
            print(f"Login error: {e}")
            return False