import streamlit as st
import pandas as pd
import plotly.express as px
import random

# Sample Data for Branches
branch_data = {
    1: {"name": "Branch 1", "students": 200, "chapters": 100, "topics": 500, "subjects": 10},
    2: {"name": "Branch 2", "students": 150, "chapters": 80, "topics": 400, "subjects": 8},
    3: {"name": "Branch 3", "students": 180, "chapters": 90, "topics": 450, "subjects": 9},
}

# Generate Performance Data Dynamically
def generate_performance_data():
    subjects = ["Math", "Physics", "Chemistry", "Biology", "English"]
    names = [
        "John Doe", "Jane Smith", "Alex Brown", "Emily Davis", "Michael Johnson", 
        "Sarah Lee", "David Wilson", "Laura Taylor", "Chris White", "Megan Harris", 
        "Tom Clark", "Anna Martin", "James Walker", "Sophia Hall", "Benjamin Allen", 
        "Olivia Young", "Ethan King", "Charlotte Scott", "Daniel Adams", "Grace Nelson"
    ]
    data = []
    for name in names:
        for subject in subjects:
            data.append({
                "student_name": name,
                "subject": subject,
                "score": random.randint(50, 100)
            })
    return data

performance_data = generate_performance_data()

# Fetch Overview Statistics
def fetch_overview_statistics(branch_id):
    if branch_id in branch_data:
        return branch_data[branch_id]
    else:
        st.error(f"Branch ID {branch_id} not found!")
        return {}

# Class and Section-wise Analysis Data
class_section_data = {
    "Class 1": {"Section A": {"students": 30}, "Section B": {"students": 25}},
    "Class 2": {"Section A": {"students": 35}, "Section B": {"students": 20}},
    "Class 3": {"Section A": {"students": 40}, "Section B": {"students": 30}},
}

# Sidebar for Branch and Class Selection
def sidebar_selection():
    branch_options = list(branch_data.keys())
    selected_branch = st.sidebar.selectbox("Select Branch", branch_options)
    class_options = list(class_section_data.keys())
    selected_class = st.sidebar.selectbox("Select Class", class_options)
    selected_section = st.sidebar.selectbox("Select Section", list(class_section_data[selected_class].keys()))
    return selected_branch, selected_class, selected_section

# Overview Section
def display_overview(branch_id):
    branch_info = fetch_overview_statistics(branch_id)
    if not branch_info:
        return

    st.title(f"{branch_info['name']} - Dashboard")
    st.subheader("Overview Statistics")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(label="Total Students", value=branch_info["students"])
    with col2:
        st.metric(label="Total Chapters", value=branch_info["chapters"])
    with col3:
        st.metric(label="Total Topics", value=branch_info["topics"])
    with col4:
        st.metric(label="Total Subjects", value=branch_info["subjects"])

# Class-wise and Section-wise Analysis
def class_section_analysis(selected_class, selected_section):
    st.subheader("Class & Section-wise Analysis")
    data = class_section_data[selected_class][selected_section]
    st.write(f"**Class:** {selected_class}, **Section:** {selected_section}")
    st.metric(label="Students in Section", value=data["students"])

# Performance Analysis by Subject
def performance_analysis():
    st.subheader("Performance Analysis by Subject")
    subject_options = list(set([entry["subject"] for entry in performance_data]))
    selected_subject = st.selectbox("Select Subject", subject_options)

    # Filter data by selected subject
    filtered_data = [entry for entry in performance_data if entry["subject"] == selected_subject]
    df = pd.DataFrame(filtered_data)

    # Visualization
    fig = px.bar(df, x="student_name", y="score", title=f"Performance Analysis - {selected_subject}",
                 labels={"student_name": "Student Name", "score": "Score"}, color="score")
    st.plotly_chart(fig)

# Performance Analysis by Student
def student_progress_tracking():
    st.subheader("Student Progress Tracking")
    student_options = list(set([entry["student_name"] for entry in performance_data]))
    selected_student = st.selectbox("Select Student", student_options)

    # Filter data by selected student
    filtered_data = [entry for entry in performance_data if entry["student_name"] == selected_student]
    df = pd.DataFrame(filtered_data)

    # Visualization
    fig = px.bar(df, x="subject", y="score", title=f"Progress Tracking - {selected_student}",
                 labels={"subject": "Subject", "score": "Score"}, color="score")
    st.plotly_chart(fig)

    return selected_student, filtered_data

# Grade Distribution
def grade_distribution(filtered_data, selected_student):
    st.subheader(f"Grade Distribution for {selected_student}")

    if not filtered_data:
        st.warning("No data available for the selected student.")
        return

    # Compute grades
    grades = []
    for entry in filtered_data:
        score = entry["score"]
        if score >= 90:
            grades.append("A")
        elif score >= 75:
            grades.append("B")
        elif score >= 60:
            grades.append("C")
        else:
            grades.append("D")

    grade_counts = pd.DataFrame({"Grade": grades}).value_counts().reset_index()
    grade_counts.columns = ["Grade", "Count"]

    # Visualization
    fig = px.pie(grade_counts, names="Grade", values="Count", title=f"Grade Distribution - {selected_student}")
    st.plotly_chart(fig)

# Yes/No Visualization (Chapter-wise Summary)
def yes_no_visualization():
    st.subheader("Yes/No Visualization - Chapter Completion")
    chapters = [f"Chapter {i}" for i in range(1, 11)]
    yes_counts = [random.randint(10, 30) for _ in chapters]
    no_counts = [random.randint(0, 10) for _ in chapters]

    data = pd.DataFrame({
        "Chapter": chapters,
        "Completed (Yes)": yes_counts,
        "Not Completed (No)": no_counts
    })

    # Bar Chart Visualization
    fig = px.bar(data, x="Chapter", y=["Completed (Yes)", "Not Completed (No)"], 
                 title="Chapter Completion Summary", barmode="group",
                 labels={"value": "Count", "Chapter": "Chapter Name", "variable": "Status"})
    st.plotly_chart(fig)

# Main Application Logic
def main():
    selected_branch, selected_class, selected_section = sidebar_selection()
    display_overview(selected_branch)
    class_section_analysis(selected_class, selected_section)
    performance_analysis()

    # Track student selection and update visualizations
    selected_student, filtered_data = student_progress_tracking()
    grade_distribution(filtered_data, selected_student)
    yes_no_visualization()

if __name__ == "__main__":
    main()
