import sys
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QHBoxLayout, QComboBox, QTableWidget, QTableWidgetItem, QHeaderView, QSizePolicy,QMainWindow, QStackedWidget
import csv

# Sample Schedule_plan data
import json
import pandas as pd
import csv

def load_json_from_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()

def load_csv_from_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()
with open('timetable1 copy.json', 'r') as file:
    Schedule_plan1= json.load(file)


def generate_schedule(json_data, csv_data, staff_name):
    schedule = {
        staff_name: {
            "monday": {},
            "tuesday": {},
            "wednesday": {},
            "thursday": {},
            "friday": {}
        }
    }

    # Parse JSON data
    json_dict = json.loads(json_data)

    # Extract course codes handled by the staff from CSV data
    staff_courses = []
    csv_lines = csv_data.strip().split('\n')[1:]
    for line in csv_lines:
        values = line.split(',')
        if values[5] == staff_name:
            staff_courses.append((f"{values[0]}_{values[1]}_{values[2]}", values[3]))  # Combine columns 0, 1, and 2

    # Iterate through JSON data to match course identifiers and generate schedule
    for section, section_courses in json_dict.items():
        if section in [course[0] for course in staff_courses]:  # Check if the section matches
            for day, periods in section_courses.items():
                if day != "timeslots":  # Exclude the "timeslots" key
                    for period, course_code in periods.items():
                        if (section, course_code) in staff_courses:  # Check if both section and course code match
                            period_numeric = period_mapping.get(period)  # Get the numeric value for the period
                            if period_numeric is not None and period_numeric < len(section_courses["timeslots"]):
                                next_period_numeric = period_numeric + 1  # Get the numeric value for the next period
                                time_slot = section_courses["timeslots"][next_period_numeric - 1]  # Get the time slot for the next period
                                schedule[staff_name][day][period] = f"{section} {time_slot}"

    return schedule
    
json_file_path = 'timetable1 copy.json'
csv_file_path = 'data_faculty.csv'
json_data = load_json_from_file(json_file_path)

# Load CSV data
csv_data = load_csv_from_file(csv_file_path)

period_mapping = {"one": 0, "two": 1, "three": 2, "four": 3, "five": 4, "six": 5, "seven": 6}

class RoleSelectionApp(QWidget):
    teacher_selected = pyqtSignal()
    student_selected = pyqtSignal()
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        # Calculate button width based on screen width
        button_width = 200

        self.student_button = QPushButton('Student', self)
        self.student_button.setStyleSheet("background-color: #007777; color: white; border: 2px solid #FFD700; border-radius: 15px;")
        self.student_button.setFont(QFont("Arial", 12, QFont.Bold))
        self.student_button.setFixedSize(button_width, 50)  # Set fixed size for the button
        self.student_button.clicked.connect(self.emit_student_selected)
        layout.addWidget(self.student_button)

        self.teacher_button = QPushButton('Teacher', self)
        self.teacher_button.setStyleSheet("background-color: #007777; color: white; border: 2px solid #FFD700; border-radius: 15px;")
        self.teacher_button.setFont(QFont("Arial", 12, QFont.Bold))
        self.teacher_button.setFixedSize(button_width, 50)  # Set fixed size for the button 
        self.teacher_button.clicked.connect(self.emit_teacher_selected)
        layout.addWidget(self.teacher_button)

        self.setLayout(layout)
        self.setWindowTitle('Role Selection')

        # Set window size to full screen (fixed)
        screen_geometry = QApplication.desktop().screenGeometry()
        self.setGeometry(screen_geometry)
        
    def emit_student_selected(self):
        self.student_selected.emit()

    def emit_teacher_selected(self):
        self.teacher_selected.emit()

