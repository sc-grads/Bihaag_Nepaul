-- Insert a new employee into [EmployeeHub].[dbo].[employees]
USE EmployeeHub

INSERT INTO [EmployeeHub].[dbo].[employees] (FirstName, LastName, Email, Department, Position, Salary)
VALUES ('John', 'Doe', 'john.doe@example.com', 'IT', 'Software Developer', 80000);
