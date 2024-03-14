--CREATE DATABASE NewDatabase;

--GO

USE EmployeeHub;

EXEC [GetGenderAverageSalary];
--CREATE TABLE [dbo].[employees](
--[EmployeeID] [int] NOT NULL,
--[FirstName] [varchar](50) NULL,
--[LastName] [varchar](50) NULL,
--);

--Insert into [dbo].[employees] (EmployeeID,FirstName,LastName)
--VALUES (2,'Bongani','Mondlane');



/*INSERT INTO [EmployeeHub].[dbo].[EmployeeData] (
    [BusinessEntityID],
    [NationalIDNumber],
    [LoginID],
    [JobTitle],
    [BirthDate],
    [MaritalStatus],
    [Gender],
    [HireDate],
    [SalariedFlag],
    [VacationHours],
    [SickLeaveHours],
    [DepartmentID],
    [ShiftID],
    [StartDate],
    [EndDate],
    [RateChangeDate],
    [Rate],
    [PayFrequency],
    [JobCandidateID],
    [ShiftName],
    [DepartmentName],
    [DepartmentGroupName],
    [ModifiedDate]
) 
VALUES (
    18,
    '987654321',
    'adventure-works\jane0',
    'Senior Software Engineer',
    '1985-08-12',
    'S',
    'M',
    '2023-02-10',
    1,
    15,
    25,
    1,
    1,
    '2023-02-10',
    NULL,
    '2023-02-10 00:00:00.000',
    85.25,
    2,
    NULL,
    'Day',
    'Engineering',
    'Research and Development',
    '2024-03-14 00:00:00.000'
);


INSERT INTO [EmployeeHub].[dbo].[EmployeeData] (
    [BusinessEntityID],
    [NationalIDNumber],
    [LoginID],
    [JobTitle],
    [BirthDate],
    [MaritalStatus],
    [Gender],
    [HireDate],
    [SalariedFlag],
    [VacationHours],
    [SickLeaveHours],
    [DepartmentID],
    [ShiftID],
    [StartDate],
    [EndDate],
    [RateChangeDate],
    [Rate],
    [PayFrequency],
    [JobCandidateID],
    [ShiftName],
    [DepartmentName],
    [DepartmentGroupName],
    [ModifiedDate]
) 
VALUES (
    19,
    '112233445',
    'adventure-works\mike0',
    'Lead Software Engineer',
    '1980-04-18',
    'M',
    'M',
    '2023-03-05',
    1,
    20,
    20,
    1,
    1,
    '2023-03-05',
    NULL,
    '2023-03-05 00:00:00.000',
    100.00,
    2,
    NULL,
    'Day',
    'Engineering',
    'Research and Development',
    '2024-03-14 00:00:00.000'
);
*/
