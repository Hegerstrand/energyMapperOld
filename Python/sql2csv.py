import pyodbc
import csv


def getBBRfromKommune(kommunekode, sqlFileName, csvFileName, limit):
    print("Attempting to retrieve BBR data for kommune "+kommunekode)
    cnxn = pyodbc.connect("Driver={SQL Server Native Client 11.0};"
                          "Server=DKLYDB7;"
                          "Database=BBR2017;"
                          "Trusted_Connection=yes;")

    cursor = cnxn.cursor()
    # Open and read the file as a single buffer
    fd = open(sqlFileName, 'r')
    sqlCommand = fd.read()
    fd.close()

    try:
        cursor.execute(sqlCommand.replace('_kommunekode', kommunekode).replace('_top', limit))
        headers = [d[0] for d in cursor.description]
        data = cursor.fetchall()
        with open(csvFileName, "w") as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=';', lineterminator='\n')
            csv_writer.writerow(headers)
            csv_writer.writerows(data)
        for row in cursor:
            print(row)

        print(sqlFileName + ' success for kommune: '+kommunekode+'. '+str(len(data))+' results printed in ' + csvFileName)

    except (pyodbc.Error, pyodbc.OperationalError) as msg:
        print(msg)
        # raise SqlmapConnectionException(msg[1])
