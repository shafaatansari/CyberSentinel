# CyberSentinel 🛡️

CyberSentinel is a personal cybersecurity monitoring platform built with Python, Flask, and SQLite.

The project focuses on defensive security monitoring, basic threat detection, authentication security, and security analysis through a web-based dashboard.

## 🚀 Features

- 🔐 User authentication with password hashing
- 🚨 Automated security alerts
- 📋 Security event monitoring
- 🔑 Password strength analysis
- 🌐 Suspicious URL analysis
- 🛡️ File integrity monitoring using SHA-256
- 📊 Security score calculation
- ⚙️ User settings
- 🧪 Automated security tests
- 🔒 Environment-based secret configuration

## 🧰 Tech Stack

- Python
- Flask
- SQLite
- HTML
- CSS
- JavaScript
- pytest
- python-dotenv

## 🏗️ Project Architecture

```text
CyberSentinel/
├── app/
│   ├── routes/
│   │   ├── auth.py
│   │   ├── alerts.py
│   │   ├── events.py
│   │   ├── password.py
│   │   ├── url_analyzer.py
│   │   ├── file_integrity.py
│   │   └── security_score.py
│   │
│   ├── services/
│   │   ├── database.py
│   │   ├── database_init.py
│   │   ├── event_service.py
│   │   ├── alert_service.py
│   │   ├── password_service.py
│   │   ├── url_analyzer.py
│   │   ├── file_integrity.py
│   │   └── security_score.py
│   │
│   ├── utils/
│   │   └── auth.py
│   │
│   ├── templates/
│   └── static/
│
├── tests/
│   └── test_security.py
│
├── instance/
├── app.py
├── config.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## 🔐 Security Features

### Authentication

- Passwords are stored using secure password hashing.
- Protected routes require authentication.
- Login and logout activity is recorded.
- Failed login attempts are monitored.

### Security Alerts

CyberSentinel detects repeated failed login attempts and generates security alerts when suspicious authentication activity is detected.

### Password Security

The password analyzer evaluates:

- Password length
- Uppercase characters
- Lowercase characters
- Numbers
- Special characters

It provides a strength classification and improvement suggestions.

### URL Analysis

The URL analyzer checks for basic suspicious indicators such as:

- Missing HTTPS
- IP-address-based URLs
- `@` characters in URLs
- Unusually long URLs
- Excessive subdomains

### File Integrity Monitoring

Files are monitored using **SHA-256 cryptographic hashes**.

The system creates a baseline hash and compares future uploads against that baseline to detect modifications.

### Security Score

CyberSentinel calculates a security score using:

- Security events
- Security alerts
- Recent failed login attempts

The score is displayed on the dashboard and dedicated security score page.

## 🧪 Testing

The project includes automated tests using `pytest`.

Current test coverage includes:

- Password strength analysis
- URL analysis
- SHA-256 file hashing
- File integrity verification
- Security score calculation

Run tests with:

```bash
python -m pytest
```

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/shafaatansari/CyberSentinel.git
cd CyberSentinel
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the virtual environment

Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure environment variables

Create a `.env` file in the project root:

```text
SECRET_KEY=your-secret-key
```

A template is provided in `.env.example`.

### 6. Run the application

```bash
python app.py
```

Open:

```text
http://127.0.0.1:5000
```

## 📁 Security & Git

The project keeps sensitive and generated files out of version control.

Excluded files include:

- `.env`
- SQLite database files
- Python virtual environment
- Python cache files

Environment configuration is provided through `.env.example`.

## 📌 Project Status

CyberSentinel is an ongoing personal cybersecurity project focused on defensive security monitoring, detection, and analysis.

Future improvements may include additional monitoring modules, expanded test coverage, and enhanced security analysis.

## 👨‍💻 Developer

**Shafaat Ansari**

GitHub:  
https://github.com/shafaatansari