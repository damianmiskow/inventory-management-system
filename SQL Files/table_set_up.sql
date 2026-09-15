WITH CustomerOrdersCounts AS (
    SELECT Orders.CustomerID,
        Customers.Name,
        COUNT(Orders.OrderID) AS OrderCount
    FROM Customers
        LEFT JOIN Orders ON Orders.CustomerID = Customers.CustomerID
    GROUP BY Customers.CustomerID,
        Customers.Name
)