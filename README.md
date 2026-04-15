# IoT Monitoring Platform

A Flask-based web application for monitoring IoT devices.

---

# 📚 Table of Contents

* [Project Description](#-project-description)
* [Technologies](#-technologies)
* [Project Structure](#-project-structure)
* [Application Routes](#-application-routes)
* [Login Credentials](#-login-credentials)
* [Installation](#-installation)
* [How to Run](#-how-to-run)
* [Future Improvements](#-future-improvements)
* [Contributors](#-contributors)

---

# 📖 Project Description

This project implements the **Milestone 1** requirements of a Flask web application.

The goal is to build a **functional Flask skeleton** that includes:

* Proper project structure
* Flask routing
* Templates with Jinja
* Session-based authentication
* Role-based dashboards (Admin / User)

For this milestone **no database is used**. Authentication uses **hardcoded credentials**.

Database integration with **MySQL will be added in Milestone 2**.

---

# 🛠 Technologies

* Python 
* HTML5
* CSS
  
---

# 📂 Project Structure

```
IoT-Monitoring-Platform
│
├── app.py
├── config.py
├── requirements.txt
├── .gitignore
│
├── templates
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   │
│   ├── user
│   │   └── dashboard.html
│   │
│   └── admin
│       └── dashboard.html
│
└── static
    ├── style.css
    ├── images
    └── js
```

---

# 🔗 Application Routes

| Route              | Method | Description        |
| ------------------ | ------ | ------------------ |
| `/`                | GET    | Homepage           |
| `/login`           | GET    | Login form         |
| `/login`           | POST   | Verify credentials |
| `/logout`          | GET    | Logout user        |
| `/user/dashboard`  | GET    | User dashboard     |
| `/admin/dashboard` | GET    | Admin dashboard    |

Protected routes require authentication.

---

# 🔑 Login Credentials

### Admin

```
username: admin
password: admin123
```

### User

```
username: user
password: user123
```

After login:

* Admin → `/admin/dashboard`
* User → `/user/dashboard`

---

# ⚙ Installation

Clone the repository:

```
git clone https://github.com/YOUR_USERNAME/IoT-Monitoring-Platform.git
```

Navigate into the folder:

```
cd IoT-Monitoring-Platform
```

Create virtual environment:

```
python3 -m venv venv
```

Activate environment:

Linux / Mac

```
source venv/bin/activate
```

Windows

```
venv\Scripts\activate
```

Install dependencies:

```
pip install -r requirements.txt
```

---

# ▶ How to Run

Run the Flask application:

```
python app.py
```

Open browser:

```
http://localhost:5000
```

---

---

# 👥 Contributors

* PanayiotisMel
* GianinaF
* ChrysovalantisEus
* Andronikos

---


