# Task 9 — Full Stack Python Project (Flask)
### Synent Technologies Internship  
### Developer: John Henry Garcia Jr

This project is my submission for **Task 9: Full Stack Python Project**, where the objective was to build a fully functional web application using **Flask**, **SQLite**, and **HTML/CSS**.

I chose to build a **Task Manager Application** that allows users to register, log in, and manage their personal tasks with features like priority levels, due dates, completion tracking, and filtering.

---

## 🚀 Features

### 🔐 Authentication
- User Registration  
- Secure Login  
- Password Hashing (Werkzeug)  
- Session Handling  
- Rate Limiting (prevents brute‑force attacks)

### 📝 Task Management
- Add new tasks  
- Edit existing tasks  
- Delete tasks  
- Mark tasks as completed  
- Priority levels (High, Medium, Low)  
- Due dates  
- Overdue task detection  
- Filter tasks (All, Pending, Completed)

### 🎨 User Interface
- Clean, responsive Bootstrap UI  
- Priority badges  
- Green highlight for completed tasks  
- Red highlight for overdue tasks  
- Flash messages for feedback  
- Custom error pages (404, 500, 403)

### 🗄️ Database
- SQLite database  
- `users` table for authentication  
- `tasks` table linked by `user_id`  
- Secure parameterized queries  
- Explicit `completed = 0` on task creation

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|------------|
| Backend | Flask (Python) |
| Frontend | HTML, CSS, Bootstrap |
| Database | SQLite |
| Security | Werkzeug hashing, Flask‑Limiter |
| Templates | Jinja2 |

---

## 📂 Project Structure

```
project/
│── app.py
│── database.db
│── /templates
│     ├── base.html
│     ├── login.html
│     ├── register.html
│     ├── dashboard.html
│     ├── add_task.html
│     ├── edit_task.html
│     ├── 404.html
│     ├── 500.html
│     ├── 403.html
│── /static
├── style.css
```

---

## ⚙️ Installation & Setup

### 1. Clone the repository
```
git clone https://github.com/<your-username>/synent-task9-taskmanager-johnhenrygarciajr
cd synent-task9-taskmanager-johnhenrygarciajr
```


### 2. Install dependencies

```
pip install flask flask-limiter werkzeug
```


### 3. Initialize the database
If `database.db` is not included, create it using:

```
python

import sqlite3
conn = sqlite3.connect("database.db")
cur = conn.cursor()
cur.execute("CREATE TABLE users (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE, password TEXT)")
cur.execute("CREATE TABLE tasks (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, title TEXT, description TEXT, priority TEXT, due_date TEXT, completed INTEGER DEFAULT 0)")
conn.commit()
conn.close()
```


### 4. Run the application
```
python app.py
```

Then open your browser and go to:
```
http://127.0.0.1:5000 (127.0.0.1 in Bing)
```


---

## 🧪 How to Use

1. Register a new account  
2. Log in  
3. Add tasks with priority and due dates  
4. Edit or delete tasks  
5. Mark tasks as completed  
6. View overdue tasks highlighted in red  
7. Filter tasks by status  

---

## 🔒 Security Features

- Password hashing (no plain‑text passwords)  
- Rate limiting on login, register, and task actions  
- Session‑based authentication  
- Protected routes (no access without login)  
- Custom error pages for better UX  

---

## 🎯 Output Requirement (Met)

✔ Fully working web application  
✔ Authentication  
✔ CRUD functionality  
✔ Database integration  
✔ Responsive UI  
✔ Clean code and structure  

---

## 📸 Screenshots (Optional)
You can add screenshots here after pushing the project.

---

## 📬 Contact
**Developer:** John Henry Garcia Jr  
**Location:** Pearland, Texas  
