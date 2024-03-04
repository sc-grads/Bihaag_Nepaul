
  SELECT
    Gender,
    MaritalStatus,
    COUNT(*) AS EmployeeCount
FROM
    [AdventureWorks2022].[dbo].[HRAnalysisTable]
GROUP BY
    Gender, MaritalStatus;


----------------------------------------------------
SELECT
    DepartmentName,
    AVG(VacationHours) AS AvgVacationHours,
    AVG(SickLeaveHours) AS AvgSickLeaveHours  ---------------------------calculating the average vacation hours and average sick leave hours for each department
FROM
    [AdventureWorks2022].[dbo].[HRAnalysisTable]
GROUP BY
    DepartmentName;

---------------------------------------------------------------
SELECT
    JobTitle,
    COUNT(*) AS EmployeeCount
FROM
    [AdventureWorks2022].[dbo].[HRAnalysisTable]
GROUP BY
    JobTitle;

