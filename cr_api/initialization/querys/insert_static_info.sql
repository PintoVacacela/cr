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
('ACTIVO'	,'HOME',	'Inicio',	'bi bi-house-door-fill',	NULL,	1	,'home'),
('ACTIVO'	,'USER',	'Usuarios',	'bi bi-people-fill',	NULL,	2	,'users'),
('ACTIVO'	,'CLIE',	'Clientes',	'bi bi-handbag-fill',	NULL,	5	,NULL),
('ACTIVO'	,'PROF',	'Perfiles',	'bi bi-fingerprint',	NULL,	4	,'profiles'),
('ACTIVO'	,'CLCA',	'Categorias', 	NULL,	'CLIE',	2	,'clients/categories'),
('ACTIVO'	,'CLCL',	'Clientes',	  NULL,	'CLIE',	1	,'clients'),
('ACTIVO'	,'PROD',	'Productos',	'bi bi-cup-hot-fill',	NULL,	6	,'products'),
('ACTIVO'	,'EVNT',	'Eventos'	,'bi bi-calendar2-event-fill',	NULL,	2,	'events'),
('ACTIVO'	,'CALE',	'Calendario',	'bi bi-calendar-week',	NULL,	7,	'calendar'),
('ACTIVO'	,'NOTF',	'Notificaciones',	'bi bi-bell-fill',	NULL,	3,	'notifications'),
('ACTIVO'	,'ASIG',	'Asignaciones',	NULL,	'CLIE',	3	,'clients/assignments'),
('ACTIVO'	,'FACT',	'Facturacion',	'bi bi-receipt',	NULL,	8,	NULL),
('ACTIVO'	,'FACF',	'Facturas', 	NULL,	'FACT',	1,	'billing')


        

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

USE [cr_test]
GO

INSERT INTO [dbo].[profile_menus]
           ([profile_id]
           ,[menu_id])
     VALUES
           (1,1),
		   (1,2),
		   (1,3),
		   (1,4),
		   (1,5),
		   (1,6),
		   (1,7),
		   (1,8),
		   (1,9),
		   (1,10),
		   (1,11),
		   (1,12)

GO


