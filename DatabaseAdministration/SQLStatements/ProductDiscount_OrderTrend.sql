
CREATE DATABASE OrderDB1;

USE OrderDB;


-- Create a table to store DiscountedProducts
CREATE TABLE dbo.DiscountedProductOrders (
    ProductID INT,
    ProductName NVARCHAR(255),
    OrderYear INT,
    OrdersWithDiscounts INT,
    AvgDiscountPercentage FLOAT,
);

-- Insert data into the DiscountedProducts table
INSERT INTO dbo.DiscountedProductOrders(ProductID, ProductName, OrderYear, OrdersWithDiscounts, AvgDiscountPercentage)
SELECT 
    p.ProductID,
    p.Name AS ProductName,
    YEAR(soh.OrderDate) AS OrderYear,
    COUNT(DISTINCT soh.SalesOrderID) AS OrdersWithDiscounts,
    AVG(sod.UnitPriceDiscount) AS AvgDiscountPercentage
FROM 
    AdventureWorks2022.Sales.SalesOrderDetail sod
INNER JOIN 
    AdventureWorks2022.Sales.SalesOrderHeader soh ON sod.SalesOrderID = soh.SalesOrderID
INNER JOIN 
    AdventureWorks2022.Production.Product p ON sod.ProductID = p.ProductID
WHERE 
    sod.UnitPriceDiscount > 0
GROUP BY 
    p.ProductID, p.Name, YEAR(soh.OrderDate);

----------------------------------
SELECT
    dp.ProductID,
    dp.ProductName,
    SUM(CASE WHEN dp.OrderYear = 2012 THEN dp.OrdersWithDiscounts ELSE NULL END) AS OrdersWithDiscounts_2012,
    SUM(CASE WHEN dp.OrderYear = 2013 THEN dp.OrdersWithDiscounts ELSE NULL END) AS OrdersWithDiscounts_2013,
    SUM(CASE WHEN dp.OrderYear = 2014 THEN dp.OrdersWithDiscounts ELSE NULL END) AS OrdersWithDiscounts_2014,
    AVG(CASE WHEN dp.OrderYear = 2012 THEN dp.AvgDiscountPercentage ELSE NULL END) AS AvgDiscountPercentage_2012,
    AVG(CASE WHEN dp.OrderYear = 2013 THEN dp.AvgDiscountPercentage ELSE NULL END) AS AvgDiscountPercentage_2013,
    AVG(CASE WHEN dp.OrderYear = 2014 THEN dp.AvgDiscountPercentage ELSE NULL END) AS AvgDiscountPercentage_2014
FROM 
    dbo.DiscountedProductOrders dp 
GROUP BY 
    dp.ProductID, dp.ProductName
HAVING 
    SUM(CASE WHEN dp.OrderYear IN (2012, 2013, 2014) THEN 1 ELSE 0 END) = 3
ORDER BY 
    dp.ProductID;

CREATE TABLE dbo.DiscountedProductOrders (
    DiscountedProductOrderID INT PRIMARY KEY IDENTITY(1,1),
    ProductID INT,
    ProductName NVARCHAR(255),
    OrderYear INT,
    OrdersWithDiscounts INT,
    AvgDiscountPercentage FLOAT
);


SELECT * FROM dbo.DiscountedProductOrders
-- Insert data into the DiscountedProducts table
INSERT INTO dbo.DiscountedProductOrders(ProductID, ProductName, OrderYear, OrdersWithDiscounts, AvgDiscountPercentage)
SELECT 
    p.ProductID,
    p.Name AS ProductName,
    YEAR(soh.OrderDate) AS OrderYear,
    COUNT(DISTINCT soh.SalesOrderID) AS OrdersWithDiscounts,
    AVG(sod.UnitPriceDiscount) AS AvgDiscountPercentage
FROM 
    AdventureWorks2022.Sales.SalesOrderDetail sod
INNER JOIN 
    AdventureWorks2022.Sales.SalesOrderHeader soh ON sod.SalesOrderID = soh.SalesOrderID
INNER JOIN 
    AdventureWorks2022.Production.Product p ON sod.ProductID = p.ProductID
WHERE 
    sod.UnitPriceDiscount > 0
GROUP BY 
    p.ProductID, p.Name, YEAR(soh.OrderDate);

	SELECT * FROM dbo.DiscountedProductOrders

----------------------------------
SELECT
    dp.ProductID,
    dp.ProductName,
    SUM(CASE WHEN dp.OrderYear = 2012 THEN dp.OrdersWithDiscounts ELSE NULL END) AS OrdersWithDiscounts_2012,
    SUM(CASE WHEN dp.OrderYear = 2013 THEN dp.OrdersWithDiscounts ELSE NULL END) AS OrdersWithDiscounts_2013,
    SUM(CASE WHEN dp.OrderYear = 2014 THEN dp.OrdersWithDiscounts ELSE NULL END) AS OrdersWithDiscounts_2014,
    AVG(CASE WHEN dp.OrderYear = 2012 THEN dp.AvgDiscountPercentage ELSE NULL END) AS AvgDiscountPercentage_2012,
    AVG(CASE WHEN dp.OrderYear = 2013 THEN dp.AvgDiscountPercentage ELSE NULL END) AS AvgDiscountPercentage_2013,
    AVG(CASE WHEN dp.OrderYear = 2014 THEN dp.AvgDiscountPercentage ELSE NULL END) AS AvgDiscountPercentage_2014
FROM 
    dbo.DiscountedProductOrders dp 
GROUP BY 
    dp.ProductID, dp.ProductName
HAVING 
    SUM(CASE WHEN dp.OrderYear IN (2012, 2013, 2014) THEN 1 ELSE 0 END) = 3
ORDER BY 
    dp.ProductID;



