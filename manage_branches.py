import streamlit as st
import sqlite3

# Set page configuration to hide the sidebar
st.set_page_config(page_title="Branch Management", layout="wide", initial_sidebar_state="collapsed")

# Connect to the database
def connect_db():
    conn = sqlite3.connect("database.db")
    return conn

# Create a new branch
def create_branch(branch_name, location, contact_number, subjects):
    conn = connect_db()
    cursor = conn.cursor()

    # Insert branch details into the branch table
    cursor.execute("""
    INSERT INTO branch (branch_name, location, contact_number)
    VALUES (?, ?, ?)
    """, (branch_name, location, contact_number))
    conn.commit()

    # Fetch the last inserted branch id
    branch_id = cursor.lastrowid

    # Insert the selected subjects for the branch
    for subject in subjects:
        cursor.execute("""
        INSERT INTO branch_subject (branch_id, subject_name)
        VALUES (?, ?)
        """, (branch_id, subject))
    conn.commit()

    conn.close()
    st.success("Branch created successfully!")
# Create a new branch admin
def create_branch_admin(admin_name, email, password, branch_id):
    try:
        conn = connect_db()
        cursor = conn.cursor()

        # Insert new branch admin details into the user table (role: 'branchadmin')
        cursor.execute("""
        INSERT INTO user (email, password, name, role, branch_id)
        VALUES (?, ?, ?, 'branchadmin', ?)
        """, (email, password, admin_name, branch_id))
        conn.commit()
        conn.close()
        st.success(f"Branch Admin '{admin_name}' created successfully!")
    except sqlite3.Error as e:
        st.error(f"An error occurred while creating the branch admin: {e}")

# Delete a branch and its associated data
def delete_branch(branch_id):
    try:
        conn = connect_db()
        cursor = conn.cursor()

        # Delete from the branch_subject table
        cursor.execute("DELETE FROM branch_subject WHERE branch_id = ?", (branch_id,))

        # Delete from the user table where role is 'branchadmin'
        cursor.execute("DELETE FROM user WHERE branch_id = ?", (branch_id,))

        # Delete from the branch table
        cursor.execute("DELETE FROM branch WHERE branch_id = ?", (branch_id,))
        conn.commit()

        conn.close()
        st.success(f"Branch with ID '{branch_id}' deleted successfully!")
    except sqlite3.Error as e:
        st.error(f"An error occurred while deleting the branch: {e}")

# Streamlit form to create a new branch
def create_branch_form():
    st.title("Create New Branch")
    with st.form(key="branch_form"):
        branch_name = st.text_input("Branch Name", max_chars=100)
        location = st.text_input("Location", max_chars=100)
        contact_number = st.text_input("Contact Number", max_chars=15)
        all_subjects = ["Mathematics", "Science", "English", "History", "Geography", "Computer Science"]
        subjects = st.multiselect("Select Subjects", options=all_subjects)
        submit_button = st.form_submit_button("Create Branch")

    if submit_button:
        if branch_name and location and contact_number and subjects:
            create_branch(branch_name, location, contact_number, subjects)
        else:
            st.error("Please fill in all the fields.")

# Streamlit form to create a new branch admin
def create_branch_admin_form():
    st.title("Create Branch Admin")
    with st.form(key="branch_admin_form"):
        admin_name = st.text_input("Branch Admin Name", max_chars=100)
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT branch_id, branch_name FROM branch")
        branches = cursor.fetchall()
        branch_names = [branch[1] for branch in branches]
        branch_ids = [branch[0] for branch in branches]
        branch = st.selectbox("Select Branch", options=branch_names, index=0)
        selected_branch_id = branch_ids[branch_names.index(branch)]
        submit_button = st.form_submit_button("Create Branch Admin")

    if submit_button:
        if admin_name and email and password and selected_branch_id:
            create_branch_admin(admin_name, email, password, selected_branch_id)
        else:
            st.error("Please fill in all the fields.")

# Display existing branches and their details
def display_existing_branches():
    try:
        conn = connect_db()
        cursor = conn.cursor()

        # Fetch existing branches and their associated admins
        cursor.execute("""
            SELECT b.branch_name, 
                   COALESCE(u.name, 'No Admin Assigned') AS admin_name, 
                   COALESCE(u.email, 'No Email') AS admin_email, 
                   b.branch_id
            FROM branch b
            LEFT JOIN user u ON b.branch_id = u.branch_id AND u.role = 'branchadmin'
        """)
        branch_admins = cursor.fetchall()

        if branch_admins:
            st.subheader("Existing Branches and Branch Admins")
            for index, (branch_name, admin_name, admin_email, branch_id) in enumerate(branch_admins):
                with st.expander(f"{branch_name} - Admin: {admin_name}"):
                    st.write(f"**Branch Name:** {branch_name}")
                    st.write(f"**Admin Name:** {admin_name}")
                    st.write(f"**Admin Email:** {admin_email}")
                    col1, col2 = st.columns(2)
                    with col1:
                        # Use a unique key by including the index
                        if st.button(f"View Details for Branch: {branch_name}", key=f"details_{branch_id}_{index}"):
                            display_branch_details(branch_id)
                    with col2:
                        # Use a unique key by including the index
                        if st.button(f"Delete: {branch_name}", key=f"delete_{branch_id}_{index}"):
                            delete_branch(branch_id)
        else:
            st.info("No branches or admins found.")
    except sqlite3.Error as e:
        st.error(f"An error occurred while fetching branches: {e}")
    finally:
        conn.close()
# Function to display details of a branch
def display_branch_details(branch_id):
    try:
        conn = connect_db()
        cursor = conn.cursor()

        # Fetch the details of the branch
        cursor.execute("""
        SELECT branch_name, location, contact_number 
        FROM branch 
        WHERE branch_id = ?
        """, (branch_id,))
        branch_details = cursor.fetchone()

        if branch_details:
            st.write(f"**Branch Name:** {branch_details[0]}")
            st.write(f"**Location:** {branch_details[1]}")
            st.write(f"**Contact Number:** {branch_details[2]}")
        else:
            st.error(f"No details found for branch with ID '{branch_id}'.")
    except sqlite3.Error as e:
        st.error(f"An error occurred while fetching branch details: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    display_existing_branches()
