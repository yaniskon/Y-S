USE [ERP]
GO

/****** Object:  Table [art].[ProductsTEMP]    Script Date: 28/11/2021 18:51:58 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [art].[Products](
	[ProductCode] [nchar](50) NULL,
	[EAN] [bigint] NOT NULL,
	[Supplier SKU] [nchar](50) NULL,
	[Brand] [nchar] (50) NULL,
	[Color] [nchar](10) NULL,
	[Size] [nchar](10) NULL,
	[Description] [nchar](100) NULL,
	[Gs1 Description] [nchar] (35) NULL,
	[Gs1 Language description] [nchar] (35) NULL,
	[Gs1 Product Catergory] [nchar] (100) NULL,
	[Gs1 Status] [nchar](20) NULL,
	[Link] [nchar](300) NULL
) ON [PRIMARY]
GO


