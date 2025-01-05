
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Mock data for demonstration (with the addition of Branch 3)
branch_data = {
    1: {
        "name": "Branch 1",
        "students": 200,
        "teachers": 15,
        "subjects": 5,
        "classes": 4,
        "sections": 3
    },
    2: {
        "name": "Branch 2",
        "students": 150,
        "teachers": 12,
        "subjects": 4,
        "classes": 3,
        "sections": 2
    },
    3: {
        "name": "Branch 3",
        "students": 180,
        "teachers": 14,
        "subjects": 6,
        "classes": 5,
        "sections": 4
    }
}

branch_data[10] = {
    "name": "Branch 10",
    "students": 250,
    "teachers": 20,
    "subjects": 7,
    "classes": 5,
    "sections": 4
}

subject_teacher_data = [
    ("Math", 5), ("Physics", 4), ("Chemistry", 4), ("Biology", 3), ("English", 2),
    ("Accounting", 3), ("Economics", 2), ("Business Studies", 3)
]

grade_statistics_data = [
    { "grade": "Grade A", "students": 50, "teachers": 5, "classes": 2},
    { "grade": "Grade B", "students": 60, "teachers": 6, "classes": 2},
    { "grade": "Grade C", "students": 90, "teachers": 8, "classes": 3},
    { "grade": "Grade D", "students": 40, "teachers": 4, "classes": 1}
]

subject_structure_data = [
    { "subject": "Math", "chapters": 10, "topics": 25},
    { "subject": "Physics", "chapters": 8, "topics": 20},
    { "subject": "Chemistry", "chapters": 12, "topics": 30},
    { "subject": "Biology", "chapters": 10, "topics": 28},
    { "subject": "English", "chapters": 6, "topics": 15},
    { "subject": "Accounting", "chapters": 8, "topics": 18},
    { "subject": "Economics", "chapters": 6, "topics": 14},
    { "subject": "Business Studies", "chapters": 7, "topics": 17}
]

# Fetch overview statistics for the branch
def fetch_overview_statistics(branch_id):
    # Check if branch_id exists in branch_data
    if branch_id in branch_data:
        return branch_data[branch_id]
    return {}  # Return an empty dictionary if branch doesn't exist

# Subject-wise Teacher Distribution
def subject_teacher_distribution(subject_filter=None):
    data = subject_teacher_data
    
    # Filter by subject if selected
    if subject_filter:
        data = [entry for entry in data if entry[0] == subject_filter]
    
    return pd.DataFrame(data, columns=['subject_name', 'teacher_count'])

def grade_statistics(grade_filter=None):
    data = grade_statistics_data
    
    # Map numeric grade selection to actual grade labels
    grade_map = {
        "1": "Grade A",
        "2": "Grade B",
        "3": "Grade C",
        "4": "Grade D",
        "5": "Grade E",
        "6": "Grade F",
        "7": "Grade G",
        "8": "Grade H",
        "9": "Grade I",
        "10": "Grade J"
    }
    
    # Filter by grade if selected
    if grade_filter:
        grade_label = grade_map.get(grade_filter, None)
        if grade_label:
            data = [entry for entry in data if entry['grade'] == grade_label]
    
    # Return as DataFrame
    grade_df = pd.DataFrame(data)
    
    # Ensure the 'grade' column exists
    if 'grade' not in grade_df.columns:
        raise ValueError("The 'grade' column is missing from grade statistics data")
    
    # Check if any data exists after filtering
    if grade_df.empty:
        st.write(f"No data available for selected grade: {grade_filter}")
    
    return grade_df


# Subject-wise Structure Analysis
def subject_structure_analysis(subject_filter=None):
    data = subject_structure_data
    
    # Filter by subject if selected
    if subject_filter:
        data = [entry for entry in data if entry['subject'] == subject_filter]
    
    return pd.DataFrame(data)

