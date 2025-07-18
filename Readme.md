# 🧑‍💼 Face Recognition Attendance System

This is a Python-based face recognition attendance system with a clean Tkinter GUI. It automatically marks attendance by recognizing faces from a webcam feed and logs them into a PostgreSQL database and a CSV file.

---

## 📂 Features

- 🎦 Real-time face detection using OpenCV
- 🤖 Face recognition with `face_recognition` library
- 🗂 GUI dashboard using Tkinter
- 🧠 Attendance data stored in PostgreSQL and CSV
- 📸 Easy to add new faces to the system
- 📅 View live attendance logs
- ⏰ Real-time clock on dashboard

---

## 🛠️ Tech Stack

- Python 3.10+
- OpenCV
- face_recognition
- PostgreSQL
- psycopg2
- python-dotenv
- Tkinter

---

## 🚀 Getting Started

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/jnishtha/FaceAttendancesystem.git
cd FaceAttendancesystem
```
### 2️⃣ Install Dependencies
Create a virtual environment (optional but recommended):

```bash
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
```
Install required packages:

```bash
pip install -r requirements.txt
```
### 3️⃣ Setup PostgreSQL
1. Create a PostgreSQL database named face_attendance
2. Create a table:

```sql
CREATE TABLE attendance (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    date DATE,
    entry_time TIME,
    exit_time TIME,
    duration INTERVAL
);
```
3. Create a .env file in the root directory with:
```ini
DB_HOST=localhost
DB_NAME=face_attendance
DB_USER=your_username
DB_PASSWORD=your_password
```
### 4️⃣ Add Known Faces
Create a folder named known_faces
Add subfolders with each person’s name (e.g. known_faces/Nishtha/)
Place their face images inside (preferably clear front-facing photos)

### 5️⃣ Run the GUI
```bash
python gui_dashboard.py
```
The GUI provides buttons to start the webcam-based attendance and view logs.

### 📁 Project Structure
```bash
FaceAttendancesystem/
│
├── attendance.py          # Handles webcam, face recognition, attendance logic
├── gui_dashboard.py       # GUI dashboard using Tkinter
├── db_connect.py          # PostgreSQL connection handler
├── utils.py               # Utility functions (if any)
├── .env                   # (Hidden) Database credentials - not uploaded
├── .gitignore
├── attendance_log.csv     # Local backup of attendance
├── known_faces/           # Folders of known people's face images
└── README.md              # Project info
```
### ✅ To Do
 Admin panel for viewing all logs

### 🤝 Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

### 📃 License
This project is open source under the MIT License.

### 🙋‍♀️ Created by
Nishtha Jain
