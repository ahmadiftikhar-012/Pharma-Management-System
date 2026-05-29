# PharmaMS – Pharmacy Management System
## Built with: Flask · SQLAlchemy · MySQL · Bootstrap 5

---

## ✅ What You Need to Install

### 1. Python (3.10 or higher)
Download from: https://www.python.org/downloads/
- During install ✅ check "Add Python to PATH"

### 2. MySQL Server (Community Edition – Free)
Download from: https://dev.mysql.com/downloads/mysql/
- Remember the root password you set during install

### 3. Git (optional, for version control)
Download from: https://git-scm.com/

---

## 🚀 Setup Steps (Run These in Order)

### Step 1 – Create a virtual environment
```bash
cd pharma_app
python -m venv venv
```

### Step 2 – Activate the virtual environment
```bash
# Windows:
venv\Scripts\activate

# Mac/Linux:
source venv/bin/activate
```
You'll see (venv) at the start of your terminal line.

### Step 3 – Install Python packages
```bash
pip install -r requirements.txt
```
This installs: Flask, SQLAlchemy, Flask-Login, PyMySQL, Werkzeug, python-dotenv

### Step 4 – Create the MySQL database
Open MySQL Workbench or terminal and run:
```sql
CREATE DATABASE pharma_db;
```
OR run the full schema:
```bash
mysql -u root -p < schema.sql
```

### Step 5 – Configure your database password
Edit the `.env` file:
```
SECRET_KEY=any-random-string-you-choose
DATABASE_URL=mysql+pymysql://root:YOUR_MYSQL_PASSWORD@localhost/pharma_db
```
Replace YOUR_MYSQL_PASSWORD with your actual MySQL root password.

### Step 6 – Create tables and the admin user
```bash
python seed.py
```
This creates all tables and makes an admin login:
- Username: **admin**
- Password: **admin123**

### Step 7 – Run the app
```bash
python app.py
```
Open your browser at: **http://localhost:5000**

---

## 📁 Project Structure
```
pharma_app/
├── app.py                  ← Main entry point
├── config.py               ← App + DB configuration
├── models.py               ← Database models (tables)
├── schema.sql              ← Raw SQL schema (alternative setup)
├── seed.py                 ← Creates admin user
├── requirements.txt        ← Python packages
├── .env                    ← Your secrets (DB password, etc.)
│
├── routes/
│   ├── auth.py             ← Login / Logout
│   ├── dashboard.py        ← Dashboard stats
│   ├── medicines.py        ← Medicine CRUD
│   ├── suppliers.py        ← Supplier CRUD
│   ├── stock.py            ← Stock management
│   └── sales.py            ← Billing & sales history
│
└── templates/
    ├── base.html           ← Sidebar layout (all pages extend this)
    ├── dashboard.html
    ├── auth/login.html
    ├── medicines/list.html + form.html
    ├── suppliers/list.html + form.html
    ├── stock/list.html + update.html
    └── sales/new.html + list.html + receipt.html
```

---

## 🔑 Default Login
| Field    | Value     |
|----------|-----------|
| Username | admin     |
| Password | admin123  |

Change after first login by editing the user in the database.

---

## 🧩 Key Features
- 🔐 Login system with session management
- 💊 Medicine management (add/edit/delete + stock)
- 🏢 Supplier management
- 📦 Stock tracking with low-stock alerts
- 🛒 Billing / sales with dynamic item rows
- 🧾 Printable receipts
- 📊 Dashboard with live stats
- ⚠️ Expiry warnings (30-day window)

---

## ⚠️ Common Issues

**"No module named pymysql"** → Run `pip install -r requirements.txt` inside venv

**"Access denied for user root"** → Wrong password in `.env`

**"Table doesn't exist"** → Run `python seed.py`

**Port 5000 in use** → Change last line of app.py to `app.run(debug=True, port=5001)`
