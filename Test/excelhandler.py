import os, os.path
import math
import csv
import pandas as pd
import win32com.client

def runMacro(xlsmFileName, macroname):
    os.listdir('.')
    modulename = "Module1"
    if os.path.exists(xlsmFileName):
        xl = win32com.client.Dispatch('Excel.Application')
        xl.Workbooks.Open(Filename=xlsmFileName, ReadOnly=1)
        xl.Application.Run("copyThings")
        xl.Application.Quit()
        del xl

    # PRINT FINAL COMPLETED MESSAGE#
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
