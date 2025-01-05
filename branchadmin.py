import streamlit as st
import sqlite3

def get_connection():
    """Establish a database connection."""
    return sqlite3.connect("database.db")

# Utility functions for fetching branches
def get_branches():
    """Fetch all branches from the database."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT branch_id, branch_name FROM branch")
    branches = cursor.fetchall()
    conn.close()
    return branches

# BranchAdmin Dashboard
def branchadmin_dashboard():
    """BranchAdmin Dashboard for managing teachers and classes/sections."""
    st.sidebar.title("Navigation")
    st.sidebar.subheader("Manage Dashboard Sections")

    options = ["Dashboard","Manage Classes and Sections","Manage Teachers"]
    choice = st.sidebar.radio("Select an option", options)

    branches = get_branches()
    if not branches:
        st.warning("No branches found.")
        return

    selected_branch = st.sidebar.selectbox("Select Branch", [branch[1] for branch in branches])
    branch_id = next(branch[0] for branch in branches if branch[1] == selected_branch)

    st.title("BranchAdmin Dashboard")

    if choice == "Dashboard":
        # Import the manage_classes_sections functionality
        from branch_dashboard import display_branch_dashboard
        display_branch_dashboard(branch_id)

    elif choice == "Manage Classes and Sections":
        # Import the manage_classes_sections functionality
        from manage_sections_classes import manage_sections_classes
        manage_sections_classes()

    elif choice == "Manage Teachers":
        # Import the manage_teachers functionality from manage_teachers.py
        from manage_teachers import manage_teachers
        manage_teachers(branch_id)

    
    

def main():
    branchadmin_dashboard()

if __name__ == "__main__":
    main()















