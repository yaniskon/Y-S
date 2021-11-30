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
-- Author:		<Yanis
-- Create date: <2021-11-29>
-- Description:	<Add Invoice information fro Bol.com API>
-- =============================================
alter PROCEDURE exc.Bol_Invoice 
(@json NVARCHAR(MAX) = '')
AS
BEGIN
	-- SET NOCOUNT ON added to prevent extra result sets from
	-- interfering with SELECT statements.
	SET NOCOUNT ON;

    -- Insert statements for procedure here
	INSERT INTO stg.Bol_Invoice
	SELECT invoiceId 
		FROM OPENJSON(@json)
		WITH (
				invoiceId NVARCHAR(50) '$.period' 	
			 )

END
GO
