import os
import math
import csv
import pandas as pd
import numpy as np
from openpyxl import load_workbook
from openpyxl import Workbook
import shutil

def csv2xl(csvFileName, xlFileName, kommunekode):
    os.listdir('.')
    workingFileName = xlFileName+kommunekode+'.xlsx'
    print("Writing "+csvFileName+" to " + workingFileName)
    shutil.copyfile(xlFileName+'.xlsx', workingFileName)
    data = pd.read_csv(csvFileName, encoding='latin1', header=0, quotechar='"', delimiter=";")
    writer = pd.ExcelWriter(workingFileName, engine='openpyxl')
    book = load_workbook(workingFileName)
    writer.book = book
    data.to_excel(writer, sheet_name='BBR')
    writer.save()
    writer.close()
    print("Saved " + workingFileName + " successfully")


def xl2csv(csvFileName, xlsxFileName, xlsxSheetName):
    print("Writing "+xlsxFileName+" to "+csvFileName)
    os.listdir('.')
    data_xls = pd.read_excel(xlsxFileName, xlsxSheetName, index_col=1, encoding='utf-8')
    data_xls.to_csv(csvFileName, encoding='utf-8-sig', header=True, index=False, quotechar='"', sep=";")



