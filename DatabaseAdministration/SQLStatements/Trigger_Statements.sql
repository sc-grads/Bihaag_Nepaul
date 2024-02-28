SELECT TOP (1000) [EmpID]
      ,[EmpName]
      ,[EmpTitle]
  FROM [AdventureWorks2022].[dbo].[Employee]

  -------------------------------------------------------------------trigger creation
    CREATE TRIGGER [dbo].[EmployeeInsert] 
   ON  [dbo].[Employee] 
   AFTER INSERT
AS 
BEGIN
	-- SET NOCOUNT ON added to prevent extra result sets from
	-- interfering with SELECT statements.
	SET NOCOUNT ON;

    -- Insert statements for trigger here
	Insert into EmployeeTriggerHistory values ((select max(EmpID) from employee),'Insert')


END

GO

select * from [dbo].[EmployeeTriggerHistory]

