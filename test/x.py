
samples=['A','B','C','D']
data = ['0/1', '1/1', '0/0', '1/2']
input_samples = ['B', 'C', 'X']

bindex=list()
for j in input_samples:
    try:
        bindex.append(samples.index(j))
    except:
        bindex.append('None')
print (bindex)



