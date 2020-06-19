import httplib2 as http
import json
import requests
import csv
import numpy
import pandas as pd

headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json; charset=UTF-8'
}

def getAdresser(xlfilename, sheetname, csvfilename):
    try:
        from urlparse import urlparse
    except ImportError:
        try:
            from urllib.parse import urlparse
        except ImportError:
            print("urlparse failed")

    exceldata = pd.read_excel(xlfilename, sheetname, encoding='utf-8')

    uri = 'https://services.datafordeler.dk/DAR/DAR/1/REST/'
    path = "adresse"
    method = 'GET'
    body = ''
    h = http.Http()

    data_file = open(csvfilename, 'w')
    csv_writer = csv.writer(data_file, delimiter=';', lineterminator='\n')

    headings = ["id_lokalId", "husnummer", "adressebetegnelse"]
    csv_writer.writerow(headings)

    dictionary = {'husnummer': 'id_lokalId',
                  }

    husnummerlist = exceldata.get_values().tolist()

    j = 0
    i = 0
    for husnummer in husnummerlist:
        request = "husnummer=" + str(husnummer[0])
        target = urlparse(uri + path + '?' + request)
        response, content = h.request(target.geturl(), method, body, headers)
        if response.status == 200:
            data = json.loads(content)
            i += 1
            for adresse in data:
                status = int(adresse["status"])
                if status != 3:
                    continue
                params = []
                for heading in headings:
                    if heading in adresse:
                        parameter = adresse[heading]
                        if type(parameter) is dict:
                            if heading in dictionary:
                                value = dictionary[heading]
                                if value in parameter:
                                    params.append(parameter[value])
                                else:
                                    params.append("")
                            else:
                                params.append("")
                        else:
                            params.append(parameter)
                    else:
                        params.append("")
                csv_writer.writerow(params)
                j += 1

    print("Printed " + str(j) + " adresser for " + str(i) + " husnummer")
    data_file.close()

def getHusnummer(postnummer, filename, limit):
    try:
        from urlparse import urlparse
    except ImportError:
        try:
            from urllib.parse import urlparse
        except ImportError:
            print("urlparse failed")

    uri = 'https://services.datafordeler.dk/DAR/DAR/1/REST/'
    path = "husnummer"
    request = "Postnr=" + str(postnummer)
    method = 'GET'
    body = ''

    h = http.Http()
    print('Getting ' + path + ' where ' + request + ' from ' + uri)

    try:
        target = urlparse(uri + path + '?' + request)
        response, content = h.request(target.geturl(), method, body, headers)

        if response.status == 200:
            data = json.loads(content)
            i = 1
            if len(data) == 100:
                while len(data) == 100*i & len(data) < limit:
                    target = urlparse(uri + path + '?' + request + "&page=" + str(i))
                    response, content = h.request(target.geturl(), method, body, headers)
                    data = numpy.append(data, json.loads(content))
                    i += 1
                    print(str(len(json.loads(content))) + ' buildings in page ' + str(i), end="\r")

            print('Got ' + str(len(data)) + " husnummer from " + str(i) + " pages på Datafrodeleren")

            data_file = open(filename, 'w')
            csv_writer = csv.writer(data_file, delimiter=';', lineterminator='\n')

            headings = ["adgangTilBygning", "id_lokalId", "jordstykke", "geoDanmarkBygning"
                , "navngivenVej", "husnummertekst", "postnummer", "adgangsadressebetegnelse"
                , "kommuneinddeling"
                , "adgangspunkt", "status"]
            csv_writer.writerow(headings)

            dictionary = {'postnummer': 'postnr'
                ,"navngivenVej": "vejadresseringsnavn"
                #, 'navngivenVej': 'navngivenVejKommunedelList' ,"navngivenVejKommunedelList": "navngivenVejKommunedel",'navngivenVejKommunedel': 'vejkode'
                , "kommuneinddeling": "kommunekode"
                , 'adgangspunkt': 'position'}

            j = 0
            for husnummer in data:
                status = int(husnummer["status"])
                if status != 3:
                    continue
                params = []
                for heading in headings:
                    if heading in husnummer:
                        parameter = husnummer[heading]
                        if type(parameter) is dict:
                            if heading in dictionary:
                                value = dictionary[heading]
                                if value in parameter:
                                    params.append(parameter[value])
                                else:
                                    params.append("")
                            else:
                                params.append("")

                        else:
                            params.append(parameter)
                    else:
                        params.append("")
                csv_writer.writerow(params)
                j += 1

            print('Printed ' + str(j) + " husnummer to: " + filename)
            data_file.close()

        else:
            print(uri + " returned status not " + response['status'])
    except response.content as msg:
        print(msg)

