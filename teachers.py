import sqlite3
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


def teacher_dashboard():
    # Sidebar
    if "username" in st.session_state:
        user_name = st.session_state["username"]
        # Display the username with a human icon
        st.sidebar.write(f"**{user_name}** 🧑")  # Username with human icon
    else:
        user_name = "Teacher"  # Default if not logged in
        st.sidebar.write(f"**{user_name}** 🙋")  # Display "Guest" with a waving hand icon

    st.sidebar.write("Subject: Mathematics, Physics, Computer Science")
    menu = st.sidebar.radio("Menu", ["Dashboard", "Manage Students", "Manage Grades"])
    logout_button = st.sidebar.button("Logout", key="logout", help="Logout from the application")

    # Logic for Logout
    if logout_button:
        # Set the authenticated state to False
        st.session_state["authenticated"] = False  # You can set this to False if your session stores the authentication status
        st.session_state.pop("username", None)  # Clear the username
        st.session_state.clear()  # Clear any other session data if necessary
        st.write("You have been logged out!")
        
        # Trigger a rerun to navigate to the login page
        st.rerun()


    if menu == "Dashboard":
        render_dashboard()
    elif menu == "Manage Students":
        manage_students()
    elif menu == "Manage Grades":
        manage_grades()
def render_dashboard():
    # Title and Metrics Section
    st.title("Teacher Dashboard")
    st.subheader("Choose Subject and Topics")
    
    # Subject Selection
    subject = st.selectbox("Select Subject", ["Mathematics", "Physics", "Computer Science"])

    # Define topics based on the selected subject
    topics = {
        "Mathematics": ["Algebra", "Geometry", "Calculus", "Trigonometry", "Statistics"],
        "Physics": ["Mechanics", "Thermodynamics", "Optics", "Electromagnetism", "Quantum Physics"],
        "Computer Science": ["Data Structures", "Algorithms", "Operating Systems", "Databases", "Networking"]
    }
    
    # Topic Selection
    selected_topics = st.multiselect("Select Topics", topics[subject])

    # Display the selected topics
    if selected_topics:
        st.write(f"You have selected the following topics for {subject}:")
        st.write(", ".join(selected_topics))
    else:
        st.write(f"Please select topics for {subject}.")

    # Metrics Section (For demonstration purposes)
    total_students = 30
    total_chapters = 10  # Chapters replacing blocks
    learning_points = 40

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Students", total_students)
    col2.metric("Chapters", total_chapters)
    col3.metric("Learning Points", learning_points)
    col4.metric("Subject", subject)

    # Grade Distribution Pie Chart
    st.markdown(f"### Overall Grade Distribution - {subject}")
    pie_data = [61.1, 38.9]  # Example data for "YES" and "NO"
    pie_labels = ["YES", "NO"]
    fig, ax = plt.subplots()
    ax.pie(pie_data, labels=pie_labels, autopct='%1.1f%%', startangle=90, colors=["#1f77b4", "#aec7e8"])
    ax.axis("equal")
    st.pyplot(fig)

    # Grade and Section Selection
    st.markdown("### Analysis for Grades and Sections")
    selected_grade = st.selectbox("Select Grade for Detailed Analysis", ["Grade 10", "Grade 11", "Grade 12"])
    st.markdown(f"#### Analysis for {selected_grade} - {subject}")
    selected_section = st.selectbox("Select Section", ["Section A", "Section B", "Section C"])
    st.markdown(f"Performance Analysis - {selected_section}")

    # Student Names (replace with actual student names)
    student_names = ["John Doe", "Jane Smith", "Alex Brown", "Emily Davis", "Michael Johnson", "Sarah Lee", "David Wilson", "Laura Taylor", "Chris White", "Megan Harris", 
                     "Tom Clark", "Anna Martin", "James Walker", "Sophia Hall", "Benjamin Allen", "Olivia Young", "Ethan King", "Charlotte Scott", "Daniel Adams", "Grace Nelson", 
                     "Noah Carter", "Ava Mitchell", "Lucas Roberts", "Isabella Perez", "Mason Evans", "Amelia Carter", "Henry Thompson", "Lily Lewis", "William Harris", "Harper Turner"]

    # Define Chapter data based on subject
    chapter_data = {
       "Mathematics": {
            "Chapter 1. Algebra": [1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1],
            "Chapter 2. Geometry": [0, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1],
            "Chapter 3. Calculus": [1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 0, 0, 1, 1, 0, 1, 1, 0, 0, 1, 1, 1, 0],
            "Chapter 4. Trigonometry": [1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1],
            "Chapter 5. Statistics": [0, 1, 1, 0, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 0, 1, 1]
        },
        "Physics": {
            "Chapter 1. Mechanics": [1, 1, 0, 1, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1, 0, 0, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 0],
            "Chapter 2. Thermodynamics": [0, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1],
            "Chapter 3. Optics": [1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1],
            "Chapter 4. Electromagnetism": [0, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 1],
            "Chapter 5. Quantum Physics": [1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 0, 1, 1, 1]
        },
        "Computer Science": {
            "Chapter 1. Data Structures": [1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 0, 1, 0, 1, 1, 1, 0, 1, 1],
            "Chapter 2. Algorithms": [0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 0, 1, 1],
            "Chapter 3. Operating Systems": [1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 0, 1, 0],
            "Chapter 4. Databases": [1, 0, 1, 1, 0, 1, 1, 0, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0],
            "Chapter 5. Networking": [1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1]
        }
    }

    # Use the selected subject's chapters
    chapters = chapter_data.get(subject, {})

    # Calculate YES and NO counts for each chapter
    chapter_summary = {}
    for chapter, grades in chapters.items():
        yes_count = grades.count(1)
        no_count = grades.count(0)
        chapter_summary[chapter] = [yes_count, no_count]

    # Display chapter-wise summary
    st.markdown(f"### Blockwise Summary - {subject}")
    summary_df = pd.DataFrame.from_dict(chapter_summary, orient='index', columns=["YES", "NO"])
    st.dataframe(summary_df)

    # Convert the chapter data into a DataFrame
    df = pd.DataFrame(chapters)
    df["Student"] = student_names
    df_melted = df.melt(id_vars="Student", var_name="Chapter", value_name="Grade")

    # Plot chapter-wise grade distribution
    fig, ax = plt.subplots(figsize=(12, 8))
    for chapter, data in df_melted.groupby("Chapter"):
        ax.bar(data["Student"], data["Grade"], label=chapter, alpha=0.7)
    ax.set_ylabel("Grade (1 = YES, 0 = NO)")
    ax.set_title(f"Chapter-wise Grade Distribution for {subject}")
    ax.legend()
    plt.xticks(rotation=90, fontsize=8)
    st.pyplot(fig)

    # Chapter-wise Performance Data
    st.markdown(f"### Chapter-wise Performance - {subject}")

    # Define the performance data for each chapter
    performance_data = {
        "Mathematics": {
        "Chapter 1. Algebra": [92, 85, 88, 90, 83, 87, 80, 78, 89, 91, 87, 84, 88, 92, 79, 91, 85, 89, 87, 92, 90, 85, 88, 87, 92, 84, 86, 81, 90, 89],
        "Chapter 2. Geometry": [80, 75, 78, 80, 81, 82, 79, 85, 79, 80, 83, 81, 84, 82, 78, 84, 77, 80, 78, 85, 87, 80, 79, 80, 83, 81, 79, 77, 85, 88],
        "Chapter 3. Calculus": [85, 87, 88, 91, 89, 90, 83, 92, 86, 85, 84, 88, 81, 83, 89, 84, 87, 82, 88, 92, 85, 86, 87, 90, 89, 91, 80, 92, 86, 90],
        "Chapter 4. Trigonometry": [91, 90, 92, 89, 84, 88, 83, 90, 91, 89, 85, 92, 87, 85, 81, 89, 88, 90, 82, 87, 89, 90, 83, 88, 91, 89, 87, 92, 90, 86],
        "Chapter 5. Statistics": [89, 85, 88, 91, 90, 84, 86, 92, 88, 89, 83, 85, 87, 90, 91, 86, 89, 91, 90, 92, 85, 88, 81, 90, 87, 89, 86, 88, 91, 84]
    },
    "Physics": {
        "Chapter 1. Mechanics": [78, 85, 82, 90, 70, 76, 84, 78, 88, 92, 85, 80, 89, 87, 91, 92, 76, 88, 90, 85, 84, 77, 82, 80, 79, 84, 85, 89, 87, 92],
        "Chapter 2. Thermodynamics": [75, 78, 82, 88, 83, 80, 87, 89, 85, 84, 79, 80, 88, 87, 85, 91, 78, 81, 88, 92, 80, 85, 79, 84, 90, 83, 84, 81, 80, 86],
        "Chapter 3. Optics": [88, 82, 79, 85, 80, 86, 88, 91, 84, 92, 81, 77, 89, 88, 85, 87, 84, 82, 91, 86, 90, 87, 81, 80, 82, 85, 90, 86, 88, 81],
        "Chapter 4. Electromagnetism": [80, 85, 89, 90, 87, 84, 82, 81, 91, 85, 86, 88, 82, 91, 87, 90, 86, 85, 82, 84, 89, 88, 85, 91, 86, 88, 84, 79, 90, 85],
        "Chapter 5. Quantum Physics": [75, 86, 81, 90, 88, 91, 89, 84, 86, 90, 88, 91, 83, 85, 80, 90, 81, 89, 92, 87, 84, 89, 87, 80, 90, 91, 85, 80, 86, 81]
    },
    "Computer Science": {
        "Chapter 1. Data Structures": [85, 78, 90, 84, 88, 83, 91, 86, 89, 83, 80, 87, 85, 89, 91, 80, 82, 87, 85, 89, 88, 85, 91, 84, 90, 88, 79, 82, 84, 91],
        "Chapter 2. Algorithms": [80, 79, 89, 90, 87, 85, 82, 91, 88, 80, 86, 87, 83, 89, 88, 85, 90, 86, 83, 81, 85, 88, 79, 85, 89, 90, 88, 87, 91, 81],
        "Chapter 3. Operating Systems": [87, 90, 85, 91, 89, 86, 84, 82, 88, 91, 83, 85, 79, 81, 87, 85, 89, 92, 80, 84, 83, 86, 90, 81, 88, 91, 79, 88, 87, 86],
        "Chapter 4. Databases": [89, 80, 90, 88, 86, 83, 92, 81, 85, 87, 84, 92, 88, 89, 83, 90, 85, 84, 91, 87, 86, 92, 82, 86, 91, 88, 80, 84, 87, 88],
        "Chapter 5. Networking": [80, 79, 88, 85, 91, 90, 86, 84, 81, 86, 87, 89, 81, 82, 85, 92, 90, 83, 86, 84, 85, 89, 92, 88, 87, 80, 84, 81, 87, 90]
    }
}
    # Use the selected subject's performance data
    performance_df = pd.DataFrame(performance_data.get(subject, {}))
    performance_df["Student"] = student_names

    # Display the performance data in a table
    st.dataframe(performance_df)



