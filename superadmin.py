import streamlit as st
import sqlite3
import pandas as pd
from dashboard import display_overall_stats, display_branch_stats
from manage_branches import create_branch_form, display_existing_branches, create_branch_admin_form
from manage_subjects import manage_subjects
from branch_dashboard import display_branch_dashboard
from student_dashboard import main as display_student_dashboard  # Import the Student Dashboard

# Connect to the database and fetch data
def get_data():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    
    # Overall statistics
    total_branches = cursor.execute("SELECT COUNT(*) FROM branch").fetchone()[0]
    total_teachers = cursor.execute("SELECT COUNT(*) FROM teachers").fetchone()[0]
    total_students = cursor.execute("SELECT COUNT(*) FROM student").fetchone()[0]
    total_subjects = cursor.execute("SELECT COUNT(*) FROM subject").fetchone()[0]
    
    query = """
    SELECT 
        b.branch_id, b.branch_name,
        COUNT(DISTINCT s.student_id) AS students,
        COUNT(DISTINCT t.teacher_id) AS teachers,
        COUNT(DISTINCT c.class_id) AS classes,
        COUNT(DISTINCT sec.section_id) AS sections,
        AVG(COALESCE(scores.math, 0)) AS math_avg,
        AVG(COALESCE(scores.science, 0)) AS science_avg
    FROM branch b
    LEFT JOIN class c ON b.branch_id = c.branch_id
    LEFT JOIN section sec ON c.class_id = sec.class_id
    LEFT JOIN student s ON sec.section_id = s.section_id
    LEFT JOIN teachers t ON b.branch_id = t.branch_id
    LEFT JOIN scores ON s.student_id = scores.student_id
    GROUP BY b.branch_name
    """
    branch_stats = pd.read_sql_query(query, conn)
    
    conn.close()
    return total_branches, total_teachers, total_students, total_subjects, branch_stats

# Fetch data
total_branches, total_teachers, total_students, total_subjects, branch_stats = get_data()

# Streamlit App Layout
def superadmin_dashboards():
    st.title("Super Admin Dashboard")
    st.sidebar.title("SuperAdmin Dashboard")  # Sidebar title
    options = ["Dashboard", "Manage Branches", "Branch Dashboard", "Manage Subjects", "Student Dashboard"]
    choice = st.sidebar.radio("Dashboard Options", options)

    if choice == "Dashboard":
        # Display overall and branch-wise statistics
        display_overall_stats(total_branches, total_teachers, total_students, total_subjects)
        display_branch_stats(branch_stats)

    elif choice == "Manage Branches":
        manage_choice = st.sidebar.radio("Manage Branch Options", ["Create Branch", "Create Branch Admin", "View Existing Branches"])

        if manage_choice == "Create Branch":
            create_branch_form()

        elif manage_choice == "Create Branch Admin":
            create_branch_admin_form()

        elif manage_choice == "View Existing Branches":
            display_existing_branches()

    elif choice == "Manage Subjects":
        manage_subjects()

    elif choice == "Branch Dashboard":
        # Add branch selection for the Super Admin
        branch_names = [branch["branch_name"] for branch in branch_stats.to_dict("records")]
        branch_ids = [branch["branch_id"] for branch in branch_stats.to_dict("records")]
        
        selected_branch_name = st.selectbox("Select Branch", branch_names)
        selected_branch_id = branch_ids[branch_names.index(selected_branch_name)]

        # Pass the selected branch ID to display_branch_dashboard
        display_branch_dashboard(selected_branch_id)

    elif choice == "Student Dashboard":
        # Directly call the Student Dashboard's main function
        display_student_dashboard()

    st.session_state.current_page = choice

if __name__ == "__main__":
    superadmin_dashboards()
