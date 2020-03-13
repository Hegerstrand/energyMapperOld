import httplib2 as http
import json

def getBygninger(kommunekode):
    filename = "BBR" + kommunekode + ".csv"
    try:
        from urlparse import urlparse
    except ImportError:
        print("urlparse failed")
        from urllib.parse import urlparse

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
    response, content = h.request(
            target.geturl(),
            method,
            body,
            headers)

    if response.status == 200:
        data = json.loads(content)
        print('Number of ' + path + ': ' + str(len(data)))
        print('printing to: ' + filename)
    else:
        print("status not OK")

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