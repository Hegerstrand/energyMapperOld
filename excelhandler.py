import os, os.path
import pandas as pd
import win32com.client

def runMacro(FileName, macroname):
    os.listdir('.')
    print('Running macro: ' + macroname)
    if os.path.exists(FileName+'.xlsm'):
        xl = win32com.client.DispatchEx("Excel.Application")
        wb = xl.Workbooks.Open(os.path.abspath(FileName+'.xlsm'))
        xl.Application.Run(FileName+'.xlsm' + "!" + macroname)
        wb.Save()
        xl.Visible = True
        wb.Close()
        xl.Application.Quit()
        del xl, wb
        print("Macro refresh completed!")




def getSbiData():
    # Retrieve current working directory (`cwd`)
    cwd = os.getcwd()
    cwd

    # Change directory
    #os.chdir('C:\Users\JOLN\PycharmProjects\Test')

    # List all files and directories in current directory
    os.listdir('.')

    ############################################################################
    inputFile = 'SBi.xlsx'
    xl = pd.ExcelFile(inputFile)

    print(xl.sheet_names)
    BBR = xl.parse('Anvendelseskode')
    print(BBR.columns)
    Varmeinstallation = xl.parse('Varmeinstallation')
    Opvarmningsmiddel = xl.parse('Opvarmningsmiddel')
    Enhedsvarmeforburg = xl.parse('Enhedsvarmeforburg')
    print(Enhedsvarmeforburg.columns)
    Brændsel = xl.parse('Relationstabel')
    print(Brændsel.columns)
