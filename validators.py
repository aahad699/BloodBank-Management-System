import re
from PyQt5.QtWidgets import QMessageBox

class Validators:
    @staticmethod
    def validate_password(password):
        """Validate password strength"""
        if len(password) < 8:
            return False, "Password must be at least 8 characters"
        if not any(c.isupper() for c in password):
            return False, "Password must contain at least one uppercase letter"
        if not any(c.isdigit() for c in password):
            return False, "Password must contain at least one digit"
        return True, ""
    
    @staticmethod
    def validate_username(username):
        """Validate username format"""
        if len(username) < 4:
            return False, "Username must be at least 4 characters"
        if not username.isalnum():
            return False, "Username can only contain letters and numbers"
        return True, ""

    @staticmethod
    def validate_phone(phone):
        """Validate international phone number format"""
        pattern = r'^\+[1-9]\d{1,14}$'  # E.164 format
        return re.match(pattern, phone) is not None
    
    @staticmethod
    def validate_email(email):
        """Basic email validation"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    @staticmethod
    def validate_date(date_str):
        """Validate date in YYYY-MM-DD format"""
        try:
            from datetime import datetime
            datetime.strptime(date_str, '%Y-%m-%d')
            return True
        except ValueError:
            return False
    
    @staticmethod
    def show_validation_error(parent, message):
        QMessageBox.warning(parent, "Validation Error", message)

    @staticmethod
    def validate_donor_fields(parent, name, contact, dob):
        if not name.strip():
            Validators.show_validation_error(parent, "Name is required")
            return False
        
        if not Validators.validate_phone(contact):
            Validators.show_validation_error(parent, "Invalid phone number format. Please use international format (+1234567890)")
            return False
            
        if not Validators.validate_date(dob):
            Validators.show_validation_error(parent, "Invalid date format. Please use YYYY-MM-DD")
            return False
            
        return True