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
git clone https://github.com/your-username/inventory-management.git
cd inventory-management
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
pip install django
```

> If you have a `requirements.txt`, run: `pip install -r requirements.txt`

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

## 👥 User Roles & Permissions

| Role      | Access Level                                      |
|-----------|---------------------------------------------------|
| **Admin** | Full access — manage users, all data, settings    |
| **Manager** | Manage products, orders, transactions, reports  |
| **Staff** | View products and create stock transactions       |

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

## 🙌 Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.
