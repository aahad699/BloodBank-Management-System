from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, 
                            QTableWidgetItem, QPushButton, QLineEdit, QLabel, 
                            QMessageBox, QFrame, QSizePolicy, QHeaderView,
                            QGroupBox, QToolButton)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon, QFont
from donor_dialog import DonorDialog

class DonorManagementTab(QWidget):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.init_ui()
        self.load_donors()
        
    def init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(15)
        
        header_layout = QHBoxLayout()
        title_label = QLabel("Donor Management")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setProperty("cssClass", "title")
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        main_layout.addLayout(header_layout)
        
        search_group = QGroupBox("Search")
        search_layout = QVBoxLayout()
        
        search_bar_layout = QHBoxLayout()
        search_icon = QLabel()
        search_icon.setPixmap(QIcon.fromTheme("edit-find").pixmap(QSize(16, 16)))
        search_bar_layout.addWidget(search_icon)
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search donors by name or contact...")
        self.search_input.textChanged.connect(self.load_donors)
        search_bar_layout.addWidget(self.search_input)
        
        clear_button = QToolButton()
        clear_button.setText("Clear")
        clear_button.clicked.connect(self.clear_search)
        search_bar_layout.addWidget(clear_button)
        
        search_layout.addLayout(search_bar_layout)
        search_group.setLayout(search_layout)
        main_layout.addWidget(search_group)
        
        button_layout = QHBoxLayout()
        
        self.add_button = QPushButton("Add Donor")
        self.add_button.setIcon(QIcon.fromTheme("list-add"))
        self.add_button.setProperty("cssClass", "success")
        self.add_button.clicked.connect(self.show_add_dialog)
        
        self.edit_button = QPushButton("Edit Donor")
        self.edit_button.setIcon(QIcon.fromTheme("document-edit"))
        self.edit_button.clicked.connect(self.show_edit_dialog)
        
        self.delete_button = QPushButton("Delete Donor")
        self.delete_button.setIcon(QIcon.fromTheme("edit-delete"))
        self.delete_button.setProperty("cssClass", "danger")
        self.delete_button.clicked.connect(self.delete_donor)
        
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.edit_button)
        button_layout.addWidget(self.delete_button)
        button_layout.addStretch()
        
        main_layout.addLayout(button_layout)
        
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        main_layout.addWidget(line)
        
        table_label = QLabel("Donor Records")
        table_label.setProperty("cssClass", "subtitle")
        main_layout.addWidget(table_label)
        
        self.donor_table = QTableWidget()
        self.donor_table.setColumnCount(7)
        self.donor_table.setHorizontalHeaderLabels([
            "ID", "Name", "Blood Type", "Gender", "Date of Birth", "Contact", "Medical History"
        ])
        self.donor_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.donor_table.setSelectionMode(QTableWidget.SingleSelection)
        self.donor_table.setAlternatingRowColors(True)
        self.donor_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.donor_table.setSortingEnabled(True)
        self.donor_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.donor_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.donor_table.setStyleSheet("QTableWidget {gridline-color: #e0e0e0;}")
        self.donor_table.doubleClicked.connect(self.show_edit_dialog)
        
        main_layout.addWidget(self.donor_table)
        
        self.status_label = QLabel("0 donors found")
        self.status_label.setAlignment(Qt.AlignRight)
        main_layout.addWidget(self.status_label)
        
        self.setLayout(main_layout)
    
    def clear_search(self):
        self.search_input.clear()
        
    def load_donors(self, search_term=""):
        query = """
        SELECT Donor_ID, Donor_Name, Donor_BloodType, Donor_Gender, 
               Donor_DOB, Donor_Contact, Donor_MedicalHistory 
        FROM donor
        WHERE Donor_Name LIKE %s OR Donor_Contact LIKE %s
        ORDER BY Donor_Name
        """
        params = (f"%{search_term}%", f"%{search_term}%")
        donors = self.db.execute_query(query, params, fetch=True)
        
        self.donor_table.setRowCount(0)
        for row, donor in enumerate(donors):
            self.donor_table.insertRow(row)
            self.donor_table.setItem(row, 0, QTableWidgetItem(str(donor['Donor_ID'])))
            self.donor_table.setItem(row, 1, QTableWidgetItem(donor['Donor_Name']))
            
            blood_type_item = QTableWidgetItem(donor['Donor_BloodType'])
            blood_color = self.get_blood_type_color(donor['Donor_BloodType'])
            if blood_color:
                blood_type_item.setForeground(blood_color)
                blood_type_item.setFont(QFont("", -1, QFont.Bold))
            self.donor_table.setItem(row, 2, blood_type_item)
            
            self.donor_table.setItem(row, 3, QTableWidgetItem(donor['Donor_Gender']))
            
            dob = donor['Donor_DOB']
            formatted_dob = self.format_date(dob)
            self.donor_table.setItem(row, 4, QTableWidgetItem(formatted_dob))
            
            self.donor_table.setItem(row, 5, QTableWidgetItem(donor['Donor_Contact']))
            self.donor_table.setItem(row, 6, QTableWidgetItem(donor['Donor_MedicalHistory']))
        
        donor_count = self.donor_table.rowCount()
        self.status_label.setText(f"{donor_count} donor{'s' if donor_count != 1 else ''} found")
        
        self.update_button_states()
        
        self.donor_table.itemSelectionChanged.connect(self.update_button_states)
    
    def get_blood_type_color(self, blood_type):
        """Return color for blood type visualization"""
        blood_colors = {
            "A+": Qt.darkRed,
            "A-": Qt.red,
            "B+": Qt.darkBlue,
            "B-": Qt.blue,
            "AB+": Qt.darkMagenta,
            "AB-": Qt.magenta,
            "O+": Qt.darkGreen,
            "O-": Qt.green
        }
        return blood_colors.get(blood_type)
        
    def format_date(self, date_str):
        """Format date for better readability"""
        if not date_str:
            return ""
        parts = date_str.split("-")
        if len(parts) == 3:
            return f"{parts[2]}-{parts[1]}-{parts[0]}"
        return date_str
    
    def update_button_states(self):
        """Enable or disable buttons based on selection state"""
        has_selection = len(self.donor_table.selectedItems()) > 0
        self.edit_button.setEnabled(has_selection)
        self.delete_button.setEnabled(has_selection)
    
    def show_add_dialog(self):
        dialog = DonorDialog(self.db)
        if dialog.exec_():
            self.load_donors(self.search_input.text())
    
    def show_edit_dialog(self):
        selected = self.donor_table.selectedItems()
        if not selected:
            QMessageBox.warning(self, "Warning", "Please select a donor to edit")
            return
            
        row = self.donor_table.currentRow()
        donor_id = int(self.donor_table.item(row, 0).text())
        dialog = DonorDialog(self.db, donor_id)
        if dialog.exec_():
            self.load_donors(self.search_input.text())
    
    def delete_donor(self):
        selected = self.donor_table.selectedItems()
        if not selected:
            QMessageBox.warning(self, "Warning", "Please select a donor to delete")
            return
            
        row = self.donor_table.currentRow()
        donor_id = int(self.donor_table.item(row, 0).text())
        donor_name = self.donor_table.item(row, 1).text()
        
        reply = QMessageBox.question(
            self, 'Confirm Delete',
            f"Are you sure you want to delete donor '{donor_name}' (ID: {donor_id})?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            query = "DELETE FROM donor WHERE Donor_ID = %s"
            result = self.db.execute_query(query, (donor_id,))
            if result:
                QMessageBox.information(self, "Success", f"Donor '{donor_name}' deleted successfully")
                self.load_donors(self.search_input.text())
            else:
                QMessageBox.warning(self, "Error", "Failed to delete donor")