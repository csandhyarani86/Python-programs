import sys
import os


def HTMLREPORT(Row_Count):
    print Row_Count
    Time = Time
    if int(Row_Count) < 100:
        fs = open("d:\\Test20.html","a+")
        fs.write("<html><head><title>NEXTI Environment Result</title></head>")
        fs.write("\n")
        fs.write("<body>")
        fs.write("\n")
        fs.write("<table width='100%' border='0' cellspacing='0' cellpadding='0' bgcolor=''  noscroll>")
        fs.write("<tr>")
        fs.write("<td width='100%' colspan='100' height='10' bgcolor='#C0C0C0'><p align='center'><b><font face='Verdana' size='4' color='#000080'>NEXTI QAT DB Status Report</font></b></td>")
        fs.write("</tr>")
        fs.write('\n')
        fs.write("<tr>")
        fs.write("<td width='05%' height='25' bgcolor='#FFFFEE'><p style='margin-left: 5'><b><font face='Verdana' size='2'>Execution Environment</font></b></td>")
        fs.write("<td width='25%' height='25' bgcolor='#FFFFEE'><p style='margin-left: 5'><b><font face='Verdana' size='2'> QAT </font></b></td>")
        fs.write("\n")
        fs.write("</tr>")
        fs.write("</table>")
        fs.write("<table border='1' width='100%' bordercolordark='#A0C0B0' cellspacing='0' cellpadding='0' bordercolorlight='#C0C0C0' bordercolor='#C0C0C0' height='35' top='10'>")
        fs.write("\n")
        fs.write("<tr>")
        fs.write("<td width='6%' align='center' bgcolor='#C0C0C0' height='35'><b><font face='Verdana' size='2' color='#000080'>Sl.No.</font></b></td>")
        fs.write("<td width='12%' align='center' bgcolor='#C0C0C0' height='35'><b><font face='Verdana' size='2' color='#000080'> customer </font></b></td>")
        fs.write("<td width='12%' align='center' bgcolor='#C0C0C0' height='35'><b><font face='Verdana' size='2' color='#000080'> Module </font></b></td>")
        fs.write("<td width='20%' align='center' bgcolor='#C0C0C0' height='35'><b><font face='Verdana' size='2' color='#000080'> Environmental status </font></b></td>")
        fs.write("</tr>")
        fs.write("\n")
        fs.write("<TR><TD WIDTH='10%' align='center' BGCOLOR='Gainsboro'><FONT FACE='VERDANA' SIZE=2>1</FONT></TD>")
        fs.write("<TD WIDTH='25%' align='center' BGCOLOR='Gainsboro'><FONT FACE='VERDANA' SIZE=2> AV </FONT></TD>")
        fs.write("<TD WIDTH='25%' align='center' BGCOLOR='Gainsboro'><FONT FACE='VERDANA' SIZE=2> SBR </FONT></TD>")
        fs.write("<TD WIDTH='25%' align='center' BGCOLOR='Gainsboro'><FONT FACE='VERDANA' SIZE=2> PASSED </FONT></TD>")
        fs.write("</tr>")
        fs.write("</table>")        
       
HTMLREPORT('80','20:15:00')
