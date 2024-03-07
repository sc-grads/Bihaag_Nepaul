--CREATE PROCEDURE SelectAllPersonAddress
--AS
--SELECT * FROM Person.Address

--go

--SELECT * FROM Person.Address

--execute SelectAllPersonAddress

--drop procedure SelectAllPersonAddressWithParam

CREATE PROCEDURE SelectAllPersonAddressWithEncryption (@City nvarchar(30) = 'New York')
WITH ENCRYPTION
AS

SET NOCOUNT ON

SELECT * FROM Person.Address where City = @City

go

execute SelectAllPersonAddressWithParam @City = 'Miami' 
execute SelectAllPersonAddressWithParam 'Miami' 