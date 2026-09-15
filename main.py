import sqlite3

from database import get_connection


connection = get_connection()
cursor = connection.cursor()

def view_products():
    cursor.execute ("""
    SELECT * 
    FROM Products
    """)
    results = cursor.fetchall()
    for r in results:
        print(f"{r[0]} - {r[1]} - ${r[2]} - Stock: {r[3]}")

def add_product(product_name, product_price, product_stock):
    cursor.execute("""

    INSERT INTO Products (Name, Price, Stock)
    VALUES (?, ?, ?)

    """, (product_name, product_price, product_stock))
    connection.commit()

def update_inventory(product_id, new_quantity):
    cursor.execute("""

    UPDATE Products
    SET Stock = ?
    WHERE ProductID = ?

    """, (new_quantity, product_id)
    )
    connection.commit()

def add_customer(customer_name, customer_email):
    try:
        cursor.execute ("""
        
        INSERT INTO Customers (Name, Email)
        VALUES (?, ?)
        
        """, (customer_name, customer_email))
        connection.commit()
    except sqlite3.IntegrityError:
        print("A customer with the same email address exists!")

def view_customers(): 
    cursor.execute("""
        SELECT *
        FROM Customers
    """)
    results = cursor.fetchall()
    for r in results:
        print(f"{r[0]} - {r[1]} - {r[2]}")

def view_customer_orders(customerID):
    cursor.execute("""
        SELECT OrderID,
            Customers.Name,
            OrderDate
        FROM Orders
            INNER JOIN Customers ON Customers.CustomerID = Orders.CustomerID
        WHERE Orders.CustomerID = ?
    """, (customerID,))

    results = cursor.fetchall()

    for r in results:
        print (f"Order {r[0]} - {r[1]} - {r[2]}")

def create_order(customer_id, order_date): 
    cursor.execute("""
        INSERT INTO Orders (CustomerID, OrderDate)
        VALUES (?, ?)    
            """, (customer_id, order_date))
    order_id = cursor.lastrowid
    return order_id

def add_order_item(order_id, product_id, quantity):
    cursor.execute ("""

        INSERT INTO OrderItems(OrderID, ProductID, Quantity)
        VALUES (?, ?, ?)

""", (order_id, product_id, quantity))

def reduce_stock(product_id, quantity):
    cursor.execute ("""
    UPDATE Products
    SET Stock = Stock - ?
    WHERE ProductID = ?
    """, (quantity, product_id))


def get_stock(product_id):
    cursor.execute("""
        SELECT Stock
        FROM Products
        WHERE ProductID = ?
    """, (product_id,))
    result = cursor.fetchone()
    if result is None:
        raise Exception ("Invalid Product ID!")

    return result[0]


def place_order(customer_id, order_date, items):
    try:
        order_id = create_order(customer_id, order_date)
        for product_id, quantity in items:
            current_stock = get_stock(product_id)
            if quantity <= 0:
                raise Exception ("Invalid quantity entry!")
            if current_stock < quantity:
                raise Exception ("Not enough stock!")
            add_order_item(order_id, product_id, quantity)
            reduce_stock(product_id, quantity)
        connection.commit()
    except Exception as e:
        connection.rollback()
        print(f"Order failed: {e}")

def view_order(order_id):
    cursor.execute("""
    SELECT Orders.OrderID,
        Customers.Name,
        Products.Name,
        OrderItems.Quantity,
        Products.Price,
        (Products.Price * OrderItems.Quantity) AS LineTotal,
        Orders.OrderDate
    FROM Orders
        INNER JOIN Customers ON Customers.CustomerID = Orders.CustomerID
        INNER JOIN OrderItems ON OrderItems.OrderID = Orders.OrderID
        INNER JOIN Products ON Products.ProductID = OrderItems.ProductID
    WHERE Orders.OrderID = ?
    """, (order_id,))


    order = cursor.fetchall()
    print(f"Order #{order[0][0]}")
    print(f"Customer: {order[0][1]}")
    print(f"Date: {order[0][6]}")
    for item in order:
        print(f"{item[2]} - Qty: {item[3]} - ${item[4]} each - ${item[5]}")

    cursor.execute("""
    SELECT SUM(Products.price * OrderItems.Quantity) AS OrderTotal
    FROM Products
        INNER JOIN OrderItems ON OrderItems.ProductID = Products.ProductID
    WHERE OrderItems.OrderID = ?
    GROUP BY OrderItems.OrderID

    """, (order_id,))


    total_order = cursor.fetchone()

    if total_order is None:
        print("Order not found!")
    else:
        print(f"Order Total: ${total_order[0]}")


def tests():
    cursor.execute("""
SELECT Customers.CustomerID,
    Customers.Name,
    COUNT(Orders.OrderID)
FROM Customers
    LEFT JOIN Orders ON Orders.CustomerID = Customers.CustomerID
GROUP BY Customers.CustomerID,
    Customers.Name
                            

        """)
    
    results = cursor.fetchall()
    for r in results:
        print(r)

if __name__ == "__main__":

    running = True
    while running:
        print("""   
=== Inventory Management System ===
1. View Products
2. Add Product
3. Update Inventory
4. Add Customer
5. View Customers 
6. View Customer Orders
7. Create Order
8. Place Order
9. View Order
10. Exit 
88. Test Function
        """)
        try:
            user_choice = int(input("Choose an option: "))
        except ValueError:
            print ("Please enter a number!")
            continue
        if user_choice == 1:
            view_products()
        elif user_choice == 2:
            product_name = input("Name of the product: ")
            product_price = float(input("Price of product: "))
            product_stock = int(input("Stock: "))
            add_product(product_name, product_price, product_stock)
        elif user_choice == 3:
            productid_to_edit = int(input("ID of the product to edit: "))
            new_stock_quant = int(input("New stock: "))
            update_inventory(productid_to_edit, new_stock_quant)
        elif user_choice == 4:
            customer_name = input("Enter customer name: ")
            customer_email = input("Enter email address: ")
            add_customer(customer_name, customer_email)
        elif user_choice == 5:
            view_customers()
        elif user_choice == 6:
            try:
                customer_id_to_view = int(input("Customer ID: "))
            except ValueError:
                print("Please enter an integer!")
                continue
            view_customer_orders(customer_id_to_view)
        elif user_choice == 7:
            customer_id = int(input("Customer ID: "))
            order_date = input("Order Date: ")
            create_order(customer_id, order_date)
        elif user_choice == 8:
            customer_id = int(input("Customer ID: "))
            order_date = input("Order Date: ")
            items = []
            while True:
                product_id = int(input("Product ID: "))
                quantity = int(input("Quantity: "))
                items.append((product_id, quantity))
                add_another_choice = input("Add another item y/n: ").lower()
                if add_another_choice == "y":
                    continue
                elif add_another_choice == "n":
                    break
                else:
                    print ("Invalid choice! Enter y or n.")
            place_order(customer_id, order_date, items)
        elif user_choice == 9:
            order_id = int(input ("Enter OrderID: "))
            view_order(order_id)
        elif user_choice == 10:
            running = False
        elif user_choice == 88:
            tests()
        else:
            print("Invalid Choice!")


    connection.close()
