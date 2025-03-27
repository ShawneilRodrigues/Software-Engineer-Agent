import subprocess
import tempfile
import os
from .code_validator import validate_code

def execute_python_code(code, timeout=5):
    """
    Securely executes Python code after validation
    
    Args:
        code (str): Python code to execute
        timeout (int): Maximum execution time in seconds
        
    Returns:
        str: Output from code execution
    """
    # First validate the code for security issues
    is_valid, issues = validate_code(code)
    
    if not is_valid:
        return f"Security validation failed:\n" + "\n".join(issues)
    
    # Create a temporary file for execution
    with tempfile.NamedTemporaryFile(suffix='.py', delete=False) as temp_file:
        temp_file_path = temp_file.name
        temp_file.write(code.encode('utf-8'))
    
    try:
        # Execute with restrictions and timeout
        result = subprocess.run(
            ['python', temp_file_path],
            capture_output=True,
            text=True,
            timeout=timeout
        )
        
        # Return output or error
        if result.returncode == 0:
            return result.stdout
        else:
            return f"Execution error:\n{result.stderr}"
    except subprocess.TimeoutExpired:
        return "Execution timed out"
    finally:
        # Clean up temporary file
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)