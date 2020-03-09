"""data= [1100,150,1111,15978]
for item in data:
    y=len(str(item))
    if(y==4):
        print(item)

print(data[-1])"""


from xlwt import Workbook

data=[11,22,33,44,55,66,77,88,99,110]

def wrtexlm():
	for i in range(10):
		for j in range(10):
			sh1.write(i,j,data[i])
            
	wb.save('xlwt_ex.xls')
    

def main():
	global wb
	wb=Workbook()
	global sh1
	sh1=wb.add_sheet('sheet_1')
	wrtexlm()

main()