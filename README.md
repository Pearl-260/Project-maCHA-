# maCHA Management System

> A modern web-based Chama (Savings & Investment Group) Management System built using **Python**, **Flask**, **SQLite**, **HTML5**, **CSS3**, and **JavaScript**.

---

## Table of Contents

- About the Project
- Features
- Technologies Used
- System Modules
- Installation
- Usage
- Project Structure
- Database
- Future Improvements
- Author
- License

---

## About the Project

The maCHA Management System is designed to simplify the management of Chama (Savings and Investment Groups). It enables administrators to manage members, groups, contributions, loans, payouts, reports, notifications, and system settings through an easy-to-use web interface.

The system improves efficiency by replacing manual record keeping with a secure digital platform.

---

## Features

- Secure User Login
- User Registration
- Dashboard Overview
- Member Management
- Group Management
- Contributions Tracking
- Loan Management
- Payout Management
- Reports Generation
- Notifications
- System Settings
- SQLite Database Integration

---

## Technologies Used

### Backend
- Python
- Flask
- Flask-SQLAlchemy

### Frontend
- HTML5
- CSS3
- JavaScript

### Database
- SQLite

### Development Tools
- Visual Studio Code
- Git
- GitHub

---

## System Modules

### Authentication
- User Login
- User Registration
- Logout

### Dashboard
Displays system statistics and quick navigation.

### Members
- Add Members
- Edit Members
- Delete Members
- View Members

### Groups
- Create Groups
- Manage Group Members

### Contributions
- Record Contributions
- View Contribution History

### Loans
- Apply for Loans
- Track Loan Status

### Payouts
- Manage Member Payouts

### Reports
Generate reports for:
- Members
- Contributions
- Loans
- Payouts

### Notifications
- Contribution Reminders
- Meeting Notifications
- Payout Alerts

### Settings
Manage:
- Theme
- Date Format
- Notification Preferences

---

## Installation

1. Clone the repository.

```
git clone <repository-url>
```

2. Open the project in Visual Studio Code.

3. Create a virtual environment.

```
python -m venv .venv
```

4. Activate the virtual environment.

Windows:

```
.venv\Scripts\activate
```

5. Install dependencies.

```
pip install -r requirements.txt
```

6. Run the application.

```
python run.py
```

7. Open your browser and visit:

```
http://127.0.0.1:5000
```

---

## Usage

1. Register a new account.
2. Login to the system.
3. Create groups.
4. Add members.
5. Record contributions.
6. Manage loans.
7. Generate reports.
8. Manage payouts.
9. Configure system settings.

---

## Project Structure

```
maCHA_SYSTEM/
│
├── app/
│   ├── templates/
│   ├── static/
│   ├── models.py
│   ├── routes.py
│   └── __init__.py
│
├── run.py
├── requirements.txt
├── README.md
└── chama.db
```

---

## Database

The application uses **SQLite** for data storage.

Main tables include:

- Users
- Members
- Groups
- Contributions
- Loans
- Payouts
- Notifications
- System Settings

---

## Future Improvements

- Email Notifications
- SMS Notifications
- Mobile Application
- M-Pesa Integration
- Advanced Analytics
- Cloud Deployment
- Multi-Administrator Support

---

## Author

Developed as an academic project using:

- Python
- Flask
- SQLite
- HTML
- CSS
- JavaScript

---

## License

This project is intended for educational purposes.
