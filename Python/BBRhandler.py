import sql2csv
import csvHandler
import excelhandler
import datafordeleren

def testApi():
    datafordeleren.getBygninger("306")


def calculateEnergyDemand(kommunekode):
    limit = 1000*1000
    Filename = "BBR" + kommunekode
    xlFilename = "SBi"

    #sql2csv.getBBRfromKommune(str(kommunekode), "BBR.sql", Filename + ".csv", str(limit))
    datafordeleren.getBygninger(str(kommunekode), Filename + ".csv")

    csvHandler.csv2xl(Filename + ".csv", xlFilename, kommunekode)

    excelhandler.runMacro(xlFilename+kommunekode + ".xlsm", "copyThings")

    csvHandler.xl2csv("BBREnergi.csv", xlFilename+kommunekode + ".xlsm", "Energi")

