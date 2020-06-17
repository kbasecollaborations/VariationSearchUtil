import requests
import os
import json

# The URL of the running server from within the docker container
url = 'http://127.0.0.1:5000'

service_token="JJPRPDD7XZWC54Q7WE2HKM3AWZDKZL3F"

def make_request(variation_ref):
    """Helper to make a JSON RPC request with the given workspace ref."""
    params = {
            'variation_ref': variation_ref,
            'auth_token': service_token,
            'method':"VariationSearchUtil.search_variation"
             }
    headers = {'Content-Type': 'application/json', 'Authorization': service_token}
    resp = requests.post(url,  params=params,  headers=headers)
    return (resp.text)



variation_ref = "39465/42/22"
resp = make_request (variation_ref)
print (resp)

