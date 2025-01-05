import streamlit as st
import sqlite3
import pandas as pd  # For handling CSV

# Database Connection
def connect_db():
    return sqlite3.connect("database.db")

# Fetch Branches
def fetch_branches():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT branch_id, branch_name FROM branch")
    branches = cursor.fetchall()
    conn.close()
    return branches

# Fetch Grades - Hardcoding Grades 1 to 5
def fetch_grades(branch_id):
    grades = [1, 2, 3, 4, 5]
    return grades

# Fetch Subjects - Hardcode Subjects for each Grade
def fetch_subjects(branch_id, grade):
    subjects_mapping = {
        1: ["Math", "English", "Science", "Social Studies", "Art"],
        2: ["Math", "English", "Science", "Social Studies", "Physical Education"],
        3: ["Math", "English", "Science", "History", "Art"],
        4: ["Math", "English", "Science", "Geography", "Physical Education"],
        5: ["Math", "English", "Science", "History", "Computer Science"]
    }
    subjects = subjects_mapping.get(grade, [])
    return [(subject, subject) for subject in subjects]

# Bulk Upload CSV
def bulk_upload_csv(csv_file, branch_id, grade, subject_id):
    data = pd.read_csv(csv_file)
    conn = connect_db()
    cursor = conn.cursor()

    for _, row in data.iterrows():
        chapter_name = row.get("chapter_name")
        description = row.get("description", "")
        if chapter_name:
            # Insert into chapters
            cursor.execute("""
                INSERT INTO chapter (chapter_name, description) 
                VALUES (?, ?)
            """, (chapter_name, description))
            chapter_id = cursor.lastrowid

            # Insert associated topics (if any)
            topics = row.get("topics", "").split(";")  # Assuming topics are semicolon-separated
            for topic_name in topics:
                if topic_name.strip():
                    cursor.execute("""
                        INSERT INTO topic (topic_name, description)
                        VALUES (?, ?)
                    """, (topic_name.strip(), ""))
                    topic_id = cursor.lastrowid
                    cursor.execute("""
                        INSERT INTO topic_association (topic_id, chapter_id) 
                        VALUES (?, ?)
                    """, (topic_id, chapter_id))

    conn.commit()
    conn.close()
    st.success("Bulk data uploaded successfully!")

def add_chapter(chapter_name, description, class_id=1):  # Defaulting to class_id=1
    conn = connect_db()
    cursor = conn.cursor()

    # Ensure that class_id is valid, or default it to 1 if not provided
    cursor.execute("""
        INSERT INTO chapter (chapter_name, description, class_id) 
        VALUES (?, ?, ?)
    """, (chapter_name, description, class_id))

    conn.commit()
    conn.close()
    st.success(f"Chapter '{chapter_name}' added successfully!")

def add_topic(topic_name, description, expected_outcome, chapter_id):
    conn = connect_db()
    cursor = conn.cursor()

    # Insert topic with description and expected outcome
    cursor.execute("""
        INSERT INTO topic (topic_name, description) 
        VALUES (?, ?)
    """, (topic_name, description))
    topic_id = cursor.lastrowid

    # Insert topic association with chapter
    cursor.execute("""
        INSERT INTO topic_association (topic_id, chapter_id) 
        VALUES (?, ?)
    """, (topic_id, chapter_id))

    # Optionally, store expected outcome in a separate table
    cursor.execute("""
        INSERT INTO topic_outcome (topic_id, expected_outcome) 
        VALUES (?, ?)
    """, (topic_id, expected_outcome))

    conn.commit()
    conn.close()
    st.success(f"Topic '{topic_name}' added successfully!")

def update_topic(topic_id, new_topic_name, new_description, new_expected_outcome):
    conn = connect_db()
    cursor = conn.cursor()

    # Update topic details
    cursor.execute("""
        UPDATE topic 
        SET topic_name = ?, description = ? 
        WHERE topic_id = ?
    """, (new_topic_name, new_description, topic_id))

    # Update expected outcome
    cursor.execute("""
        UPDATE topic_outcome 
        SET expected_outcome = ? 
        WHERE topic_id = ?
    """, (new_expected_outcome, topic_id))

    conn.commit()
    conn.close()
    st.success(f"Topic '{new_topic_name}' updated successfully!")

