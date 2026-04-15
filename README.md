Περιγραφή Έργου

Το παρόν project αποτελεί την υλοποίηση του Milestone 1 

Στόχος του Milestone 1 είναι η δημιουργία ενός λειτουργικού Flask skeleton με σωστή δομή αρχείων, routes, templates και βασικό σύστημα authentication.

Σε αυτό το στάδιο δεν χρησιμοποιείται βάση δεδομένων. Το login υλοποιείται με hardcoded credentials και χρήση Flask sessions για τη διαχείριση των χρηστών.

Στο Milestone 2 το σύστημα θα επεκταθεί με βάση δεδομένων MySQL.

 Project Description

This project is the Milestone 1 implementation 
The goal of this milestone is to create a functional Flask skeleton with proper project structure, routing, templates, and authentication logic.

At this stage the application does not use a database. Authentication is implemented using hardcoded credentials and Flask sessions.

In Milestone 2, the application will be extended with a MySQL database.

Τεχνολογίες / Technologies

Python 
java script
HTML
CSS

Δομή Project / Project Structure

IoT-Monitoring-Platform
│
├── app.py
├── config.py
├── requirements.txt
├── .gitignore
│
├── templates
│   ├── alerts.html
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   │
│   ├── user
│   │   └── dashboard.html
│   │       └── devices.html
│   │
│   └── admin
│       └── dashboard.html
│        └── devices.html
│
└── static
    ├── style.css
    ├── script.js
    └── data.json
    └── image
        └── alerts-bg.jpg
        └── devices.bg
        └── iot-bg.jpg


Routes της εφαρμογής / Application Routes

Route	Method	Description
/	GET	Homepage / Αρχική σελίδα
/login	GET	Login form
/login	POST	Verify credentials
/logout	GET	Logout user
/user/dashboard	GET	User dashboard (protected)
/admin/dashboard	GET	Admin dashboard (protected)
