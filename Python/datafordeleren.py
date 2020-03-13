import httplib2 as http
import json
import csv

def getBygninger(kommunekode):
    filename = "BBR" + kommunekode + ".csv"
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

    uri = 'https://services.datafordeler.dk/BBR/BBRPublic/1/REST/'
    path = "bygning"
    request = "kommunekode=0" + kommunekode
    user = "username=AYWWPEBUAL&password=Login4Kort&format=json"

    target = urlparse(uri + path + '?' + request + '&' + user)
    method = 'GET'
    body = ''

    h = http.Http()
    print('getting ' + path + ' where ' + request + ' from ' + uri)

    try:
        response, content = h.request(
                target.geturl(),
                method,
                body,
                headers)

        if response.status == 200:
            data = json.loads(content)
            print('Number of ' + path + ': ' + str(len(data)))

            print('printing to: ' + filename)
            # now we will open a file for writing
            data_file = open(filename, 'w')
            # create the csv writer object
            csv_writer = csv.writer(data_file, delimiter=';', lineterminator='\n')
            # Counter variable used for writing
            # headers to the CSV file
            for bygning in data:
                # Writing he    aders of CSV file
                #header = bygning.keys()
                header = ["id_lokalId", "param2"]
                csv_writer.writerow(header)

                params = []
                if "id_lokalId" in header:
                    params.append(bygning["id_lokalId"])
                    csv_writer.writerow(params)
                #csv_writer.writerow(header)
                #csv_writer.writerow(bygning.values())

            data_file.close()

        else:
            print("status not OK")
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






############################################################################
############################################################################
############################################################################