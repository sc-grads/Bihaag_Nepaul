SELECT 
    CountryRegionCode,
    SUM(SalesLastYear) AS TotalSalesLastYear,
    SUM(SalesYTD) AS TotalSalesYTD
FROM 
    dbo.SalesTerritoryData
GROUP BY 
    CountryRegionCode;