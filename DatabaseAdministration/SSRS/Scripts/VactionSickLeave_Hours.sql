  SELECT
    Gender,
    SUM(VacationHours) AS TotalVacationHours,
    SUM(SickLeaveHours) AS TotalSickLeaveHours
FROM
    [AdventureWorks2022].[dbo].[HRAnalysisTable]
GROUP BY
    Gender;