def delete_topic(topic_id):
    conn = connect_db()
    cursor = conn.cursor()

    # Delete topic outcome
    cursor.execute("""
        DELETE FROM topic_outcome 
        WHERE topic_id = ?
    """, (topic_id,))

    # Delete topic association
    cursor.execute("""
        DELETE FROM topic_association 
        WHERE topic_id = ?
    """, (topic_id,))

    # Delete topic
    cursor.execute("""
        DELETE FROM topic 
        WHERE topic_id = ?
    """, (topic_id,))

    conn.commit()
    conn.close()
    st.success("Topic deleted successfully!")

# UI for Managing Subjects
def manage_subjects():
    st.title("Manage Subjects")

    # Step 1: Select Branch
    branches = fetch_branches()
    branch_options = {name: id_ for id_, name in branches}
    branch_name = st.selectbox("Select Branch", options=branch_options.keys())
    branch_id = branch_options.get(branch_name)

    # Save branch_id to session state
    st.session_state['branch_id'] = branch_id

    # Step 2: Select Grade
    grades = fetch_grades(branch_id)
    grade = st.selectbox("Select Grade", options=grades)

    # Save grade to session state
    st.session_state['grade'] = grade

    # Step 3: Select Subject
    subjects = fetch_subjects(branch_id, grade)
    subject_options = {name: id_ for id_, name in subjects}
    subject_name = st.selectbox("Select Subject", options=subject_options.keys())
    subject_id = subject_options.get(subject_name)

    # Step 4: Bulk Upload Chapters/Topics
    st.subheader("Bulk Upload Chapters and Topics")
    csv_file = st.file_uploader("Upload CSV File", type=["csv"])
    if csv_file and st.button("Upload Data"):
        bulk_upload_csv(csv_file, branch_id, grade, subject_id)

    # Step 5: Add New Chapter (with Expander)
    with st.expander("Add New Chapter"):
        with st.form(key="add_chapter_form"):
            chapter_name = st.text_input("Chapter Name")
            description = st.text_area("Description")
            submit = st.form_submit_button("Add Chapter")
            if submit and chapter_name:
                add_chapter(chapter_name, description)

    # Step 6: Select Chapter to Manage Topics
    st.subheader("Select Chapter to Manage Topics")
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT chapter_id, chapter_name FROM chapter")
    chapters = cursor.fetchall()
    conn.close()

    chapter_options = {name: id_ for id_, name in chapters}
    selected_chapter_name = st.selectbox("Select Chapter", options=chapter_options.keys())
    selected_chapter_id = chapter_options.get(selected_chapter_name)

    if selected_chapter_id:
        # Step 7: Add Topics for the Selected Chapter (with Expander)
        with st.expander(f"Add Topics to Chapter: {selected_chapter_name}"):
            with st.form(key="add_topic_form"):
                topic_name = st.text_input("Topic Name")
                description = st.text_area("Description")
                expected_outcome = st.text_area("Expected Outcome")
                submit_topic = st.form_submit_button("Add Topic")
                if submit_topic and topic_name:
                    add_topic(topic_name, description, expected_outcome, selected_chapter_id)

        # UI for Managing Topics (inside the Chapter Expander)
        with st.expander(f"Manage Topics for Chapter: {selected_chapter_name}"):
            st.subheader(f"Existing Topics in {selected_chapter_name}")
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT t.topic_id, t.topic_name, t.description, "to".expected_outcome
                FROM topic t
                JOIN topic_association ta ON t.topic_id = ta.topic_id
                LEFT JOIN topic_outcome "to" ON t.topic_id = "to".topic_id
                WHERE ta.chapter_id = ?
            """, (selected_chapter_id,))
            topics = cursor.fetchall()
            conn.close()

            if topics:
                for topic_id, topic_name, description, expected_outcome in topics:
                    st.write(f"**Topic Name:** {topic_name}")
                    st.write(f"**Description:** {description}")
                    st.write(f"**Expected Outcome:** {expected_outcome}")

                    # Option to Update or Delete the Topic
                    update_button = st.button(f"Update", key=f"update_{topic_id}")
                    delete_button = st.button(f"Delete", key=f"delete_{topic_id}")

                    if update_button:
                        # Show form to update the topic
                        with st.form(key=f"update_form_{topic_id}"):
                            new_topic_name = st.text_input("New Topic Name", value=topic_name)
                            new_description = st.text_area("New Description", value=description)
                            new_expected_outcome = st.text_area("New Expected Outcome", value=expected_outcome)
                            save_changes_button = st.form_submit_button("Save Changes")

                            if save_changes_button:
                                update_topic(topic_id, new_topic_name, new_description, new_expected_outcome)

                    if delete_button:
                        delete_topic(topic_id)

# Run the App
if __name__ == "__main__":
    manage_subjects()
