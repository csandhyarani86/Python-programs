
def wrapStringInHTMLMac(program, url, body):
    import datetime
    from webbrowser import open_new_tab
    Date = datetime.datetime.today().strftime("%Y-%m-%d")
    now = datetime.datetime.today().strftime("%Y%m%d-%H%M%S")
    filename = program + '.html'
    f = open(filename,'w')

    wrapper = """<html>
    <head>
    <title>NEXTI Environment Result</title>
    </head>
    <body>
    <"\n">
    <table width='100%' border='0' cellspacing='0' cellpadding='0' bgcolor=''  noscroll>
    <tr><td width='100%' colspan='100' height='10' bgcolor='#C0C0C0'><p align='center'><b><font face='Verdana' size='4' color='#000080'>NEXTI QAT DB Status Report</font></b></td></tr>
    <tr><td width='05%' height='25' bgcolor='#FFFFEE'><p style='margin-left: 5'><b><font face='Verdana' size='2'>Execution Environment</font></b></td><td width='25%' height='25' bgcolor='#FFFFEE'><p style='margin-left: 5'><b><font face='Verdana' size='2'> QAT </font></b></td>
    <"\n">
    <td width='05%' height='25' bgcolor='#FFFFEE'><p style='margin-left: 5'><b><font face='Verdana' size='2'>Execution Date</font></b></td><td width='25%' height='25' bgcolor='#FFFFEE'><p style='margin-left: 5'><b><font face='Verdana' size='2'>%s</font></b></td>
    </tr>
    </table>
    </body>
    </html>"""

    whole = wrapper % (Date)
    f.write(whole)
    f.close()

    #Change the filepath variable below to match the location of your directory
    filename = 'd:\\Test1' + filename

    #open_new_tab(filename)

wrapStringInHTMLMac("d:\\Test2" ,"https:\\google.com", "test")
