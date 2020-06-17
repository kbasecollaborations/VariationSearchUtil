import json

data ='''{
"samples":["BESC-101", "BESC-102"],
"locations":["Chr01:100", "Chr01:102", "Chr01:103"],
"refalt":["A/T", "T/GGG", "TGA/T"],
"genotypes":[
    ["0/1", "1/1"],
    ["1/1", "0/1"],
    ["0/1", "0/0"]
]
}'''

snpdata = json.loads(data)
#print (snpdata)

def get_tsv(snpdata):
    out =  "CHR:POS\t" + "REF:ALT\t" + "\t".join(snpdata.get("samples")) + "\n"
    for i,l in enumerate(snpdata.get('locations')):
         out += snpdata.get('locations')[i] + "\t" + snpdata.get('refalt')[i] + "\t"  
         out +=  "\t".join(snpdata.get("genotypes")[i]) + "\n"
    return out
   

def get_snp(snpdata, location, sample):
    s_index = snpdata.get("samples").index(sample)
    p_index = snpdata.get("locations").index(location)
    ref, alt = snpdata.get("refalt")[p_index].split("/")
    value = snpdata.get('genotypes')[p_index][s_index]
    if value =='0/1':
       return ref + alt
    if value =='1/1':
       return ref + ref
    if value == '0/0':
       return ref + ref

from collections import Counter
def get_allele_frequency(snpdata, location):
    p_index = snpdata.get("locations").index(location)
    return (Counter(snpdata.get("genotypes")[p_index])) 
       

snpdata = json.loads(data)
print (get_allele_frequency(snpdata, "Chr01:100"))

#print (get_snp(snpdata, "Chr01:100", "BESC-101"))
#print (get_tsv(snpdata))




d = list()
a = ["1.1", "1.2", "1.3"]
b = ["2.1", "2.2", "2.3"]
d.append(a)
d.append(b)


def get_2d_list_slice(self, matrix, start_row, end_row, start_col, end_col):
    return [row[start_col:end_col] for row in matrix[start_row:end_row]]


# still a copy, but cleaner with a list comprehension!
a = [ [ 1, 2, 3 ] , [ 4, 5, 6 ] ]
cols = [1,2]

newlist = list()
for i,j in enumerate(d):
   n = list()
   for col in cols:
       n.append(j[col])
   newlist.append(n)



x=[1,2,3]
y=[4,6]


print (newlist)






