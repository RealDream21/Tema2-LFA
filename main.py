automat = dict()
alfabet = []
stariFinale = []
stareInitiala = None
"""
!!!!!!!trebuie eliminate starile din care nu se ajunge in stare finala(asta dupa ce termin tabelul si toate alea)
!!!!!!!se poate opri algoritmul daca la pasul k - 1 nu s a facut nicio modificare

https://drive.google.com/file/d/1QBEbr0P_OpTgUGbsxT3-PgKvSQtkeLvd/view
pg 23
automat = {'0':{'a', '1', 'b', '3'}, '1':{'a': '3', 'b': '2'}}
"""
f = open("automat_input.txt", "r")
for line in f.readlines():
    line = line.strip('\n').split()
    tranzitii = dict()
    parsedLinie = [(line[i], line[i + 1]) for i in range(1, len(line) - 1, 2)]

    if "iF" in line[0]:
        stareInitiala = line[0][:-2]
        stariFinale.append(line[0][:-2])
        line[0] = line[0][:-2]
    elif line[0][-1] == "F":
        stariFinale.append(line[0][:-1])
        line[0] = line[0][:-1]
    elif line[0][-1] == "i":
        stareInitiala = line[0][:-1]
        line[0] = line[0][:-1]

    for tranzitie in parsedLinie:
        if tranzitie[0] not in alfabet:
            alfabet.append(tranzitie[0])

    parsedLinie.append(('lambda', line[0]))
    automat.update({line[0]: dict(parsedLinie)})

f.close()
#elimin starile inaccesibile
stariDeParcurs = [stareInitiala]
stariParcurse = []
while len(stariDeParcurs) != 0:
    stare = stariDeParcurs.pop(0)
    stariParcurse.append(stare)
    for litera in alfabet:
        if automat[stare][litera] not in stariParcurse and automat[stare][litera] not in stariDeParcurs:
            stariDeParcurs.append(automat[stare][litera])
#print(stariParcurse)

#print(automat)

for stare in automat.copy():
    if stare not in stariParcurse:
        automat.pop(stare)

separabile = {stare:dict() for stare in automat.keys()}
#print(automat)


lungime = 0
cuvinteDeParcurs = alfabet.copy()
"""s = ['lambda' for i in range(len(automat.keys()))]
bkt(0)
print(s)
"""
maxN = max([int(x) for x in automat])
minN = min([int(x) for x in automat])

for i in range(maxN, minN - 1, -1):
    toAdd = []
    for j in range(i - 1, minN - 1, - 1):
        i = str(i)
        j = str(j)
        if i not in automat.keys() or j not in automat.keys():
            continue
        if (automat[i]['lambda'] in stariFinale and automat[j]['lambda'] not in stariFinale) or (automat[i]['lambda'] not in stariFinale and automat[j]['lambda'] in stariFinale):
            toAdd.append((j, 'lambda'))
    if i in automat.keys():
        separabile[str(i)].update(dict(toAdd)) #interpretarea este: i este separabil de j prin separabile[i][j], daca aleg dictionarul altfel sunt duplicate si nu pot avea lambda la mai multe

for _ in range(len(automat) + 2):
    for i in range(maxN, minN - 1, -1):
        if str(i) not in automat.keys():
            continue
        toAdd = []
        for j in range(i - 1, minN - 1, -1):
            if str(j) not in automat.keys():
                continue
            i = str(i)
            j = str(j)
            for cuvant in cuvinteDeParcurs:
                nod1 = i
                nod2 = j
                for litera in cuvant:
                    nod1 = automat[nod1][litera]
                    nod2 = automat[nod2][litera]
                    #if nod1 == nod2: optimizare dar riscant
                        #break
                if(nod1 in stariFinale and nod2 not in stariFinale) or (nod1 not in stariFinale and nod2 in stariFinale):
                    toAdd.append((j, cuvant))
        for tuplu in toAdd:
            if tuplu[0] not in separabile[str(i)]:
                separabile[str(i)].update({tuplu[0]: tuplu[1]})
    auxCuvinteDeParcurs = []
    for cuvant in cuvinteDeParcurs:
        for litera in alfabet:
            auxCuvinteDeParcurs.append(cuvant + litera)
    cuvinteDeParcurs = auxCuvinteDeParcurs.copy()

