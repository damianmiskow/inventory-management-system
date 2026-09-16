def list_products(connection):
    return connection.execute("""
        SELECT ProductID, Name, Price, Stock
        FROM Products
        ORDER BY Name
    """).fetchall()


def insert_product(connection, name, price, stock):
    cursor = connection.execute("""
        INSERT INTO Products (Name, Price, Stock)
        VALUES (?, ?, ?)
    """, (name, price, stock))
    return cursor.lastrowid


def set_product_stock(connection, product_id, stock):
    cursor = connection.execute("""
        UPDATE Products SET Stock = ? WHERE ProductID = ?
    """, (stock, product_id))
    return cursor.rowcount


def list_customers(connection):
    return connection.execute("""
        SELECT CustomerID, Name, Email
        FROM Customers
        ORDER BY Name
    """).fetchall()


def insert_customer(connection, name, email):
    cursor = connection.execute("""
        INSERT INTO Customers (Name, Email) VALUES (?, ?)
    """, (name, email))
    return cursor.lastrowid


def customer_exists(connection, customer_id):
    return connection.execute("""
        SELECT 1 FROM Customers WHERE CustomerID = ?
    """, (customer_id,)).fetchone() is not None


def list_customer_orders(connection, customer_id):
    return connection.execute("""
        SELECT Orders.OrderID, Customers.Name, Orders.OrderDate
        FROM Orders
        INNER JOIN Customers ON Customers.CustomerID = Orders.CustomerID
        WHERE Orders.CustomerID = ?
        ORDER BY Orders.OrderDate DESC, Orders.OrderID DESC
    """, (customer_id,)).fetchall()


def insert_order(connection, customer_id, order_date):
    cursor = connection.execute("""
        INSERT INTO Orders (CustomerID, OrderDate) VALUES (?, ?)
    """, (customer_id, order_date))
    return cursor.lastrowid


def get_product_for_order(connection, product_id):
    return connection.execute("""
        SELECT ProductID, Name, Price, Stock
        FROM Products
        WHERE ProductID = ?
    """, (product_id,)).fetchone()


def insert_order_item(connection, order_id, product_id, quantity, unit_price):
    connection.execute("""
        INSERT INTO OrderItems (OrderID, ProductID, Quantity, UnitPrice)
        VALUES (?, ?, ?, ?)
    """, (order_id, product_id, quantity, unit_price))


def reduce_product_stock(connection, product_id, quantity):
    connection.execute("""
        UPDATE Products SET Stock = Stock - ? WHERE ProductID = ?
    """, (quantity, product_id))


def get_order_details(connection, order_id):
    return connection.execute("""
        SELECT OrderID, CustomerName, ProductName, Quantity,
               UnitPrice, LineTotal, OrderDate
        FROM OrderDetails
        WHERE OrderID = ?
    """, (order_id,)).fetchall()


def get_order_total(connection, order_id):
    return connection.execute("""
        SELECT SUM(LineTotal) AS OrderTotal
        FROM OrderDetails
        WHERE OrderID = ?
    """, (order_id,)).fetchone()
