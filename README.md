# 📦 Inventory Management System

A full-featured **Inventory Management System** built with **Django 5** and **SQLite**. It supports role-based access control, product tracking, stock transactions, purchase orders, sales orders, reporting, and CSV/PDF export.

---

## 🚀 Features

- 🔐 **Role-Based Authentication** — Admin, Manager, and Staff roles with permission guards
- 📊 **Dashboard** — Live charts, low-stock alerts, and key business metrics
- 🛍️ **Product Management** — Add, edit, delete products with SKU, category, supplier, price, cost, and image URL
- 🏷️ **Category Management** — Organise products into categories
- 🏭 **Supplier Management** — Track supplier contact details
- 🔄 **Stock Transactions** — Record Stock In, Stock Out, and Adjustment movements
- 📋 **Purchase Orders (PO)** — Create and manage POs with multi-item support and status tracking (Draft → Sent → Received → Completed)
- 🧾 **Sales Orders (SO)** — Create and manage SOs with status tracking (Draft → Confirmed → Shipped → Delivered)
- 📈 **Reports** — Business reports with CSV and PDF export
- ⚠️ **Low Stock Alerts** — Automatic alerts when stock falls below configurable threshold

---

## 🗂️ Project Structure

```
Inventary_management/
├── inventory_system/          # Django project root
│   ├── inventory/             # Main application
│   │   ├── models.py          # Data models
│   │   ├── views.py           # Business logic & views
│   │   ├── urls.py            # URL routing
│   │   ├── forms.py           # Django forms
│   │   ├── decorators.py      # Role-based access decorators
│   │   ├── templates/         # HTML templates
│   │   ├── static/            # CSS, JS, images
│   │   └── migrations/        # Database migrations
│   ├── inventory_system/      # Django settings & config
│   │   ├── settings.py
│   │   ├── urls.py
│   │   ├── wsgi.py
│   │   └── asgi.py
│   ├── media/                 # Uploaded media files
│   ├── manage.py
│   └── db.sqlite3             # SQLite database
└── README.md
```

---

## 🛠️ Tech Stack

| Layer        | Technology            |
|--------------|-----------------------|
| Backend      | Python 3.x, Django 5  |
| Database     | SQLite3               |
| Frontend     | HTML, CSS, JavaScript |
| Auth         | Django Custom User Model |
| Timezone     | Asia/Kolkata (IST)    |

---

## ⚙️ Setup & Installation

### Prerequisites

- Python 3.10 or higher
- pip

### 1. Clone the Repository

```bash
git clone https://github.com/Pawankumar16122114/Inventary_Management.git
cd Inventary_Management
```

### 2. Create a Virtual Environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Apply Database Migrations

```bash
cd inventory_system
python manage.py migrate
```

### 5. Create a Superuser (Admin)

```bash
python manage.py createsuperuser
```

Follow the prompts to set a username, email, and password.

### 6. Run the Development Server

```bash
python manage.py runserver
```

Visit **http://127.0.0.1:8000** in your browser.

---

## 🔑 Default URL Routes

| URL                    | Description                  |
|------------------------|------------------------------|
| `/`                    | Redirects to Dashboard       |
| `/login/`              | Login page                   |
| `/dashboard/`          | Main dashboard               |
| `/products/`           | Product list                 |
| `/categories/`         | Category management          |
| `/suppliers/`          | Supplier management          |
| `/transactions/`       | Stock transactions           |
| `/purchase-orders/`    | Purchase order list          |
| `/sales-orders/`       | Sales order list             |
| `/reports/`            | Reports & exports            |
| `/admin/`              | Django admin panel           |

---

## 🔐 Authentication — Sign In & Sign Up

### 🔑 Sign In (Login)

The system uses **Django's built-in username & password authentication**.

| Field      | Type             | Required |
|------------|------------------|----------|
| `username` | Text             | ✅ Yes   |
| `password` | Password (masked)| ✅ Yes   |

**How it works:**
1. Navigate to **http://127.0.0.1:8000/login/**
2. Enter your **username** and **password**
3. On success → redirected to the **Dashboard**
4. On failure → error message `Invalid username or password.` is shown
5. Already logged-in users are automatically redirected to the dashboard

> 💡 All pages are protected. Unauthenticated users are automatically redirected to `/login/`.

---

### 📝 Sign Up (Register a New User)

This system does **not** have a public self-registration page. New user accounts are created by an **Admin** through one of the following methods:

#### Method 1 — Django Admin Panel *(Recommended)*

1. Go to **http://127.0.0.1:8000/admin/**
2. Log in with your superuser credentials
3. Click **Users → Add User**
4. Fill in:
   - **Username** (required)
   - **Password** (set and confirm)
   - **Email** (optional)
   - **Role** — choose `Admin`, `Manager`, or `Staff`
5. Click **Save**

#### Method 2 — Django Management Command (Terminal)

