from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, 
                            QTableWidgetItem, QPushButton, QComboBox, QLabel,
                            QGroupBox, QFormLayout, QSpacerItem, QSizePolicy)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor

class InventoryManagementTab(QWidget):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.init_ui()
        self.load_inventory()
        
    def init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)
        
        # Title
        title_label = QLabel("Inventory Management")
        title_label.setProperty("cssClass", "title")
        main_layout.addWidget(title_label)
        
        # Filter Group Box
        filter_group = QGroupBox("Filters")
        filter_layout = QFormLayout()
        filter_layout.setVerticalSpacing(10)
        filter_layout.setHorizontalSpacing(15)
        
        self.blood_bank_combo = QComboBox()
        self.load_blood_banks()
        self.blood_bank_combo.currentIndexChanged.connect(self.load_inventory)
        
        self.blood_type_combo = QComboBox()
        self.blood_type_combo.addItem("All Blood Types", "")
        self.blood_type_combo.addItems(["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"])
        self.blood_type_combo.currentIndexChanged.connect(self.load_inventory)
        
        self.component_combo = QComboBox()
        self.component_combo.addItem("All Components", "")
        self.component_combo.addItems(["Whole Blood", "Plasma", "Platelets", "Red Blood Cells"])
        self.component_combo.currentIndexChanged.connect(self.load_inventory)
        
        filter_layout.addRow("Blood Bank:", self.blood_bank_combo)
        filter_layout.addRow("Blood Type:", self.blood_type_combo)
        filter_layout.addRow("Component:", self.component_combo)
        
        filter_group.setLayout(filter_layout)
        main_layout.addWidget(filter_group)
        
        # Action buttons
        button_layout = QHBoxLayout()
        
        refresh_btn = QPushButton("Refresh")
        refresh_btn.clicked.connect(self.load_inventory)
        
        export_btn = QPushButton("Export Data")
        export_btn.setProperty("cssClass", "secondary")
        
        button_layout.addWidget(refresh_btn)
        button_layout.addWidget(export_btn)
        button_layout.addStretch(1)
        
        main_layout.addLayout(button_layout)
        
        # Inventory table with status indicators
        table_label = QLabel("Current Inventory Status")
        table_label.setProperty("cssClass", "subtitle")
        main_layout.addWidget(table_label)
        
        self.inventory_table = QTableWidget()
        self.inventory_table.setColumnCount(7)
        self.inventory_table.setHorizontalHeaderLabels([
            "ID", "Blood Type", "Component", "Quantity", "Expiration", "Blood Bank", "Status"
        ])
        self.inventory_table.setSortingEnabled(True)
        self.inventory_table.setAlternatingRowColors(True)
        self.inventory_table.setSelectionBehavior(QTableWidget.SelectRows)
        
        # Set stretch for the table
        main_layout.addWidget(self.inventory_table)
        
        # Status bar at the bottom
        status_layout = QHBoxLayout()
        self.status_label = QLabel("Ready")
        status_layout.addWidget(self.status_label)
        main_layout.addLayout(status_layout)
        
        self.setLayout(main_layout)
    
    def load_blood_banks(self):
        query = "SELECT BloodBank_ID, BB_Name FROM blood_bank ORDER BY BB_Name"
        blood_banks = self.db.execute_query(query, fetch=True)
        self.blood_bank_combo.addItem("All Blood Banks", "")
        for bb in blood_banks:
            self.blood_bank_combo.addItem(bb['BB_Name'], bb['BloodBank_ID'])
    
    def load_inventory(self):
        blood_bank_id = self.blood_bank_combo.currentData()
        blood_type = self.blood_type_combo.currentText() if self.blood_type_combo.currentIndex() > 0 else ""
        component_type = self.component_combo.currentText() if self.component_combo.currentIndex() > 0 else ""
        
        query = """
        SELECT 
            i.Inventory_ID, 
            bc.Blood_Type, 
            bc.Component_Type, 
            i.`Quantity_Available (BloodBag)`, 
            i.Expiration_Date,
            bb.BB_Name,
            CASE 
                WHEN i.Expiration_Date < CURDATE() THEN 'Expired'
                WHEN DATEDIFF(i.Expiration_Date, CURDATE()) <= 7 THEN 'Expiring Soon'
                ELSE 'Good'
            END AS Status
        FROM inventory i
        JOIN blood_component bc ON i.Componnet_ID = bc.Component_ID
        JOIN blood_bank bb ON i.BloodBank_ID = bb.BloodBank_ID
        WHERE (%s = '' OR i.BloodBank_ID = %s)
          AND (%s = '' OR bc.Blood_Type = %s)
          AND (%s = '' OR bc.Component_Type = %s)
        ORDER BY i.Expiration_Date
        """
        
        params = (
            "" if blood_bank_id in (None, "") else str(blood_bank_id),
            "" if blood_bank_id in (None, "") else str(blood_bank_id),
            "" if not blood_type else blood_type,
            "" if not blood_type else blood_type,
            "" if not component_type else component_type,
            "" if not component_type else component_type
        )
        
        try:
            inventory = self.db.execute_query(query, params, fetch=True)
            
            self.inventory_table.setRowCount(0)
            for row, item in enumerate(inventory):
                self.inventory_table.insertRow(row)
                self.inventory_table.setItem(row, 0, QTableWidgetItem(str(item['Inventory_ID'])))
                self.inventory_table.setItem(row, 1, QTableWidgetItem(item['Blood_Type']))
                self.inventory_table.setItem(row, 2, QTableWidgetItem(item['Component_Type']))
                self.inventory_table.setItem(row, 3, QTableWidgetItem(str(item['Quantity_Available (BloodBag)'])))
                self.inventory_table.setItem(row, 4, QTableWidgetItem(item['Expiration_Date']))
                self.inventory_table.setItem(row, 5, QTableWidgetItem(item['BB_Name']))
                
                # Create status item with proper styling
                status_item = QTableWidgetItem(item['Status'])
                
                if item['Status'] == 'Expired':
                    status_item.setBackground(QColor(255, 200, 200))  # Light red
                elif item['Status'] == 'Expiring Soon':
                    status_item.setBackground(QColor(255, 255, 200))  # Light yellow
                else:
                    status_item.setBackground(QColor(200, 255, 200))  # Light green
                
                self.inventory_table.setItem(row, 6, status_item)
            
            self.inventory_table.resizeColumnsToContents()
            self.status_label.setText(f"Loaded {len(inventory)} inventory items")
        
        except Exception as e:
            self.status_label.setText(f"Error: {str(e)}")