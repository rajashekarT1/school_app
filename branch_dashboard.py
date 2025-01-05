import streamlit as st
import pandas as pd
import plotly.express as px
import random

# Load the branch data from CSV
@st.cache_data
def load_branch_data():
    return pd.read_csv('branch.csv')

# Fetch branch data for a given branch id
def fetch_overview_statistics(branch_id):
    branch_data = load_branch_data()
    branch_info = branch_data[branch_data['index'] == branch_id]
    
    if not branch_info.empty:
        return branch_info.iloc[0].to_dict()  # Convert the row to a dictionary
    return {}

# Function to display teacher distribution per subject and grade
def teacher_distribution(branch_id, selected_grade, selected_subject):
    branch_data = load_branch_data()
    branch_info = branch_data[branch_data['index'] == branch_id]
    
    if not branch_info.empty:
        # List of subjects (limited to 4)
        subjects = [selected_subject]  # Only show the selected subject
        teacher_count = []
        
        for subject in subjects:
            # Check for columns with the format 'Subject_Grade_teachers'
            column_name = f"{subject}_{selected_grade}_teachers"
            if column_name in branch_info.columns:
                teacher_count.append(branch_info[column_name].values[0])
            else:
                teacher_count.append(0)  # Set default value if column is missing
        
        # Create a DataFrame for Plotly visualization
        teacher_data = pd.DataFrame({
            'Subject': subjects,
            'Teacher Count': teacher_count
        })
        
        # Create a bar chart showing teacher distribution per subject
        fig = px.bar(teacher_data, x='Subject', y='Teacher Count', 
                     title=f"Teacher Distribution for {branch_info['name'].values[0]} - Grade {selected_grade}",
                     labels={'Subject': 'Subject', 'Teacher Count': 'Number of Teachers'},
                     color='Teacher Count', color_continuous_scale='Viridis')
        st.plotly_chart(fig)

# Function to simulate performance data
def get_performance_data(branch_id, subject, grade):
    num_students = 50  # Assume 50 students for each grade
    performance = []
    
    for _ in range(num_students):
        performance.append(random.choice(["Yes", "No"]))
    
    return performance

# Function to display performance analysis with grade distribution
def performance_analysis(branch_id, selected_subject, selected_grade):
    # Fetch or simulate performance data
    performance_data = get_performance_data(branch_id, selected_subject, selected_grade)
    
    # Create a DataFrame to count "Yes" and "No" distributions
    performance_df = pd.DataFrame(performance_data, columns=["Performance"])
    performance_count = performance_df["Performance"].value_counts().reset_index()
    performance_count.columns = ["Result", "Count"]
    
    # Plotting the distribution using a bar chart
    fig = px.bar(performance_count, x="Result", y="Count", 
                 title=f"Performance Distribution for {selected_subject} - Grade {selected_grade}",
                 labels={"Result": "Pass/Fail", "Count": "Number of Students"},
                 color="Result", color_discrete_map={"Yes": "green", "No": "red"})
    st.plotly_chart(fig)

    # Display the Performance Data in a table format
    st.subheader(f"Grade Distribution for {selected_subject} - Grade {selected_grade}")
    
    # Adding "Yes" and "No" counts to the table
    performance_table = pd.DataFrame({
        "Result": ["Yes", "No"],
        "Count": [performance_count[performance_count["Result"] == "Yes"]["Count"].sum(),
                  performance_count[performance_count["Result"] == "No"]["Count"].sum()]
    })

    # Display the performance table
    st.table(performance_table)

# Function to display most active chapters
def most_active_chapters(branch_id, selected_subject, selected_grade):
    active_data = get_active_chapters_topics(branch_id, selected_subject, selected_grade)
    chapters_data = active_data["Chapters"]
    
    # Creating a DataFrame for most active chapters
    chapters_df = pd.DataFrame(chapters_data)
    
    # Sorting by active count to display most active chapters
    chapters_df = chapters_df.sort_values(by="Active Count", ascending=False)
    
    # Displaying table for most active chapters
    with st.expander("Most actvie chapters"):
        st.subheader(f"Most Active Chapters for {selected_subject} - Grade {selected_grade}")
        st.table(chapters_df)

# Function to display most active topics
def most_active_topics(branch_id, selected_subject, selected_grade):
    active_data = get_active_chapters_topics(branch_id, selected_subject, selected_grade)
    topics_data = active_data["Topics"]
    
    # Creating a DataFrame for most active topics
    topics_df = pd.DataFrame(topics_data)
    
    # Sorting by active count to display most active topics
    topics_df = topics_df.sort_values(by="Active Count", ascending=False)
    
    # Displaying table for most active topics
    with st.expander("Most actvie topics"):
        st.subheader(f"Most Active Topics for {selected_subject} - Grade {selected_grade}")
        st.table(topics_df)

