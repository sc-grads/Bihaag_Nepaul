-- Create a table named FunctionEmployee with columns: EmpID, FirstName, LastName, Salary, and Address
CREATE TABLE [dbo].[FunctionEmployee](
	[EmpID] [int] NOT NULL,
	[FirstName] [varchar](50) NULL,
	[LastName] [varchar](50) NULL,
	[Salary] [int] NULL,
	[Address] [varchar](100) NULL,
)

-- Insert data into the FunctionEmployee table
INSERT INTO [FunctionEmployee] ([EmpID],[FirstName],[LastName],[Salary],[Address]) VALUES (1,'Abbas','Mehmood', 20000, 'Delhi')
INSERT INTO [FunctionEmployee] ([EmpID],[FirstName],[LastName],[Salary],[Address]) VALUES (2,'Imran','Afzal', 50000, 'Delhi')
INSERT INTO [FunctionEmployee] ([EmpID],[FirstName],[LastName],[Salary],[Address]) VALUES (3,'James','Dino', 90000, 'Delhi')
INSERT INTO [FunctionEmployee] ([EmpID],[FirstName],[LastName],[Salary],[Address]) VALUES (4,'Jaga','Babu', 70000, 'Delhi')

-- Select all records from the FunctionEmployee table
SELECT * FROM FunctionEmployee

-- Create a scalar-valued function named fnGetEmpFullName that concatenates First Name and Last Name
CREATE FUNCTION fnGetEmpFullName
( @FirstName varchar(50), @LastName varchar(50))
RETURNS varchar(101)
AS
BEGIN
    RETURN(SELECT @FirstName + ' ' + @LastName);
END

-- Select the full name and salary by applying the fnGetEmpFullName function on the FunctionEmployee table
SELECT dbo.fnGetEmpFullName(FirstName,LastName) as FullName, Salary FROM FunctionEmployee

--------------------------------------------------------------------------------------------
-- Create a table-valued function named fnGetEmployee that returns all records from the FunctionEmployee table
CREATE FUNCTION fnGetEmployee()
RETURNS TABLE
AS
RETURN (SELECT * FROM FunctionEmployee)

-- Select all records from the FunctionEmployee table using the fnGetEmployee function
SELECT * FROM dbo.FunctionEmployee

------------------------------------------------------------------------------

-- Create a table-valued function named fnGetMulEmployee
CREATE FUNCTION [dbo].[fnGetMulEmployee]()
RETURNS @Emp TABLE
(
    Empid int,
    FirstName varchar(50),
    Salary int
)
AS
BEGIN
    -- Insert data into the @Emp table by selecting from the FunctionEmployee table
    INSERT INTO @Emp SELECT e.EmpID, e.FirstName, e.Salary FROM FunctionEmployee e;

    -- Update the salary of the first employee in the @Emp table
    UPDATE @Emp SET Salary = 25000 WHERE EmpID = 1;

    -- It will update only in the @Emp table, not in the original FunctionEmployee table
    RETURN
END 
GO

-- Select all records from the @Emp table using the fnGetMulEmployee function
SELECT * FROM dbo.fnGetMulEmployee()

