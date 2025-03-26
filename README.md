# 🚀 AI Software Development Agent

## Complete Project Documentation


# 🚀 AI Software Development Agent

A comprehensive AI-powered application that assists with frontend development, backend API generation, and DSA problem-solving, built with security as a priority.

## 📌 Table of Contents
- [Features](#-features)
- [Security Features](#-security-features)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Usage](#-usage)
- [Project Structure](#-project-structure)
- [Technical Details](#-technical-details)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)
- [License](#-license)

## 🌟 Features

### 🌐 Frontend Development
- Generate complete HTML/CSS/JS code for various website types (portfolios, e-commerce sites, blogs, etc.)
- Live preview of generated websites directly in the application
- Secure HTML sanitization to prevent XSS attacks
- Easily open the generated sites in your default browser

### 🔧 Backend Development
- Generate complete API code based on natural language descriptions
- Automatic validation of code for security vulnerabilities
- Instant API deployment with interactive documentation
- Test your APIs directly from the application interface
- FastAPI documentation embedding (Swagger UI)

### 📊 DSA Problem Solving
- Solve complex data structure and algorithm problems
- Generate optimized solutions with explanations
- Secure code execution with proper sandboxing and timeouts
- View output directly in the interface

## 🔒 Security Features

The application implements multiple layers of security:

1. **Static Code Analysis**
   - Validation of all generated code before execution
   - Detection of dangerous modules, functions, and patterns
   - AST-based code inspection

2. **Secure Execution Environment**
   - Timeouts to prevent long-running operations
   - Resource limitation to prevent DoS attacks
   - Temporary file management with proper cleanup

3. **API Key Management**
   - Encryption of API keys using Fernet symmetric encryption
   - Keys stored only in session state, not in database or files
   - Environment variable management using dotenv

4. **Content Sanitization**
   - HTML sanitization to prevent XSS vulnerabilities
   - Input validation across all user-provided content

5. **Secure File Operations**
   - Atomic file operations to prevent race conditions
   - Temporary file usage for secure writes
   - Hashed filenames to prevent predictability
   - Proper cleanup of temporary resources

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- A Gemini API key from Google AI Studio

### Step-by-Step Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/ShawneilRodrigues/Software-Engineer-Agent.git
   cd Software-Engineer-Agent
   

2. **Create a virtual environment (recommended):**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment:**
   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - macOS and Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install required packages:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Create a .env file:**
   ```bash
   echo APP_SECRET_KEY=your_secret_key > .env
   ```
   Replace `your_secret_key` with a secure random string or use the one generated when you first run the application.

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the project root directory with the following variables:

```
APP_SECRET_KEY=your_generated_secret_key
```

If you don't set this variable, the application will generate a new key on startup and print it in the console. Copy this key to your `.env` file to maintain consistent encryption between restarts.

### API Key Requirements

You'll need a Gemini API key from Google AI Studio:
1. Go to https://makersuite.google.com/
2. Sign in with your Google account
3. Create an API key
4. Enter this key in the application sidebar when prompted

## 🏃‍♂️ Usage

### Running the Application

**Start the application:**
```bash
streamlit run app.py
```

The application will be available at `http://localhost:8501`

### Basic Workflow

1. **Enter your API key:**
   - Input your Gemini API key in the sidebar
   - The key will be encrypted and stored securely in your session

2. **Select your task:**
   - Frontend Development
   - Backend Development
   - DSA Problem Solving

3. **Enter requirements:**
   - Provide a description of what you want to generate
   - Be specific to get the best results

4. **Generate and interact:**
   - Click the generate button for your chosen task
   - Review the generated code
   - For frontend: preview and open in browser
   - For backend: test the deployed API
   - For DSA: view the solution and execution output

### Task-Specific Usage

#### Frontend Development
1. Enter a website type (e.g., "Portfolio website for a photographer")
2. Click "Generate & Preview Website"
3. View the live preview in the application
4. Click "Open in Browser" to see the full site in your browser

#### Backend Development
1. Describe your API requirements (e.g., "A REST API for a book inventory system with CRUD operations")
2. Click "Generate & Run API"
3. Review the generated code
4. If the code passes security validation, the API will automatically start
5. Use the provided links to test your API endpoints
6. Interact with the Swagger UI embedded in the application

#### DSA Problem Solving
1. Describe your algorithm problem (e.g., "Find the longest substring without repeating characters")
2. Click "Solve DSA Problem"
3. Review the solution code and explanation
4. View the execution output

## 📁 Project Structure

```
Software-Engineer-Agent/
│
├── app.py                  # Main application entry point
├── requirements.txt        # Required Python packages
├── .env                    # Environment variables (create this file)
├── .gitignore              # Git ignore file
├── Dockerfile              # Docker configuration (optional)
│
├── backend/                # Backend development module
│   └── backend_dev.py      # API code generation utilities
│
├── frontend/               # Frontend development module
│   └── frontend_dev.py     # Website generation utilities
│
├── dsa/                    # DSA problem-solving module
│   └── dsa_solver.py       # Algorithm problem solver
│
├── utils/                  # Utility functions
│   ├── code_execution.py   # Secure code execution utilities
│   ├── code_extractor.py   # Code extraction from AI responses
│   ├── code_validator.py   # Security validation for generated code
│   ├── secure_config.py    # Secure configuration management
│   └── port_utils.py       # Network port utilities
│
└── tests/                  # Unit and integration tests
```

## 🔍 Technical Details

### Security Implementation

#### Code Validation
The application uses AST (Abstract Syntax Tree) parsing to analyze generated code for security issues:
- Detection of dangerous modules like `os`, `subprocess`, etc.
- Identification of potentially harmful functions like `eval`, `exec`, etc.
- Pattern matching for obfuscated security bypasses

```python
# Example from code_validator.py
DANGEROUS_MODULES = {
    'os', 'subprocess', 'sys', 'shutil', 'requests', 'socket',
    'pickle', 'urllib', 'ftplib', 'telnetlib', 'smtplib'
}
```

#### API Key Encryption
The application uses Fernet symmetric encryption to protect API keys:
```python
# From secure_config.py
def encrypt(self, data):
    return self.cipher_suite.encrypt(data.encode()).decode()
```

### Backend API Deployment
The application dynamically finds available ports and runs generated APIs as subprocesses:
```python
available_port = find_available_port(8000, 9000)
api_process = subprocess.Popen(["python", filename], ...)
```

## 🔧 Troubleshooting

### Common Issues

1. **API Key Error:**
   - Make sure your Gemini API key is valid and has not expired
   - Check that you have sufficient quota remaining

2. **Port Already in Use:**
   - If the application can't find an available port, close other applications that might be using ports in the 8000-9000 range

3. **Security Validation Failures:**
   - If code generation fails security validation, try modifying your request to avoid asking for system access or dangerous operations

4. **Module Import Errors:**
   - Make sure you have installed all required dependencies with `pip install -r requirements.txt`

### Getting Help
If you encounter issues not covered here, please open an issue on GitHub with:
- A description of the problem
- Steps to reproduce
- Error messages (with sensitive information redacted)
- Your operating system and Python version

## 🚢 Containerization (Optional)

The application can be run in a Docker container for improved isolation:

1. **Build the Docker image:**
   ```bash
   docker build -t software-engineer-agent .
   ```

2. **Run the container:**
   ```bash
   docker run -p 8501:8501 software-engineer-agent
   ```

The application will be available at `http://localhost:8501`

## 📝 Contributing

Contributions to the project are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines
- Maintain the existing security measures
- Add tests for new features
- Follow PEP 8 style guidelines
- Document new functions and features

## 🔒 Security Notice

While this application includes security measures, please use caution when running generated code, especially in production environments. Always review generated code before deploying to critical systems.

## 📜 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

Developed with ❤️ by ShawneilRodrigues

Last updated: 2025-03-26
```

This comprehensive README provides complete documentation for your AI Software Development Agent project, including detailed installation instructions, usage guides, security features, and troubleshooting information. It's structured to be both informative for new users and helpful for developers who might want to contribute to or modify the project.
