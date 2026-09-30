# Enterprise Biometric E-Voting System

[![System Status](https://img.shields.io/badge/Status-Operational-brightgreen.svg)](#)
[![Security Level](https://img.shields.io/badge/Security-AES--256-blue.svg)](#)
[![Python Version](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](#)
[![Django Version](https://img.shields.io/badge/Django-4.2-green.svg)](#)

A high-security, zero-trust digital election platform backed by optical iris pattern matching and cryptographic ballot verification. This system ensures 100% tamper-proof elections, real-time vote tallying, and maximum voter transparency.

## 🚀 Key Features

*   **Biometric Iris Authentication**: Advanced computer-vision pattern comparison for voter validation (replaces traditional password-only sign-ins).
*   **Cryptographic Audit Ledger**: Secure, encrypted single-vote transaction protocol to prevent ballot tampering.
*   **Real-time Analytics Dashboard**: Executive control dashboard for election commissioners to monitor live distribution analytics.
*   **Secure Admin Portal**: Granular access control for managing candidates, polling positions, and election configurations.
*   **Certified PDF Reporting**: Automated generation of cryptographically signed election result exports.

## 🛠️ Technology Stack

*   **Backend**: Python, Django 4.2
*   **Frontend**: Tailwind CSS, Glassmorphism UI, Chart.js
*   **Biometrics Processing**: Pillow (Python Imaging Library)
*   **Database**: SQLite (Development) / PostgreSQL (Production ready)
*   **Deployment**: Vercel Serverless Functions

## 💻 Local Setup & Installation

### Prerequisites
*   Python 3.9+
*   Git

### Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/guruvishnuk/Secure-e-voting-system-using-iris-recognization.git
   cd Secure-e-voting-system-using-iris-recognization
   ```

2. **Set up virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run database migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Start the secure server**
   ```bash
   python manage.py runserver
   ```
   *The application will be live at `http://localhost:8000`*

## 🔒 Security & Compliance

This platform enforces strict security guidelines:
*   Strict RBAC (Role-Based Access Control) separating Voters and Election Administrators.
*   Biometric iris templates are temporarily processed in-memory and immediately destroyed after structural comparison to comply with PII handling standards.
*   CSRF & XSS protection enabled globally via Django's security middleware.

## 👨‍💻 Developer

**Developed by [@guruvishnuk](https://github.com/guruvishnuk)**

---
*&copy; 2026 Election Commission Security Operations. All Rights Reserved.*
