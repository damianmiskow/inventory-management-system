from database import get_connection

connection = get_connection()
cursor = connection.cursor()

cursor.execute("""

CREATE TABLE IF NOT EXISTS Products (
    ProductID INTEGER PRIMARY KEY,
    Name TEXT NOT NULL,
    Price FLOAT NOT NULL CHECK (Price >= 0),
    Stock INTEGER NOT NULL CHECK (Stock >= 0)
)
""")

cursor.execute("""

CREATE TABLE IF NOT EXISTS Customers (
    CustomerID INTEGER PRIMARY KEY,
    Name TEXT NOT NULL,
    Email TEXT NOT NULL UNIQUE
)
""")

cursor.execute("""

CREATE TABLE IF NOT EXISTS Orders (
    OrderID INTEGER PRIMARY KEY,
    CustomerID INTEGER NOT NULL,
    OrderDate TEXT NOT NULL,
    FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID))

""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS OrderItems (
        OrderItemID INTEGER NOT NULL PRIMARY KEY,
        OrderID INTEGER NOT NULL, 
        ProductID INTEGER NOT NULL,
        Quantity INTEGER NOT NULL CHECK (Quantity > 0),
        UnitPrice FLOAT NOT NULL CHECK (UnitPrice >= 0),

        FOREIGN KEY (OrderID) REFERENCES Orders(OrderID),
        FOREIGN KEY (ProductID) REFERENCES Products(ProductID)
    )
""")

cursor.execute("""
    CREATE INDEX IF NOT EXISTS index_orders_customers
    ON Orders(CustomerID)
""")

cursor.execute("""
    CREATE INDEX IF NOT EXISTS index_orderitems_order
    ON OrderItems(OrderID)
""")

cursor.execute("""
    CREATE INDEX IF NOT EXISTS index_orderitems_product
    ON OrderItems(ProductID)
""")

cursor.execute("""
    CREATE VIEW IF NOT EXISTS OrderDetails AS
    SELECT
        Orders.OrderID,
        Customers.Name AS CustomerName,
        Products.Name AS ProductName,
        OrderItems.Quantity,
        OrderItems.UnitPrice,
        OrderItems.UnitPrice * OrderItems.Quantity AS LineTotal,
        Orders.OrderDate
    FROM Orders
    INNER JOIN Customers
        ON Customers.CustomerID = Orders.CustomerID
    INNER JOIN OrderItems
        ON OrderItems.OrderID = Orders.OrderID
    INNER JOIN Products
        ON Products.ProductID = OrderItems.ProductID
""")

connection.commit()
connection.close()

print("Database setup completed successfully.")
