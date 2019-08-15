import os
import pandas as pd
from openpyxl import load_workbook
import shutil

def csv2xl(csvFileName, xlFileName, kommunekode):
    os.listdir('.')
    FileName = xlFileName+kommunekode
    print("Writing " + csvFileName + " to " + FileName+'.xlsm')
    shutil.copyfile(xlFileName+'.xlsm', FileName+'.xlsm')
    data = pd.read_csv(csvFileName, encoding='latin1', header=0, quotechar='"', delimiter=";")
    book = load_workbook(filename=xlFileName+'.xlsm', read_only=False, keep_vba=True)
    writer = pd.ExcelWriter(FileName+'.xlsm', engine='openpyxl')
    writer.book = book
    data.to_excel(writer, sheet_name='BBR')
    writer.save()
    writer.close()
    print("Done writing " + csvFileName + " to " + FileName + '.xlsm')



def xl2csv(csvFileName, xlsxFileName, xlsxSheetName):
    print("Writing "+xlsxFileName+" to "+csvFileName)
    os.listdir('.')
    data_xls = pd.read_excel(xlsxFileName, xlsxSheetName, index_col=1, encoding='utf-8')
    data_xls.to_csv(csvFileName, encoding='utf-8-sig', header=True, index=False, quotechar='"', sep=";")



