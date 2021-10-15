USE ERP
GO

CREATE table art.Measurements (
	[Productcode] varchar(50),
	[EAN] bigint NOT NULL,
	[Waist(cm)] decimal(3,2) NULL,
	[Hips(cm)] decimal(3,2) NULL,
	[Waist(inch)] decimal (3,2) NULL,
	[Hips(inch)] decimal (3,2) NULL,
	[Waist range(cm)] varchar(20) NULL,
	[Hips range(cm)] varchar(20) NULL,
	[Package height (cm)] int NULL,
	[Package length (cm)] int NULL,
	[Package width (mm)] int NULL
	)