import sqlite3
import pandas as pd
import streamlit as st

# Function to create the student_new table
def create_student_table():
    try:
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()

        # Create the 'student_new' table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS student_new (
            student_id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_name TEXT NOT NULL,
            roll_number INTEGER NOT NULL,
            age INTEGER NOT NULL,
            gender TEXT NOT NULL,
            branch TEXT NOT NULL
        )
        """)

        connection.commit()
        print("Table 'student_new' created successfully")
    except sqlite3.Error as e:
        print(f"An error occurred while creating the table: {e}")
    finally:
        if connection:
            connection.close()

# Call the function to create the table when the app starts
create_student_table()

# Helper function to get all students from the database
def get_all_students():
    try:
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM student_new")  # Fetching data from student_new table
        students = cursor.fetchall()
        return students
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        return []
    finally:
        if connection:
            connection.close()

# Add student function
def add_student(name, roll_number, age, gender, branch):
    try:
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()

        # Update the SQL query to match the 'student_new' table structure without the 'email' column
        cursor.execute("""
        INSERT INTO student_new (student_name, roll_number, age, gender, branch) 
        VALUES (?, ?, ?, ?, ?)
        """, (name, roll_number, age, gender, branch))  # No 'email' field here

        connection.commit()
        print("Student added successfully")
    except sqlite3.Error as e:
        print(f"An error occurred while adding the student: {e}")
    finally:
        if connection:
            connection.close()

# Update student function
def update_student(student_id, name, roll_number, age, gender, branch):
    try:
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        cursor.execute("""
        UPDATE student_new 
        SET student_name = ?, roll_number = ?, age = ?, gender = ?, branch = ?
        WHERE student_id = ?
        """, (name, roll_number, age, gender, branch, student_id))
        connection.commit()
    except sqlite3.Error as e:
        print(f"An error occurred while updating the student: {e}")
    finally:
        if connection:
            connection.close()





# Example functions (you should replace these with your actual database functions)
def add_student(name, roll_number, age, gender, branch):
    # Add student logic here (e.g., insert into database)
    pass

def update_student(student_id, name, roll_number, age, gender, branch):
    # Update student logic here (e.g., update database)
    pass

def get_all_students():
    # Get all students from the database (replace with actual database query)
    return []

# Manage Students function
def manage_students():
    st.title("Manage Students")

    # Define the subjects list
    subjects = ["Mathematics", "Physics", "Computer"]

    # Use selectbox for subject, grade, and section
    subject = st.selectbox("Select Subject", subjects)
    grade = st.selectbox("Select Grade", ["Grade 1", "Grade 2", "Grade 3", "Grade 4", "Grade 5"])
    section = st.selectbox("Select Section", ["Section A", "Section B", "Section C", "Section D"])

    # Add student section inside an expander
    with st.expander("Add Student"):
        student_id = st.number_input("Student ID (Leave blank for new)", min_value=0, max_value=1000, value=0)
        name = st.text_input("Name")
        roll_number = st.number_input("Roll Number", min_value=1, max_value=1000, value=1)
        age = st.number_input("Age", min_value=1, max_value=100, value=18)
        gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        branch = st.text_input("Branch")

        if student_id == 0:
            if st.button("Add Student"):
                add_student(name, roll_number, age, gender, branch)
                st.success(f"Student {name} with Roll Number {roll_number} added successfully!")
        else:
            if st.button("Update Student"):
                update_student(student_id, name, roll_number, age, gender, branch)
                st.success(f"Student {name} with Roll Number {roll_number} updated successfully!")

    # Displaying existing students
    st.subheader("Existing Students")
    students = get_all_students()  # Fetch all students from the database

    if students:
        student_df = pd.DataFrame(students, columns=["student_id", "student_name", "roll_number", "age", "gender", "branch", "address", "phone_number"])
        st.write(student_df)
    else:
        st.write("No existing students found.")
    
    # Bulk Upload Section
    st.subheader("Bulk Upload Students")
    uploaded_file = st.file_uploader("Upload CSV", type="csv")
    
    if uploaded_file is not None:
        student_data = pd.read_csv(uploaded_file)
        st.write(student_data)
        
        if st.button("Add Students from CSV"):
            for index, row in student_data.iterrows():
                add_student(row['name'], row['roll_number'], row['age'], row['gender'], row['branch'])
            
            st.success("Students added successfully from CSV!")
            students = get_all_students()
            if students:
                student_df = pd.DataFrame(students, columns=["student_id", "student_name", "roll_number", "age", "gender", "branch"])
                st.write(student_df)

# Call manage_students to run the Streamlit app functionality
manage_students()


import sqlite3
import pandas as pd
import streamlit as st

# Function to create grades table (if not exists)
def create_grades_table():
    try:
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS grades (
            grade_id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER,
            student_name TEXT,
            subject TEXT,
            chapter TEXT,
            section TEXT,
            grade INTEGER,
            FOREIGN KEY(student_id) REFERENCES student_new(student_id)
        )
        """)
        connection.commit()
    except sqlite3.Error as e:
        st.error(f"An error occurred while creating the grades table: {e}")
    finally:
        if connection:
            connection.close()

