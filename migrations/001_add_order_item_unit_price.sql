BEGIN;

DROP VIEW IF EXISTS OrderDetails;

ALTER TABLE OrderItems
ADD COLUMN UnitPrice FLOAT NOT NULL DEFAULT 0 CHECK (UnitPrice >= 0);

CREATE VIEW OrderDetails AS
SELECT Orders.OrderID,
       Customers.Name AS CustomerName,
       Products.Name AS ProductName,
       OrderItems.Quantity,
       OrderItems.UnitPrice,
       OrderItems.UnitPrice * OrderItems.Quantity AS LineTotal,
       Orders.OrderDate
FROM Orders
INNER JOIN Customers ON Customers.CustomerID = Orders.CustomerID
INNER JOIN OrderItems ON OrderItems.OrderID = Orders.OrderID
INNER JOIN Products ON Products.ProductID = OrderItems.ProductID;

COMMIT;