Create a superuser (Admin role) from the command line:

```bash
cd inventory_system
python manage.py createsuperuser
```

Follow the prompts:
```
Username: admin
Email address: admin@example.com
Password: ••••••••
Password (again): ••••••••
Superuser created successfully.
```

#### Method 3 — Django Shell (Advanced)

Create any user with a specific role programmatically:

```bash
python manage.py shell
```

```python
from inventory.models import CustomUser

# Create a Manager
user = CustomUser.objects.create_user(
    username='manager1',
    password='SecurePass123',
    email='manager1@example.com',
    role='manager'           # Options: 'admin', 'manager', 'staff'
)
user.save()
print(f'User {user.username} created with role: {user.role}')
```

---

### 🔓 Sign Out (Logout)

- Click the **Logout** button in the navigation bar, or
- Visit **http://127.0.0.1:8000/logout/** directly
- You will be redirected back to the login page with a confirmation message

---

### 🔄 Session Management

| Behaviour                | Details                                      |
|--------------------------|----------------------------------------------|
| Session backend          | Django database-backed sessions              |
| Session storage          | `django_session` table in SQLite             |
| Authenticated redirect   | `/dashboard/` after successful login         |
| Unauthenticated redirect | `/login/` for all protected routes           |
| CSRF Protection          | Enabled on all POST forms via `{% csrf_token %}` |

---

### 🔑 Password Validation Rules

Django's built-in validators are enforced on password creation:

| Rule                        | Description                              |
|-----------------------------|------------------------------------------|
| User Attribute Similarity   | Password must not be too similar to username/email |
| Minimum Length              | At least **8 characters**                |
| Common Password             | Cannot be a commonly used password       |
| Numeric Only                | Password cannot be entirely numeric      |

---

## 👥 User Roles & Permissions

| Role        | Access Level                                                             |
|-------------|--------------------------------------------------------------------------|
| **Admin**   | Full access — create/delete users, manage all data, delete any record    |
| **Manager** | Create & edit products, categories, suppliers, orders, transactions, reports |
| **Staff**   | View-only access to products, categories, suppliers + create stock transactions |

### Role-Based Access Matrix

| Feature                  | Staff | Manager | Admin |
|--------------------------|:-----:|:-------:|:-----:|
| View Dashboard           | ✅    | ✅      | ✅    |
| View Products            | ✅    | ✅      | ✅    |
| Add / Edit Products      | ❌    | ✅      | ✅    |
| Delete Products          | ❌    | ❌      | ✅    |
| View Categories          | ✅    | ✅      | ✅    |
| Add / Edit Categories    | ❌    | ✅      | ✅    |
| Delete Categories        | ❌    | ❌      | ✅    |
| View Suppliers           | ✅    | ✅      | ✅    |
| Add / Edit Suppliers     | ❌    | ✅      | ✅    |
| Delete Suppliers         | ❌    | ❌      | ✅    |
| View Transactions        | ✅    | ✅      | ✅    |
| Create Transactions      | ❌    | ✅      | ✅    |
| View Purchase Orders     | ✅    | ✅      | ✅    |
| Create / Update POs      | ❌    | ✅      | ✅    |
| Delete Purchase Orders   | ❌    | ❌      | ✅    |
| View Sales Orders        | ✅    | ✅      | ✅    |
| Create / Update SOs      | ❌    | ✅      | ✅    |
| Delete Sales Orders      | ❌    | ❌      | ✅    |
| View Reports & Export    | ✅    | ✅      | ✅    |

---

## 📤 Export Options

- **CSV Export** — Download reports as spreadsheets
- **PDF Export** — Download printable PDF reports

---

## 🗄️ Data Models

| Model               | Description                                  |
|---------------------|----------------------------------------------|
| `CustomUser`        | Extended user with role field                |
| `Category`          | Product categories                           |
| `Supplier`          | Supplier contact details                     |
| `Product`           | Products with SKU, price, cost, stock level  |
| `StockTransaction`  | Stock In / Out / Adjustment records          |
| `PurchaseOrder`     | PO header (auto-numbered PO-XXXXX)           |
| `PurchaseOrderItem` | Line items for each PO                       |
| `SalesOrder`        | SO header (auto-numbered SO-XXXXX)           |
| `SalesOrderItem`    | Line items for each SO                       |

---

## 🔒 Security Notes

- Change the `SECRET_KEY` in `settings.py` before deploying to production.
- Set `DEBUG = False` and configure `ALLOWED_HOSTS` for production.
- Use environment variables (e.g., `python-decouple` or `django-environ`) to manage secrets.

---

## 📸 Screenshots

> Add screenshots of your dashboard, product list, and reports here.

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

## 🔗 Repository

**GitHub:** [https://github.com/Pawankumar16122114/Inventary_Management](https://github.com/Pawankumar16122114/Inventary_Management)

---

## 🙌 Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.
