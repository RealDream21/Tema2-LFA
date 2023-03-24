automat = dict()
alfabet = []
stariFinale = []
"""
https://drive.google.com/file/d/1QBEbr0P_OpTgUGbsxT3-PgKvSQtkeLvd/view
pg 23
automat = {'0':{'a', '1', 'b', '3'}, '1':{'a': '3', 'b': '2'}}
"""
f = open("automat_input.txt", "r")
for line in f.readlines():
    line = line.strip('\n').split()
    tranzitii = dict()
    parsedLinie = [(line[i], line[i + 1]) for i in range(1, len(line) - 1, 2)]

    if line[0][-1] == "F":
        stariFinale.append(line[0][:-1])
        line[0] = line[0][:-1]

    for tranzitie in parsedLinie:
        if tranzitie[0] not in alfabet:
            alfabet.append(tranzitie[0])
            
    parsedLinie.append(('lambda', line[0]))
    automat.update({line[0]: dict(parsedLinie)})

for elem in automat.items():
    print(elem)
