---------------------------------------------- Normal Joins
SELECT * FROM [dbo].[Employee]

SELECT * FROM [dbo].[Sales]

select e.EmpID,e.EmpName,s.SalesNumber,s.ItemSold from [dbo].[Employee] e
JOIN [dbo].[Sales] s
on e.empid = s.empid

SELECT e.EmpID,e.EmpName,s.SalesNumber,s.ItemSold FROM [dbo].[Employee] e
join [dbo].[Sales] s 
on e.EmpID = s.[EmpID]
order by e.EmpID


SELECT count(s.SalesNumber) AS NoOfSales,e.EmpID,e.EmpName FROM [dbo].[Employee] e
join [dbo].[Sales] s 
on e.EmpID = s.[EmpID]
group by e.EmpID,e.EmpName

SELECT * FROM [dbo].[Student]

SELECT * FROM [dbo].[Course]

---------------------------------------------- Different Joins(inner,left,right,full)
select * from [dbo].[Student] s
inner join [dbo].[Course] c 
on s.RollNo = c.RollNO

select s.RollNo,s.StudentName,c.CourseID from [dbo].[Student] s
inner join [dbo].[Course] c 
on s.RollNo = c.RollNO

select s.RollNo,s.StudentName,c.CourseID from [dbo].[Student] s
left join [dbo].[Course] c 
on s.RollNo = c.RollNO


select s.RollNo,s.StudentName,c.CourseID from [dbo].[Student] s
right join [dbo].[Course] c 
on s.RollNo = c.RollNO


select s.RollNo,s.StudentName,c.CourseID from [dbo].[Student] s
full join [dbo].[Course] c 
on s.RollNo = c.RollNO

