# 🛡️ TechNexus - Enterprise IT Helpdesk System

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Django](https://img.shields.io/badge/Django-5.0-green)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5-purple)

**TechNexus** is a full-stack enterprise ticketing system designed to streamline IT support operations. It features a secure, role-based architecture connecting End Users, Support Engineers, and Administrators.

---

## 🚀 Key Features

### 🔐 Role-Based Access Control (RBAC)
* **Administrators:** Full system oversight, user approvals, ticket assignment, and analytics dashboards.
* **Engineers:** Dedicated workspace to view assigned tasks and update ticket statuses.
* **End Users:** Self-service portal to log issues, track history, and receive updates.

### 🎫 Intelligent Ticketing
* **Lifecycle Management:** Track tickets from `Open` → `In Progress` → `Resolved`.
* **Priority Levels:** Classify issues by Severity (High/Medium/Low).
* **Real-time Collaboration:** Integrated comment threads allow communication between users and engineers.

### 🤖 TechNexus AI Assistant
* Built-in **Virtual Assistant** for instant navigation and troubleshooting.
* Provides automated solutions for common issues (e.g., Password Resets, Wi-Fi connectivity).

### 📊 Analytics Dashboard
* Visualizes ticket distribution by Priority and Status using **Chart.js**.

---

## 🛠️ Technology Stack
* **Backend:** Python, Django 5.0
* **Frontend:** HTML5, CSS3, Bootstrap 5, JavaScript
* **Database:** SQLite (Development)
* **Visualization:** Chart.js

---

## ⚙️ Installation

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/jayasoorya-kr/TechNexus-Helpdesk.git](https://github.com/jayasoorya-kr/TechNexus-Helpdesk.git)
    ```
2.  **Install Dependencies:**
    ```bash
    pip install django
    ```
3.  **Run Migrations & Server:**
    ```bash
    python manage.py migrate
    python manage.py runserver
    ```