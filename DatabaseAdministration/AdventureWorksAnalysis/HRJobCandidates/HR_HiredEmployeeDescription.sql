USE AdventureWorks2022;

SELECT 
    j.[BusinessEntityID]
    ,d.Name AS DepartmentName
	,CONCAT(p.FirstName, ' ', p.LastName) AS Name
    ,j.JobTitle 
    ,j.[HireDate]
    ,j.[Resume]

INTO HiredEmployeeDescription
FROM 
    [dbo].[EmployeeJobDescription] j
INNER JOIN
    [HumanResources].[Department] d ON j.DepartmentID = d.DepartmentID
INNER JOIN
	[Person].[Person] p ON j.BusinessEntityID = p.BusinessEntityID;