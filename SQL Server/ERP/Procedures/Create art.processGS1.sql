-- ================================================
-- Template generated from Template Explorer using:
-- Create Procedure (New Menu).SQL
--
-- Use the Specify Values for Template Parameters 
-- command (Ctrl-Shift-M) to fill in the parameter 
-- values below.
--
-- This block of comments will not be included in
-- the definition of the procedure.
-- ================================================
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
-- =============================================
-- Author:		<Yanis>
-- Create date: <28/11/2021>
-- Description:	<Gs1 From Staging into main table>
-- =============================================
CREATE PROCEDURE art.Process 

AS
BEGIN
	-- SET NOCOUNT ON added to prevent extra result sets from
	-- interfering with SELECT statements.
	SET NOCOUNT ON;


	INSERT INTO ERP.art.Products ([EAN], [Gs1 Product Catergory], [Brand], [Gs1 Description], [Gs1 Language description], [Gs1 Status])

	SELECT DISTINCT [GS1 Artikelcode (GTIN)],
					[Productclassificatie],
					[Merk],
					[Productomschrijving (max 35 tekens)],
					[Taal van productomschrijving],
					[Status]
	FROM ERP.stg.Gs1
	WHERE [Productomschrijving (max 35 tekens)] <> ''
	AND [GS1 Artikelcode (GTIN)]  <> '8720387440030' --This Gs1 code is not used (I can use it in the future or deactivate from Gs1)
	AND [GS1 Artikelcode (GTIN)] NOT IN (SELECT EAN FROM ERP.art.Products)

	UPDATE pr
	SET pr.ProductCode = bn.ProductCode, pr.[Supplier SKU] = bn.[Supplier SKU], pr.Color = bn.Color, pr.Size = bn.Size
	FROM [ERP].[art].[Products] pr, [ERP].[art].[Bnatural] bn
	WHERE pr.EAN = bn.EAN

END
GO
