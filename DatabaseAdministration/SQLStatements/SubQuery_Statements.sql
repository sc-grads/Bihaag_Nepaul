-- Use the AdventureWorks2022 database
USE [AdventureWorks2022]
GO

-- Retrieve all records from the EmployeePayHistory table
-- where the BusinessEntityID is in the set of BusinessEntityIDs
-- where the Rate is greater than 60
SELECT *
FROM [HumanResources].[EmployeePayHistory]
WHERE [BusinessEntityID] IN (SELECT BusinessEntityID FROM [HumanResources].[EmployeePayHistory] WHERE Rate > 60)

-- Retrieve all records from the EmployeePayHistory table
-- where the BusinessEntityID is in the set of BusinessEntityIDs
-- where the Rate is equal to 39.06
SELECT *
FROM [HumanResources].[EmployeePayHistory]
WHERE [BusinessEntityID] IN (SELECT BusinessEntityID FROM [HumanResources].[EmployeePayHistory] WHERE Rate = 39.06)

-- Retrieve all records from the Product table
-- where the ProductID is in the set of ProductIDs
-- where the Quantity in the associated ProductInventory table is greater than 300
SELECT *
FROM [Production].[Product]
WHERE ProductID IN (SELECT ProductID FROM [Production].[ProductInventory] WHERE Quantity > 300)
