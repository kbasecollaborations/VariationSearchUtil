import requests
import json
import uuid



class GenericClient:
    def __init__(self):
        self.module="VariationSearchUtil"
        self.token = "JJPRPDD7XZWC54Q7WE2HKM3AWZDKZL3F"
        self.timeout = 1000
        self.url = "http://127.0.0.1:5000"
        pass

    def call_func(self, func_name=None, params=None, timeout=None):
        # Since this is designed to call KBase JSONRPC 1.1 services, we
        # follow the KBase conventions:
        # - params are always wrapped in an array; this emulates positional arguments
        # - a method with no arguments is called as either missing params in the call
        #   or the value None, and represented as an empty array in the service call
        # - a method with params is called with a single argument value which must be
        #   convertable to JSON; it is represented in the call to the service as an array
        #   wrapping that value.
        # Note that KBase methods can take multiple positional arguments (multiple elements
        # in the array), but by far most take just a single argument; this library makes that
        # simplifying assumption.

        params = {"abc": "def"}
        func_name = "search_variation" 
        if params is None:
            wrapped_params = []
        else:
            wrapped_params = [params]

        # The standard jsonrpc 1.1 calling object, with KBase conventions.
        # - id should be unique for this call (thus uuid), but is unused; it isn't
        #   really relevant for jsonrpc over http since each request always has a
        #   corresponding response; but it could aid in debugging since it connects
        #   the request and response.
        # - method is always the module name, a period, and the function name
        # - version is always 1.1 (even though there was no officially published jsonrpc 1.1)
        # - params as discussed above.
        call_params = {
            'id': str(uuid.uuid4()),
            'method': self.module + '.' + func_name,
            'version': '1.1',
            'params': wrapped_params
        }

        header = {
            'Content-Type': 'application/json'
        }

        # Calls may be authorized or not with a KBase token.
        if self.token:
            header['Authorization'] = self.token

        timeout = timeout or self.timeout

        # Note that timeout should be set here (except for type errors).
        # The constructor requires it, and it can be overridden in the call
        # to this method.
        try:
            response = requests.post(self.url, headers=header,
                                     data=json.dumps(call_params), timeout=timeout)
        except:
            raise ValueError("There is an error")
        return response.text

if __name__ == "__main__":
    gu = GenericClient()
    x = gu.call_func()
    print (x)
