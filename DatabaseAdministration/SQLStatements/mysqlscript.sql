--CREATE DATABASE NewDatabase;

--GO

USE NewDatabase;


--CREATE TABLE [dbo].[employees](
--[EmployeeID] [int] NOT NULL,
--[FirstName] [varchar](50) NULL,
--[LastName] [varchar](50) NULL,
--);

Insert into [dbo].[employees] (EmployeeID,FirstName,LastName)
VALUES (2,'Bongani','Mondlane');



SELECT * FROM employees;
  
--SELECT name
--FROM sys.databases;


