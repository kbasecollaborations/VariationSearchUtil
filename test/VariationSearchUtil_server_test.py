# -*- coding: utf-8 -*-
import os
import time
import unittest
from configparser import ConfigParser

from VariationSearchUtil.VariationSearchUtilImpl import VariationSearchUtil
from VariationSearchUtil.VariationSearchUtilServer import MethodContext
from VariationSearchUtil.authclient import KBaseAuth as _KBaseAuth

from installed_clients.WorkspaceClient import Workspace


class VariationSearchUtilTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        token = os.environ.get('KB_AUTH_TOKEN', None)
        config_file = os.environ.get('KB_DEPLOYMENT_CONFIG', None)
        cls.cfg = {}
        config = ConfigParser()
        config.read(config_file)
        for nameval in config.items('VariationSearchUtil'):
            cls.cfg[nameval[0]] = nameval[1]
        # Getting username from Auth profile for token
        authServiceUrl = cls.cfg['auth-service-url']
        auth_client = _KBaseAuth(authServiceUrl)
        user_id = auth_client.get_user(token)
        # WARNING: don't call any logging methods on the context object,
        # it'll result in a NoneType error
        cls.ctx = MethodContext(None)
        cls.ctx.update({'token': token,
                        'user_id': user_id,
                        'provenance': [
                            {'service': 'VariationSearchUtil',
                             'method': 'please_never_use_it_in_production',
                             'method_params': []
                             }],
                        'authenticated': 1})
        cls.wsURL = cls.cfg['workspace-url']
        cls.wsClient = Workspace(cls.wsURL)
        cls.serviceImpl = VariationSearchUtil(cls.cfg)
        cls.scratch = cls.cfg['scratch']
        cls.callback_url = os.environ['SDK_CALLBACK_URL']
        suffix = int(time.time() * 1000)
        cls.wsName = "test_ContigFilter_" + str(suffix)
        ret = cls.wsClient.create_workspace({'workspace': cls.wsName})  # noqa

    @classmethod
    def tearDownClass(cls):
        if hasattr(cls, 'wsName'):
            cls.wsClient.delete_workspace({'workspace': cls.wsName})
            print('Test workspace was deleted')

    # NOTE: According to Python unittest naming rules test method names should start from 'test'. # noqa
    def test_good_example(self):
        # To test request permission to narrative 51264 on ci
        # TODO remove the hardcoded variation stuff
        params = {
            "variation_ref": "51264/5/1",
            "locations": ["Chr01:52", "Chr01:100-500"],
            "samples":['93-968', 'OSU-418', 'BESC-52']
        }
        ret = self.serviceImpl.search_variation(self.ctx, params)
        assert (len(ret[0]['positions']) == 5)

    def test_no_variation(self):
        # To test request permission to narrative 51264 on ci
        # TODO remove the hardcoded variation stuff
        params = {
            "variation_ref": "51264/5/1",
            "locations": ["Chr01:1"],
            "samples":['93-968', 'OSU-418', 'BESC-52xxxx']
        }
        ret = self.serviceImpl.search_variation(self.ctx, params)
        assert (len(ret[0]['positions']) == 0)
        # only 2 samples found as 3rd sample is not there
        assert (len(ret[0]['samples']) == 2)

    def test_redundant_regions(self):
        # To test request permission to narrative 51264 on ci
        # TODO remove the hardcoded variation stuff
        params = {
            "variation_ref": "51264/5/1",
            "locations": ["Chr01:1"],
            "samples": ['93-968', 'OSU-418']
        }
        ret = self.serviceImpl.search_variation(self.ctx, params)
        assert (len(ret[0]['positions']) == 0)
        # only 2 samples found as 3rd sample is not there
        assert (len(ret[0]['samples']) == 2)


