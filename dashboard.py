# import streamlit as st
# import pandas as pd
# import matplotlib.pyplot as plt
# import seaborn as sns

# # Function to display overall stats
# def display_overall_stats(total_branches, total_teachers, total_students, total_subjects):
#     st.subheader("Overall Statistics")
    
#     # Use Streamlit's metric to display key numbers
#     cols = st.columns(5)
#     cols[0].metric("Total Branches", total_branches)
#     cols[1].metric("Total Teachers", total_teachers)
#     cols[2].metric("Total Students", total_students)
#     cols[3].metric("Total LPs", 119)  # Mocked for now
#     cols[4].metric("Subjects", total_subjects)

#     # Bar chart for Overall Statistics
#     overall_data = {
#         "Total Branches": total_branches,
#         "Total Teachers": total_teachers,
#         "Total Students": total_students,
#         "Total Subjects": total_subjects
#     }
#     bar_chart_data = pd.DataFrame(overall_data, index=[0])
#     st.bar_chart(bar_chart_data)

# # Function to display branch stats
# def display_branch_stats(branch_stats):
#     st.subheader("Branch-wise Statistics")
    
#     # Display the branch statistics as a table
#     st.dataframe(branch_stats)

#     # Visualizations for Branch-wise Data
#     # Number of Students per Branch
#     fig, ax = plt.subplots(figsize=(10, 6))
#     sns.barplot(x='branch_name', y='students', data=branch_stats, ax=ax)
#     ax.set_title('Number of Students per Branch')
#     ax.set_xlabel('Branch Name')
#     ax.set_ylabel('Number of Students')
#     st.pyplot(fig)

#     # Average Math Scores per Branch
#     fig, ax = plt.subplots(figsize=(10, 6))
#     sns.barplot(x='branch_name', y='math_avg', data=branch_stats, ax=ax, palette='Blues_d')
#     ax.set_title('Average Math Scores per Branch')
#     ax.set_xlabel('Branch Name')
#     ax.set_ylabel('Average Math Score')
#     st.pyplot(fig)

#     # Number of Teachers per Branch
#     fig, ax = plt.subplots(figsize=(10, 6))
#     sns.barplot(x='branch_name', y='teachers', data=branch_stats, ax=ax, palette='Greens_d')
#     ax.set_title('Number of Teachers per Branch')
#     ax.set_xlabel('Branch Name')
#     ax.set_ylabel('Number of Teachers')
#     st.pyplot(fig) 










import streamlit as st
import pandas as pd
import plotly.express as px

# Sample branch data
branch_data = {
    1: {"name": "Branch 1", "students": 200, "teachers": 15, "math_avg": 75, "classes": 5, "sections": 10, "subjects": 10, "grade": "Grade 1"},
    2: {"name": "Branch 2", "students": 150, "teachers": 12, "math_avg": 80, "classes": 4, "sections": 8, "subjects": 8, "grade": "Grade 2"},
    3: {"name": "Branch 3", "students": 180, "teachers": 13, "math_avg": 78, "classes": 6, "sections": 12, "subjects": 9, "grade": "Grade 1"},
}

# Function to display overall stats
def display_overall_stats(total_branches, total_teachers, total_students, total_subjects):
    st.subheader("Overall Statistics")
    
    # Use Streamlit's metric to display key numbers
    cols = st.columns(5)
    cols[0].metric("Total Branches", total_branches)
    cols[1].metric("Total Teachers", total_teachers)
    cols[2].metric("Total Students", total_students)
    cols[3].metric("Total LPs", 119)  # Mocked for now
    cols[4].metric("Subjects", total_subjects)

    # Display Bar chart for Overall Statistics
    overall_data = {
        "Total Branches": total_branches,
        "Total Teachers": total_teachers,
        "Total Students": total_students,
        "Total Subjects": total_subjects
    }
    bar_chart_data = pd.DataFrame(overall_data, index=[0])
    st.bar_chart(bar_chart_data)

# Function to display branch stats using Plotly
def display_branch_stats(branch_stats, grade_filter=None, subject_filter=None):
    st.subheader("Branch-wise Statistics")
    
    # Apply filters if any
    if grade_filter:
        branch_stats = branch_stats[branch_stats['grade'] == grade_filter]
    if subject_filter:
        branch_stats = branch_stats[branch_stats['subjects'] == subject_filter]
    
    # Display the branch statistics as a table
    st.dataframe(branch_stats)

    # Plotly Bar chart for Number of Students per Branch
    fig = px.bar(branch_stats, x='branch_name', y='students', 
                 labels={'branch_name': 'Branch Name', 'students': 'Number of Students'},
                 title='Number of Students per Branch')
    st.plotly_chart(fig)

    # Plotly Bar chart for Average Math Scores per Branch
    fig = px.bar(branch_stats, x='branch_name', y='math_avg', color='branch_name',
                 labels={'branch_name': 'Branch Name', 'math_avg': 'Average Math Score'},
                 title='Average Math Scores per Branch')
    st.plotly_chart(fig)

    # Plotly Bar chart for Number of Teachers per Branch
    fig = px.bar(branch_stats, x='branch_name', y='teachers', color='branch_name',
                 labels={'branch_name': 'Branch Name', 'teachers': 'Number of Teachers'},
                 title='Number of Teachers per Branch')
    st.plotly_chart(fig)

# Main Application Logic
def main():
    # Create a DataFrame for the branch stats
    branch_stats = pd.DataFrame.from_dict(branch_data, orient='index')
    
    # Ensure correct column names
    branch_stats['branch_name'] = branch_stats['name']  # Add branch name as a separate column

    # Sidebar selection for grade and subject
    grade_options = branch_stats['grade'].unique()
    subject_options = branch_stats['subjects'].unique()

    selected_grade = st.sidebar.selectbox("Select Grade", options=grade_options)
    selected_subject = st.sidebar.selectbox("Select Subject", options=subject_options)

    # Calculate total values for overall stats
    total_branches = len(branch_data)
    total_teachers = sum([branch["teachers"] for branch in branch_data.values()])
    total_students = sum([branch["students"] for branch in branch_data.values()])
    total_subjects = sum([branch["subjects"] for branch in branch_data.values()])

    # Display overall stats
    display_overall_stats(total_branches, total_teachers, total_students, total_subjects)

    # Display branch-wise statistics
    display_branch_stats(branch_stats, grade_filter=selected_grade, subject_filter=selected_subject)

if __name__ == "__main__":
    main()