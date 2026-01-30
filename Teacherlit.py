import streamlit as st
import pandas as pd
import json

def load_json_from_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()

def load_csv_from_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()

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
csv_file_path = 'data_faculty copy.csv'
json_data = load_json_from_file(json_file_path)

# Load CSV data
csv_data = load_csv_from_file(csv_file_path)

period_mapping = {"one": 0, "two": 1, "three": 2, "four": 3, "five": 4, "six": 5, "seven": 6}

# Sidebar options
st.sidebar.header('Select Staff Name')
staff_names = pd.read_csv("data_faculty copy.csv")["Course Handling Staff"].unique().tolist()
staff_name = st.sidebar.selectbox("", ["Select Staff Name"] + staff_names)

if staff_name != "Select Staff Name":
    # Call the generate_schedule function
    timetable = generate_schedule(json_data, csv_data, staff_name)

    st.subheader("Timetable")

    days = list(timetable[staff_name].keys())
    time_slots = ["one", "two", "three", "four", "five", "six", "seven"]

    # Create DataFrame for timetable data
    df = pd.DataFrame(index=days, columns=time_slots)

    # Populate the DataFrame with timetable data
    for day in days:
        for slot in time_slots:
            value = timetable[staff_name][day].get(slot, "Free")
            df.at[day, slot] = value

    # Calculate the maximum width and height of the cell content
    max_width = 200
    max_height = 100  # Adjust as needed

    # Highlight 'Free' slots in green color
    def highlight_free(value):
        return f'background-color: #21B84A; width: {max_width}px; height: {max_height}px;' if value == 'Free' else f'background-color: #D7BC14;width: {max_width}px; height: {max_height}px;'
    
    # Apply the highlight function to the DataFrame
    df_styled = df.style.applymap(highlight_free)

    # Display the styled DataFrame with fixed size, entire table visible, and increased cell width
    table_html = df_styled.to_html()

    styled_table_with_auto_size_and_width = f'<div style="min-width: 850px; min-height: 350px; overflow: auto;">{table_html}</div>'
    st.write(styled_table_with_auto_size_and_width, unsafe_allow_html=True)
