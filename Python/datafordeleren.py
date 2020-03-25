import httplib2 as http
import json
import csv
import numpy

def getHusnummer(postnummer, filename, limit):
    try:
        from urlparse import urlparse
    except ImportError:
        try:
            from urllib.parse import urlparse
        except ImportError:
            print("urlparse failed")

    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json; charset=UTF-8'
    }

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

            headers = ["adgangTilBygning", "id_lokalId", "jordstykke", "geoDanmarkBygning"
                , "navngivenVej", "husnummertekst", "postnummer", "adgangsadressebetegnelse"
                , "kommuneinddeling"
                , "adgangspunkt", "status"]
            csv_writer.writerow(headers)

            dictionary = {'postnummer': 'postnr'
                , 'navngivenVej': 'vejadresseringsnavn'
                , "kommuneinddeling": "kommunekode"
                , 'adgangspunkt': 'position'}

            j = 0
            for husnummer in data:
                status = int(husnummer["status"])
                if status != 3:
                    continue
                params = []
                for heading in headers:
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

    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json; charset=UTF-8'
    }

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

            headers = ["id_lokalId", "husnummer", "jordstykke", "byg021BygningensAnvendelse"
                , "byg038SamletBygningsareal", "byg039BygningensSamledeBoligAreal", "byg040BygningensSamledeErhvervsAreal", "placehodlerForKælder"
                , "byg026Opførelsesår", "byg027OmTilbygningsår", "byg056Varmeinstallation", "byg057Opvarmningsmiddel", "byg058SupplerendeVarme", "byg404Koordinat"
                , "byg406Koordinatsystem", "status"]
            csv_writer.writerow(headers)

            j = 0
            for bygning in data:
                if "byg021BygningensAnvendelse" in bygning and "status" in bygning:
                    status = int(bygning["status"])
                    if int(bygning["byg021BygningensAnvendelse"]) > 600 or status < 5 or status > 9 or "byg406Koordinatsystem" not in bygning:
                        continue
                    params = []
                    for heading in headers:
                        if heading in bygning:
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



############################################################################
def getDar():
    try:
        from urlparse import urlparse
    except ImportError:
        from urllib.parse import urlparse

    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json; charset=UTF-8'
    }

    uri = 'https://services.datafordeler.dk/DAR/DAR/1/REST/'
    path='husnummer'
    request = 'nord=6172177&syd=6171495&vest=705501&oest=703917'
    #request = 'id=0a3f507c-f0e9-32b8-e044-0003ba298018'

    target = urlparse(uri+path+'?'+request)
    method = 'GET'
    body = ''

    h = http.Http()
    print('getting ' + path + ' where ' + request + ' from ' + uri)
    response, content = h.request(
            target.geturl(),
            method,
            body,
            headers)

    data = json.loads(content)

    if (response['status'] == '200'):
        printstr = 'Antal ' + path + ' returned: ' + str(len(data))
        print(printstr)
        if (len(data) > 0):
            print('Første husnummer: ' + data[0]['adgangsadressebetegnelse'])
    else :
        print('getcall returned statuscode' + response['status'])

############################################################################