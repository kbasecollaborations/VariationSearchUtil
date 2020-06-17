import requests
import json

ws_token="JJPRPDD7XZWC54Q7WE2HKM3AWZDKZL3F"

def _post_req(payload, url):
    """Make a post request to the workspace server and process the response."""
    headers = {'Authorization': ws_token}
    resp = requests.post(url, data=json.dumps(payload), headers=headers)
    if not resp.ok:
        raise RuntimeError('Error response from workspace:\n%s' % resp.text)
    resp_json = resp.json()
    if 'error' in resp_json:
        raise RuntimeError('Error response from workspace:\n%s' % resp.text)
    elif 'result' not in resp_json or not len(resp_json['result']):
        raise RuntimeError('Invalid workspace response:\n%s' % resp.text)
    return resp_json['result'][0]

def req(method, params):
    """
    Make a JSON RPC request to the workspace server.
    KIDL docs: https://kbase.us/services/ws/docs/Workspace.html
    """
    payload = {'version': '1.1', 'method': method, 'params': [params]}
    return _post_req(payload)

def admin_req(method, params):
    """
    Make a JSON RPC administration request (method is wrapped inside the "administer" method).
    Docs for this interface: https://kbase.us/services/ws/docs/administrationinterface.html
    """
    payload = {
        'version': '1.1',
        'method': 'VariationSearchUtil.get_variation',
        'params': {'command': method, 'params': "bbx"}
    }
    return _post_req(payload, '127.0.0.1:5000/get_variation')


x=admin_req("method", "params")
print (x)
