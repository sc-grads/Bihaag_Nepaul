Create Database EmployeeDatabase;

Use EmployeeDatabase;

--------------------------------------------------Create Table 1
/*CREATE TABLE [dbo].[EmployeeData](
	[BusinessEntityID] [int] NOT NULL,
	[NationalIDNumber] [nvarchar](15) NOT NULL,
	[LoginID] [nvarchar](256) NOT NULL,
	[JobTitle] [nvarchar](50) NOT NULL,
	[BirthDate] [date] NOT NULL,
	[MaritalStatus] [nchar](1) NOT NULL,
	[Gender] [nchar](1) NOT NULL,
	[HireDate] [date] NOT NULL,
	[SalariedFlag] [bit] NOT NULL,
	[VacationHours] [smallint] NOT NULL,
	[SickLeaveHours] [smallint] NOT NULL,
	[DepartmentID] [smallint] NOT NULL,
	[ShiftID] [tinyint] NOT NULL,
	[StartDate] [date] NOT NULL,
	[EndDate] [date] NULL,
	[RateChangeDate] [datetime] NOT NULL,
	[Rate] [money] NOT NULL,
	[PayFrequency] [tinyint] NOT NULL,
	[JobCandidateID] [int] NULL,
	[ShiftName] [nvarchar](50) NULL,
	[DepartmentName] [nvarchar](50) NULL,
	[DepartmentGroupName] [nvarchar](50) NULL,
	[ModifiedDate] [datetime] NOT NULL
)
*/

GO
--------------------------------------------------Create Table 2

/*CREATE TABLE [dbo].[GenderAvg](
	[Gender] [nvarchar](20) NULL,
	[AverageSalary] [decimal](18, 4) NULL
)*/

GO
----------------------------------------------------------Populate Table
/*INSERT INTO EmployeeDatabase.dbo.EmployeeData (
    BusinessEntityID,
    NationalIDNumber,
    LoginID,
    JobTitle,
    BirthDate,
    MaritalStatus,
    Gender,
    HireDate,
    SalariedFlag,
    VacationHours,
    SickLeaveHours,
    DepartmentID,
    ShiftID,
    StartDate,
    EndDate,
    RateChangeDate,
    Rate,
    PayFrequency,
    JobCandidateID,
    ShiftName,
    DepartmentName,
    DepartmentGroupName,
    ModifiedDate
)
SELECT 
    BusinessEntityID,
    NationalIDNumber,
    LoginID,
    JobTitle,
    BirthDate,
    MaritalStatus,
    Gender,
    HireDate,
    SalariedFlag,
    VacationHours,
    SickLeaveHours,
    DepartmentID,
    ShiftID,
    StartDate,
    EndDate,
    RateChangeDate,
    Rate,
    PayFrequency,
    JobCandidateID,
    ShiftName,
    DepartmentName,
    DepartmentGroupName,
    ModifiedDate
FROM [AdventureWorks2022].[dbo].[HRAnalysisTable];*/

--------------------------------------------------------------------- Stored Procedure
/*
CREATE PROCEDURE [dbo].[GetGenderAverageSalary]
AS
BEGIN
	TRUNCATE TABLE [dbo].[GenderAvg]
    SELECT Gender, AVG(Rate) AS AverageSalary
    FROM EmployeeData
    GROUP BY Gender;

	INSERT INTO [dbo].[GenderAvg] (Gender, AverageSalary)
    SELECT Gender, AVG(Rate) AS AverageSalary
    FROM EmployeeData
    GROUP BY Gender;
	
	EXEC msdb.dbo.sp_send_dbmail
	@recipients = 'sqlreportsbn@gmail.com',
	@subject = 'Average Salary per Gender',  
	@body = 'Company Employee Average Salary',
	@query = 'USE EmployeeHub SELECT * FROM [dbo].[GenderAvg];';

END;
*/

--EXEC [GetGenderAverageSalary]; Executing Stored Procedure



DROP DATABASE EmployeeDatabase;