class TimetableApp(QWidget):
    back_signal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)

        # Add rectangular box on the top of the page
        top_box = QLabel(self)
        top_box.setStyleSheet("background-color: #007777; padding: 10px;")

        # Calculate the height for the top box
        screen_geometry = QApplication.desktop().screenGeometry()
        top_box_height = int(screen_geometry.height() * 0.1)  # Convert to integer

        # Set fixed height for the top box
        top_box.setFixedHeight(top_box_height)

        # Add the dropdown menu for Staff Name
        self.staff_dropdown = QComboBox(self)
        self.staff_dropdown.addItem("Staff Name")
        data_fac = pd.read_csv("data_faculty.csv")
        staff_names = data_fac["Course Handling Staff"].unique().tolist()
        self.staff_dropdown.addItems(staff_names)
        self.staff_dropdown.setStyleSheet("""
            QComboBox {
                background-color: Light blue;
                border: 4px solid #FFD700;
                border-radius: 5px;
                padding: 1px 18px 1px 3px;
                min-width: 6em;
            }
            QComboBox::drop-down {
                background-color: Light blue;
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 20px;
            }
            QComboBox QAbstractItemView {
                border: 2px solid #FFD700;
                selection-background-color: #007777;
            }
        """)

        top_box_layout = QHBoxLayout()
        top_box_layout.addWidget(self.staff_dropdown)
        top_box.setLayout(top_box_layout)
        layout.addWidget(top_box)


        # Add buttons
        buttons_layout = QHBoxLayout()

        # Back button
        self.back_button = QPushButton("Back", self)
        self.back_button.clicked.connect(self.back_to_role_selection)
        self.back_button.setStyleSheet("""
            QPushButton {
                color: white;
                background-color: #007777;
                border: 2px solid #FFD700;
                border-radius: 5px;
                padding: 3px 8px;
                min-width: 100px;
                min-height: 30px;
                font-size: 15px;
            }
        """)
        buttons_layout.addWidget(self.back_button)

        spacer_item = QWidget()
        spacer_item.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        buttons_layout.addWidget(spacer_item)

        # Reset button
        reset_button = QPushButton("Reset", self)
        reset_button.setStyleSheet("""
            QPushButton {
                color: white;
                background-color: #007777;
                border: 2px solid #FFD700;
                border-radius: 5px;
                padding: 3px 8px;
                min-width: 100px;
                min-height: 30px;
                font-size: 15px;
            }
        """)
        reset_button.clicked.connect(self.reset_selection)
        buttons_layout.addWidget(reset_button)

        # Submit button
        submit_button = QPushButton("Submit", self)
        submit_button.setStyleSheet("""
            QPushButton {
                color: white;
                background-color: #007777;
                border: 2px solid #FFD700;
                border-radius: 5px;
                padding: 3px 8px;
                min-width: 100px;
                min-height: 30px;
                font-size: 15px;
            }
        """)
        submit_button.clicked.connect(self.generate_table)
        buttons_layout.addWidget(submit_button)

        layout.addLayout(buttons_layout)
        
        self.table_widget = QTableWidget()
        layout.addWidget(self.table_widget)

        # Set window size to full screen
        screen_geometry = QApplication.desktop().screenGeometry()
        self.setGeometry(screen_geometry)

    def generate_table(self):
        # Clear previous table content
        self.table_widget.clearContents()
        self.table_widget.setRowCount(0)
        self.table_widget.setColumnCount(0)

        # Get selected staff name
        staff_name = self.staff_dropdown.currentText()

        if staff_name != "Staff Name":
            # Call the faculty_timetable function
            timetable = generate_schedule(json_data, csv_data, staff_name)
            timetable=json.dumps(timetable, indent=4)
            timetable = json.loads(timetable)

            days = list(timetable[staff_name].keys())
            time_slots = ["one", "two", "three", "four", "five", "six", "seven"]

            # Set row and column count
            self.table_widget.setRowCount(len(days))
            self.table_widget.setColumnCount(len(time_slots))

            self.table_widget.setHorizontalHeaderLabels(time_slots)
            self.table_widget.setVerticalHeaderLabels(days)

            # Populate the table with timetable data
            for i, day in enumerate(days):
                for j, slot in enumerate(time_slots):
                    value = timetable[staff_name][day].get(slot, "Free")
                    item = QTableWidgetItem(value)
                    item.setForeground(QColor("black"))
                    if value == 'Free':
                        item.setBackground(QColor("#01b170"))
                    else:
                        item.setBackground(QColor("gold"))
                    self.table_widget.setItem(i, j, item)

            # Set stretch factor for columns to make them fill the available width
            for j in range(len(time_slots)):
                self.table_widget.horizontalHeader().setSectionResizeMode(j, QHeaderView.Stretch)

            # Set stretch factor for rows to make them fill the available height
            for i in range(len(days)):
                self.table_widget.verticalHeader().setSectionResizeMode(i, QHeaderView.Stretch)

    def reset_selection(self):
        # Reset staff dropdown to default value
        self.staff_dropdown.setCurrentIndex(0)

    def back_to_role_selection(self):
        self.back_signal.emit()
        self.hide()
