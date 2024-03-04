SELECT
    soh.CustomerID,
    soh.SalesOrderID,
    sod.ProductID,
    p.Name AS ProductName,
    sod.OrderQty,
    sod.UnitPrice,
    soh.OrderDate,
    soh.TotalDue
INTO
    [AdventureWorks2022].[Sales].[MultiPurchaseDetails]
FROM
    [AdventureWorks2022].[Sales].[SalesOrderHeader] soh
JOIN
    [AdventureWorks2022].[Sales].[SalesOrderDetail] sod ON soh.SalesOrderID = sod.SalesOrderID
JOIN
    [AdventureWorks2022].[Production].[Product] p ON sod.ProductID = p.ProductID
JOIN
    (
        SELECT
            CustomerID
        FROM
            [AdventureWorks2022].[Sales].[SalesOrderHeader]
        GROUP BY
            CustomerID
        HAVING
            COUNT(SalesOrderID) > 1
    ) multiPurchaseCustomers
ON
    soh.CustomerID = multiPurchaseCustomers.CustomerID;


Select * from [Sales].[MultiPurchaseDetails]