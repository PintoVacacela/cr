USE [cr_test]
GO

INSERT INTO [dbo].[document_type]
           ([name]
           ,[state])
     VALUES
           ('CEDULA','ACTIVO'),
		   ('PASAPORTE','ACTIVO')

INSERT INTO [dbo].[user_type]
           ([nombre]
           ,[state])
     VALUES
           ('ADMIN','ACTIVO'),
		   ('CLIENTE','ACTIVO')

INSERT INTO [dbo].[application_user]
           ([name]
           ,[username]
           ,[lastname]
           ,[documentType_id]
           ,[identification]
           ,[email]
           ,[password]
           ,[userState]
           ,[userType_id])
     VALUES
           ('iuser1', 'iuser1','iuser1', 1, '0000000000','pintoandres2014a@gmail.com','m','ACTIVO',1),
		   ('iuser2', 'iuser2','iuser2', 1, '0000000001','1542265@gmail.com','m','ACTIVO',1)
GO


