SELECT
    e.BusinessEntityID,
    e.NationalIDNumber,
    e.LoginID,
    e.JobTitle,
    e.BirthDate,
    e.MaritalStatus,
    e.Gender,
    e.HireDate,
    e.SalariedFlag,
    e.VacationHours,
    e.SickLeaveHours,
    edh.DepartmentID,
    edh.ShiftID,
    edh.StartDate,
    edh.EndDate,
    eph.RateChangeDate,
    eph.Rate,
    eph.PayFrequency,
    jc.JobCandidateID,
    s.Name AS ShiftName,
    d.Name AS DepartmentName,
    d.GroupName AS DepartmentGroupName,
    e.ModifiedDate

INTO [HRAnalysisTable]
FROM
    [AdventureWorks2022].[HumanResources].[Employee] e
JOIN
    [AdventureWorks2022].[HumanResources].[EmployeeDepartmentHistory] edh ON e.BusinessEntityID = edh.BusinessEntityID
JOIN
    [AdventureWorks2022].[HumanResources].[EmployeePayHistory] eph ON e.BusinessEntityID = eph.BusinessEntityID
LEFT JOIN
    [AdventureWorks2022].[HumanResources].[JobCandidate] jc ON e.BusinessEntityID = jc.BusinessEntityID
LEFT JOIN
    [AdventureWorks2022].[HumanResources].[Shift] s ON edh.ShiftID = s.ShiftID
LEFT JOIN
    [AdventureWorks2022].[HumanResources].[Department] d ON edh.DepartmentID = d.DepartmentID;
