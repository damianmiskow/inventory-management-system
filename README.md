# Inventory Management System

A Python and SQLite inventory and order management application. The project demonstrates relational database design, explicit SQL queries, transaction safety, inventory tracking, and multi-item order processing.

## Current features

- Product and customer management
- Inventory updates and stock validation
- Multi-item order creation
- Automatic stock reduction
- Transaction commit and rollback
- Order details and totals
- Primary and foreign keys
- Database constraints and indexes
- Parameterized SQL queries
- Reusable SQL view for order details
- Command-line interface

## Technologies

- Python
- SQLite
- SQL

## Architecture

- `main.py` provides the current command-line interface.
- `services.py` contains validation and business rules.
- `repositories.py` contains explicit, parameterized SQL queries.
- `database.py` manages connections, commits, and rollbacks.
- `setup_db.py` creates a new local database.
- `migrations/` contains versioned changes for existing databases.

Order items store the price charged at the time of purchase, so historical
order totals remain accurate when a product's current price changes.

## Run locally

Create the database:

```bash
python3 setup_db.py
```

Start the application:

```bash
python3 main.py
```

## Project status

This application is being developed into a full portfolio project. Planned
work includes automated tests, reporting queries, a FastAPI backend, a React
and TypeScript interface, PostgreSQL, and AWS deployment.
