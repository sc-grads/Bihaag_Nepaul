create table salesstaff
(
	staffid int not null primary key,
	fName nvarchar(30) not null,
	lName nvarchar(30) not null
	)

CREATE TABLE [dbo].[salesstaffNew](
	ID [int] not null IDENTITY PRIMARY KEY,
	[staffid] [int] NOT NULL,
	[fName] [nvarchar](30),
	[lName] [nvarchar](30)
	)
------------------------------------------------------------------------------------------ Normal Insert Statements
	insert into salesstaff (staffid,fName,lName) VALUES (200,'bihaag','nepaul')

	INSERT INTO [dbo].[salesstaff] (STAFFID,FNAME,LNAME) VALUES (300,'Imran','Afzal'),(325,'John','Vick'),(314,'James','Dino')

	--SalesStaffNew insert

	INSERT INTO [dbo].[salesstaffNew] (STAFFID,FNAME,LNAME) VALUES (300,'Imran','Afzal'),(325,'John','Vick'),(314,'James','Dino')

	insert into salesstaffnew(staffid,fName,lName) VALUES (200,'bihaag','nepaul')

	select * from salesstaffNew

	select * from salesstaff

	--NameOnlyTable

	CREATE TABLE [dbo].[nameOnlyTable](
	
	[fName] [nvarchar](30),
	[lName] [nvarchar](30)
	)

	select * from [nameOnlyTable]
------------------------------------------------------------------------------------------ Insert Statement With Where Clause
	insert into nameOnlyTable (fname,lname)
	select fname,lname from salesstaffNew where id >= 3
------------------------------------------------------------------------------------------ Insert Statement for bkp File
	select * into salesstaffNew_bkp from salesstaffNew

	  select * from salesstaffNew_bkp