# Function to simulate getting active chapters and topics data
def get_active_chapters_topics(branch_id, selected_subject, selected_grade):
    # Simulated data for chapters and topics with active counts
    active_data = {
        "Chapters": [
            {"Chapter": "Algebra", "Active Count": random.randint(5, 20)},
            {"Chapter": "Geometry", "Active Count": random.randint(5, 20)},
            {"Chapter": "Calculus", "Active Count": random.randint(5, 20)},
            {"Chapter": "Statistics", "Active Count": random.randint(5, 20)},
            {"Chapter": "Trigonometry", "Active Count": random.randint(5, 20)}
        ],
        "Topics": [
            {"Topic": "Linear Equations", "Active Count": random.randint(5, 20)},
            {"Topic": "Polynomials", "Active Count": random.randint(5, 20)},
            {"Topic": "Quadratic Equations", "Active Count": random.randint(5, 20)},
            {"Topic": "Factorization", "Active Count": random.randint(5, 20)},
            {"Topic": "Functions", "Active Count": random.randint(5, 20)}
        ]
    }
    return active_data

# Sidebar options for subject and grade selection
def sidebar_selection():
    selected_subject = st.sidebar.selectbox("Select Subject", ["Math", "Physics", "Chemistry", "Biology"])
    selected_grade = st.sidebar.selectbox("Select Grade", ["1", "2", "3", "4"])
    return selected_subject, selected_grade

# Example usage in the display branch dashboard function
def display_branch_dashboard(branch_id):
    selected_subject, selected_grade = sidebar_selection()

    # Get branch info
    branch_info = fetch_overview_statistics(branch_id)
    
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

    # Plotly Overview Statistics
    overview_data = {'Categories': ['Sections'], 'Counts': [branch_info['sections']]}
    overview_df = pd.DataFrame(overview_data)
    fig = px.bar(overview_df, x='Categories', y='Counts', 
                 title=f"Sections Overview for {branch_name}",
                 labels={'Categories': 'Category', 'Counts': 'Count'},
                 color='Counts', color_continuous_scale='Viridis', hover_name="Counts")
    st.plotly_chart(fig)

    # Teacher Distribution per Grade and Subject
    teacher_distribution(branch_id, selected_grade, selected_subject)
    
    # Subject-wise Structure Analysis
    display_subject_structure(selected_subject)

    # Performance Analysis
    performance_analysis(branch_id, selected_subject, selected_grade)

    # Display Most Active Chapters
    most_active_chapters(branch_id, selected_subject, selected_grade)

    # Display Most Active Topics
    most_active_topics(branch_id, selected_subject, selected_grade)

# Function to display the subject structure
def display_subject_structure(subject):
    subject_data = subject_structure(subject)
    chapters = subject_data["Chapters"]

    # Prepare data for sunburst chart
    sunburst_data = []
    for chapter in chapters:
        chapter_name = chapter["Chapter"]
        for subtopic in chapter["Subtopics"]:
            sunburst_data.append({
                "Chapter": chapter_name,
                "Subtopic": subtopic,
                "Level": "Subtopic"
            })
            sunburst_data.append({
                "Chapter": chapter_name,
                "Subtopic": subtopic,
                "Level": "Chapter"
            })

    # Create a DataFrame for the sunburst chart
    sunburst_df = pd.DataFrame(sunburst_data)

    # Create sunburst chart using Plotly
    fig = px.sunburst(sunburst_df, 
                      path=['Chapter', 'Subtopic'],
                      title=f"Subject Structure for {subject}",
                      labels={'Chapter': 'Chapter', 'Subtopic': 'Subtopic'},
                      color='Level',
                      color_discrete_map={'Chapter': 'blue', 'Subtopic': 'orange'})
    
    # Display the sunburst chart
    st.plotly_chart(fig)

