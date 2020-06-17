/*
A KBase module: VariationSearchUtil
*/

module VariationSearchUtil {

    typedef structure {
        string contig_id;
        int begin;
        int end;
    } variation_region;


    typedef structure {
        string variation_ref;
        list <variation_region> variation_regions;
    } SearchVariationOptions;

    typedef string genotype;

    typedef structure {
        string contig_id;
        string position;
        string ref;
        string alt;
        list <genotype> genotypes;
    } variation_result;

    typedef structure {
        list <variation_result> variation_results;
    } SearchVariationResult;


    /*
       Search variation data 
    */

    funcdef search_variation(SearchVariationOptions params) 
        returns (SearchVariationResult result) authentication required;
};
