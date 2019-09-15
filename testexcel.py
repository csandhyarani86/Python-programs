import win32com.client
from win32com.client import constants

f = r"d:\Userfiles\bchandrashekar\Desktop\Test_Plan\NexTi_Master_Test_Plan_SBR.xlsx"
#DELETE_THIS = "X"

exc = win32com.client.gencache.EnsureDispatch("Excel.Application")
exc.Visible = 1
exc.Workbooks.Open(Filename=f)

