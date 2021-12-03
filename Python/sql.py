  conn = pyodbc.connect('Driver={SQL Server};'
                    'Server=DESKTOP-5RJSIM1\SQLEXPRESS;'
                    'Database=ERP;'
                    'Trusted_Connection=yes;')
  cursor = conn.cursor()



    # query = 'Declare @json1 nvarchar(max); SET @json1 = ?; EXC [exc].[Bol_Invoice] @json1 ;'
    # val = (response_invoice)
    #cursor.execute('Declare @json1 nvarchar(max); SET @json1 = ?; EXC [exc].[Bol_Invoice] @json1 ;', response_invoice)
    # for invoice in response_invoice['invoiceListItems']:
    # InvoiceId.append(invoice['invoiceId'])
    # InvoiceId.append(invoice['issuePeriod'])

    
  conn.commit()
  conn.close()