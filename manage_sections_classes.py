import streamlit as st
import sqlite3
import pandas as pd
import io

# Database connection
def get_connection():
    return sqlite3.connect("database.db")

# Utility Functions
def get_classes_by_grade(grade):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT class_id, class_name FROM class WHERE grade = ?", (grade,))
    classes = cursor.fetchall()
    conn.close()
    return classes

def get_sections(class_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT section_id, section_name FROM section WHERE class_id = ?", (class_id,))
    sections = cursor.fetchall()
    conn.close()
    return sections

def get_students(section_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT student_name, roll_number, gender, phone_number, dob, address, father_name, mother_name FROM student WHERE section_id = ?", (section_id,))
    students = cursor.fetchall()
    conn.close()
    return students

def add_section(section_name, class_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO section (section_name, class_id) VALUES (?, ?)", (section_name, class_id))
    conn.commit()
    conn.close()

def add_student(name, father_name, mother_name, roll_number, gender, phone, dob, address, section_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO student (student_name, father_name, mother_name, roll_number, gender, phone_number, dob, address, section_id)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (name, father_name, mother_name, roll_number, gender, phone, dob, address, section_id)
    )
    conn.commit()
    conn.close()

def bulk_upload_students(student_data, section_id):
    conn = get_connection()
    cursor = conn.cursor()
    for _, row in student_data.iterrows():
        cursor.execute("""
            INSERT INTO student (student_name, father_name, mother_name, roll_number, gender, phone_number, dob, address, section_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (row['Student Name'], row['Father Name'], row['Mother Name'], row['Roll Number'],
             row['Gender'], row['Phone Number'], row['Date of Birth'], row['Address'], section_id)
        )
    conn.commit()
    conn.close()

def manage_sections_classes():
    st.header("Manage Classes and Sections")
    
    # Predefined grades from 1 to 10
    grades = [str(i) for i in range(1, 11)]
    selected_grade = st.selectbox("Select Grade", grades, key="grade_selectbox")

    # Fetch classes for the selected grade
    classes = get_classes_by_grade(selected_grade)
    
    if classes:
        # Automatically select the first class in the list
        class_id = classes[0][0]  # Class ID of the first class
        selected_class_name = classes[0][1]  # Class name of the first class
        
        st.write(f"Selected Class: {selected_class_name}")

        # Manage Sections
        st.subheader(f"Sections for Grade {selected_grade}")
        sections = get_sections(class_id)

        if sections:
            # Use a unique key for the section selectbox based on the grade and class
            section_key = f"section_selectbox_{selected_grade}_{class_id}"
            selected_section = st.selectbox("Select Section", [sec[1] for sec in sections], key=section_key)
            section_id = next(sec[0] for sec in sections if sec[1] == selected_section)
            with st.expander("students in section"):
                st.write(f"Students in Section: {selected_section}")
                students = get_students(section_id)
                
                # Display the student list in a table format
                if students:
                    student_df = pd.DataFrame(students, columns=["Student Name", "Roll Number", "Gender", "Phone Number", "Date of Birth", "Address", "Father's Name", "Mother's Name"])
                    st.dataframe(student_df)

            # Add New Section using a small form
            with st.expander("add new esction"):
                with st.form(key="add_section_form"):
                    st.subheader("Add a New Section")
                    new_section_name = st.text_input("Section Name")
                    submit_button = st.form_submit_button("Add Section")
                    
                    if submit_button:
                        if new_section_name:
                            add_section(new_section_name, class_id)
                            st.success(f"Section '{new_section_name}' added to Grade '{selected_grade}'.")
                            # Refresh the sections after adding the new one
                            sections = get_sections(class_id)
                            # Update the section selectbox with the newly added section
                            selected_section = st.selectbox("Select Section", [sec[1] for sec in sections], key="section_selectbox")
                            section_id = next(sec[0] for sec in sections if sec[1] == selected_section)
                        else:
                            st.error("Please enter a valid section name.")
            
            # Manage Students using a larger form with 2 columns
            with st.expander("add new student"):
                with st.form(key="add_student_form"):
                    st.subheader("Add a New Student")
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        student_name = st.text_input("Student Name")
                        father_name = st.text_input("Father's Name")
                        mother_name = st.text_input("Mother's Name")
                        roll_number = st.text_input("Roll Number")
                        gender = st.selectbox("Gender", ["Male", "Female", "Other"])
                    
                    with col2:
                        phone_number = st.text_input("Phone Number")
                        date_of_birth = st.date_input("Date of Birth")
                        address = st.text_area("Address")
                    
                    submit_button = st.form_submit_button("Add Student")
                    
                    if submit_button:
                        if student_name and roll_number and gender and phone_number and date_of_birth:
                            try:
                                add_student(
                                    student_name, father_name, mother_name, roll_number,
                                    gender, phone_number, date_of_birth, address, section_id
                                )
                                st.success(f"Student '{student_name}' added to Section '{selected_section}'.")
                                # Dynamically update the student list after adding a student
                                students = get_students(section_id)
                                student_df = pd.DataFrame(students, columns=["Student Name", "Roll Number", "Gender", "Phone Number", "Date of Birth", "Address", "Father's Name", "Mother's Name"])
                                st.dataframe(student_df)

                            except sqlite3.IntegrityError as e:
                                st.error(f"Database error: {e}")
                        else:
                            st.error("Please fill in all required fields.")
            
            with st.expander("Bulk upload students"):
                st.subheader("Bulk Upload Students")
                uploaded_file = st.file_uploader("Upload CSV File", type=["csv"])
                if uploaded_file:
                    try:
                        student_data = pd.read_csv(uploaded_file)
                        st.write("Preview of uploaded data:")
                        st.dataframe(student_data.head())
                        if st.button("Upload Students"):
                            bulk_upload_students(student_data, section_id)
                            st.success("Students uploaded successfully.")
                            # Dynamically update the student list after bulk upload
                            students = get_students(section_id)
                            student_df = pd.DataFrame(students, columns=["Student Name", "Roll Number", "Gender", "Phone Number", "Date of Birth", "Address", "Father's Name", "Mother's Name"])
                            st.dataframe(student_df)

                    except Exception as e:
                        st.error(f"Error uploading file: {e}")
                    
            # Create CSV buffer for export (Move the download button outside of the form)
            if students:
                student_df = pd.DataFrame(students, columns=["Student Name", "Roll Number", "Gender", "Phone Number", "Date of Birth", "Address", "Father's Name", "Mother's Name"])
                csv_buffer = io.StringIO()
                student_df.to_csv(csv_buffer, index=False)
                csv_buffer.seek(0)
                
                # Convert CSV buffer to bytes
                csv_data = csv_buffer.getvalue().encode('utf-8')

                # Display the download button after the forms are handled
                with st.expander("Export student list"):
                    st.subheader("Export Student List")
                    col1, col2 = st.columns([1, 1])  # Create two columns for side-by-side layout
                    with col1:
                        st.download_button(
                            label="Download Student List as CSV",
                            data=csv_data,
                            file_name=f"student_list_grade_{selected_grade}_section_{selected_section}.csv",
                            mime="text/csv"
                        )
                    
        else:
            st.warning(f"No classes found for Grade {selected_grade}.")

# Call the main function to display the Streamlit UI
manage_sections_classes()
