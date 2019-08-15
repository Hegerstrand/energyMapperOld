import sql2csv
import csvHandler
import excelhandler


def calculateEnergyDemand(kommunekode):
    limit = 100*1000
    BBR = 'BBR'
    SBi = 'Energi'
    xlFilename = 'SBi'

    sql2csv.getBBRfromKommune(str(kommunekode), BBR + '.sql', BBR + '.csv', str(limit))
    # #sql2csv.getBBRfromKommune(str(kommunekode), BBR+'Sum.sql', BBR+'Sum.csv', str(limit))

    csvHandler.csv2xl(BBR + '.csv', xlFilename, BBR, kommunekode, True)

    excelhandler.runMacro(xlFilename+kommunekode+'.xlsm', 'copyThings')

    csvHandler.xl2csv(BBR + SBi + '.csv', xlFilename+kommunekode+'.xlsm', SBi)

