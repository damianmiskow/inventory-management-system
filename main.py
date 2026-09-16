from services import (
    ApplicationError,
    create_customer,
    create_product,
    get_customer_orders,
    get_customers,
    get_order,
    get_products,
    place_order,
    update_stock,
)


def show_products():
    products = get_products()
    if not products:
        print("No products found.")
        return
    for product in products:
        print(
            f"{product['ProductID']} - {product['Name']} - "
            f"${product['Price']:.2f} - Stock: {product['Stock']}"
        )


def show_customers():
    customers = get_customers()
    if not customers:
        print("No customers found.")
        return
    for customer in customers:
        print(
            f"{customer['CustomerID']} - {customer['Name']} - "
            f"{customer['Email']}"
        )


def show_customer_orders(customer_id):
    orders = get_customer_orders(customer_id)
    if not orders:
        print("This customer has no orders.")
        return
    for order in orders:
        print(f"Order {order['OrderID']} - {order['Name']} - {order['OrderDate']}")


def show_order(order_id):
    details, total = get_order(order_id)
    print(f"Order #{details[0]['OrderID']}")
    print(f"Customer: {details[0]['CustomerName']}")
    print(f"Date: {details[0]['OrderDate']}")
    for item in details:
        print(
            f"{item['ProductName']} - Qty: {item['Quantity']} - "
            f"${item['UnitPrice']:.2f} each - ${item['LineTotal']:.2f}"
        )
    print(f"Order Total: ${total:.2f}")


def collect_order_items():
    items = []
    while True:
        items.append((
            int(input("Product ID: ")),
            int(input("Quantity: ")),
        ))
        if input("Add another item? (y/n): ").strip().lower() != "y":
            return items


def run_cli():
    while True:
        print("""
=== Order & Inventory Management ===
1. View Products
2. Add Product
3. Update Product Stock
4. View Customers
5. Add Customer
6. View Customer Orders
7. Place Order
8. View Order
9. Exit
        """)

        try:
            choice = int(input("Choose an option: "))

            if choice == 1:
                show_products()
            elif choice == 2:
                product_id = create_product(
                    input("Product name: "),
                    float(input("Price: ")),
                    int(input("Starting stock: ")),
                )
                print(f"Product #{product_id} created.")
            elif choice == 3:
                update_stock(
                    int(input("Product ID: ")),
                    int(input("New stock quantity: ")),
                )
                print("Stock updated.")
            elif choice == 4:
                show_customers()
            elif choice == 5:
                customer_id = create_customer(
                    input("Customer name: "),
                    input("Email address: "),
                )
                print(f"Customer #{customer_id} created.")
            elif choice == 6:
                show_customer_orders(int(input("Customer ID: ")))
            elif choice == 7:
                order_id = place_order(
                    int(input("Customer ID: ")),
                    input("Order date (YYYY-MM-DD): "),
                    collect_order_items(),
                )
                print(f"Order #{order_id} placed successfully.")
            elif choice == 8:
                show_order(int(input("Order ID: ")))
            elif choice == 9:
                print("Goodbye!")
                return
            else:
                print("Choose a number from 1 through 9.")
        except ValueError:
            print("Enter a valid number.")
        except ApplicationError as error:
            print(f"Unable to complete that action: {error}")


if __name__ == "__main__":
    run_cli()
