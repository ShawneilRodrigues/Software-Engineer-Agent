# main.py
import os
import streamlit as st
import streamlit.components.v1 as components
import webbrowser
import traceback
import re
import tempfile
import hashlib
import time
import socket
import subprocess
from dotenv import load_dotenv

# Rest of your imports...
from utils.port_utils import find_available_port

# Load environment variables from .env file
load_dotenv()

from frontend.frontend_dev import generate_frontend_code
from backend.backend_dev import generate_backend_code
from dsa.dsa_solver import solve_dsa_problem
from utils.code_execution import execute_python_code
from utils.code_extractor import extract_code_block
from utils.code_validator import validate_code
from utils.secure_config import SecureConfig

# Initialize secure configuration
secure_config = SecureConfig()

def main():
    # Set page configuration
    st.set_page_config(
        page_title="AI Software Development Agent", 
        page_icon="💻", 
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Custom CSS for improved styling
    st.markdown("""
    <style>
    .main-container {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border: none;
        padding: 10px 20px;
        border-radius: 5px;
        transition: background-color 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    .code-output {
        background-color: #f4f4f4;
        border-radius: 5px;
        padding: 10px;
        max-height: 400px;
        overflow-y: auto;
    }
    </style>
    """, unsafe_allow_html=True)

    # Initialize session state
    if 'api_key_set' not in st.session_state:
        st.session_state.api_key_set = False

    # Main title with custom styling
    st.markdown("<h1 style='text-align: center; color: #2C3E50;'>🚀 AI Software Development Agent</h1>", unsafe_allow_html=True)

    # Sidebar for API Key and task selection
    with st.sidebar:
        st.header("Configuration")
        api_key = st.text_input("Enter your Gemini API Key", type="password")
        if api_key:
            # Securely store API key
            secure_config.store_api_key(st.session_state, api_key)
            st.session_state.api_key_set = True
            
            # Set the API key for current session
            retrieved_api_key = secure_config.get_api_key(st.session_state)
            if retrieved_api_key:
                os.environ["GOOGLE_API_KEY"] = retrieved_api_key

        task = st.selectbox("Select a task:", [
            "Frontend Development", 
            "Backend Development", 
            "DSA Problem Solving"
        ])

    # Main content area
    st.markdown('<div class="main-container">', unsafe_allow_html=True)

    # Task-specific sections with error handling
    try:
        if task == "Frontend Development":
            frontend_development()
        elif task == "Backend Development":
            backend_development()
        elif task == "DSA Problem Solving":
            dsa_problem_solving()
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        # Only log the full traceback, don't show it to users
        print(traceback.format_exc())

    st.markdown('</div>', unsafe_allow_html=True)

def sanitize_html(html_content):
    """
    Sanitize HTML content to prevent XSS attacks
    """
    # Basic sanitization - in production use a proper HTML sanitizer library
    # This is a simplified example
    html_content = re.sub(r'<script.*?>.*?</script>', '', html_content, flags=re.DOTALL)
    html_content = re.sub(r'javascript:', '', html_content, flags=re.IGNORECASE)
    html_content = re.sub(r'on\w+\s*=', '', html_content, flags=re.IGNORECASE)
    return html_content

def write_file_securely(content, filename, file_type="txt"):
    """
    Write content to a file securely, with proper validation
    """
    # For Python code, validate before writing
    if file_type == "python":
        is_valid, issues = validate_code(content)
        if not is_valid:
            return False, issues
    
    # Use temporary file for secure writing
    try:
        with tempfile.NamedTemporaryFile(delete=False) as temp:
            temp_name = temp.name
            temp.write(content.encode('utf-8'))
        
        # Move to final location
        os.replace(temp_name, filename)
        return True, None
    except Exception as e:
        return False, [str(e)]

def frontend_development():
    st.subheader("🌐 Frontend Website Generation")
    
    # Input and validation
    website_name = st.text_input("Enter website type (e.g., Portfolio, E-Commerce, Blog)")
    
    if st.button("Generate & Preview Website"):
        if not website_name:
            st.warning("Please enter a website type.")
            return

        with st.spinner("Generating frontend code..."):
            try:
                # Generate the full HTML response
                html_response = generate_frontend_code(website_name)
                
                # Extract only the HTML code
                html_code = extract_code_block(html_response, 'html')
                
                # Sanitize the HTML before displaying
                sanitized_html = sanitize_html(html_code)
                
                # Hash as filename for security
                filename = f"generated_site_{hashlib.md5(website_name.encode()).hexdigest()}.html"
                
                # Securely write to file
                success, issues = write_file_securely(sanitized_html, filename, "html")
                if not success:
                    st.error(f"Failed to save HTML file: {issues}")
                    return
                
                # Display preview using components.html with height limit
                st.subheader("Live Preview:")
                components.html(sanitized_html, height=600, scrolling=True)

                # Browser opening with error handling
                if st.button("Open in Browser"):
                    try:
                        webbrowser.open("file://" + os.path.abspath(filename))
                    except Exception as e:
                        st.error(f"Could not open browser: {str(e)}")

            except Exception as e:
                st.error(f"Error generating frontend code: {str(e)}")
                # Log the full traceback but don't display it
                print(traceback.format_exc())

def backend_development():
    st.subheader("🔧 Backend API Generation")
    
    api_description = st.text_area("Describe your API requirements")
    
    if st.button("Generate & Run API"):
        if not api_description:
            st.warning("Please provide API requirements.")
            return

        with st.spinner("Generating and launching backend code..."):
            try:
                # Generate the full backend code response
                backend_response = generate_backend_code(api_description)
                
                # Extract only the Python code
                backend_code = extract_code_block(backend_response, 'python')
                
                # Validate the code before displaying
                is_valid, issues = validate_code(backend_code)
                
                # Display code
                st.code(backend_code, language="python")
                
                if not is_valid:
                    st.error("Security issues detected in generated code:")
                    for issue in issues:
                        st.error(f"- {issue}")
                    return
                
                # Hash as filename for security
                filename = f"generated_api_{hashlib.md5(api_description.encode()).hexdigest()}.py"
                
                # Securely write to file
                success, issues = write_file_securely(backend_code, filename, "python")
                if not success:
                    st.error(f"Failed to save Python file: {issues}")
                    return
                
                # Execute the API in a separate process with a port checker
                available_port = find_available_port(8000, 9000)
                if available_port:
                    # Modify the code to use the available port if needed
                    if 'uvicorn.run' in backend_code:
                        # Attempt to modify the port in the code
                        modified_code = re.sub(
                            r'uvicorn\.run\(app,\s*host=["\']0\.0\.0\.0["\'],\s*port=\d+',
                            f'uvicorn.run(app, host="0.0.0.0", port={available_port}',
                            backend_code
                        )
                        # Write the modified code back to the file
                        success, issues = write_file_securely(modified_code, filename, "python")
                        if not success:
                            st.error(f"Failed to update port in API file: {issues}")
                            return
                
                    # Launch the API in a separate process
                    api_process = subprocess.Popen(
                        ["python", filename],
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        text=True
                    )
                    
                    # Wait a short time for the API to start
                    time.sleep(3)
                    
                    # Check if the process is still running
                    if api_process.poll() is None:
                        # Process is still running, API likely started successfully
                        st.success(f"🚀 API is running! You can test it at:")
                        api_url = f"http://localhost:{available_port}"
                        st.markdown(f"**API Base URL:** [{api_url}]({api_url})")
                        
                        # If FastAPI is detected, add a link to the docs
                        if "fastapi" in backend_code.lower():
                            docs_url = f"{api_url}/docs"
                            st.markdown(f"**Swagger UI:** [{docs_url}]({docs_url})")
                            
                            # Embed the Swagger UI in an iframe
                            st.subheader("API Documentation:")
                            components.iframe(docs_url, height=600, scrolling=True)
                    else:
                        # Process terminated, get the error
                        stdout, stderr = api_process.communicate()
                        st.error("API failed to start:")
                        st.code(stderr or stdout)
                else:
                    st.error("Could not find an available port to run the API.")

            except Exception as e:
                st.error(f"Error generating or running backend code: {str(e)}")
                # Log the full traceback but don't display it
                print(traceback.format_exc())

def dsa_problem_solving():
    st.subheader("📊 DSA Problem Solver")
    
    problem_statement = st.text_area("Describe your DSA problem")
    
    if st.button("Solve DSA Problem"):
        if not problem_statement:
            st.warning("Please provide a problem statement.")
            return

        with st.spinner("Solving DSA problem..."):
            try:
                # Generate the full DSA solution response
                dsa_response = solve_dsa_problem(problem_statement)
                
                # Extract only the Python code
                dsa_solution = extract_code_block(dsa_response, 'python')
                
                # Validate the code
                is_valid, issues = validate_code(dsa_solution)
                
                # Display code
                st.code(dsa_solution, language="python")
                
                if not is_valid:
                    st.error("Security issues detected in generated code:")
                    for issue in issues:
                        st.error(f"- {issue}")
                    return
                
                # Execute solution with error handling and timeout
                result = execute_python_code(dsa_solution, timeout=5)
                st.subheader("Output:")
                st.code(result)

            except Exception as e:
                st.error(f"Error solving DSA problem: {str(e)}")
                # Log the full traceback but don't display it
                print(traceback.format_exc())

if __name__ == "__main__":
    main()