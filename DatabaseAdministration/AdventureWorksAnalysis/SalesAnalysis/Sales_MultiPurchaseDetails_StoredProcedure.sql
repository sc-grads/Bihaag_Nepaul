SELECT TOP (1000) [CustomerID]
      ,[SalesOrderID]
      ,[ProductID]
      ,[ProductName]
      ,[OrderQty]
      ,[UnitPrice]
      ,[OrderDate]
      ,[TotalDue]
  FROM [AdventureWorks2022].[Sales].[MultiPurchaseDetails]

CREATE PROCEDURE GetMostPurchasedProductPerCustomer
AS
BEGIN
    WITH RankedProducts AS (
        SELECT
            CustomerID,
            ProductID,
            ProductName,
            OrderQty,
            ROW_NUMBER() OVER (PARTITION BY CustomerID ORDER BY OrderQty DESC) AS RowNum
        FROM
            [AdventureWorks2022].[Sales].[MultiPurchaseDetails]
    )

    SELECT
        CustomerID,
        ProductID,
        ProductName,
        OrderQty
    FROM
        RankedProducts
    WHERE
        RowNum = 1;
END;

----------------------------------------------------------------------------------------------------------
CREATE PROCEDURE GetMostPurchasedProductPerCustomerWithMultipleProductPurchases
AS
BEGIN
    WITH RankedProducts AS (
        SELECT
            CustomerID,
            ProductID,
            ProductName,
            OrderQty,
            ROW_NUMBER() OVER (PARTITION BY CustomerID ORDER BY OrderQty DESC) AS RowNum
        FROM
            [AdventureWorks2022].[Sales].[MultiPurchaseDetails]
        WHERE
            CustomerID IN (
                SELECT
                    CustomerID
                FROM
                    [AdventureWorks2022].[Sales].[MultiPurchaseDetails]
                GROUP BY
                    CustomerID, ProductID
                HAVING
                    COUNT(*) > 1
            )
    )

    SELECT
        CustomerID,
        ProductID,
        ProductName,
        OrderQty
    FROM
        RankedProducts
    WHERE
        RowNum = 1;
END;

--------------------------------------------------------------------------- Final Stored procedure for getting most purchased item per customerS

CREATE PROCEDURE GetMostPurchasedProductPerCustomer
AS
BEGIN
    WITH RankedProducts AS (
        SELECT
            CustomerID,
            ProductID,
            ProductName,
            OrderQty,
            ROW_NUMBER() OVER (PARTITION BY CustomerID ORDER BY OrderQty DESC) AS RowNum
        FROM
            [AdventureWorks2022].[Sales].[MultiPurchaseDetails]
    )

    SELECT
        CustomerID,
        ProductID,
        ProductName,
        OrderQty
    FROM
        RankedProducts
    WHERE
        RowNum = 1
        AND CustomerID IN (
            SELECT CustomerID
            FROM RankedProducts
            GROUP BY CustomerID
            HAVING MAX(OrderQty) > 1
        );
END;


EXEC GetMostPurchasedProductPerCustomer;