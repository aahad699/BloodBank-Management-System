import sys
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QTabWidget, QWidget, 
                            QVBoxLayout, QHBoxLayout, QPushButton, QLabel, 
                            QMessageBox, QStatusBar, QDialog, QFrame)
from PyQt5.QtCore import Qt
from database import DatabaseManager
from login_dialog import LoginDialog
from signup_dialog import SignUpDialog

class AuthDialog(QDialog):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.user_data = None
        self.setWindowTitle("AAHAD_69")
        self.setMinimumSize(600, 500)
        self.setModal(True)
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)
        
        header_label = QLabel("Blood Bank Management System")
        header_label.setStyleSheet("font-size: 22px; font-weight: bold; color: #c0392b;")
        header_label.setAlignment(Qt.AlignHCenter)
        
        subtitle_label = QLabel("Please login or create a new account")
        subtitle_label.setStyleSheet("font-size: 14px; color: #555;")
        subtitle_label.setAlignment(Qt.AlignHCenter)
        
        layout.addWidget(header_label)
        layout.addWidget(subtitle_label)
        layout.addSpacing(10)
        
        tab_widget = QTabWidget()
        tab_widget.setStyleSheet("QTabWidget::pane { border-top: 0px; }")
        
        login_widget = QWidget()
        login_layout = QVBoxLayout(login_widget)
        login_layout.setContentsMargins(0, 20, 0, 0)
        
        self.login_dialog = LoginDialog(self.db)
        self.login_dialog.setParent(login_widget)
        self.login_dialog.setWindowFlags(Qt.Widget)
        
        self.login_dialog.accepted.connect(self.handle_login_success)
        
        login_layout.addWidget(self.login_dialog)
        
        signup_widget = QWidget()
        signup_layout = QVBoxLayout(signup_widget)
        signup_layout.setContentsMargins(0, 20, 0, 0)
        
        self.signup_dialog = SignUpDialog(self.db)
        self.signup_dialog.setParent(signup_widget)
        self.signup_dialog.setWindowFlags(Qt.Widget)
        
        self.signup_dialog.accepted.connect(self.handle_signup_success)
        
        signup_layout.addWidget(self.signup_dialog)
        
        tab_widget.addTab(login_widget, "Login")
        tab_widget.addTab(signup_widget, "Sign Up")
        
        layout.addWidget(tab_widget)
        self.setLayout(layout)
    
    def handle_login_success(self):
        self.user_data = self.login_dialog.user_data
        self.accept()
    
    def handle_signup_success(self):
        QMessageBox.information(self, "Success", "Account created successfully. Please log in.")
        # Switch to login tab
        self.findChild(QTabWidget).setCurrentIndex(0)


class MainWindow(QMainWindow):
    def __init__(self, db=None, user_data=None):
        super().__init__()
        self.user_data = user_data
        self.setWindowTitle("Blood Bank Management System")
        self.setGeometry(100, 100, 1200, 800)
        
        if db is None:
            self.db = DatabaseManager()
            if not self.db.connect():
                QMessageBox.critical(None, "Database Error", "Failed to connect to database")
                sys.exit(1)
            self.db_owner = True  # We created it, we should close it
        else:
            self.db = db
            self.db_owner = False  # External db connection, don't close it
        
        if self.user_data is None:
            if not self.check_admin_exists():
                self.initial_setup()
            else:
                self.show_authentication()
            
            if not self.user_data:
                sys.exit(0)
        
        self.init_ui()
    
    def check_admin_exists(self):
        query = "SELECT COUNT(*) as count FROM admin"
        result = self.db.execute_query(query, fetch=True)
        return result and result[0]['count'] > 0
    
    def initial_setup(self):
        """First-time setup when no admin exists"""
        reply = QMessageBox.question(
            self, 
            "First Run Setup",
            "No admin accounts found. Create the first admin account now?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            signup = SignUpDialog(self.db)
            if signup.exec_() == QDialog.Accepted:
                QMessageBox.information(self, "Success", "Admin account created. Please log in.")
                login = LoginDialog(self.db)
                if login.exec_() == QDialog.Accepted:
                    self.user_data = login.user_data
    
    def show_authentication(self):
        auth_dialog = AuthDialog(self.db)
        
        if auth_dialog.exec_() == QDialog.Accepted:
            self.user_data = auth_dialog.user_data
    
    def init_ui(self):
        status_bar = QStatusBar()
        self.setStatusBar(status_bar)
        status_bar.showMessage(f"Logged in as: {self.user_data['Admin_Name']} | Blood Bank: {self.user_data.get('BB_Name', 'System Admin')}")
        
        self.tabs = QTabWidget()
        
        try:
            from donor_tab import DonorManagementTab
            from inventory_tab import InventoryManagementTab
            from reports_tab import ReportsTab
            
            self.donor_tab = DonorManagementTab(self.db)
            self.inventory_tab = InventoryManagementTab(self.db)
            self.reports_tab = ReportsTab(self.db)
            
            self.tabs.addTab(self.donor_tab, "Donor Management")
            self.tabs.addTab(self.inventory_tab, "Inventory Management")
            self.tabs.addTab(self.reports_tab, "Reports")
            
            if not self.user_data.get('BloodBank_ID'):
                try:
                    from admin_tab import AdminTab
                    self.admin_tab = AdminTab(self.db)
                    self.tabs.addTab(self.admin_tab, "Admin Management")
                except ImportError:
                    pass
                
        except ImportError as e:
            QMessageBox.warning(self, "Module Error", f"Failed to load module: {str(e)}")
        
        self.setCentralWidget(self.tabs)
        
    def closeEvent(self, event):
        """Clean up when closing the application"""
        if self.db_owner and self.db:
            self.db.disconnect()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    
    try:
        style_path = "styles.qss"
        if os.path.exists(style_path):
            with open(style_path, "r") as style_file:
                style = style_file.read()
                app.setStyleSheet(style)
    except Exception as e:
        print(f"Failed to load stylesheet: {e}")
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec_())