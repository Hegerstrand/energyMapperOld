import sql2csv
import csvHandler
import excelhandler
import datafordeleren


def calculateEnergyDemand(kommunekode):
    limit = 200*1000
    Filename = "BBR" + str(kommunekode)
    xlFilename = "SBi"

    #sql2csv.getBBRfromKommune(str(kommunekode), "BBR.sql", Filename + ".csv", str(limit))
    datafordeleren.getBygninger(kommunekode, Filename + ".csv", limit)

    csvHandler.csv2xl(Filename + ".csv", xlFilename, kommunekode)

    excelhandler.runMacro(xlFilename + str(kommunekode) + ".xlsm", "copyThings")

    csvHandler.xl2csv("BBREnergi.csv", xlFilename + str(kommunekode) + ".xlsm", "Energi")

