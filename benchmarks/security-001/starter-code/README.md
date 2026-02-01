# E-commerce Web Application

A Flask-based e-commerce platform for managing products and users.

## Setup

```bash
pip install -r requirements.txt
python app.py
```

## Features

- User authentication and authorization
- Product catalog and search
- Admin panel for user management
- File upload and download
- Data import/export functionality
- Database backup utilities

## API Endpoints

- `GET /` - Home page
- `POST /login` - User login
- `GET /products` - List products with optional filtering
- `GET /search` - Search products
- `GET /download` - Download files
- `POST /admin/backup` - Backup database
- `POST /api/import` - Import data
- `GET /admin` - Admin panel
- `POST /upload/avatar` - Upload user avatar

## Database

The application uses SQLite with the following tables:
- `users` - User accounts and credentials
- `products` - Product catalog

## Security Notes

Please ensure proper security measures are in place before deploying to production.
