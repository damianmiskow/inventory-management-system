import sqlite3
from collections import defaultdict
from datetime import date

import repositories
from database import database_connection


class ApplicationError(Exception):
    """An error that can be displayed safely to an application user."""


def get_products():
    with database_connection() as connection:
        return repositories.list_products(connection)


def create_product(name, price, stock):
    name = name.strip()
    if not name:
        raise ApplicationError("Product name is required.")
    if price < 0:
        raise ApplicationError("Price cannot be negative.")
    if stock < 0:
        raise ApplicationError("Stock cannot be negative.")
    with database_connection() as connection:
        return repositories.insert_product(connection, name, price, stock)


def update_stock(product_id, stock):
    if stock < 0:
        raise ApplicationError("Stock cannot be negative.")
    with database_connection() as connection:
        if repositories.set_product_stock(connection, product_id, stock) == 0:
            raise ApplicationError("Product not found.")


def get_customers():
    with database_connection() as connection:
        return repositories.list_customers(connection)


def create_customer(name, email):
    name = name.strip()
    email = email.strip().lower()
    if not name:
        raise ApplicationError("Customer name is required.")
    if not email or "@" not in email:
        raise ApplicationError("Enter a valid email address.")
    try:
        with database_connection() as connection:
            return repositories.insert_customer(connection, name, email)
    except sqlite3.IntegrityError as error:
        raise ApplicationError("A customer with that email already exists.") from error


def get_customer_orders(customer_id):
    with database_connection() as connection:
        if not repositories.customer_exists(connection, customer_id):
            raise ApplicationError("Customer not found.")
        return repositories.list_customer_orders(connection, customer_id)


def place_order(customer_id, order_date, items):
    if not items:
        raise ApplicationError("An order must contain at least one item.")

    try:
        parsed_order_date = date.fromisoformat(order_date)
    except ValueError as error:
        raise ApplicationError(
            "Order date must be a valid date in YYYY-MM-DD format."
        ) from error

    if parsed_order_date.isoformat() != order_date:
        raise ApplicationError(
            "Order date must use YYYY-MM-DD format, for example 2026-09-15."
        )

    combined_items = defaultdict(int)
    for product_id, quantity in items:
        if quantity <= 0:
            raise ApplicationError("Item quantities must be greater than zero.")
        combined_items[product_id] += quantity

    with database_connection() as connection:
        if not repositories.customer_exists(connection, customer_id):
            raise ApplicationError("Customer not found.")

        products = []
        for product_id, quantity in combined_items.items():
            product = repositories.get_product_for_order(connection, product_id)
            if product is None:
                raise ApplicationError(f"Product {product_id} was not found.")
            if product[3] < quantity:
                raise ApplicationError(
                    f"Not enough stock for {product[1]}. Available: {product[3]}."
                )
            products.append((product, quantity))

        order_id = repositories.insert_order(connection, customer_id, order_date)
        for product, quantity in products:
            repositories.insert_order_item(
                connection, order_id, product[0], quantity, product[2]
            )
            repositories.reduce_product_stock(connection, product[0], quantity)

    return order_id


def get_order(order_id):
    with database_connection() as connection:
        details = repositories.get_order_details(connection, order_id)
        if not details:
            raise ApplicationError("Order not found.")
        total = repositories.get_order_total(connection, order_id)
    return details, total[0]
