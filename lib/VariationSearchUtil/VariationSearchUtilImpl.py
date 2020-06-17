# -*- coding: utf-8 -*-
#BEGIN_HEADER
import logging
import subprocess
import requests
import json
from VariationSearchUtil.Utils.vcf_parser import vcf_parser
# from VariationSearchUtil.Utils.vcf_parser import vcf_parser
from kbase_workspace_client import WorkspaceClient
import re

#END_HEADER


class VariationSearchUtil:
    '''
    Module Name:
    VariationSearchUtil

    Module Description:
    A KBase module: VariationSearchUtil
    '''

    ######## WARNING FOR GEVENT USERS ####### noqa
    # Since asynchronous IO can lead to methods - even the same method -
    # interrupting each other, you must be *very* careful when using global
    # state. A method could easily clobber the state set by another while
    # the latter method is running.
    ######################################### noqa
    VERSION = "0.0.1"
    GIT_URL = ""
    GIT_COMMIT_HASH = ""

    #BEGIN_CLASS_HEADER
    def run_cmd(self, cmd):
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        out, err = p.communicate()
        return out

    def get_variation_service_url(self, sw_url):
        '''
        get the most recent VariationFileServ url from the service wizard.
        sw_url: service wizard url
        '''
        # TODO Fix the following dev thing to beta or release or future
        json_obj = {
            "method": "ServiceWizard.get_service_status",
            "id": "",
            "params": [{"module_name": "VariationFileServ", "version": "dev"}]
        }
        sw_resp = requests.post(url=sw_url, data=json.dumps(json_obj))
        vfs_resp = sw_resp.json()
        self.shock_url = self.shock_url.replace("https://", "")
        vfs_url = vfs_resp['result'][0]['url'] + "/jbrowse_query/" + self.shock_url + "/node"
        return vfs_url


    def get_db_urls(self, var_obj, vfs_url):
       # vcf_node_url = "/".join([var_obj['vcf_handle']['url'],
       #                          "node",
       #                          var_obj['vcf_handle']['id']
       #                          ])
       # vcf_node_url = vcf_node_url.replace("https://", "")
       # vcf_index_node_url = "/".join([var_obj['vcf_index_handle']['url'],
       #                                "node",
       #                                var_obj['vcf_index_handle']['id']
       #                                ])
       # vcf_index_node_url = vcf_index_node_url.replace("https://", "")

        url_template = "/".join([vfs_url,
                                 var_obj['vcf_handle']['id']
                                 ])
        tbi_url_template = "/".join([vfs_url,
                                     var_obj['vcf_index_handle']['id']
                                     ])
        return url_template, tbi_url_template

    def format_locations(self, params):
        formatted_locations = list()
        locations = params.get("locations")
        for i,l in enumerate(locations):
            contig_id, region = locations[i].split(":")
            if len(region.split("-")) == 2:
                start, stop = region.split("-")
            elif len(region.split("-")) == 1:
                start = region
                stop = region
            else:
                raise Valuerror("wrong format of locations: Contig_id:start-stop " + l )
            # ########################## IMPORTANT AND CONFUSING ############################
            # https://www.biostars.org/p/84686/
            # tabix-js and jbrowse are 0-index-based systems
            # tabix is 1-index system (so the way to query tabix is very different
            # So if you are looking for region 500-501, you need
            # coordinates to be 409-501. so just need to subtract start by 1
            # Pay close attention to the difference in case of indels for 0- and 1-index systems
            # and the need to take care of it in parsing.
            # See the function get_variations where we are getting the result and parsing them.
            start = int(start) -1
            formatted_locations.append(contig_id + ":" + str(start) + "-" + str(stop))
        return formatted_locations

    def get_variations(self, token, location, all_samples, url_template, tbi_url_template, positions=[],
                     refalts=[], input_samples=None, variations=list() ):
        contig_id, region = location.split(":")
        start, stop = region.split("-")
        gv = "/kb/module/deps/get_variants.js"
        cmd = ["node",
               gv,
               str(contig_id),
               str(start),
               str(stop),
               url_template,
               tbi_url_template,
               token
               ]
        variation_result = self.run_cmd(cmd).decode('ascii').rstrip().split("\n")

        # ###################################IMPORTANT AND CONFUSING##################
        # https://www.biostars.org/p/84686/
        # We formatted the location in format_locations function to account for
        # 0-based index. Also look at how indels are different between 0-based index and
        # 1-based index.
        # Here we just try to make sure, we don't have any position that is not part of the
        # request. So actual_start is the position in 1-based index

        actual_start = int(start) + 1

        # TODO: Types SNP/INDEL or anything else
        # TODO: append annotations if they exist
        for i,v in enumerate(variation_result):
            v = v.rstrip()
            var = v.split("\t")
            ######################### Important ########################
            # In 0-based index indels are considered differently.
            # eg. if you request region 7-8 , it may also return position 4
            # see here https://www.biostars.org/p/84686/
            # so we skip all positions that are less than 1-based index.
            if int(var[1]) < int(actual_start):
                continue
            positions.append(var[0] + ":" + var[1])
            refalts.append(var[3] + "/" + var[4])

            tmp = list()
            if input_samples is not None:
                for i,s in enumerate(input_samples):
                    s_index = all_samples.index(s)
                    new_index = 9 + s_index
                    tmp.append(var[new_index])
            else:
                tmp.append(var[9:])
            variations.append(tmp)
        return positions, refalts, variations



    #END_CLASS_HEADER

    # config contains contents of config file in a hash or None if it couldn't
    # be found
    def __init__(self, config):
        #BEGIN_CONSTRUCTOR
        self.shared_folder = config['scratch']
        logging.basicConfig(format='%(created)s %(levelname)s: %(message)s',
                            level=logging.INFO)
        self.vp = vcf_parser()
        self.ws_url = config['workspace-url']
        # Use service-wizard-url to get the latest version of the VariationFileServ
        self.sw_url = config['srv-wiz-url']
        self.shock_url = config['shock-url']
        #END_CONSTRUCTOR


    def search_variation(self, ctx, params):
        """
        Search variation data
        :param params: instance of type "SearchVariationOptions" ->
           structure: parameter "variation_regions" of list of type
           "variation_region" -> structure: parameter "contig_id" of String,
           parameter "begin" of Long, parameter "end" of Long
        :returns: instance of type "SearchVariationResult" -> structure:
           parameter "variation_results" of list of type "variation_result"
           -> structure: parameter "contig_id" of String, parameter
           "position" of String, parameter "ref" of String, parameter "alt"
           of String, parameter "genotypes" of list of type "genotype"
        """
        # ctx is the context object
        # return variables are: result
        #BEGIN search_variation

        # print (params)
        # print (token)
        token = ctx['token']

        #use service wizard to find the latest version of variation file serve url
        vfs_url =  self.get_variation_service_url(self.sw_url)

        ws = WorkspaceClient(url=self.ws_url, token=ctx['token'])
        var_obj = ws.req("get_objects2", {'objects': [{"ref": params['variation_ref']}]})['data'][0]['data']

        samples = var_obj['samples']
        found_samples = list(set(params["samples"]) & set(samples))
        if (len(found_samples)==0):
            raise ValueError("None of the input samples found in variation object. Please choose from:" + " ".join(samples))


        url_template, tbi_url_template = self.get_db_urls(var_obj, vfs_url)
        formatted_locations = self.format_locations(params)

        print (url_template)
        print (tbi_url_template)

        positions = list()
        refalts = list()
        variations = list()

        for l in formatted_locations:
            positions, refalts, variations = self.get_variations(token, l, samples,
                                url_template, tbi_url_template, positions, refalts,
                                found_samples, variations)

        # ##########################Understanding the result #########################
        # 'result': [{'samples': ['OSU-418', '93-968', 'BESC-52'],
        #             'positions': ['Chr01:52', 'Chr01:203', 'Chr01:224', 'Chr01:306', 'Chr01:369'],
        #             'refalts': ['T/A', 'CTTTTTTTTTTT/CTTTTTTTTTTTT', 'T/C', 'T/C', 'C/A'],
        #             'variations': [
        #                 ['0/0', '0/0', '0/0'],
        #                 ['0/1', '0/0', '0/0'],
        #                 ['0/0', '0/0', '0/0'],
        #                 ['1/1', '0/0', '0/0'],
        #                 ['0/0', '0/0', '1/1']]}]
        # The above json in tabular format is same as the following table
        # If annotation information is present there would be an additional field
        # corresponding to annotation
        # positions	    refalts 	                   OSU-418	93-968	BESC-52
        # Chr01:52	    T/A	                             0/0	0/0	      0/0
        # Chr01:203	    CTTTTTTTTTTT/CTTTTTTTTTTTT	     0/1	0/0	      0/0
        # Chr01:224	    T/C	                             0/0	0/0	      0/0
        # Chr01:306	    T/C	                             1/1	0/0	      0/0
        # Chr01:369	    C/A	                             0/0	0/0	      1/1

        result = {
            "samples": found_samples,
            "positions":positions,
            "refalts": refalts,
            "variations": variations
        }

        #END search_variation

        # At some point might do deeper type checking...
        if not isinstance(result, dict):
            raise ValueError('Method search_variation return value ' +
                             'result is not type dict as required.')
        # return the results
        return [result]

    def status(self, ctx):
        #BEGIN_STATUS
        returnVal = {'state': "OK",
                     'message': "",
                     'version': self.VERSION,
                     'git_url': self.GIT_URL,
                     'git_commit_hash': self.GIT_COMMIT_HASH}
        #END_STATUS
        return [returnVal]
