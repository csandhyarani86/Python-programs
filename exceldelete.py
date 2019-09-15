import win32com.client
app = win32com.client.Dispatch("Excel.Application")   
#app.Visible = 1

# Lastly we will assume that the workbook is active and get the first sheet
Excel_path = raw_input("Input Excel file path: \n") 
wbk = app.Workbooks.Open(Excel_path)
sheet = wbk.Sheets(1) 
  
# delete the first row in your active sheet 
sheet.Rows(2).Delete()
wbk.Save()
app.Application.Quit()
sheet = None
wbk = None
app = None
