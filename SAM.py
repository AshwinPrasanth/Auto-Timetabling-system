import sys
import pandas as pd
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QTableWidget, QTableWidgetItem, QComboBox, QVBoxLayout, QWidget, QHeaderView,QSizePolicy
from PyQt5.QtCore import Qt 

class AllocationSystem(QMainWindow):
    def __init__(self, course_df, faculty_df):
        super().__init__()

        self.course_df = course_df
        self.faculty_df = faculty_df
        self.selected_faculties = {}

        self.initUI()

    def initUI(self):
        self.setWindowTitle("Allocation System")

        main_widget = QWidget(self)
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)

        self.table = QTableWidget()
        self.table.setRowCount(len(self.course_df))
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["Code","Name","Sem","Sec","Load","Faculty"])

        for i, (Code, Name, Sem,Sec,Load) in enumerate(zip(self.course_df["Code"], self.course_df["Name"], self.course_df["Sem"],self.course_df["Sec"],self.course_df["Load"])):
            self.table.setItem(i, 0, QTableWidgetItem(Code))
            self.table.setItem(i, 1, QTableWidgetItem(Name))
            self.table.setItem(i, 2, QTableWidgetItem(str(Sem)))
            self.table.setItem(i, 3, QTableWidgetItem(Sec))
            self.table.setItem(i, 4,QTableWidgetItem(str(Load)))
            
            combo = QComboBox()
            combo.setMinimumWidth(150)
            for faculty in self.faculty_df["First Name"]:
                if self.faculty_df.loc[self.faculty_df['First Name'] == faculty, 'Numbers'].values[0] > 0:
                    combo.addItem(faculty)
            combo.currentIndexChanged.connect(lambda state, row=i, combo=combo: self.update_selection(row, combo.currentText()))
            self.table.setCellWidget(i, 5, combo)
        
        layout.addWidget(self.table)

        self.done_button = QPushButton('Done', self)
        self.done_button.setMaximumWidth(100)
        self.done_button.clicked.connect(self.save_allocation)
        layout.addWidget(self.done_button, alignment=Qt.AlignCenter)

        self.show()

        # Set size policies
        self.table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def update_selection(self, row, faculty):
        self.selected_faculties[row] = faculty

    def save_allocation(self):
        for row, faculty in self.selected_faculties.items():
            self.course_df.at[row, "Faculty"] = faculty
            current_number = self.faculty_df.loc[self.faculty_df['First Name'] == faculty, 'Numbers'].values[0]
            self.faculty_df.loc[self.faculty_df['First Name'] == faculty, 'Numbers'] = current_number - 1

        self.course_df.to_csv("allocation.csv", index=False)


if __name__ == '__main__':
    course_data = pd.read_csv("timetable.csv")
    if("faculty" not in  list(course_data.columns)):
        course_data["faculty"] = ""
        
    faculty_data = pd.read_csv("faculty.csv")
    faculty_data["Numbers"] = range(1,len(faculty_data["First Name"])+1)
    

    course_df = pd.DataFrame(course_data)
    faculty_df = pd.DataFrame(faculty_data)

    app = QApplication(sys.argv)
    screen = app.primaryScreen()
    screen_size = screen.size()
    window = AllocationSystem(course_df, faculty_df)
    window.setGeometry(0, int(screen_size.height()*0.03), screen_size.width(), int(screen_size.height()*0.95))

    sys.exit(app.exec_())