def getBygninger(kommunekode, filename, limit):
    try:
        from urlparse import urlparse
    except ImportError:
        try:
            from urllib.parse import urlparse
        except ImportError:
            print("urlparse failed")

    uri = 'https://services.datafordeler.dk/BBR/BBRPublic/1/REST//'
    path = "bygning"
    request = "kommunekode=0" + str(kommunekode)
    user = "username=AYWWPEBUAL&password=Login4Kort&format=json"
    method = 'GET'
    body = ''

    h = http.Http()
    print('Getting ' + path + ' where ' + request + ' from ' + uri)

    try:
        target = urlparse(uri + path + '?' + request + '&' + user)
        response, content = h.request(target.geturl(), method, body, headers)

        if response.status == 200:
            data = json.loads(content)
            i = 1
            if len(data) == 100:
                while len(data) == 100*i & len(data) < limit:
                    target = urlparse(uri + path + '?' + request + '&' + user + "&page=" + str(i))
                    response, content = h.request(target.geturl(), method, body, headers)
                    data = numpy.append(data, json.loads(content))
                    i += 1
                    print(str(len(json.loads(content))) + ' buildings in page ' + str(i), end="\r")

            print('Got ' + str(len(data)) + " buildings from " + str(i) + " pages på Datafrodeleren")

            data_file = open(filename, 'w')
            csv_writer = csv.writer(data_file, delimiter=';', lineterminator='\n')

            headings = ["id_lokalId", "husnummer", "jordstykke", "byg021BygningensAnvendelse"
                , "byg038SamletBygningsareal", "byg039BygningensSamledeBoligAreal", "byg040BygningensSamledeErhvervsAreal", "eta022Kælderareal"
                , "byg026Opførelsesår", "byg027OmTilbygningsår", "byg056Varmeinstallation", "byg057Opvarmningsmiddel", "byg058SupplerendeVarme", "byg404Koordinat"
                , "byg406Koordinatsystem", "status"]
            csv_writer.writerow(headings)

            j = 0
            for bygning in data:
                if "byg021BygningensAnvendelse" in bygning and "status" in bygning:
                    status = int(bygning["status"])
                    if int(bygning["byg021BygningensAnvendelse"]) > 600 or status < 5 or status > 9 or "byg406Koordinatsystem" not in bygning:
                        continue
                    params = []
                    for heading in headings:
                        if heading == "eta022Kælderareal" and "etageList" in bygning:
                            eta022Kælderareal = getEta022Kælderareal(bygning["etageList"])
                            params.append(eta022Kælderareal)
                        elif heading in bygning:
                                params.append(bygning[heading])
                        else:
                            params.append("")
                    csv_writer.writerow(params)
                    j += 1

            print('Printed ' + str(j) + " buildings to: " + filename)
            data_file.close()

        else:
            print(uri + " returned status not " + response['status'])
    except response.content as msg:
        print(msg)

def getEta022Kælderareal(etageList):
    areal = 0
    for etage in etageList:
        if "etage" in etage:
            etagedata = etage["etage"]
            if "eta022Kælderareal" in etagedata and int(etagedata["status"]) == 6:
                areal += int(etagedata["eta022Kælderareal"])
    return str(areal)

def getBygningsList(kommunekode):
    try:
        from urlparse import urlparse
    except ImportError:
        try:
            from urllib.parse import urlparse
        except ImportError:
            print("urlparse failed")

    headings = ["id_lokalId", "husnummer", "byg021BygningensAnvendelse"
        , "byg038SamletBygningsareal", "byg039BygningensSamledeBoligAreal", "byg040BygningensSamledeErhvervsAreal"
        , "byg026Opførelsesår", "byg027OmTilbygningsår", "byg056Varmeinstallation", "byg057Opvarmningsmiddel"
        , "byg058SupplerendeVarme", "byg404Koordinat"
        , "byg406Koordinatsystem", "status"]

    uri = 'https://services.datafordeler.dk/BBR/BBRPublic/1/REST//'
    path = "bygning"
    request = "kommunekode=0" + str(kommunekode)
    user = "username=AYWWPEBUAL&password=Login4Kort&format=json"
    method = 'GET'
    body = ''

    h = http.Http()
    print('Getting ' + path + ' where ' + request + ' from ' + uri)

    try:
        target = urlparse(uri + path + '?' + request + '&' + user)
        response, content = h.request(target.geturl(), method, body, headers)
        bygningsList = []

        kommune_csv_file = open("BBR" + str(kommunekode) + ".csv", 'w')
        kommune_writer = csv.writer(kommune_csv_file, delimiter=';', lineterminator='\n')
        kommune_writer.writerow(headings)

        if response.status == 200:
            data = json.loads(content)
            i = 1
            if len(data) == 100:
                while len(data) == 100*i:
                    target = urlparse(uri + path + '?' + request + '&' + user + "&page=" + str(i))
                    response, content = h.request(target.geturl(), method, body, headers)
                    data = numpy.append(data, json.loads(content))
                    i += 1

            print("Found " + str(len(data)) + " bygninger in " + str(i) + " pages")
            for bygning in data:
                bygningsList.append(bygning["id_lokalId"])
                Bygningsdata = []
                for heading in headings:
                    if heading in bygning:
                        Bygningsdata.append(bygning[heading])
                    else:
                        Bygningsdata.append("")

                kommune_writer.writerow(Bygningsdata)
        else:
            print("getBygningsList failed")

        return bygningsList

    except response.content as msg:
        print(msg)


def getDawaBygning(bygnignID):
    SearchEnergyLabelBBR = "https://dawa.aws.dk/bbrlight/"
    query = "bygninger?id=" + bygnignID
    try:
        DawaBygning = requests.get(url=SearchEnergyLabelBBR + query, headers=headers).json()
    except:
        return

    if len(DawaBygning) > 0:
        return DawaBygning[0]