import sql2csv
import csvHandler
import excelhandler


def calculateEnergyDemand(kommunekode):
    limit = 100*1000
    Filename = "BBR" + kommunekode
    xlFilename = "SBi"

    sql2csv.getBBRfromKommune(str(kommunekode), "BBR.sql", Filename + ".csv", str(limit))

    csvHandler.csv2xl(Filename + ".csv", xlFilename, kommunekode)

    excelhandler.runMacro(xlFilename+kommunekode + ".xlsm", "copyThings")

    #csvHandler.xl2csv("BBREnergi.csv", xlFilename+kommunekode + ".xlsm", "Energi")

