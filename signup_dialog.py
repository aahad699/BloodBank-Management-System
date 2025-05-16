from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QFormLayout, QLineEdit, 
                            QPushButton, QLabel, QMessageBox, QComboBox, QHBoxLayout,
                            QSizePolicy, QSpacerItem)
from PyQt5.QtCore import Qt
from validators import Validators
import hashlib

class SignUpDialog(QDialog):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.setWindowTitle("Create New Admin Account")
        self.setModal(True)
        self.setMinimumSize(500, 450)
        
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(15)
        
        title_label = QLabel("Create Admin Account")
        title_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #c0392b;")
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)
        
        layout.addSpacing(15)
        
        form_layout = QFormLayout()
        form_layout.setSpacing(12)
        form_layout.setLabelAlignment(Qt.AlignRight)
        form_layout.setFormAlignment(Qt.AlignHCenter)
        
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter your full name")
        self.name_input.setMinimumWidth(300)
        
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Choose a username")
        self.username_input.setMinimumWidth(300)
        
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Enter your email address")
        self.email_input.setMinimumWidth(300)
        
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Create a password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setMinimumWidth(300)
        
        self.confirm_password_input = QLineEdit()
        self.confirm_password_input.setPlaceholderText("Confirm your password")
        self.confirm_password_input.setEchoMode(QLineEdit.Password)
        self.confirm_password_input.setMinimumWidth(300)
        
        self.blood_bank_combo = QComboBox()
        self.blood_bank_combo.setMinimumWidth(300)
        self.blood_bank_combo.setMinimumHeight(38)
        
        self.load_blood_banks()
        
        form_layout.addRow("Full Name:", self.name_input)
        form_layout.addRow("Username:", self.username_input)
        form_layout.addRow("Email:", self.email_input)
        form_layout.addRow("Password:", self.password_input)
        form_layout.addRow("Confirm Password:", self.confirm_password_input)
        form_layout.addRow("Blood Bank:", self.blood_bank_combo)
        
        layout.addLayout(form_layout)
        layout.addSpacing(25)
        
        button_layout = QHBoxLayout()
        self.signup_button = QPushButton("Sign Up")
        self.signup_button.setMinimumWidth(120)
        self.signup_button.clicked.connect(self.create_account)
        
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.setMinimumWidth(120)
        self.cancel_button.clicked.connect(self.close)
        
        button_layout.addStretch()
        button_layout.addWidget(self.signup_button)
        button_layout.addSpacing(15)
        button_layout.addWidget(self.cancel_button)
        button_layout.addStretch()
        
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
        self.adjustSize()
    
    def load_blood_banks(self):
        query = "SELECT BloodBank_ID, BB_Name FROM blood_bank"
        blood_banks = self.db.execute_query(query, fetch=True)
        self.blood_bank_combo.addItem("Select Blood Bank", None)
        for bb in blood_banks:
            self.blood_bank_combo.addItem(bb['BB_Name'], bb['BloodBank_ID'])
    
    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()
    
    def create_account(self):
        name = self.name_input.text().strip()
        username = self.username_input.text().strip()
        email = self.email_input.text().strip()
        password = self.password_input.text()
        confirm_password = self.confirm_password_input.text()
        blood_bank_id = self.blood_bank_combo.currentData()
        
        if not all([name, username, email, password, confirm_password]):
            QMessageBox.warning(self, "Warning", "All fields are required")
            return
            
        if password != confirm_password:
            QMessageBox.warning(self, "Warning", "Passwords do not match")
            return
            
        if not Validators.validate_email(email):
            QMessageBox.warning(self, "Warning", "Invalid email format")
            return
            
        if blood_bank_id is None:
            QMessageBox.warning(self, "Warning", "Please select a blood bank")
            return
            
        query = "SELECT Admin_ID FROM admin WHERE Username = %s"
        result = self.db.execute_query(query, (username,), fetch=True)
        if result:
            QMessageBox.warning(self, "Warning", "Username already exists")
            return
            
        hashed_password = self.hash_password(password)
        
        query = """
        INSERT INTO admin 
            (Admin_Name, Username, Password, Email, BloodBank_ID)
        VALUES (%s, %s, %s, %s, %s)
        """
        params = (name, username, hashed_password, email, blood_bank_id)
        
        result = self.db.execute_query(query, params)
        if result:
            QMessageBox.information(self, "Success", "Account created successfully")
            self.accept()
        else:
            QMessageBox.warning(self, "Error", "Failed to create account")