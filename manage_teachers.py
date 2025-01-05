import streamlit as st
import sqlite3

def get_connection():
    return sqlite3.connect("database.db")

def add_teacher(name, email, password, subject, classes, branch_id):
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO teachers (teacher_name, email, password, subject, classes, branch_id)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (name, email, password, subject, classes, branch_id))

    connection.commit()
    connection.close()

def delete_teacher(email):
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()

    cursor.execute("DELETE FROM teachers WHERE email = ?", (email,))
    connection.commit()
    connection.close()

def get_teachers_by_subject(subject):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT teacher_name, email, subject, classes FROM teachers WHERE subject = ?", (subject,))
    teachers = cursor.fetchall()
    conn.close()
    return teachers

def manage_teachers(branch_id):
    st.title("Manage Teachers")
    
    # Form to Add New Teacher

    st.subheader("Add New Teacher")

    teacher_name = st.text_input("Teacher Name")
    teacher_email = st.text_input("Teacher Email")
    teacher_password = st.text_input("Password", type="password")
    
    # Subject selection
    subject_list = ["Mathematics", "Physics", "Chemistry", "Computer Science", "Biology"]
    teacher_subject = st.selectbox("Select Subject", subject_list)

    # Class assignment (could be a comma-separated list or use checkboxes)
    class_list = ["Class A", "Class B", "Class C", "Class D"]
    teacher_classes = st.multiselect("Assign Classes", class_list)
    
    # Add Teacher Button
 
    if st.button("Add Teacher"):
        if teacher_name and teacher_email and teacher_password and teacher_subject and teacher_classes:
            # Join selected classes into a comma-separated string
            classes = ', '.join(teacher_classes)
            
            # Call the function to add teacher to the database
            add_teacher(teacher_name, teacher_email, teacher_password, teacher_subject, classes, branch_id)
            st.success(f"Teacher {teacher_name} added successfully!")
        else:
            st.warning("Please fill in all fields.")

    # Display Existing Teachers
    with st.expander("view teachers by subject"):
        st.subheader("View Teachers by Subject")
        
        selected_subject = st.selectbox("Select Subject to View Teachers", subject_list)
        if selected_subject:
            teachers = get_teachers_by_subject(selected_subject)
            if teachers:
                for teacher in teachers:
                    st.write(f"Name: {teacher[0]}")
                    st.write(f"Email: {teacher[1]}")
                    st.write(f"Classes: {teacher[3]}")
                    
                    # Delete Button
                    if st.button(f"Delete"):
                        delete_teacher(teacher[1])  # Pass email to delete the teacher
                        st.success(f"Teacher {teacher[0]} deleted successfully!")
                        st.rerun()  # Re-run the app to refresh the list
                    st.write("-" * 50)
            else:
                st.warning(f"No teachers found for {selected_subject}.")
