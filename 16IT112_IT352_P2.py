'''Read Input'''
from numpy import binary_repr
entry = str(input("Give the string "))

if len(entry)<8:
    print("Error, length less than 8")
    exit()

usercode = str(input("Enter code 1 (first 8 chars) or 2 (last 8 chars) "))

key_stage_1 = []
if usercode == '1':
    for i in range(8):
        key_stage_1.append(ord(entry[i]))
elif usercode == '2':
    entry = entry[-8:]
    for i in range(8):
        key_stage_1.append(ord(entry[i]))
else:
    print("Error, invalid code")
    exit()


'''ASCII TO BINARY'''


for i in range(len(key_stage_1)):
    key_stage_1[i] = binary_repr(key_stage_1[i],width = 8)


'''PC-1'''


PC_1_table = [57, 49, 41, 33, 25, 17, 9,
        1, 58, 50, 42, 34, 26, 18,
        10, 2, 59, 51, 43, 35, 27,
        19, 11, 3, 60, 52, 44, 36,
        63, 55, 47, 39, 31, 23, 15,
        7, 62, 54, 46, 38, 30, 22,
        14, 6, 61, 53, 45, 37, 29,
        21, 13, 5, 28, 20, 12, 4]
'''convert the 64 bit values to 56 bit values and subtract 1 for index values'''
for i in range(len(PC_1_table)):
    PC_1_table[i] -= 1

key_stage_1 = ''.join(key_stage_1)


key_stage_2 = [2 for i in range(56)]
'''replace values...perform pc1 operation'''
for i in range(56):
    key_stage_2[i] = key_stage_1[PC_1_table[i]]

key_stage_2 = ''.join(key_stage_2)


'''PC2 table conversion'''
PC_2_table = [14, 17, 11, 24, 1, 5, 3, 28,
        15, 6, 21, 10, 23, 19, 12, 4,
        26, 8, 16, 7, 27, 20, 13, 2,
        41, 52, 31, 37, 47, 55, 30, 40,
        51, 45, 33, 48, 44, 49, 39, 56,
        34, 53, 46, 42, 50, 36, 29, 32]

for i in range(len(PC_2_table)):
    PC_2_table[i] -=1

def leftshift(test):
    tempc = test[0]
    test = test[1:]
    test += tempc
    return test

def round(no,key,pc2,keygroup):
    '''left shift'''
    lkey = key[:28]
    rkey = key[28:]

    # print(lkey)
    # print(rkey)

    if no not in (1,2,9,16):
        lkey = leftshift(lkey)
        rkey = leftshift(rkey)

    lkey = leftshift(lkey)
    rkey = leftshift(rkey)

    newkey = lkey+rkey
    keyop = ['' for _ in range(48)]
    for i in range(48):
        keyop[i] = newkey[PC_2_table[i]]

    keygroup.append(''.join(keyop))

    return newkey

'''EXECUTION'''
keygroup = []

prevkey = key_stage_2
for i in range(1,17):
    currentkey = round(i,prevkey,PC_2_table,keygroup)
    prevkey = currentkey


def tohex(bits):
    ans = ''
    while len(bits)>0:
        current = bits[:4]
        bits = bits[4:]
        ans += hex(int(current,2))[2:]
    return ans


for i in range(len(keygroup)):
    print('Round ',i,' key is : ',keygroup[i] ,' in hex : ',tohex(keygroup[i]))