st = ""
class FullScreenPage(QWidget):
    back_signal = pyqtSignal()
    def __init__(self):
        super().__init__()
        self.department = ""
        self.semester = ""
        self.section = ""
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)

        # Add rectangular box on the top of the page
        top_box = QLabel(self)
        top_box.setStyleSheet("background-color: #007777; padding: 10px;")

        # Calculate the height for the top box
        screen_geometry = QApplication.desktop().screenGeometry()
        top_box_height = int(screen_geometry.height() * 0.1)  # Convert to integer

        # Set fixed height for the top box
        top_box.setFixedHeight(top_box_height)

        # Add the dropdown menu for Department Name
        self.department_dropdown = QComboBox(self)
        self.department_dropdown.addItem("Department Name")
        self.department_dropdown.currentIndexChanged.connect(self.update_semester_dropdown)
        self.department_dropdown.setStyleSheet("""
            QComboBox {
                background-color: Light blue;
                border: 4px solid #FFD700;
                border-radius: 5px;
                padding: 1px 18px 1px 3px;
                min-width: 6em;
            }
            QComboBox::drop-down {
                background-color: Light blue;
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 20px;
            }
            QComboBox QAbstractItemView {
                border: 2px solid #FFD700;
                selection-background-color: #007777;
            }
        """)

        # Add the dropdown menu for Semester
        self.semester_dropdown = QComboBox(self)
        self.semester_dropdown.addItem("Semester")
        self.semester_dropdown.currentIndexChanged.connect(self.update_section_dropdown)
        self.semester_dropdown.setStyleSheet("""
            QComboBox {
                background-color: Light blue;
                border: 4px solid #FFD700;
                border-radius: 5px;
                padding: 1px 18px 1px 3px;
                min-width: 6em;
            }
            QComboBox::drop-down {
                background-color: Light blue;
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 20px;
            }
            QComboBox QAbstractItemView {
                border: 2px solid #FFD700;
                selection-background-color: #007777;
            }
        """)

        # Add the dropdown menu for Section
        self.section_dropdown = QComboBox(self)
        self.section_dropdown.addItem("Section")
        self.section_dropdown.setStyleSheet("""
            QComboBox {
                background-color: Light blue;
                border: 4px solid #FFD700;
                border-radius: 5px;
                padding: 1px 18px 1px 3px;
                min-width: 6em;
            }
            QComboBox::drop-down {
                background-color: Light blue;
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 20px;
            }
            QComboBox QAbstractItemView {
                border: 2px solid #FFD700;
                selection-background-color: #007777;
            }
        """)

        # Add items to the Department Name dropdown menu
        departments = sorted(set([key.split('_')[0] for key in Schedule_plan1.keys()]))
        self.department_dropdown.addItems(departments)

        # Add the Department Name dropdown menu to a horizontal layout
        hbox = QHBoxLayout()
        hbox.addWidget(self.department_dropdown)
        hbox.addWidget(self.semester_dropdown)
        hbox.addWidget(self.section_dropdown)

        # Set the layout of the top box to the horizontal layout
        top_box.setLayout(hbox)

        # Align the top box to the top of the layout
        layout.addWidget(top_box, alignment=Qt.AlignTop)
        
        back = QPushButton("Back", self)
        back.setStyleSheet("""
            QPushButton {
                color: white; /* Set text color to white */
                background-color: #007777;
                border: 2px solid #FFD700; /* Reduce border width */
                border-radius: 5px;
                padding: 3px 8px; /* Reduce padding */
                min-width: """ + str(screen_geometry.width() * 0.05) + """px;
                min-height: 20px; /* Adjust minimum height */
                font-size: 15px; /* Reduce font size */
            }
        """)

        back.clicked.connect(self.back_to_role_selection)

        back.move(18, 115)

        # Add reset button below the rectangular box
        reset_button = QPushButton("Reset", self)
        reset_button.setStyleSheet("""
            QPushButton {
                color: white; /* Set text color to white */
                background-color: #007777;
                border: 2px solid #FFD700; /* Reduce border width */
                border-radius: 5px;
                padding: 3px 8px; /* Reduce padding */
                min-width: """ + str(screen_geometry.width() * 0.05) + """px;
                min-height: 20px; /* Adjust minimum height */
                font-size: 15px; /* Reduce font size */
            }
        """)

        reset_button.clicked.connect(self.reset_selection)

        reset_button.move(1220, 115)

        submit_button = QPushButton("Submit", self)
        submit_button.setStyleSheet("""
            QPushButton {
                color: white; /* Set text color to white */
                background-color: #007777;
                border: 2px solid #FFD700; /* Reduce border width */
                border-radius: 5px;
                padding: 3px 8px; /* Reduce padding */
                min-width: """ + str(screen_geometry.width() * 0.05) + """px;
                min-height: 20px; /* Adjust minimum height */
                font-size: 15px; /* Reduce font size */
            }
        """)

        submit_button.move(1323, 115)
        submit_button.clicked.connect(self.generate_table)

        # Table widget for timetable
        self.table_widget = QTableWidget()
        layout.addWidget(self.table_widget, alignment=Qt.AlignCenter)
        self.table_widget.move(200, 200)
        self.table_widget.hide()

        # Table widget for second table
        self.second_table_widget = QTableWidget()
        layout.addWidget(self.second_table_widget, alignment=Qt.AlignCenter)
        self.second_table_widget.hide()

        # Set window size to full screen
        screen_geometry = QApplication.desktop().screenGeometry()
        self.setGeometry(screen_geometry)

    def update_semester_dropdown(self, index):
        # Clear previous semester and section dropdowns
        self.semester_dropdown.clear()
        self.section_dropdown.clear()

        # Get selected department
        self.department = self.department_dropdown.currentText()

        # Extract semester values based on the selected department
        semesters = sorted(set([key.split('_')[1] for key in Schedule_plan1.keys() if key.startswith(self.department)]))
        self.semester_dropdown.addItems(semesters)

    def update_section_dropdown(self, index):
        # Clear previous section dropdown
        self.section_dropdown.clear()

        # Get selected department and semester
        self.semester = self.semester_dropdown.currentText()
        # Extract section values based on the selected department and semester
        sections = sorted([key.split('_')[2] for key in Schedule_plan1.keys() if
                           key.startswith(self.department + '_' + self.semester)])
        self.section_dropdown.addItems(sections)

    def reset_selection(self):
        # Reset all dropdowns to default values
        self.department_dropdown.setCurrentIndex(0)
        self.semester_dropdown.clear()
        self.semester_dropdown.addItem("Semester")
        self.section_dropdown.clear()
        self.section_dropdown.addItem("Section")

    def generate_table(self):
        # Generate and display the timetable table
        self.section= self.section_dropdown.currentText()
        self.st = self.department + "_" + self.semester + "_" + self.section
        print(self.st)
        timetable = Schedule_plan1[self.st]

        self.populate_table(self.table_widget, timetable)
        self.table_widget.show()
        table_size = self.table_widget.size()  # Get the size of the first table
        print(table_size)
        # Generate and display the second table
        self.generate_second_table(table_size)

    def populate_table(self, table_widget, timetable):
        time_slots1 = Schedule_plan1[self.st]["timeslots"]
        if "timeslots" in Schedule_plan1[self.st]:   
          del Schedule_plan1[self.st]["timeslots"]
        days =(list(outer_value for outer_value in Schedule_plan1[self.st]))
        first_staff_schedule = next(iter(Schedule_plan1.values())) 
        first_day = next(iter(first_staff_schedule))
        time_slots = list(first_staff_schedule[first_day].keys())
        
        table_widget.setRowCount(len(days))
        table_widget.setColumnCount(len(time_slots))

        table_widget.setHorizontalHeaderLabels(time_slots1)
        table_widget.setVerticalHeaderLabels(days)

        # Set stretch factor for columns to make them fill the available width
        for j in range(len(time_slots)):
            table_widget.horizontalHeader().setSectionResizeMode(j, QHeaderView.Stretch)

        # Set stretch factor for rows to make them fill the available height
        for i in range(len(days)):
            table_widget.verticalHeader().setSectionResizeMode(i, QHeaderView.Stretch)

        for i, day in enumerate(days):
            for j, slot in enumerate(time_slots):
                value = timetable[day.lower()][slot]
                item = QTableWidgetItem(value)
                item.setForeground(QColor("white")) 
                if value == 'CBCS':
                    item.setBackground(QColor("#8d488d"))  
                elif value == 'LUNCH':
                    item.setBackground(QColor("#d60000"))
                elif value == 'BREAK':
                    item.setBackground(QColor("#01b170"))
                else:
                    item.setBackground(QColor("#3585e8"))
                table_widget.setItem(i, j, item)
        table_widget.setFixedSize(900, 350)
    

    def generate_second_table(self, table_size):
        data = self.load_data_from_csv()
        filtered_data = self.filter_data(data)
        self.populate_second_table(filtered_data, table_size)
        self.second_table_widget.show()

    def load_data_from_csv(self):
        data = []
        with open('data_faculty.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                data.append(row)
        return data

    def filter_data(self, data):
        filtered_data = [row for row in data if row['Dept'] == self.department
                         and row['Semester'] == self.semester
                         and row['Section'] == self.section]
        return filtered_data

    def populate_second_table(self, filtered_data, table_size):
        self.second_table_widget.clear()
        self.second_table_widget.setRowCount(len(filtered_data))
        self.second_table_widget.setColumnCount(4)
        column_labels = ['Course Code', 'Name of Course', 'Course Handling Staff', 'Course Type']
        self.second_table_widget.setHorizontalHeaderLabels(column_labels)
        column_width = table_size.width() // 4

        for i in range(4):
            self.second_table_widget.setColumnWidth(i, column_width)

        for i, row in enumerate(filtered_data):
            self.second_table_widget.setVerticalHeaderItem(i, QTableWidgetItem(str(i + 1)))  
            for j, key in enumerate(['Course Code', 'Name of the Course', 'Course Handling Staff', 'Course Type']):
                value = row.get(key, '')
                item = QTableWidgetItem(value)
                self.second_table_widget.setItem(i, j, item)
        row_height = table_size.height() // len(filtered_data)

        for i in range(len(filtered_data)):
            self.second_table_widget.setRowHeight(i, row_height)
        self.second_table_widget.setFixedSize(table_size)
    
    def back_to_role_selection(self):
        self.back_signal.emit()
        self.hide()

class Controller(QMainWindow):
    def __init__(self):
        super().__init__()

        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        self.role_selection_app = RoleSelectionApp()
        self.role_selection_app.teacher_selected.connect(self.show_timetable)
        self.role_selection_app.student_selected.connect(self.show_Student)
        
        self.student_app = FullScreenPage()
        self.student_app.back_signal.connect(self.show_role_selection)
        

        self.timetable_app = TimetableApp()
        self.timetable_app.back_signal.connect(self.show_role_selection)

        self.stacked_widget.addWidget(self.role_selection_app)
        self.stacked_widget.addWidget(self.timetable_app)
        self.stacked_widget.addWidget(self.student_app)
        self.stacked_widget.setCurrentWidget(self.role_selection_app)
        screen_geometry = QApplication.desktop().screenGeometry()
        self.setGeometry(screen_geometry)
        self.showFullScreen()

    def show_role_selection(self):
        self.stacked_widget.setCurrentWidget(self.role_selection_app)

    def show_timetable(self):
        self.stacked_widget.setCurrentWidget(self.timetable_app)
    
    def show_Student(self):
        self.stacked_widget.setCurrentWidget(self.student_app)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    controller = Controller()
    sys.exit(app.exec_())
