USE AdventureWorks2022;

SELECT
	e.BusinessEntityID,
	d.DepartmentID,
    e.JobTitle,
    e.HireDate,
    ejc.Resume
INTO EmployeeJobDescription

FROM
    HumanResources.Employee e
INNER JOIN
    [HumanResources].[JobCandidate] ejc ON e.BusinessEntityID = ejc.BusinessEntityID
INNER JOIN
	[HumanResources].[EmployeeDepartmentHistory] d ON e.BusinessEntityID = d.BusinessEntityID;