# Function to get all students (hardcoded for now)
def get_students():
    return ["John Doe", "Jane Smith", "Alex Brown", "Emily Davis", "Michael Johnson", "Sarah Lee", "David Wilson", "Laura Taylor", "Chris White", "Megan Harris", 
                     "Tom Clark", "Anna Martin", "James Walker", "Sophia Hall", "Benjamin Allen", "Olivia Young", "Ethan King", "Charlotte Scott", "Daniel Adams", "Grace Nelson", 
                     "Noah Carter", "Ava Mitchell", "Lucas Roberts", "Isabella Perez", "Mason Evans", "Amelia Carter", "Henry Thompson", "Lily Lewis", "William Harris", "Harper Turner"]

# Function to get all subjects (hardcoded for now)
def get_subjects():
    return ["Mathematics", "Physics", "Computer Science"]

# Function to get chapters/topics for each subject (hardcoded mapping)
def get_chapters_for_subject(subject):
    subject_chapters = {
        "Mathematics": ["Algebra", "Geometry", "Calculus", "Statistics"],
        "Physics": ["Mechanics", "Electromagnetism", "Thermodynamics", "Optics"],
        "Computer Science": ["Data Structures", "Algorithms", "Operating Systems", "Networks"]
    }
    return subject_chapters.get(subject, [])

