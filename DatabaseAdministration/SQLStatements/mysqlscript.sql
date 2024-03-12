CREATE DATABASE NewDatabase;


Use NewDatabase;


CREATE TABLE [dbo].[employees](
	[EmployeeID] [int] NOT NULL,
	[FirstName] [varchar](50) NULL,
	[LastName] [varchar](50) NULL,
);

Insert into [dbo].[employees] (EmployeeID,FirstName,LastName)
VALUES (1,'Bihaag','Nepaul');


SELECT * FROM employees;
  
SELECT name
FROM sys.databases;


