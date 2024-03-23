EXEC msdb.dbo.sp_send_dbmail
 @recipients = 'sqlreportsbn@gmail.com',
 @subject = 'Average Salary per Gender',  
 @body = 'Company Employee Average Salary',
 @query = 'USE EmployeeHub SELECT * FROM [dbo].[GenderAvg];';
--
