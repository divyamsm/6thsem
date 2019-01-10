from numpy import binary_repr
import itertools
import binascii
"""INITIAL PERM TABLE """
ini_perm_table = [0 for i in range(64)]
ini_perm_table[0] = 58
for i in range(1,8):
    ini_perm_table[i] = ini_perm_table[i-1]-8
#print(ini_perm_table)
j = 1
for k in range(3):
    for i in range(0,8):
        ini_perm_table[i+j*8] = ini_perm_table[i+(j-1)*8]+2
    j+=1
ini_perm_table[39] = 1
for i in range(38, 31,-1):
    ini_perm_table[i] = ini_perm_table[i+1] +8
ini_perm_table[47] = 3
for i in range(46, 39,-1):
    ini_perm_table[i] = ini_perm_table[i+1] +8
ini_perm_table[55] = 5
for i in range(54, 47,-1):
    ini_perm_table[i] = ini_perm_table[i+1] +8
ini_perm_table[63] = 7
for i in range(62, 55,-1):
    ini_perm_table[i] = ini_perm_table[i+1] +8

#print(ini_perm_table)
"""DONE"""

final_perm_table = [0 for i in range(63)]
final_perm_table[0] =40
final_perm_table[1] =8
for i in range(2,8):
    final_perm_table[i] = final_perm_table[i-2] +8

for i in range(8,63):
    final_perm_table[i] = final_perm_table[i-8] -1

final_perm_table.append(25)
# for i in range(8):
#     print(final_perm_table[i*8:i*8+8])

"""DONE"""

def mygrouper(n, iterable):
    args = [iter(iterable)] * n
    return ([e for e in t if e != None] for t in itertools.zip_longest(*args))


'''OPERATIONS'''
def perform(entry,ini_perm_table,final_perm_table):
    number = []
    for i in range(len(entry)):
        number.append( ord(entry[i]))

    for i in range(len(number)):
        number[i] = binary_repr(number[i],width = 8)

    print("Block before initial permutation: ",number)
    number = ''.join(number)


    permlist = []

    for i in range(64):
        permlist.append(number[ini_perm_table[i]-1])

    temp = list(mygrouper(8,permlist))
    for i in range(len(temp)):
        temp[i]=''.join(temp[i])

    print("Block after initial permutation:  ",temp)

    ''.join(permlist)

    fperm = []

    for i in range(64):
        fperm.append(permlist[final_perm_table[i]-1])

    fperm = ''.join(fperm)

    fperm22 = list(mygrouper(8,fperm))
    for i in range(len(fperm22)):
        fperm22[i] = ''.join(fperm22[i])

    print("Block after final permutation:    ",fperm22)
    fstr = ''
    for i in range(len(fperm22)):
        n = int(fperm22[i], 2)
        fstr += str(chr(n))
    return(fstr)

entry = str(input('Enter the string'))

l = len(entry)

outputstr = ''
ctb = 0
while len(entry)>=8:
    ctb += 1
    print('\nBlock no: ',ctb)
    outputstr += perform(entry[:8],ini_perm_table,final_perm_table)
    entry = entry[8:]

if len(entry)>0:
    print("\nBlock no: ",ctb+1)
    ct = 0
    while len(entry)!=8:
        entry = entry +' '
        ct += 1
    print("No of trailing spaces added: " ,ct)
    outputstr += perform(entry,ini_perm_table,final_perm_table)

print( "\nFinal decoded text: ",outputstr)
