# Billing System

A web-based billing system built with Flask and SQLite.

## Features

- Add products to cart
- Calculate totals with tax
- Save invoices to database
- Print receipts
- Web-based interface

## Setup

1. Install Python 3.x from python.org
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
   python src/app.py
   ```
   or use the batch file:
   ```bash
   START_APP.bat
   ```

4. Open browser to `http://localhost:5000`

## Project Structure

```
Billing_Projects/
├── data/              # Database files (not in git)
├── src/
│   ├── app.py         # Flask application
│   └── templates/
│       └── index.html # Web interface
├── requirements.txt   # Python dependencies
├── START_APP.bat      # Windows startup script
└── README.md          # This file
```

## Database

The app uses SQLite database stored in `data/billing.db`. The database is created automatically when you first run the app.

## Team

- Piyush (Developer)