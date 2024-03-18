WITH DepartmentGenderContribution AS (
    SELECT 
        D.DepartmentGroupName,
        D.DepartmentName,
        D.Gender,
        AVG(D.Rate) AS TotalSalaryContribution,
        ROW_NUMBER() OVER (PARTITION BY D.DepartmentName ORDER BY AVG(D.Rate) DESC) AS ContributionRank
    FROM 
        [AdventureWorks2022].[dbo].[HRAnalysisTable] D
    GROUP BY 
        D.DepartmentGroupName, D.DepartmentName, D.Gender
),
DepartmentGroupMaxAvgRate AS (
    SELECT 
        DGMAR.DepartmentGroupName,
        DGMAR.DepartmentName,
        MAX(DGMAR.AvgRate) AS MaxAvgRate
    FROM (
        SELECT 
            D.DepartmentGroupName,
            D.DepartmentName,
            AVG(D.Rate) AS AvgRate
        FROM 
            [AdventureWorks2022].[dbo].[HRAnalysisTable] D
        GROUP BY 
            D.DepartmentGroupName, D.DepartmentName, D.Gender
    ) DGMAR
    GROUP BY 
        DGMAR.DepartmentGroupName, DGMAR.DepartmentName
)
SELECT 
    DGC.DepartmentGroupName,
    DGC.Gender,
    AVG(DGMAR.MaxAvgRate) AS AverageHighestEarning
FROM 
    DepartmentGenderContribution DGC
JOIN 
    DepartmentGroupMaxAvgRate DGMAR ON DGC.DepartmentName = DGMAR.DepartmentName AND DGC.TotalSalaryContribution = DGMAR.MaxAvgRate
GROUP BY 
    DGC.DepartmentGroupName, DGC.Gender;