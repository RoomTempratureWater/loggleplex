import requests
import gzip
import json


async def esupload(file):
    print(file)
    base_url = 'https://search-jonathanlogs-tfvc4bowafzvwyzjiscandotga.aos.eu-north-1.on.aws/' # The domain with https:// and a trailing slash. For example, https://my-test-domain.us-east-1.es.amazonaws.com/
    auth = ('aizensosuke', 'Aizen_goat1311') # For testing only. Don't store credentials in code.

    headers = {'Accept-Encoding': 'gzip', 'Content-Type': 'application/json',
            'Content-Encoding': 'gzip'}

    document = {
    "title": "Moneyball",
    "director": "Bennett Miller",
    "year": "2011"
    }

    # Compress the document.
    compressed_document = gzip.compress(file)

    
    # Send the request.
    path = 'logs/_doc?refresh=true'
    url = base_url + path
    response = requests.post(url, auth=auth, headers=headers, data=compressed_document)
    print(response.text)
    print(response.status_code)
    return response
    print(response.text)