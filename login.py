import streamlit as st
import sqlite3
from database import init_db
from superadmin import superadmin_dashboards


# Custom CSS for styling the login page
custom_css = """
<style>
    .login-title {
        text-align: left;
        color: #b02a37;
        font-family: "Arial", sans-serif;
        font-size: 36px;
        font-weight: bold;
        margin-bottom: 20px;
    }

    .login-subtitle {
        text-align: left;
        color: #444444;
        font-family: "Arial", sans-serif;
        font-size: 20px;
        margin-bottom: 40px;
    }

    .login-container {
        max-width: 500px;
        margin: auto;
        padding: 30px;
        border: 1px solid #ddd;
        border-radius: 10px;
        box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
        background-color: #ffffff;
    }

    input {
        font-size: 18px;
        padding: 10px;
        border-radius: 5px;
        border: 1px solid #ccc;
    }

    .login-button {
        background-color: #b02a37;
        color: #ffffff;
        font-size: 18px;
        font-weight: bold;
        padding: 15px;
        border-radius: 5px;
        border: none;
        width: 100%;
        margin-top: 20px;
    }

    .login-button:hover {
        background-color: #92212f;
    }

    .error-message {
        color: #b02a37;
        font-weight: bold;
        margin-top: 15px;
    }

    .remember-me {
        margin-top: 15px;
    }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# Initialize page and role in session state if not present
if "page" not in st.session_state:
    st.session_state.page = "Login"
if "role" not in st.session_state:
    st.session_state.role = None

# Function to authenticate the user based on email and password
def authenticate_user(email, password):
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    
    cursor.execute("""
        SELECT role FROM user WHERE email = ? AND password = ?
    """, (email, password))
    result = cursor.fetchone()
    connection.close()
    
    if result:
        return result[0]  
    else:
        return None

# Function to handle login form
def login_form():
    st.markdown("<h1 class='login-title'>Indian Public High School</h1>", unsafe_allow_html=True)
    st.markdown("<h3 class='login-subtitle'>Login Portal</h3>", unsafe_allow_html=True)

    with st.form(key="login_form", clear_on_submit=False):
        col1, col2 = st.columns(2)
        with col1:
            st.text_input("Enter Your Email", placeholder="", key="email")
        with col2:
            st.text_input("Enter Your Password", placeholder="", type="password", key="password")

        remember_me = st.checkbox("Remember me", key="remember_me", help="Stay signed in on this device")
        
        submit_button = st.form_submit_button("Login", use_container_width=True)

        if submit_button:
            if not remember_me:
                st.markdown("<p class='error-message'>Please select 'Remember Me' to login.</p>", unsafe_allow_html=True)
                return
            
            role = authenticate_user(st.session_state.email, st.session_state.password)
            if role is None:
                st.markdown("<p class='error-message'>Invalid email or password. Please try again.</p>", unsafe_allow_html=True)
            else:
                st.session_state.role = role
                st.session_state.page = f"{role.capitalize()}Dashboard"
                st.success(f"Login successful! Welcome back, {role.capitalize()}!")

# Superadmin Dashboard
def superadmin_dashboard_page():
    if st.session_state.role != "superadmin":
        st.warning("You are not logged in as Superadmin. Please login first.")
        st.session_state.page = "Login"
        st.stop()

    superadmin_dashboards()

    if st.button("Logout"):
        logout()

# Branchadmin Dashboard
def branchadmin_dashboard_page():
    if st.session_state.role != "branchadmin":
        st.warning("You are not logged in as BranchAdmin. Please login first.")
        st.session_state.page = "Login"
        st.stop()

    # Import here to avoid circular imports
    from branchadmin import branchadmin_dashboard
    branchadmin_dashboard()

    if st.button("Logout"):
        logout()
  
# Teacher Dashboard
def teacher_dashboard_page():
    if st.session_state.role != "teacher":
        st.warning("You are not logged in as Teacher. Please login first.")
        st.session_state.page = "Login"
        st.stop()

    # Import here to avoid circular imports
    from teachers import teacher_dashboard
    teacher_dashboard()

    if st.button("Logout"):
        logout()

# Main function to drive the app
def main():
    init_db()  # Initialize the database if needed
    
    if st.session_state.page == "Login":
        login_form()
    elif st.session_state.page == "SuperadminDashboard":
        superadmin_dashboard_page()
    elif st.session_state.page == "BranchadminDashboard":
        branchadmin_dashboard_page()
    elif st.session_state.page == "TeacherDashboard":
        teacher_dashboard_page()

# Logout function
def logout():
    st.session_state.page = "Login"
    st.session_state.role = None

if __name__ == "__main__":
    main()