#corectie pentru vid(unde nu pot fi separate => echivalente)
for i in range(maxN, minN - 1, -1):
    if str(i) not in automat.keys():
        continue
    for j in range(i - 1, minN - 1, -1):
        if str(j) not in automat.keys():
            continue
        i = str(i)
        j = str(j)
        if j not in separabile[i].keys():
            separabile[i][j] = 'vid'

newAutomat = dict()
stariConcatenate = []
for stare in separabile:
    if 'vid' in separabile[stare].values():
        for other in separabile[stare].keys():
            if 'vid' in separabile[stare][other]:
                newAutomat[other + "-" + stare] = {}
                stariConcatenate.append(other)
                stariConcatenate.append(stare)
    else:
        newAutomat[stare] = {}

#elimin starile duplicate de genul 1, 1 2
for duplicate in stariConcatenate:
    try:
        newAutomat.pop(duplicate)
    except KeyError:
        continue

#folosesc tranzitivitatea pentru a verifica daca am cate 3 stari echivalente intr-un singur nod
auxAutomat = dict()
for newStare in newAutomat:
    if '-' in newStare:
        bigStare = set(newStare.split('-'))
        for othernewStare in newAutomat:
            if othernewStare == newStare:
                continue
            for stare in othernewStare.split('-'):
                if stare in bigStare:
                    for _ in othernewStare.split('-'):
                        bigStare.add(_)
                    break
        auxAutomat["-".join(sorted(bigStare))] = dict()
    else:
        auxAutomat[newStare] = dict()
newAutomat = auxAutomat

#print(newAutomat)

for newStare in newAutomat:
    for stare in newStare.split('-'):
        newAutomat[newStare] = automat[stare]

#newNotations = {'1':'1-2', '2': '1-2'}
newNotations = {}
for newStare in newAutomat:
    for stare in newStare.split('-'):
        newNotations[stare] = newStare

for newStare in newAutomat:
    for tranzitie in newAutomat[newStare].keys():
        try:
            newAutomat[newStare][tranzitie] = newNotations[newAutomat[newStare][tranzitie]]
        except KeyError: #TO BE TESTED!!!!!!!!!!!!
            pass

f = open("automat_minimal.txt", "w")

newStareInitiala = newNotations[stareInitiala]
newStariFinale = [newNotations[x] for x in stariFinale]

for node in newAutomat:
    newAutomat[node].pop('lambda')

#eliminate the states from which i can never reach final states
auxCuvinteDeParcurs = alfabet.copy()
toPop = []
noPop = []
for _ in range(len(newAutomat) + 2):
    for stare in newAutomat:
        for cuvant in auxCuvinteDeParcurs:
            nod = stare
            for litera in cuvant:
                nod = newAutomat[nod][litera]
            if nod in newStariFinale:
                noPop.append(stare)
                break
    auxCuvinteDeParcurs = [x + y for x in auxCuvinteDeParcurs for y in alfabet]

for stare in newAutomat:
    if stare not in noPop:
        toPop.append(stare)
    
for stare in newAutomat:
    tranzitieToPop = []
    for tranzitie in newAutomat[stare]:
        if newAutomat[stare][tranzitie] in toPop:
            tranzitieToPop.append(tranzitie)
    for tranzitie in tranzitieToPop:
        newAutomat[stare].pop(tranzitie)

for stare in toPop:
    newAutomat.pop(stare)


for newStare in newAutomat:
    to_write = newStare
    if stareInitiala in newStare.split('-'):
        to_write += 'i'
    if newStare in newStariFinale:
        to_write += 'F'
    to_write += " "
    for newTranzitie in newAutomat[newStare]:
        to_write += newTranzitie + " " + newAutomat[newStare][newTranzitie] + " "
    f.write(to_write + '\n')

f.close()
input("DONE")