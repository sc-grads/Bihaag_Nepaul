
Use AdventureWorks2022

--Solution 1**

Select * from [HumanResources].[Employee] order by jobtitle;

--Solution 2**

Select * from [Person].[Person] ORDER BY LastName;

--Solution 3

SELECT FirstName,Lastname,BusinessEntityID AS employee_id From [Person].[Person];

--Solution 4

SELECT ProductID, ProductNumber,Name as producname from [Production].[Product] where sellstartdate IS NOT NULL and productline = 'T' ORDER BY Name ASC;

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

SELECT productid, sum(quantity) AS total_quantity from [Production].[Productinventory] 
where Shelf in ('A','C','H')
GROUP BY productid
HAVING sum(quantity) > 500
ORDER BY productid ASC;

--Solution 10

Select SUM(Quantity) as total_quantity from [Production].[Productinventory] GROUP BY (locationid * 10);

--Solution 11

select person.BusinessEntityID, person.firstname, person.lastname, phoneno.phonenumber as person_phone
from Person.Person as person
inner join person.PersonPhone as phoneno
on person.BusinessEntityID = phoneno.BusinessEntityID
where lastname LIKE 'L%'  
ORDER BY lastname, firstname;

--Solution 12 **
select * from [Sales].[SalesOrderHeader]

/*
Syntax:

SELECT column, aggregate_function(column)

FROM table

GROUP BY ROLLUP (column);*/

SELECT salespersonid, customerid, SUM(SubTotal) AS sum_total from [Sales].[SalesOrderHeader] WHERE SalesPersonID IS NOT NULL
GROUP BY ROLLUP (salespersonid, customerid);

--Solution 13**
select locationid, shelf, SUM(quantity) as totalquantity from [Production].[ProductInventory]
Group by rollup (locationid, shelf)
order by locationId;

--tried also using rollup

--Solution 14**

select locationid, shelf, SUM(Quantity) as totalquantity from [Production].[ProductInventory]
Group by grouping sets (rollup (locationId,shelf), CUBE (locationid,shelf));

--Solution 15**

SELECT LocationID, SUM(Quantity) AS TotalQuantity FROM Production.ProductInventory GROUP BY rollup (LocationID)

--Solution 16
 select * from [Person].[BusinessEntityAddress]
select * from [Person].[Address]


select pa.city, count(ba.addressid) as noofemployees
from [Person].[BusinessEntityAddress] ba
join [Person].[Address] pa
on ba.addressid = pa.addressid
group by city
order by city asc;

--Solution 17
select * from [Sales].[SalesOrderHeader]

select year(orderdate) as year, sum(totaldue) as orderamount
from [Sales].[SalesOrderHeader]
group by year(orderdate)
order by year asc;

--Solution 18
select year(orderdate) as year, sum(totaldue) as orderamount
from [Sales].[SalesOrderHeader]
group by year(orderdate)
having year(orderdate) <=2016
order by year asc;

--Solution 19
select * from [Person].[ContactType]

select contacttypeid, name from [Person].[ContactType] WHERE name LIKE '%Manager%'
Order by name desc

--Solution 20
select * from [Person].[BusinessEntityContact]
select * from [Person].[ContactType]
select * from [Person].[Person]



select psn.BusinessEntityID, psn.firstname, psn.lastname

from [Person].[BusinessEntityContact] as bec

inner join [Person].[ContactType] as ct
on ct.ContactTypeID = bec.ContactTypeID

inner join [Person].[Person] as psn
on psn.BusinessEntityID = bec.PersonID

where ct.Name = 'Purchasing Manager'

order by lastname, firstname ASC;

--Solution 21

Select * from [Person].[Person]
Select * from [Person].[Address]
Select * from [Sales].[SalesPerson]


select ROW_NUMBER() Over (Partition by PostalCode Order by salesytd desc) as "Row Number",
p.lastname, sls.salesytd, ad.postalcode

from [Sales].[SalesPerson] as sls

join [Person].[Person] as p
on sls.BusinessEntityID = p.BusinessEntityID

join [Person].[Address] as ad
on ad.AddressID = p.BusinessEntityID

where TerritoryID IS NOT NULL 
	and SalesYTD <> 0
Order by PostalCode;

--Solution 22

select * from [Person].[BusinessEntityContact]
select * from [Person].[ContactType]


select ct.contacttypeid, ct.name as ctypename, COUNT(*) as nocontacts

from [Person].[BusinessEntityContact] as bec
join  [Person].[ContactType] as ct 
on ct.ContactTypeID = bec.ContactTypeID

group by ct.ContactTypeID,ct.Name
having count(*) >= 100
order by count(*) desc;


--Solution 23
select * from [HumanResources].[EmployeePayHistory]
select * from [Person].[Person]

select cast(hr.ratechangedate as date) as fromdate, CONCAT(lastname, ',', firstname, ' ',middleName) as NameinFull,
(40*hr.rate) as salaryinaweek

from [Person].[Person] as p
join [HumanResources].[EmployeePayHistory] as hr
on hr.BusinessEntityID = p.BusinessEntityID
order by NameinFull;


--Solution 24
select cast(hr.ratechangedate as date) as fromdate, CONCAT(lastname, ',', firstname, ' ',middleName) as NameinFull,
(40*hr.rate) as salaryinaweek

from [Person].[Person] as p
join [HumanResources].[EmployeePayHistory] as hr
on hr.BusinessEntityID = p.BusinessEntityID

where hr.RateChangeDate = (select MAX(ratechangedate) from [HumanResources].[EmployeePayHistory] where BusinessEntityID = hr.BusinessEntityID)


order by NameinFull;

--Solution 25
select * from [Sales].[SalesOrderDetail];

select SalesOrderID,ProductID,OrderQty,

SUM(OrderQty) over (PARTITION BY Salesorderid) as "TotalQuantity",

AVG(cast(OrderQty as decimal(10,4))) over (PARTITION BY salesorderid) as "No of Orders",

count(OrderQty) over (PARTITION BY salesorderid) as "No of Orders",

min(OrderQty) over (PARTITION BY salesorderid) as "Min Quantity",

max(OrderQty) over (PARTITION BY salesorderid) as "Max Quantity"
from [Sales].[SalesOrderDetail]

where SalesOrderID IN (43659,43664);






