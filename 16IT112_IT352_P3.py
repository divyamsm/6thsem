from numpy import binary_repr
import itertools

expansion_table = [
        31,  0,  1,  2,  3,  4,
		 3,  4,  5,  6,  7,  8,
		 7,  8,  9, 10, 11, 12,
		11, 12, 13, 14, 15, 16,
		15, 16, 17, 18, 19, 20,
		19, 20, 21, 22, 23, 24,
		23, 24, 25, 26, 27, 28,
		27, 28, 29, 30, 31,  0
    ]

s_box = [
		# S1
		[14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7,
		 0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8,
		 4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0,
		 15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13],

		# S2
		[15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10,
		 3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5,
		 0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15,
		 13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9],

		# S3
		[10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8,
		 13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1,
		 13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7,
		 1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12],

		# S4
		[7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15,
		 13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9,
		 10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4,
		 3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14],

		# S5
		[2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9,
		 14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6,
		 4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14,
		 11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3],

		# S6
		[12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11,
		 10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8,
		 9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6,
		 4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13],

		# S7
		[4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1,
		 13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6,
		 1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2,
		 6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12],

		# S8
		[13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7,
		 1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2,
		 7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8,
		 2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11],
	]

p_box = [
		15, 6, 19, 20, 28, 11,
		27, 16, 0, 14, 22, 25,
		4, 17, 30, 9, 1, 7,
		23,13, 31, 26, 2, 8,
		18, 12, 29, 5, 21, 10,
		3, 24
	]

def middlespaces(entry_p):
    entry = ''
    for i in entry_p:
        if i != ' ':
            entry += i
    return entry

#repetitive for the getp64 func
def getbinary64chars(entry):
    number = []
    for i in range(len(entry)):
        number.append( ord(entry[i]))

    for i in range(len(number)):
        number[i] = binary_repr(number[i],width = 8)

    print("Block before initial permutation: ",number)
    number = ''.join(number)

    return number

# returns 64 binary string
def getallblocks(entry):
    outputstr = ''
    ctb = 0
    while len(entry)>=8:
        ctb += 1
        print('\nBlock no: ',ctb)
        outputstr += getbinary64chars(entry[:8])
        #alternative below for binary input
        #outputstr += entry[:8]
        entry = entry[8:]

    if len(entry)>0:
        print("\nBlock no: ",ctb+1)
        ct = 0
        while len(entry)!=8:
            entry = entry +' '
            #entry = entry + '0'
            ct += 1
        print("No of trailing spaces added: " ,ct)
        outputstr += getbinary64chars(entry)

    return (outputstr)

#returns 48 bit expanded str
def ebox(r32):
    bits = list(r32)
    newlist = []
    for i in range(len(expansion_table)):
        newlist.append(bits[expansion_table[i]])
    newlist = ''.join(newlist)
    return newlist

#returns xor o/p
def xor(entry,key):
    if len(entry)!=len(key):
        print("error")
        exit()
    newstr = ''
    for i in range(len(entry)):
        if entry[i] == key[i]:
            newstr += '0'
        else:
            newstr += '1'
    return newstr

#converts 48 to 32 by taking blocks of 6 and using indexing from s_box
def sbox(entry):
    i = 0
    opstr = ''
    while len(entry)>0:
        row = entry[0] + entry[5]
        col = entry[1:5]
        mul = int(row,2)
        ind = int(col,2) + 16*mul
        s = s_box[i][ind]
        s = str(binary_repr(s,4))
        opstr += s
        entry = entry[6:]
        i += 1
    return opstr

#shuffles sbox op
def pbox(entry):
    newstr = ''
    for i in range(len(entry)):
        newstr += entry[p_box[i]]
    return newstr

tcindex = 1

while tcindex<6:

    #entry_p = str(input('Enter the string'))
    entry_p = str(open('PT-TC'+str(tcindex)+'.txt').readline().strip())

    finalanswerlist = []

    #entry = middlespaces(entry_p)
    entry = entry_p

    l = len(entry)
    #print(l)

    #part0 = getallblocks(entry)
    part0 = entry

    while len(part0)>0:
        part1 = part0[:64]
        part0 = part0[64:]
        #print("part1 ",part1)

        f = open("RK-TC"+str(tcindex)+".txt", 'r')

        r32 = part1[32:]
        l32 = part1[:32]

        for i in range(16):
            part2 = ebox(r32)
            #print("part2 ",part2)
            part3 = xor(part2,f.readline().strip())
            #print("part3 ",part3)
            part4 = sbox(part3)
            #print("part4 ", part4)
            part5 = pbox(part4)
            #print("part5 ",part5)
            part6 = xor(part5,l32)
            #print("part6 ",part6)
            l32 = r32
            r32 = part6
        finalanswerlist.append(str(r32+l32)) #added reverse order because last iteration should not be swapped

    print( "Test case ",tcindex," : ", finalanswerlist)

    tcindex += 1


