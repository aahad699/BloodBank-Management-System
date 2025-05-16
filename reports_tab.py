from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QComboBox, 
                            QPushButton, QLabel, QTableWidget, QTableWidgetItem,
                            QGroupBox, QFormLayout, QSpacerItem, QSizePolicy, QFrame)
from PyQt5.QtChart import QChart, QChartView, QBarSeries, QBarSet, QBarCategoryAxis, QValueAxis, QPieSeries, QPieSlice
from PyQt5.QtGui import QPainter, QColor, QFont
from PyQt5.QtCore import Qt, QMargins
from datetime import datetime

class ReportsTab(QWidget):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.current_chart = None
        self.init_ui()
        
    def init_ui(self):
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.layout.setSpacing(15)
        
        title_label = QLabel("Blood Bank Reports")
        title_label.setProperty("cssClass", "title")
        self.layout.addWidget(title_label)
        
        description = QLabel("Generate visual reports and analytics about donations, inventory, and more.")
        description.setProperty("cssClass", "subtitle")
        self.layout.addWidget(description)
        
        controls_group = QGroupBox("Report Options")
        control_layout = QFormLayout()
        
        self.report_combo = QComboBox()
        self.report_combo.addItems([
            "Blood Type Distribution",
            "Monthly Donations",
            "Inventory Status",
            "Expiring Soon",
            "Donation Trends"
        ])
        
        self.generate_btn = QPushButton("Generate Report")
        self.generate_btn.clicked.connect(self.generate_report)
        
        control_layout.addRow("Select Report:", self.report_combo)
        control_layout.addRow("", self.generate_btn)
        controls_group.setLayout(control_layout)
        
        self.layout.addWidget(controls_group)
        
        # Separator
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        self.layout.addWidget(line)
        
        # Report title section
        self.report_title = QLabel("")
        self.report_title.setProperty("cssClass", "title")
        self.report_title.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.report_title)
        
        self.display_area = QWidget()
        self.display_layout = QVBoxLayout()
        self.display_area.setLayout(self.display_layout)
        
        self.layout.addWidget(self.display_area)
        
        self.status_label = QLabel("Ready")
        self.layout.addWidget(self.status_label)
        
        self.setLayout(self.layout)
    
    def generate_report(self):
        for i in reversed(range(self.display_layout.count())): 
            widget = self.display_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)
        
        report_type = self.report_combo.currentText()
        self.report_title.setText(report_type)
        
        try:
            if report_type == "Blood Type Distribution":
                self.show_blood_type_distribution()
            elif report_type == "Monthly Donations":
                self.show_monthly_donations()
            elif report_type == "Inventory Status":
                self.show_inventory_status()
            elif report_type == "Expiring Soon":
                self.show_expiring_soon()
            elif report_type == "Donation Trends":
                self.show_donation_trends()
                
            self.status_label.setText(f"Report generated: {report_type}")
        except Exception as e:
            self.status_label.setText(f"Error generating report: {str(e)}")
            self.show_no_data_message(f"Error: {str(e)}")
    
    def show_blood_type_distribution(self):
        query = """
        SELECT 
            d.Donor_BloodType as blood_type,
            COUNT(*) as count
        FROM donor d
        GROUP BY d.Donor_BloodType
        ORDER BY count DESC
        """
        data = self.db.execute_query(query, fetch=True)
        
        if not data:
            self.show_no_data_message()
            return
        
        description = QLabel("Distribution of donors by blood type")
        description.setProperty("cssClass", "subtitle")
        description.setAlignment(Qt.AlignCenter)
        self.display_layout.addWidget(description)
            
        chart = QChart()
        chart.setTitle("Blood Type Distribution")
        chart.setAnimationOptions(QChart.SeriesAnimations)
        chart.setBackgroundVisible(False)
        chart.setMargins(QMargins(10, 10, 10, 10))
        
        series = QPieSeries()
        
        blood_type_colors = {
            "A+": QColor("#e74c3c"),
            "A-": QColor("#c0392b"),
            "B+": QColor("#3498db"),
            "B-": QColor("#2980b9"),
            "AB+": QColor("#9b59b6"),
            "AB-": QColor("#8e44ad"),
            "O+": QColor("#2ecc71"), 
            "O-": QColor("#27ae60")
        }
        
        for i, item in enumerate(data):
            slice = series.append(f"{item['blood_type']} ({item['count']})", item['count'])
            if item['blood_type'] in blood_type_colors:
                slice.setColor(blood_type_colors[item['blood_type']])
            slice.setLabelVisible(True)
            slice.setLabelPosition(QPieSlice.LabelOutside)
            slice.setExploded(True)
            slice.setExplodeDistanceFactor(0.05)
        
        chart.addSeries(series)
        chart.legend().setVisible(True)
        chart.legend().setAlignment(Qt.AlignRight)
        
        chart_view = QChartView(chart)
        chart_view.setRenderHint(QPainter.Antialiasing)
        chart_view.setMinimumHeight(400)
        
        self.display_layout.addWidget(chart_view)
    
    def show_monthly_donations(self):
        query = """
        SELECT 
            DATE_FORMAT(STR_TO_DATE(Donation_Date, '%%Y-%%m-%%d'), '%%Y-%%m') as month,
            SUM(`Quantity_Donated (BloodBags)`) as total
        FROM blood_donations
        WHERE Donation_Date >= DATE_SUB(CURDATE(), INTERVAL 12 MONTH)
        GROUP BY month
        ORDER BY month
        """
        data = self.db.execute_query(query, fetch=True)
        
        if not data:
            self.show_no_data_message()
            return
            
        description = QLabel("Total blood donations over the last 12 months")
        description.setProperty("cssClass", "subtitle")
        description.setAlignment(Qt.AlignCenter)
        self.display_layout.addWidget(description)
            
        chart = QChart()
        chart.setTitle("Monthly Donations (Last 12 Months)")
        chart.setAnimationOptions(QChart.SeriesAnimations)
        chart.setBackgroundVisible(False)
        
        series = QBarSeries()
        bar_set = QBarSet("Donations")
        bar_set.setColor(QColor("#c0392b"))
        
        categories = []
        for item in data:
            bar_set.append(item['total'])
            try:
                date_obj = datetime.strptime(item['month'], '%Y-%m')
                formatted_month = date_obj.strftime('%b %Y')
                categories.append(formatted_month)
            except ValueError:
                categories.append(item['month'])
        
        series.append(bar_set)
        chart.addSeries(series)
        
        axis_x = QBarCategoryAxis()
        axis_x.append(categories)
        chart.addAxis(axis_x, Qt.AlignBottom)
        series.attachAxis(axis_x)
        
        axis_y = QValueAxis()
        max_value = max(float(item['total']) for item in data) if data else 0
        axis_y.setRange(0, max_value * 1.1)
        axis_y.setTitleText("Blood Bags")
        chart.addAxis(axis_y, Qt.AlignLeft)
        series.attachAxis(axis_y)
        
        chart_view = QChartView(chart)
        chart_view.setRenderHint(QPainter.Antialiasing)
        chart_view.setMinimumHeight(400)
        
        self.display_layout.addWidget(chart_view)
    
    def show_inventory_status(self):
        query = """
        SELECT 
            bb.BB_Name as blood_bank,
            bc.Blood_Type,
            SUM(i.`Quantity_Available (BloodBag)`) as quantity,
            CASE 
                WHEN i.Expiration_Date < CURDATE() THEN 'Expired'
                WHEN DATEDIFF(i.Expiration_Date, CURDATE()) <= 7 THEN 'Expiring Soon'
                ELSE 'Good'
            END AS status
        FROM inventory i
        JOIN blood_bank bb ON i.BloodBank_ID = bb.BloodBank_ID
        JOIN blood_component bc ON i.Componnet_ID = bc.Component_ID
        GROUP BY bb.BB_Name, bc.Blood_Type, status
        """
        data = self.db.execute_query(query, fetch=True)
        
        if not data:
            self.show_no_data_message()
            return
        
        description = QLabel("Current inventory status across all blood banks")
        description.setProperty("cssClass", "subtitle")
        description.setAlignment(Qt.AlignCenter)
        self.display_layout.addWidget(description)
            
        table = QTableWidget()
        table.setColumnCount(4)
        table.setHorizontalHeaderLabels(["Blood Bank", "Blood Type", "Quantity", "Status"])
        table.setRowCount(len(data))
        table.setAlternatingRowColors(True)
        
        for row, item in enumerate(data):
            table.setItem(row, 0, QTableWidgetItem(item['blood_bank']))
            table.setItem(row, 1, QTableWidgetItem(item['Blood_Type']))
            table.setItem(row, 2, QTableWidgetItem(str(item['quantity'])))
            status_item = QTableWidgetItem(item['status'])
            
            if item['status'] == 'Expired':
                status_item.setBackground(QColor(255, 150, 150))  # Light red
            elif item['status'] == 'Expiring Soon':
                status_item.setBackground(QColor(255, 255, 150))  # Light yellow
            else:
                status_item.setBackground(QColor(200, 255, 200))  # Light green
            
            table.setItem(row, 3, status_item)
        
        table.resizeColumnsToContents()
        table.setMinimumHeight(300)
        self.display_layout.addWidget(table)
    
    def show_expiring_soon(self):
        query = """
        SELECT 
            i.Inventory_ID,
            bb.BB_Name as blood_bank,
            bc.Blood_Type,
            bc.Component_Type,
            i.`Quantity_Available (BloodBag)`,
            i.Expiration_Date,
            DATEDIFF(i.Expiration_Date, CURDATE()) as days_remaining
        FROM inventory i
        JOIN blood_bank bb ON i.BloodBank_ID = bb.BloodBank_ID
        JOIN blood_component bc ON i.Componnet_ID = bc.Component_ID
        WHERE i.Expiration_Date BETWEEN CURDATE() AND DATE_ADD(CURDATE(), INTERVAL 14 DAY)
        ORDER BY i.Expiration_Date
        """
        data = self.db.execute_query(query, fetch=True)
        
        if not data:
            self.show_no_data_message()
            return
        
        warning_label = QLabel("⚠️ ATTENTION: These items will expire within the next 14 days")
        warning_label.setProperty("cssClass", "subtitle")
        warning_label.setAlignment(Qt.AlignCenter)
        warning_label.setStyleSheet("color: #e74c3c; font-weight: bold;")
        self.display_layout.addWidget(warning_label)
            
        table = QTableWidget()
        table.setColumnCount(6)
        table.setHorizontalHeaderLabels(["ID", "Blood Bank", "Blood Type", "Component", "Quantity", "Expires In"])
        table.setRowCount(len(data))
        table.setAlternatingRowColors(True)
        
        for row, item in enumerate(data):
            table.setItem(row, 0, QTableWidgetItem(str(item['Inventory_ID'])))
            table.setItem(row, 1, QTableWidgetItem(item['blood_bank']))
            table.setItem(row, 2, QTableWidgetItem(item['Blood_Type']))
            table.setItem(row, 3, QTableWidgetItem(item['Component_Type']))
            table.setItem(row, 4, QTableWidgetItem(str(item['Quantity_Available (BloodBag)'])))
            
            days_item = QTableWidgetItem(f"{item['days_remaining']} days")
            if item['days_remaining'] <= 3:
                days_item.setForeground(QColor(255, 0, 0))
                days_item.setBackground(QColor(255, 200, 200))
                days_item.setFont(QFont("Arial", 9, QFont.Bold))
            elif item['days_remaining'] <= 7:
                days_item.setBackground(QColor(255, 255, 200))
            table.setItem(row, 5, days_item)
        
        table.resizeColumnsToContents()
        table.setMinimumHeight(300)
        self.display_layout.addWidget(table)
        
        action_layout = QHBoxLayout()
        
        notify_btn = QPushButton("Send Notifications")
        notify_btn.setProperty("cssClass", "danger")
        
        transfer_btn = QPushButton("Plan Transfers")
        transfer_btn.setProperty("cssClass", "secondary")
        
        print_btn = QPushButton("Print Report")
        
        action_layout.addWidget(notify_btn)
        action_layout.addWidget(transfer_btn)
        action_layout.addWidget(print_btn)
        
        self.display_layout.addLayout(action_layout)
    
    def show_donation_trends(self):
        query = """
        SELECT 
            d.Donor_BloodType,
            COUNT(*) as donation_count,
            SUM(bd.`Quantity_Donated (BloodBags)`) as total_quantity
        FROM blood_donations bd
        JOIN donor d ON bd.Donor_ID = d.Donor_ID
        WHERE bd.Donation_Date >= DATE_SUB(CURDATE(), INTERVAL 6 MONTH)
        GROUP BY d.Donor_BloodType
        ORDER BY total_quantity DESC
        """
        data = self.db.execute_query(query, fetch=True)
        
        if not data:
            self.show_no_data_message()
            return
        
        description = QLabel("Donation trends by blood type over the last 6 months")
        description.setProperty("cssClass", "subtitle")
        description.setAlignment(Qt.AlignCenter)
        self.display_layout.addWidget(description)
        
        chart = QChart()
        chart.setTitle("Donation Trends by Blood Type (Last 6 Months)")
        chart.setAnimationOptions(QChart.SeriesAnimations)
        chart.setBackgroundVisible(False)
        
        series = QBarSeries()
        
        count_set = QBarSet("Donation Count")
        count_set.setColor(QColor("#2980b9"))  # Blue
        
        quantity_set = QBarSet("Total Quantity")
        quantity_set.setColor(QColor("#c0392b"))  # Red
        
        categories = []
        for item in data:
            count_set.append(float(item['donation_count']))
            quantity_set.append(float(item['total_quantity']))
            categories.append(item['Donor_BloodType'])
        
        series.append(count_set)
        series.append(quantity_set)
        chart.addSeries(series)
        
        axis_x = QBarCategoryAxis()
        axis_x.append(categories)
        chart.addAxis(axis_x, Qt.AlignBottom)
        series.attachAxis(axis_x)
        
        axis_y = QValueAxis()
        max_value = max(max(float(item['donation_count']) for item in data), 
                    max(float(item['total_quantity']) for item in data))
        axis_y.setRange(0, max_value * 1.2)
        chart.addAxis(axis_y, Qt.AlignLeft)
        series.attachAxis(axis_y)
        
        chart.legend().setVisible(True)
        chart.legend().setAlignment(Qt.AlignBottom)
        
        chart_view = QChartView(chart)
        chart_view.setRenderHint(QPainter.Antialiasing)
        chart_view.setMinimumHeight(400)
        
        self.display_layout.addWidget(chart_view)
        
        total_donations = sum(float(item['donation_count']) for item in data)
        total_quantity = sum(float(item['total_quantity']) for item in data)
        
        summary_label = QLabel(f"Summary: {int(total_donations)} donations totaling {int(total_quantity)} blood bags")
        summary_label.setAlignment(Qt.AlignCenter)
        summary_label.setStyleSheet("font-weight: bold; margin-top: 10px;")
        self.display_layout.addWidget(summary_label)

    def show_no_data_message(self, message="No data available for this report."):
        label = QLabel(message)
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("color: #6c757d; font-size: 16px; padding: 40px;")
        self.display_layout.addWidget(label)
        
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        btn_layout.addStretch()
        
        self.display_layout.addLayout(btn_layout)