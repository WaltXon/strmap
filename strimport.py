import xlwt
import xlrd

fileToRead = ''
fileToWrite = ''
##READ ORIGINAL SS

def ImportDIData(filepath_in, filepath_out):
    pass

##ADD A GUID


##WRITE OUT NEW SPREADSHEET
sheet.write(0,0,'TO_FILE_NAME')
sheet.write(0,1,"TO_FILE_PATH")

row = 1
for item in inventory:
    sheet.write(row, 0, item[0])
    sheet.write(row, 1, item[1])
    row +=1
print('============Saving Excel File------------------')

book.save(excelFile)

print('============All your base  are belong to us!------------------')
##READ IN ONLY THE IMPORTANT COLUMNS FROM NEW SPREADSHEET

##RETURN A LIST WITH IMPORTANT DATA