# Function to get all sections (hardcoded for now)
def get_sections():
    return ["Section A", "Section B", "Section C", "Section D"]

# Function to save grades to the database
def save_grade(student_id, student_name, subject, chapter, section, grade):
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute("""
    INSERT INTO grades (student_id, student_name, subject, chapter, section, grade)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (student_id, student_name, subject, chapter, section, grade))
    connection.commit()
    
    # Fetch the last inserted grade_id
    cursor.execute("SELECT last_insert_rowid()")
    grade_id = cursor.fetchone()[0]
    
    connection.close()
    
    return grade_id  # Return the generated grade_id

# Function to delete all grades from the database
def delete_all_grades_from_db():
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute("DELETE FROM grades")  # Deletes all rows in the grades table
    connection.commit()
    connection.close()

# Main function to manage grades
def manage_grades():
    st.title("Manage Student Grades")

    # Select student from list
    student_name = st.selectbox("Select Student", get_students(), key="student_selectbox")
    
    # Get student ID based on the selected student (In a real scenario, you would fetch this from the database)
    student_id = get_students().index(student_name) + 1  # Simple ID based on list index

    # Container for grade selection
    with st.container():
        st.subheader("Select Grade Details")
        
        col1, col2, col3 = st.columns([2, 3, 2])
        with col1:
            subject = st.selectbox("Select Subject", get_subjects(), key="subject_selectbox")
        
        with col2:
            chapters = get_chapters_for_subject(subject)
            chapter = st.selectbox(f"Select Chapter for {subject}", chapters, key="chapter_selectbox")
        
        with col3:
            section = st.selectbox("Select Section", get_sections(), key="section_selectbox")

    # Initialize grades in session state if not already initialized
    if "grades" not in st.session_state:
        st.session_state["grades"] = []  # Initialize a session state for grades

    # Grade selection
    with st.container():
        st.subheader("Select Grade")
        grade = st.selectbox("Grade", list(range(1, 11)), key="grade_selectbox")
        
    # Add grade entry to session state when button is clicked
    with st.container():
        if st.button("Add", key="add_grade"):
            grade_id = save_grade(student_id, student_name, subject, chapter, section, grade)
            grade_entry = {
                "grade_id": grade_id,  # Include the grade_id here
                "student_name": student_name,
                "subject": subject,
                "chapter": chapter,
                "section": section,
                "grade": grade
            }
            st.session_state["grades"].append(grade_entry)
            st.success("Grade Added Successfully!")

    # Layout for buttons: Save and Download
    with st.container():
        col1, col2 = st.columns([2, 1])
        
        with col1:
            if st.button("Save"):
                if "grades" in st.session_state and st.session_state["grades"]:
                    for grade_entry in st.session_state["grades"]:
                        if "grade" in grade_entry:
                            save_grade(student_id=student_id,  # Using the student_id derived from the name
                                       student_name=student_name,
                                       subject=grade_entry["subject"],
                                       chapter=grade_entry["chapter"],
                                       section=grade_entry["section"],
                                       grade=grade_entry["grade"])
                    st.success("Grades Saved Successfully!")
                else:
                    st.warning("No grades to save.")
        
        with col2:
            if st.session_state.get("grades"):
                with st.expander("Download Grades Summary", expanded=False):
                    grades_df = pd.DataFrame(st.session_state["grades"])
                    if not grades_df.empty:
                        st.write("Grades Summary:")
                        st.dataframe(grades_df, use_container_width=True)

                        # Add "Delete All Grades" button to delete the entire table
                        if st.button("Delete"):
                            # Clear grades from session state
                            st.session_state["grades"] = []
                            # Delete all grades from the database
                            delete_all_grades_from_db()
                            st.success("All grades deleted successfully!")

                        # Download button for CSV
                        csv_data = grades_df.to_csv(index=False).encode('utf-8')
                        st.download_button(
                            label="Download Summary (CSV)",
                            data=csv_data,
                            file_name="grades_summary.csv",
                            mime="text/csv"
                        )
                    else:
                        st.warning("No grades available to download.")
            else:
                st.warning("No grades added yet.")

if __name__ == "__main__":
    if "authenticated" in st.session_state and st.session_state["authenticated"]:
        create_grades_table()  # Ensure grades table exists
        manage_grades()  # Main grade management logic
    else:
        st.warning("Please log in to access the dashboard.")
