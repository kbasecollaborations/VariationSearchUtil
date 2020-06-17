import os
class vcf_parser:
  
   def init(self):
       pass

   def get_variants(self, chr, start, stop, url_template, tbi_url_template):
       os.system("node get_variants.js " + chr + " " + start + " " + stop + " " + url_template + " " + tbi_url_template )

   def getjson(self, header_file, variant_file):
       
       Variations = []
       harray = []
       with open(header_file,"r") as hfile:
            for hline in hfile:
                hline = hline.rstrip()
                harray = hline.split(",")
       #print(harray)

       with open(variant_file,"r") as vfile:
            for vline in vfile:
                vline = vline.rstrip()
                varray = vline.split(",")
                for var in varray:
                    vcfarray = var.split("\t")
                    #print(vcfline)
                    chrm = vcfarray[0]
                    pos = vcfarray[1]
                    ref = vcfarray[3]
                    alt = vcfarray[4]
                    values = vcfarray[9:len(vcfarray)]
                    #print(values)
                    Variations.append(
                                       {
                                          "Chr" : chrm,
                                          "Pos" : pos,
                                          "Ref" : ref,
                                          "Alt" : alt,
                                          "type": "SNP/Indel" 
                                       }
                  
                   )
       print("SNP\tCHR\tBP\tP\tPOS")
       for i in range(0, len(Variations)):
           print(Variations[i]["Chr"]+"_"+Variations[i]["Pos"] + "\t" + Variations[i]["Chr"] + "\t" + Variations[i]["Ref"]+ "\t" + Variations[i]["Alt"] + "\t" + Variations[i]["Pos"])       

       return {"genotype" :harray, "variations":Variations }
                
                    
if __name__ == '__main__':
   vp = vcf_parser()
   vp.get_variants( "Chr02", "1" , "10000",  "https://appdev.kbase.us/dynserv/b8fedfd6d8a1fc10372bcbad4f152b4b6d85507b.VariationFileServ/shock/a293a557-47b3-4fcc-8bef-d2049ad6368a", "https://appdev.kbase.us/dynserv/b8fedfd6d8a1fc10372bcbad4f152b4b6d85507b.VariationFileServ/shock/f19936ff-6f66-4a44-831f-1bfcdc6e88c4")
   vp.getjson("sample_names.txt", "data.txt")
