import os
import subprocess 

class vcf_parser:
  
   def init(self):
       pass

   def validate_params(self, params):
       if 'variation_object_name' not in params:
           raise ValueError('required variation_object_name field was not defined')
       elif 'coordinates' not in params:
           raise ValueError('required coordinates field was not defined')

   def run_cmd(self, cmd):

       try:
          process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
          stdout, stderr = process.communicate()
          if stdout:
             print ("ret> ", process.returncode)
             print ("OK> output ", stdout)
          if stderr:
             print ("ret> ", process.returncode)
             print ("Error> error ", stderr.strip())

       except OSError as e:
           print ("OSError > ", e.errno)
           print ("OSError > ", e.strerror)
           print ("OSError > ", e.filename) 

   def get_variants(self, chr, start, stop, url_template, tbi_url_template, index):
       outpath = "/kb/module/deps"
       cmd =  "node " + outpath + "/get_variants.js " + chr + " " + start + " " + stop + " " + url_template + " " + tbi_url_template +" " + str(index)
       self.run_cmd(cmd)

   def getjson(self, header_file, variant_file, output_dir, index):

       harray = []
       try:
            with open(header_file,"r") as hfile:
                for hline in hfile:
                    hline = hline.rstrip()
                    harray = hline.split(",")
       except IOError:
           print("Unable to open "+ header_file)

       Variations = []
       try:
            with open(variant_file,"r") as vfile:
                for vline in vfile:
                    vline = vline.rstrip()
                    varray = vline.split(",")
                    for var in varray:
                        vcfarray = var.split("\t")
                        Variations.append( vcfarray)
       except IOError:
           print("Unable to open "+ variant_file)

       outfile = os.path.join(output_dir, "variants.tsv" )

       try:
            with open(outfile, "a") as fout:
                if (index == 0):
                    fout.write("CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\t")
                    fout.write("\t".join(harray) + "\n")

                for i in range(0, len(Variations)):
                    rec = []
                    for j in range (0, len(Variations[i])):
                        rec.append(Variations[i][j])
                    joined_line = "\t".join(rec)
                    fout.write(joined_line + "\n")
       except IOError:
           print("Unable to write to "+ outfile)

       return outfile
                

