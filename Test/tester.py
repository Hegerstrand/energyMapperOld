import pandas as pd
from openpyxl import load_workbook
import excelhandler
import os
import BBRhandler

os.listdir('.')
#excelhandler.runMacro('SBiCopy.xlsm', 'copyThings')
BBRhandler.calculateEnergyDemand('860')
