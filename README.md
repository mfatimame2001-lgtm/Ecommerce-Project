# 🛒 ShopEase — E-Commerce Management System

A full-featured E-Commerce Management System built with **FastAPI**, **SQLite**, and **Jinja2** templates.

---

## ✅ Features

| Feature | Details |
|---|---|
| 🔐 User Authentication | Register, Login, Logout with JWT (python-jose) + passlib (sha256_crypt) |
| 🛒 Shopping Cart | Add/Remove items, quantity tracking |
| 📦 Product Management | Add, Edit, Delete, View (Admin) |
| 🗂 Category Management | Create and delete categories (Admin) |
| 🧾 Order Management | Place orders, view history, update status |
| 👥 User Management | View all registered users (Admin) |
| 📊 Admin Dashboard | Revenue, order count, product count stats |
| 📱 Responsive UI | Works on desktop, tablet, and mobile |

---

## 🚀 Quick Start (Windows)

### Option 1 — Double-click setup (Easiest)
1. Make sure **Python 3.10+** is installed → [python.org](https://python.org)
2. Double-click **`setup.bat`**
3. Open browser → **http://127.0.0.1:8000**

### Option 2 — Manual (VS Code Terminal)

```bash
# 1. Create virtual environment
python -m venv venv

# 2. Activate it
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Mac/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Seed demo data (creates admin + sample products)
python seed.py

# 5. Run the server
uvicorn main:app --reload
```

Open → **http://127.0.0.1:8000**

---

## � Deployment

This project can be deployed on any Python-ready hosting service. Two easy options are Render and Railway.

### Deploy on Render
1. Create a Render account and connect your GitHub repository.
2. Create a new Web Service.
3. Set the repository root to `.`
4. Render can auto-detect this project using `render.yaml`.
5. If needed, use these commands:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
6. Deploy and open the generated URL.

> Note: The deployed app will seed an admin user and sample demo data automatically on startup.

### Deploy on Railway
1. Create a Railway account and connect GitHub.
2. Choose the project repo and deploy.
3. Use:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
4. Railway will provide a live URL after deployment.

> Note: Because this app uses SQLite, deployment will work best for demos and small assignments. A production-ready app should use a managed database like PostgreSQL.

---

## �🔑 Default Credentials

| Role | Email | Password |
|---|---|---|
| Admin | admin@shop.com | 1234567@ |
| Customer | Register at /register | — |

---

## 📁 Project Structure

```
ecommerce-project/
├── main.py              # FastAPI routes
├── models.py            # SQLAlchemy DB models
├── auth.py              # JWT authentication
├── database.py          # DB connection
├── seed.py              # Demo data seeder
├── requirements.txt     # Python dependencies
├── setup.bat            # Windows one-click setup
├── setup.sh             # Mac/Linux setup
├── static/
│   ├── css/style.css    # Stylesheet
│   └── js/app.js        # Frontend JS
└── templates/
    ├── base.html         # Shop layout
    ├── admin_base.html   # Admin layout
    ├── auth/
    │   ├── login.html
    │   └── register.html
    ├── shop/
    │   ├── home.html
    │   ├── cart.html
    │   └── orders.html
    └── admin/
        ├── dashboard.html
        ├── products.html
        ├── edit_product.html
        ├── categories.html
        ├── orders.html
        └── users.html
```

---

## 🛠 Tech Stack

- **Backend**: Python 3.10+, FastAPI, SQLAlchemy
- **Database**: SQLite (zero config, file-based)
- **Auth**: JWT tokens (python-jose) + passlib (sha256_crypt)
- **Templates**: Jinja2 (server-side rendering)
- **Frontend**: Pure HTML/CSS/JS (no Node.js needed)

---

## 📸 Pages

| URL | Description |
|---|---|
| `/` | Home — product listing with category filter |
| `/register` | New user registration |
| `/login` | Login page |
| `/cart` | Shopping cart |
| `/orders` | My order history |
| `/admin/dashboard` | Admin stats overview |
| `/admin/products` | Manage products |
| `/admin/categories` | Manage categories |
| `/admin/orders` | Manage all orders |
| `/admin/users` | View all users |

---

## 📤 Publish to GitHub

1. Create a new GitHub repository.
2. In this folder, run:

```powershell
git init
git add .
git commit -m "Initial project setup"
git branch -M main
git remote add origin https://github.com/<your-username>/<repo-name>.git
git push -u origin main
```

3. Share the GitHub repository link for submission.
4. If you want live deployment, use a service like Render, Fly.io, or Railway and point it at this repo.
