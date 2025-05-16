from validators import Validators
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QFormLayout, 
                            QLineEdit, QComboBox, QDateEdit, QPushButton, 
                            QLabel, QMessageBox, QGroupBox, QFrame, QSpacerItem,
                            QSizePolicy)
from PyQt5.QtCore import QDate, Qt
from PyQt5.QtGui import QFont, QIcon

class DonorDialog(QDialog):
    def __init__(self, db, donor_id=None):
        super().__init__()
        self.db = db
        self.donor_id = donor_id
        self.setWindowTitle("Add Donor" if not donor_id else "Edit Donor")
        self.setModal(True)
        self.setMinimumWidth(500)
        self.setMinimumHeight(400)
        
        self.init_ui()
        if donor_id:
            self.load_donor_data()
    
    def init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)
        
        # Title
        title_label = QLabel(self.windowTitle())
        title_label.setProperty("cssClass", "title")
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)
        
        # Separator
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        main_layout.addWidget(line)
        
        # Group box for personal info
        personal_group = QGroupBox("Personal Information")
        personal_layout = QFormLayout()
        personal_layout.setSpacing(10)
        personal_layout.setLabelAlignment(Qt.AlignRight)
        
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter full name")
        
        self.gender_combo = QComboBox()
        self.gender_combo.addItems(["Male", "Female", "Other"])
        
        self.dob_input = QDateEdit()
        self.dob_input.setCalendarPopup(True)
        self.dob_input.setMaximumDate(QDate.currentDate())
        self.dob_input.setDisplayFormat("dd-MM-yyyy")
        
        self.contact_input = QLineEdit()
        self.contact_input.setPlaceholderText("Phone number")
        
        personal_layout.addRow("Name:", self.name_input)
        personal_layout.addRow("Gender:", self.gender_combo)
        personal_layout.addRow("Date of Birth:", self.dob_input)
        personal_layout.addRow("Contact:", self.contact_input)
        
        personal_group.setLayout(personal_layout)
        main_layout.addWidget(personal_group)
        
        # Group box for medical info
        medical_group = QGroupBox("Medical Information")
        medical_layout = QFormLayout()
        medical_layout.setSpacing(10)
        medical_layout.setLabelAlignment(Qt.AlignRight)
        
        self.blood_type_combo = QComboBox()
        self.blood_type_combo.addItems(["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"])
        
        self.medical_history_input = QLineEdit()
        self.medical_history_input.setPlaceholderText("Brief medical history (allergies, conditions, etc.)")
        
        medical_layout.addRow("Blood Type:", self.blood_type_combo)
        medical_layout.addRow("Medical History:", self.medical_history_input)
        
        medical_group.setLayout(medical_layout)
        main_layout.addWidget(medical_group)
        
        # Add vertical spacer before buttons
        main_layout.addItem(QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Expanding))
        
        # Button layout
        button_layout = QHBoxLayout()
        
        self.save_button = QPushButton("Save")
        self.save_button.setIcon(QIcon.fromTheme("document-save"))
        self.save_button.clicked.connect(self.save_donor)
        
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.setProperty("cssClass", "secondary")
        self.cancel_button.setIcon(QIcon.fromTheme("dialog-cancel"))
        self.cancel_button.clicked.connect(self.reject)
        
        button_layout.addStretch()
        button_layout.addWidget(self.cancel_button)
        button_layout.addWidget(self.save_button)
        
        main_layout.addLayout(button_layout)
        
        self.setLayout(main_layout)
    
    def load_donor_data(self):
        query = "SELECT * FROM donor WHERE Donor_ID = %s"
        donor = self.db.execute_query(query, (self.donor_id,), fetch=True)
        if donor:
            donor = donor[0]
            self.name_input.setText(donor['Donor_Name'])
            self.blood_type_combo.setCurrentText(donor['Donor_BloodType'])
            self.gender_combo.setCurrentText(donor['Donor_Gender'])
            dob = QDate.fromString(donor['Donor_DOB'], "yyyy-MM-dd")
            self.dob_input.setDate(dob)
            self.contact_input.setText(donor['Donor_Contact'])
            self.medical_history_input.setText(donor['Donor_MedicalHistory'])
    
    def save_donor(self):
        name = self.name_input.text().strip()
        blood_type = self.blood_type_combo.currentText()
        gender = self.gender_combo.currentText()
        dob = self.dob_input.date().toString("yyyy-MM-dd")
        contact = self.contact_input.text().strip()
        medical_history = self.medical_history_input.text().strip()
        
        if not Validators.validate_donor_fields(self, name, contact, dob):
            return
            
        if self.donor_id:
            query = """
            UPDATE donor SET 
                Donor_Name = %s,
                Donor_BloodType = %s,
                Donor_Gender = %s,
                Donor_DOB = %s,
                Donor_Contact = %s,
                Donor_MedicalHistory = %s
            WHERE Donor_ID = %s
            """
            params = (name, blood_type, gender, dob, contact, medical_history, self.donor_id)
        else:  # Insert new donor
            query = """
            INSERT INTO donor 
                (Donor_Name, Donor_BloodType, Donor_Gender, Donor_DOB, Donor_Contact, Donor_MedicalHistory)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            params = (name, blood_type, gender, dob, contact, medical_history)
        
        result = self.db.execute_query(query, params)
        if result:
            QMessageBox.information(self, "Success", "Donor saved successfully")
            self.accept()
        else:
            QMessageBox.warning(self, "Error", "Failed to save donor")