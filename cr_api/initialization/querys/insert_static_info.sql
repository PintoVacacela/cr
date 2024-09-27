USE [cr_test]
GO

INSERT INTO [dbo].[application_menu]
           ([state]
           ,[code]
           ,[name]
           ,[icon]
           ,[code_parent]
           ,[position]
           ,[route])
     VALUES
           ('ACTIVO','HOME','Inicio','bi bi-house',null,1,'home'),
		   ('ACTIVO','USER','Usuarios','bi bi-people-fill',null,1,'users'),
		   ('ACTIVO','CLIE','Clientes','bi bi-handbag',null,1,'clients')

INSERT INTO [dbo].[document_type]
           ([state]
           ,[name])
     VALUES
           ('ACTIVO','CEDULA'),
		('ACTIVO','PASAPORTE')

INSERT INTO [dbo].[user_type]
           ([state]
           ,[name])
     VALUES
          ('ACTIVO','ADMIN'),
		   ('ACTIVO','CLIENTE')

INSERT INTO [dbo].[profile]
           ([name]
           ,[code]
           ,[state])
     VALUES
           ('ADMIN'
           ,'ADMIN'
           ,'ACTIVO')

INSERT INTO [dbo].[application_user]
           ([state]
           ,[name]
           ,[username]
           ,[lastname]
           ,[documentType_id]
           ,[identification]
           ,[email]
           ,[designation]
           ,[phone_number]
           ,[password]
           ,[userState]
           ,[userType_id]
           ,[photo_url]
           ,[profile_id])
     VALUES
           ('ACTIVO','iuser1', 'iuser1','iuser1', 1, '0000000000','pintoandres2014a@gmail.com','admin_test','0992626973','m','ACTIVO',1,'',1),
		   ('ACTIVO','iuser2', 'iuser2','iuser2', 1, '0000000001','1542265@gmail.com','admin_test','0992626973','m','ACTIVO',1,'',1)
GO