# Sidebar options for subject and grade selection
def sidebar_selection():
    # Show all subjects (no branch distinction)
    all_subjects = set([subject for subject, _ in subject_teacher_data])
    selected_subject = st.sidebar.selectbox("Select Subject", list(all_subjects))

    # Allow users to select predefined grades 1, 2, 3, 4 (matching the grade labels)
    selected_grade = st.sidebar.selectbox("Select Grade", ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"])

    return selected_subject, selected_grade

def display_branch_dashboard(branch_id):  
    # Sidebar selection for subject and grade
    selected_subject, selected_grade = sidebar_selection()

    # Get branch name from branch_data using branch_id
    branch_info = fetch_overview_statistics(branch_id)
    
    # If branch info is empty, show an empty page instead of error
    if not branch_info:
        st.write(f"No data available for Branch {branch_id}")
        return

    branch_name = branch_info["name"]
    
    st.title(f"{branch_name} Dashboard")

    # Overview Statistics
    st.subheader("Overview Statistics")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(label="Students", value=branch_info['students'])
    with col2:
        st.metric(label="Teachers", value=branch_info['teachers'])
    with col3:
        st.metric(label="Subjects", value=branch_info['subjects'])
    with col4:
        st.metric(label="Classes", value=branch_info['classes'])

    # Visualizing Overview Statistics with Plotly
    overview_data = {
        'Categories': ['Sections'],
        'Counts': [branch_info['sections']]
    }
    overview_df = pd.DataFrame(overview_data)
    fig = px.bar(overview_df, x='Categories', y='Counts', 
                 title=f"Sections Overview for {branch_name}",
                 labels={'Categories': 'Category', 'Counts': 'Count'},
                 color='Counts', color_continuous_scale='Viridis',
                 hover_name="Counts")
    st.plotly_chart(fig)

    # Subject-wise Teacher Distribution
    st.subheader("Subject-wise Teacher Distribution")
    subject_teacher_data_df = subject_teacher_distribution(selected_subject)
    fig = px.bar(subject_teacher_data_df, x='subject_name', y='teacher_count', 
                 title=f"Teacher Distribution for {branch_name} - {selected_subject}",
                 labels={'subject_name': 'Subject', 'teacher_count': 'Teacher Count'},
                 hover_data=['subject_name', 'teacher_count'],
                 color='teacher_count', color_continuous_scale='Blues')
    st.plotly_chart(fig)

    # Grade-wise Statistics
    st.subheader("Grade-wise Statistics")
    grade_stats_data = grade_statistics(selected_grade)
    fig = go.Figure()
    fig.add_trace(go.Bar(x=grade_stats_data['grade'], y=grade_stats_data['students'], 
                         name='Students', marker_color='skyblue', hovertemplate='%{y} students'))
    fig.add_trace(go.Bar(x=grade_stats_data['grade'], y=grade_stats_data['teachers'], 
                         name='Teachers', marker_color='orange', hovertemplate='%{y} teachers'))
    fig.add_trace(go.Bar(x=grade_stats_data['grade'], y=grade_stats_data['classes'], 
                         name='Classes', marker_color='green', hovertemplate='%{y} classes'))

    fig.update_layout(barmode='stack', 
                      title="Grade-wise Statistics", 
                      xaxis_title="Grade", 
                      yaxis_title="Count", 
                      xaxis=dict(showgrid=False),
                      plot_bgcolor='rgba(0, 0, 0, 0)',  
                      bargap=0.15)
    st.plotly_chart(fig)

    # Subject-wise Structure Analysis
    st.subheader("Subject-wise Structure Analysis")
    subject_structure_data_df = subject_structure_analysis(selected_subject)
    fig = go.Figure()
    fig.add_trace(go.Bar(x=subject_structure_data_df['subject'], 
                         y=subject_structure_data_df['chapters'], 
                         name="Chapters", 
                         marker_color='salmon', 
                         hovertemplate='%{y} chapters'))
    fig.add_trace(go.Bar(x=subject_structure_data_df['subject'], 
                         y=subject_structure_data_df['topics'], 
                         name="Topics", 
                         marker_color='lightgreen', 
                         hovertemplate='%{y} topics'))

    fig.update_layout(barmode='group', 
                      title="Subject-wise Structure Analysis", 
                      xaxis_title="Subject", 
                      yaxis_title="Count",
                      plot_bgcolor='rgba(0, 0, 0, 0)',
                      xaxis=dict(showgrid=False),
                      bargap=0.2)
    st.plotly_chart(fig)

# Displaying the Dashboard for Branch 1 (you can also call for Branch 2 or Branch 3)
display_branch_dashboard(1)  # Change the branch_id to 2, 3, or 10 as needed
