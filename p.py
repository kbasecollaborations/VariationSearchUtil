import requests
import json

def query_sketch_mags():
    '''
    Query the sketch service for items related to the workspace reference.
    sw_url: service wizard url
    input_upas: list of workspace references
    n_max_results: number of results to return
    auth_token: authorization token
    '''
    #sketch_url = get_sketch_service_url(sw_url)
    sketch_url = "http://127.0.0.1"

    auth_token="JJPRPDD7XZWC54Q7WE2HKM3AWZDKZL3F"
    payload = {
            "method":"get_variation",
            "params": {
                'ws_ref': "upa",
                'search_db': "search_db",
                'n_max_results': 500
            }
        }

    print('='*80)
    print('sketch_url:',sketch_url)
    print('='*80)

    resp = requests.post(url=sketch_url, data=json.dumps(payload),
                             headers={'content-type':'application/json', 'authorization':auth_token})
    results = resp.text
    return results


x=query_sketch_mags()
print (x)
