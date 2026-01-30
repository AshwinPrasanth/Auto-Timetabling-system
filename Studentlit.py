import json
with open('timetable1.json', 'r') as file:
    Schedule_plan= json.load(file)
import pandas as pd
import streamlit as st
import csv

def main():
    st.title("Demo School")
    st.sidebar.write("Select Department, Semester, and Section to generate the timetable.")

    department_options = [""] + sorted(set([key.split('_')[0] for key in Schedule_plan.keys()]))
    department = st.sidebar.selectbox("Department Name", department_options)

    semester_options = [""] + sorted(set([key.split('_')[1] for key in Schedule_plan.keys() if key.startswith(department)]))
    semester = st.sidebar.selectbox("Semester", semester_options)

    section_options = [""] + sorted([key.split('_')[2] for key in Schedule_plan.keys() if key.startswith(department + '_' + semester)])
    section = st.sidebar.selectbox("Section", section_options)

    if st.sidebar.button("Submit"):
        if department and semester and section:
            generate_timetable_display(department, semester, section)
            display_course_details(department, semester, section)

def display_course_details(department, semester, section):
    st.subheader("Course Details:")
    # Load data from CSV file
    data = load_data_from_csv()
    # Filter data based on user selection
    filtered_data = filter_data(data, department, semester, section)
    if filtered_data:
        # Extract only the required columns
        selected_columns = ['Course Code', 'Name of the Course', 'Course Handling Staff', 'Course Type']
        filtered_data_selected = [{key: row[key] for key in selected_columns} for row in filtered_data]
        df_filtered = pd.DataFrame(filtered_data_selected)
        
        # Add golden outline to table gridlines
        st.markdown(
            """
            <style>
            /* Define golden color */
            .golden-table {
                border-collapse: collapse;
                border: 3px solid #DAA520;
                width: 100%;
            }
            .golden-table th, .golden-table td {
                border: 2px solid #DAA520;
                padding: 8px;
                text-align: left;
            }
            </style>
            """
            , unsafe_allow_html=True
        )
        
        # Display DataFrame as HTML with golden outline
        st.write(df_filtered.to_html(index=False, classes='golden-table'), unsafe_allow_html=True)
    else:
        st.write("No course details available for the selected options.")

def generate_timetable_display(department, semester, section):
    st.subheader("Timetable:")
    timetable = Schedule_plan.get(f"{department}_{semester}_{section}")
    time_slots = timetable.pop("timeslots")
    df_data = []
    for day, subjects in timetable.items():
        df_data.append([day] + list(subjects.values()))
    columns = ["Time Slot"] + time_slots
    df = pd.DataFrame(df_data, columns=columns)
    df.set_index("Time Slot", inplace=True)

    # Define CSS classes for different cell content
    def apply_styles(val):
        if val == 'CBCS':
            return 'background-color: #D7BC14; color: white;'
        elif val in ['LUNCH', 'BREAK']:
            return 'background-color: #F54040; color: white;'
        else:
            return 'background-color: #21B84A; color:white;'

    # Apply styles to DataFrame
    styled_df = df.style.applymap(apply_styles)
    styled_df.set_table_styles([{'selector': 'table', 'props': [('border-collapse', 'collapse'), ('border', '3px solid #DAA520')]}])

    # Write styled DataFrame to Streamlit
    st.write(styled_df)








def load_data_from_csv():
    data = []
    with open('data_faculty.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            data.append(row)
    return data

def filter_data(data, department, semester, section):
    return [row for row in data if row['Dept'] == department
            and row['Semester'] == semester
            and row['Section'] == section]

if __name__ == '__main__':
    main()