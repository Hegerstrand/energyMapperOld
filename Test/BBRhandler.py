import sql2csv
import csvHandler
import excelhandler


def calculateEnergyDemand(kommunekode):
    limit = 100*1000
    Filename = 'BBR'+kommunekode
    SBi = 'Energi'
    xlFilename = 'SBi'

    sql2csv.getBBRfromKommune(str(kommunekode), 'BBR.sql', Filename + '.csv', str(limit))
    # #sql2csv.getBBRfromKommune(str(kommunekode), BBR+'Sum.sql', BBR+'Sum.csv', str(limit))

    csvHandler.csv2xl(Filename + '.csv', xlFilename, Filename, kommunekode, True)

    excelhandler.runMacro(xlFilename+kommunekode+'.xlsm', 'copyThings')

    csvHandler.xl2csv(Filename + SBi + '.csv', xlFilename+kommunekode+'.xlsm', SBi)

