import json

# Function to generate JSON file for all teachers
def generate_all_teachers_json(timetable_data, teacher_data):
    all_teachers_schedule = {}
    for teacher, classes in teacher_data.items():
        teacher_schedule = {}
        for class_section, subject in classes.items():
            teacher_schedule[class_section] = {}
            for day, schedule in timetable_data.items():
                teacher_schedule[class_section][day] = {}
                for slot, subj in schedule.items():
                    if subj == subject:
                        teacher_schedule[class_section][day][slot] = subj
        all_teachers_schedule[teacher] = teacher_schedule
    with open('all_teachers_schedule.json', 'w') as json_file:
        json.dump(all_teachers_schedule, json_file, indent=4)

# Timetable data
timetable = {
    "monday": {"one": "ENG", "two": "Pre-Lunch Break", "three": "SOC", "four": "BIO", "five": "Lunch Break", "six": "TAM", "seven": "TAM", "eight": "Post-Lunch Break", "nine": "SOC"},
    "tuesday": {"one": "SOC", "two": "Pre-Lunch Break", "three": "CS", "four": "CS", "five": "Lunch Break", "six": "TAM", "seven": "PHY", "eight": "Post-Lunch Break", "nine": "MAT"},
    "wednesday": {"one": "TAM", "two": "Pre-Lunch Break", "three": "ENG", "four": "MAT", "five": "Lunch Break", "six": "BIO", "seven": "MAT", "eight": "Post-Lunch Break", "nine": "SOC"},
    "thursday": {"one": "BIO", "two": "Pre-Lunch Break", "three": "SOC", "four": "CHE", "five": "Lunch Break", "six": "SOC", "seven": "MAT", "eight": "Post-Lunch Break", "nine": "ENG"},
    "friday": {"one": "CHE", "two": "Pre-Lunch Break", "three": "MAT", "four": "MAT", "five": "Lunch Break", "six": "CHE", "seven": "MAT", "eight": "Post-Lunch Break", "nine": "PHY"},
    "saturday": {"one": "TAM", "two": "Pre-Lunch Break", "three": "SOC", "four": "ENG", "five": "Lunch Break", "six": "ENG", "seven": "PHY", "eight": "Post-Lunch Break", "nine": "SOC"}
}

# Teacher data
teacher_data = {
    "PREM": {"10_A": "BIO", "10_A": "TAM", "10_B": "SOC"},
    "PONRAM": {"10_A": "ENG", "12_A": "ENG"},
    "MANOGARI": {"10_A": "SOC", "10_B": "SOC"},
    "RAMESH": {"10_A": "MAT", "10_C": "MAT"},
    "A": {"10_A": "PHY", "10_B": "PHY", "10_C": "PHY"},
    "B": {"10_A": "CS", "10_B": "CS", "10_C": "CS"},
    "RUBINA": {"10_A": "CHE", "10_B": "CHE", "10_C": "CHE"}
}

# Generate JSON file for all teachers
generate_all_teachers_json(timetable, teacher_data)