# Function to get subject structure (chapters and subtopics)
def subject_structure(subject):
    subject_data = {
        "Math": {
            "Chapters": [
                {"Chapter": "Algebra", "Subtopics": ["Linear Equations", "Polynomials", "Quadratic Equations", "Factorization", "Functions", "Graphing", "Inequalities", "Exponents"]},
                {"Chapter": "Geometry", "Subtopics": ["Angles", "Triangles", "Circles", "Parallel Lines", "Perimeter", "Area", "Volume", "3D Shapes"]},
                {"Chapter": "Calculus", "Subtopics": ["Limits", "Derivatives", "Integrals", "Differentiation", "Chain Rule", "Integration Techniques", "Fundamental Theorem", "Applications of Calculus"]},
                {"Chapter": "Statistics", "Subtopics": ["Mean", "Median", "Mode", "Probability", "Standard Deviation", "Variance", "Normal Distribution", "Hypothesis Testing"]},
                {"Chapter": "Trigonometry", "Subtopics": ["Trigonometric Functions", "Pythagorean Theorem", "Sine and Cosine", "Angle Sum Identities", "Graphs of Trigonometric Functions", "Inverse Trigonometric Functions", "Law of Sines", "Law of Cosines"]}
            ]
        },
        "Physics": {
            "Chapters": [
                {"Chapter": "Mechanics", "Subtopics": ["Force", "Motion", "Newton's Laws", "Work and Energy", "Conservation Laws", "Rotational Motion", "Linear Momentum", "Friction"]},
                {"Chapter": "Thermodynamics", "Subtopics": ["Heat", "Temperature", "Laws of Thermodynamics", "Entropy", "Work Done by Gases", "Ideal Gas Laws", "Carnot Engine", "Specific Heat"]},
                {"Chapter": "Electromagnetism", "Subtopics": ["Electric Field", "Magnetic Field", "Coulomb's Law", "Faraday's Law", "Ampere's Law", "Magnetic Forces", "Electromagnetic Waves", "Capacitance"]},
                {"Chapter": "Optics", "Subtopics": ["Reflection", "Refraction", "Lenses", "Mirrors", "Optical Instruments", "Interference", "Diffraction", "Polarization"]},
                {"Chapter": "Modern Physics", "Subtopics": ["Quantum Mechanics", "Relativity", "Atomic Models", "Photoelectric Effect", "Nuclear Physics", "Particle Physics", "Fission and Fusion", "Radioactivity"]}
            ]
        },
        "Chemistry": {
            "Chapters": [
                {"Chapter": "Organic Chemistry", "Subtopics": ["Hydrocarbons", "Alcohols", "Aldehydes", "Ketones", "Carboxylic Acids", "Amines", "Polymers", "Organic Reactions"]},
                {"Chapter": "Inorganic Chemistry", "Subtopics": ["Periodic Table", "Atomic Structure", "Ionic Bonds", "Covalent Bonds", "Acids and Bases", "Oxidation and Reduction", "Transition Metals", "Coordination Compounds"]},
                {"Chapter": "Physical Chemistry", "Subtopics": ["Thermodynamics", "Reaction Kinetics", "Electrochemistry", "Chemical Equilibria", "Colligative Properties", "Solubility", "Rates of Reactions", "Catalysis"]},
                {"Chapter": "Analytical Chemistry", "Subtopics": ["Qualitative Analysis", "Quantitative Analysis", "Spectroscopy", "Chromatography", "Electrochemical Analysis", "Gravimetric Analysis", "Titration", "Analysis Techniques"]},
                {"Chapter": "Biochemistry", "Subtopics": ["Carbohydrates", "Proteins", "Lipids", "Enzymes", "DNA", "RNA", "Metabolism", "Vitamins and Minerals"]}
            ]
        },
        "Biology": {
            "Chapters": [
                {"Chapter": "Cell Biology", "Subtopics": ["Cell Structure", "Cell Membrane", "Mitochondria", "Nucleus", "Chloroplasts", "Endoplasmic Reticulum", "Ribosomes", "Golgi Apparatus"]},
                {"Chapter": "Genetics", "Subtopics": ["DNA", "RNA", "Genetic Code", "Gene Expression", "Mutations", "Mendelian Inheritance", "Genetic Disorders", "Chromosomes"]},
                {"Chapter": "Ecology", "Subtopics": ["Ecosystem", "Food Chains", "Energy Flow", "Biomes", "Biodiversity", "Conservation", "Human Impact", "Population Dynamics"]},
                {"Chapter": "Human Physiology", "Subtopics": ["Digestive System", "Respiratory System", "Circulatory System", "Nervous System", "Excretory System", "Endocrine System", "Muscular System", "Reproductive System"]},
                {"Chapter": "Plant Biology", "Subtopics": ["Photosynthesis", "Plant Structure", "Plant Growth", "Reproduction", "Transport in Plants", "Plant Hormones", "Plant Diseases", "Agriculture"]}
            ]
        }
    }
    return subject_data.get(subject, {"Chapters": []})

