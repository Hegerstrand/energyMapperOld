import httplib2 as http
import json

############################################################################
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