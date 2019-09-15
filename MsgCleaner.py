file1=r"d:\Userfiles\bchandrashekar\Desktop\DWH_19-06-18\message2_AY_4140.edi"
out=open('cleaned.txt','w')
with open(file1,'r') as edi:
    for line in edi:
        ln1=line.replace('\x1d','+')
        ln2=ln1.replace('\x1f',':')
        ln3=ln2.replace('\x1c','\'\n')
        ln4 = ln3.replace('\x19','*')
        out.write(ln4)
out.close()
        
                    
