# 🏥 Hospital Management System

A web-based **Hospital Management System** built with **Flask** and **MySQL**. It lets an administrator manage patients, doctors, and appointments through a clean Bootstrap interface. Built as a DBMS mini project to demonstrate relational database design and CRUD operations in a real web app.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.0.3-black?logo=flask)
![MySQL](https://img.shields.io/badge/MySQL-8.x-orange?logo=mysql&logoColor=white)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-7952B3?logo=bootstrap&logoColor=white)

---

## 📑 Table of Contents

- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Database Design](#-database-design)
- [Getting Started](#-getting-started)
- [Configuration](#-configuration)
- [Usage](#-usage)
- [Application Routes](#-application-routes)
- [DBMS Concepts Demonstrated](#-dbms-concepts-demonstrated)
- [Security Notes](#-security-notes)
- [Future Improvements](#-future-improvements)
- [Contributing](#-contributing)

---

## ✨ Features

- 🔐 **Admin authentication** – session-based login and logout; all pages are protected
- 📊 **Dashboard** – live counts of patients, doctors, total appointments, scheduled appointments, and today's appointments
- 🧑‍🤝‍🧑 **Patient management** – add, view, edit, delete, and search by name or patient ID
- 👨‍⚕️ **Doctor management** – add, view, edit, delete, and search by name or specialization
- 📅 **Appointment management** – book, view, edit, delete, and filter by status (Scheduled / Completed / Cancelled)
- 🔗 **JOIN queries** – the appointment list combines data from `appointments`, `patients`, and `doctors`
- ⚠️ **Flash messages & error page** – clear feedback for every action and graceful error handling
- 📱 **Responsive UI** – built with Bootstrap 5

---

## 🛠 Tech Stack

| Layer      | Technology                                |
| ---------- | ----------------------------------------- |
| Backend    | Python, Flask 3.0.3                       |
| Database   | MySQL (via `mysql-connector-python` 9.0.0)|
| Frontend   | HTML5, Jinja2 templates, Bootstrap 5.3.3  |
| Styling/JS | Custom CSS and JavaScript                 |

---

## 📁 Project Structure

```
hospital_management_system/
├── app.py                  # Flask application: routes and DB helpers
├── config.py               # Configuration (reads environment variables)
├── hospital_db.sql         # Database schema + sample data
├── requirements.txt        # Python dependencies
├── README.md
├── static/
│   ├── css/style.css       # Custom styles
│   └── js/script.js        # Custom scripts
└── templates/
    ├── base.html           # Shared layout
    ├── login.html
    ├── dashboard.html
    ├── patients.html
    ├── add_patient.html
    ├── edit_patient.html
    ├── doctors.html
    ├── add_doctor.html
    ├── edit_doctor.html
    ├── appointments.html
    ├── add_appointment.html
    ├── edit_appointment.html
    └── error.html
```

---

## 🗄 Database Design

The database `hospital_db` contains four tables:

| Table          | Purpose                          | Key columns                                                                 |
| -------------- | -------------------------------- | --------------------------------------------------------------------------- |
| `admin`        | Administrator login credentials  | `id` (PK), `username` (unique), `password`                                  |
| `patients`     | Patient records                  | `patient_id` (PK), `name`, `age`, `gender`, `phone`, `address`, `disease`   |
| `doctors`      | Doctor records                   | `doctor_id` (PK), `name`, `specialization`, `phone`, `room_no`              |
| `appointments` | Links patients to doctors        | `appointment_id` (PK), `patient_id` (FK), `doctor_id` (FK), `appointment_date`, `appointment_time`, `status` |

### Relationships

```
patients (1) ────< appointments >──── (1) doctors
```

- Each appointment belongs to **one patient** and **one doctor**.
- Both foreign keys use `ON DELETE CASCADE`, so deleting a patient or doctor also removes their appointments.
- `gender` is an `ENUM('Male', 'Female', 'Other')` and `status` is an `ENUM('Scheduled', 'Completed', 'Cancelled')`.

---

## 🚀 Getting Started

### Prerequisites

- [Python 3.8+](https://www.python.org/downloads/)
- [MySQL Server 8.x](https://dev.mysql.com/downloads/) (or XAMPP / WAMP / MAMP with phpMyAdmin)
- `pip` and (recommended) `venv`

### Installation

**1. Clone the repository**

```bash
git clone https://github.com/<your-username>/hospital_management_system.git
cd hospital_management_system
```

**2. Create and activate a virtual environment (recommended)**

```bash
# macOS / Linux
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

**3. Install dependencies**

```bash
pip install -r requirements.txt
```

**4. Set up the database**

Import the provided SQL file using the MySQL command line:

```bash
mysql -u root -p < hospital_db.sql
```

Or import `hospital_db.sql` through **phpMyAdmin** (Import tab).

> ⚠️ The script runs `DROP TABLE IF EXISTS` on all four tables, so re-importing will **erase existing data**.

**5. Configure database credentials**

See [Configuration](#-configuration) below.

**6. Run the application**

```bash
python app.py
```

**7. Open in your browser**

```
http://127.0.0.1:5000
```

---

## ⚙️ Configuration

Settings live in `config.py` and are read from **environment variables**, with these defaults:

| Variable         | Default                    | Description                    |
| ---------------- | -------------------------- | ------------------------------ |
| `SECRET_KEY`     | `dev-secret-key-change-me` | Flask session secret key       |
| `MYSQL_HOST`     | `localhost`                | MySQL server host              |
| `MYSQL_USER`     | `root`                     | MySQL username                 |
| `MYSQL_PASSWORD` | *(empty)*                  | MySQL password                 |
| `MYSQL_DATABASE` | `hospital_db`              | Database name                  |

Example (macOS / Linux):

```bash
export MYSQL_USER=root
export MYSQL_PASSWORD=your_password
export SECRET_KEY=a-long-random-string
python app.py
```

Example (Windows PowerShell):

```powershell
$env:MYSQL_USER="root"
$env:MYSQL_PASSWORD="your_password"
$env:SECRET_KEY="a-long-random-string"
python app.py
```

Alternatively, edit the default values directly in `config.py` for local development.

---

## 💻 Usage

Log in with the demo account:

| Username | Password   |
| -------- | ---------- |
| `admin`  | `admin123` |

After login you can:

1. View summary statistics on the **Dashboard**
2. Manage records under **Patients**, **Doctors**, and **Appointments**
3. Use the search box on the Patients and Doctors pages
4. Filter appointments by status

The sample SQL data includes 3 patients, 3 doctors, and 3 appointments so you can explore right away.

---

## 🧭 Application Routes

| Route                              | Methods   | Description                           |
| ---------------------------------- | --------- | ------------------------------------- |
| `/`                                | GET       | Redirects to dashboard or login       |
| `/login`                           | GET, POST | Admin login                           |
| `/logout`                          | GET       | Log out                               |
| `/dashboard`                       | GET       | Statistics overview                   |
| `/patients`                        | GET       | List / search patients                |
| `/patients/add`                    | GET, POST | Add a patient                         |
| `/patients/edit/<id>`              | GET, POST | Edit a patient                        |
| `/patients/delete/<id>`            | GET       | Delete a patient                      |
| `/doctors`                         | GET       | List / search doctors                 |
| `/doctors/add`                     | GET, POST | Add a doctor                          |
| `/doctors/edit/<id>`               | GET, POST | Edit a doctor                         |
| `/doctors/delete/<id>`             | GET       | Delete a doctor                       |
| `/appointments`                    | GET       | List appointments (filter by status)  |
| `/appointments/add`                | GET, POST | Book an appointment                   |
| `/appointments/edit/<id>`          | GET, POST | Edit an appointment                   |
| `/appointments/delete/<id>`        | GET       | Delete an appointment                 |

---

## 📚 DBMS Concepts Demonstrated

- Primary keys and auto-increment IDs
- Foreign keys with `ON DELETE CASCADE`
- Relational database design and normalization
- `ENUM` data types and `NOT NULL` / `UNIQUE` constraints
- Full CRUD operations (Create, Read, Update, Delete)
- `JOIN` queries across multiple tables
- Parameterized queries (protection against SQL injection)
- Aggregate queries (`COUNT`) for dashboard statistics
- `LIKE` pattern searching

---

## 🔒 Security Notes

This project is intended for **learning and demonstration**. Before using anything similar in production, address the following:

- **Passwords are stored in plain text** in the `admin` table. Use hashing (e.g. `werkzeug.security.generate_password_hash` / `check_password_hash`).
- **Change the default admin credentials** (`admin` / `admin123`) and the default `SECRET_KEY`.
- **Delete actions use GET requests**, which makes them vulnerable to CSRF and accidental triggers. Switch to POST with CSRF tokens (e.g. Flask-WTF).
- **Run with `debug=False`** in production and use a production WSGI server such as Gunicorn or Waitress.
- Don't commit real database credentials; use environment variables or a `.env` file.

---

## 🔮 Future Improvements

- [ ] Hash admin passwords and support multiple admin / staff roles
- [ ] CSRF protection and POST-based deletes
- [ ] Prevent double-booking of a doctor at the same date and time
- [ ] Pagination for large patient / doctor / appointment lists
- [ ] Patient medical history and prescriptions
- [ ] Billing and invoice module
- [ ] Export reports to PDF / CSV
- [ ] Docker setup for one-command deployment

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Commit your changes: `git commit -m "Add your feature"`
4. Push to the branch: `git push origin feature/your-feature`
5. Open a Pull Request

---

## 📄 License

This project is released for educational purposes. Add a license of your choice (e.g. [MIT](https://choosealicense.com/licenses/mit/)) by creating a `LICENSE` file.

---

⭐ If you found this project useful, consider giving it a star!
