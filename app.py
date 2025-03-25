import os
import streamlit as st
import streamlit.components.v1 as components
import webbrowser
import subprocess

from frontend.frontend_dev import generate_frontend_code
from backend.backend_dev import generate_backend_code
from dsa.dsa_solver import solve_dsa_problem
from utils.code_execution import execute_python_code

# Streamlit UI
st.title("💻 AI Software Development Agent")

# Get API Key from user
api_key = st.text_input("Enter your Gemini API Key", type="password")
if api_key:
    os.environ["GOOGLE_API_KEY"] = api_key

# Task selection
task = st.selectbox("Select a task:", ["Frontend Development", "Backend Development", "DSA Problem Solving"])

if task == "Frontend Development":
    website_name = st.text_input("Enter website type (e.g., Portfolio, E-Commerce, Blog)")
    
    if st.button("Generate & Preview Website"):
        html_code = generate_frontend_code(website_name)
        
        # Save the HTML file
        with open("generated_site.html", "w") as f:
            f.write(html_code)
        
        # Preview HTML inside Streamlit
        st.subheader("Live Preview:")
        components.html(html_code, height=600, scrolling=True)

        # Open in browser option
        if st.button("Open in Browser"):
            webbrowser.open("generated_site.html")

elif task == "Backend Development":
    api_description = st.text_area("Describe your API requirements")
    
    if st.button("Generate API Code"):
        backend_code = generate_backend_code(api_description)
        st.code(backend_code, language="python")

        # Save and execute the API code
        with open("generated_api.py", "w") as f:
            f.write(backend_code)
        
        # Run the API in the background
        subprocess.Popen(["python", "generated_api.py"])
        st.success("API is running! Test it on http://127.0.0.1:8000/docs")

elif task == "DSA Problem Solving":
    problem_statement = st.text_area("Describe your DSA problem")
    
    if st.button("Solve DSA Problem"):
        dsa_solution = solve_dsa_problem(problem_statement)
        st.code(dsa_solution, language="python")
        
        # Execute the DSA solution and print the result
        result = execute_python_code(dsa_solution)
        st.write("Output:", result)
