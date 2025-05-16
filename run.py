import sys
import os
from PyQt5.QtWidgets import QApplication, QMessageBox, QDialog, QSplashScreen
from PyQt5.QtGui import QFontDatabase, QFont, QPixmap
from PyQt5.QtCore import Qt, QTimer
from database import DatabaseManager
from login_dialog import LoginDialog
from signup_dialog import SignUpDialog

def load_styles(app):
    """Load application stylesheet and set default font"""
    try:
        style_path = "styles.qss"
        if os.path.exists(style_path):
            with open(style_path, 'r') as f:
                app.setStyleSheet(f.read())
            print("Stylesheet loaded successfully")
        else:
            print("Stylesheet file not found")
    except Exception as e:
        print(f"Error loading stylesheet: {e}")
    
    font = QFont("Segoe UI", 10)
    app.setFont(font)

def show_splash_screen(app):
    """Show splash screen while app initializes"""
    try:
        splash_pix = QPixmap("resources/splash.png")
        if splash_pix.isNull():
            splash_pix = QPixmap(500, 300)
            splash_pix.fill(Qt.white)
    except:
        splash_pix = QPixmap(500, 300)
        splash_pix.fill(Qt.white)
    
    splash = QSplashScreen(splash_pix, Qt.WindowStaysOnTopHint)
    splash.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
    splash.setEnabled(False)
    
    splash.showMessage("<h2>Blood Bank Management System</h2><p>Starting application...</p>", 
                      Qt.AlignCenter | Qt.AlignBottom, Qt.black)
    
    splash.show()
    app.processEvents()
    
    return splash

def main():
    """Main application entry point"""
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    load_styles(app)
    
    splash = show_splash_screen(app)
    
    db = DatabaseManager()
    if not db.connect():
        splash.finish(None)
        QMessageBox.critical(None, "Database Error", 
                           "Failed to connect to database.\nPlease check database settings and try again.")
        return 1
    
    query = "SELECT COUNT(*) as count FROM admin"
    result = db.execute_query(query, fetch=True)
    admin_exists = result and result[0]['count'] > 0
    
    from main import MainWindow
    
    if not admin_exists:
        splash.showMessage("<h2>Blood Bank Management System</h2><p>First-time setup...</p>", 
                         Qt.AlignCenter | Qt.AlignBottom, Qt.black)
        app.processEvents()
        
        splash.finish(None)
        
        msg = QMessageBox()
        msg.setWindowTitle("First Run Setup")
        msg.setText("No admin accounts found. You need to create the first admin account.")
        msg.setIcon(QMessageBox.Information)
        msg.exec_()
        
        signup = SignUpDialog(db)
        if signup.exec_() != QDialog.Accepted:
            db.disconnect()
            return 0
        
        login = LoginDialog(db)
        if login.exec_() != QDialog.Accepted:
            db.disconnect()
            return 0
        
        window = MainWindow(db, login.user_data)
        window.show()
    else:
        QTimer.singleShot(1500, lambda: splash.finish(None))
        
        window = MainWindow(db)
        window.show()
    
    return app.exec_()

if __name__ == "__main__":
    sys.exit(main())