create table salesstaff
(
staffid int not null primary key,
firstname nvarchar(50) not null,
lastname nvarchar(50) not null,
countryregion nvarchar(50) not null
)

select * from salesstaff

----------------------------------------Standard Delete Statement
insert into salesstaff
select [BusinessEntityID],[FirstName],[LastName],[CountryRegionName] from [Sales].[vSalesPerson]

delete salesstaff;

delete from salesstaff

delete from salesstaff where countryregion =  'united states'


----------------------------------------Delete With RollBack
begin tran
delete from salesstaff where countryregion =  'united states'

commit

rollback tran


----------------------------------------Delete With Where Clause
delete from salesstaff where staffid in (select [BusinessEntityID] from [Sales].[vSalesPerson] where SalesLastYear = 0)


----------------------------------------Delete With Inner Join
delete salesstaff 
from  [Sales].[vSalesPerson] sp
inner join salesstaff ss
on sp.[BusinessEntityID] = ss.staffid
where sp.saleslastyear = 0 