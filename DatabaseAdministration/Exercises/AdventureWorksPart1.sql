
Use AdventureWorks2022

--Solution 1 

Select * from [HumanResources].[Employee];

--Solution 2

Select * from [Person].[Person] ORDER BY LastName;

--Solution 3

SELECT FirstName,Lastname,BusinessEntityID AS employee_id From [Person].[Person];

--Solution 4

SELECT ProductID, ProductNumber,Name from [Production].[Product] where sellstartdate IS NOT NULL and productline = 'T' ORDER BY Name ASC;

--Solution 5

SELECT salesorderid, customerid, orderdate, subtotal,(TaxAmt/SubTotal) * 100 as tax_percentage FROM [Sales].[SalesOrderHeader]
ORDER BY SubTotal DESC;

--Solution 6

SELECT DISTINCT Jobtitle from [HumanResources].[Employee] order by JobTitle asc;

--Solution 7

Select CustomerID,SUM(Freight) as total_freight from [Sales].[SalesOrderHeader] GROUP BY CustomerID ORDER BY CustomerID ASC;

--Solution 8

SELECT customerid,salespersonid,AVG(SubTotal) as avg_subtotal,SUM(SubTotal) as sum_subtotal FROM [Sales].[SalesOrderHeader] 
GROUP BY CustomerID,salespersonid
Order by CustomerID desc;

--Solution 9

SELECT productid, sum(quantity) AS total_quantity from production.productinventory 
where Shelf in ('A','C','H')
GROUP BY productid
HAVING sum(quantity) > 500
ORDER BY productid ASC;

--Solution 10

Select SUM(Quantity) as total_quantity from production.productinventory GROUP BY (locationid * 10);

--Solution 11

select person.BusinessEntityID, person.firstname, person.lastname, phoneno.phonenumber as person_phone
from Person.Person as person
inner join person.PersonPhone as phoneno
on person.BusinessEntityID = phoneno.BusinessEntityID
where lastname LIKE 'L%'  
ORDER BY lastname, firstname;