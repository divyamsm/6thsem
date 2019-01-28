import csv
import itertools
from collections.abc import Iterable

def read_transactions(filename='td1.csv'):
    trlist = []
    with open(filename) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            for i in range(len(row)):
                row[i] = int(row[i])
            trlist.append(row)
    return (trlist)


def filter(l0,freqdict,min_sup):
    l1 = []
    for i in l0:
        j = i.pop()
        if freqdict[j] >= min_sup:
            l1.append({j})
    return l1


trlist = read_transactions("retail_dataset.csv")
print("Transaction list:",trlist)
min_support = len(trlist)*2/9


def getfrequency(freqict):
    for i in trlist:
        for j in i:
            # j=(j,)
            freqdict[j] = 0
    for i in trlist:
        for j in i:
            # j = (j,)
            freqdict[j] = freqdict[j] + 1
    return freqdict


#
freqdict = getfrequency({})
l1 = []
for i in freqdict.items():
    if i[1] >= min_support:
        l1.append(i[0])
#print(l1)


def getl(curc,trlist):
    curl = []
    for elementgroup in curc:
        ct = 0
        for transaction in trlist:
            #print(elementgroup , transaction)
            if set(elementgroup) <= set(transaction):
                ct+=1
                #print('True')
        #print(elementgroup,ct)
        if elementgroup == (39,48):
            print("stored")
        freqdict[elementgroup] = ct
        if ct >= min_support:
            curl.append(list(elementgroup))
    return curl

print("L value for i =  1  = ",l1)

curc,prevc = [], []
prevl,curl= [],[]

ctemp = l1

llist = []

ind = 2
while True:
    curc = list(itertools.combinations(ctemp, ind))
    #print("C value for i = ",ind," = ",curc)

    curl = getl(curc, trlist)
    print("L value for i = ",ind," = ", curl)

    llist.append(curl)
    ctemp = set()
    for i in curl:
        for j in i:
            ctemp.add(j)
    #print(ctemp)

    ind = ind+1

    if len(curl) == 0:
        break

def powerset(iterable):
    s = list(iterable)
    return itertools.chain.from_iterable(itertools.combinations(s,r) for r in range(len(s)+1))

print("Frequency table: ",freqdict)

#print(type(_) for _ in freqdict.items())

confidence_table = []

#print(freqdict[sorted((48,39))],"val")

for i in llist:
    for j in i:
        rhs = lhs = [set(l) for l in powerset(j)][1:]
        for a in lhs:
            for b in rhs:
                if len(a.intersection(b)) ==0:
                    x = tuple(a.union(b))
                    x = tuple(sorted(x))
                    #print("final", x)
                    if len(a) == 1:
                        y1 = int(a.pop())
                        y = y1
                        a.add(y1)
                    else:
                        y = tuple(a)
                    print("x is ",x)
                    print("y is ",y)
                    confidence = freqdict[x]/freqdict[y]
                    confidence_table.append([a,b,confidence])

min_confidence = 0.5

for i in confidence_table:
    if i[2]>= min_confidence:
        print("Rule : ",i[0]," -> ",i[1]," : ",i[2])


