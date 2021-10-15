USE [ERP]
GO

/****** Object:  Table [art].[Products]    Script Date: 15/10/2021 22:26:39 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [art].[Products](
	[ProductCode] [nchar](50) NULL,
	[EAN] [bigint] NOT NULL,
	[Supplier SKU] [nchar](50) NULL,
	[Color] [nchar](10) NULL,
	[Size] [nchar](10) NULL,
	[Description] [nchar](100) NULL,
	[Link] [nchar](300) NULL
) ON [PRIMARY]
GO


