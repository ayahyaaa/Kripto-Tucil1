import numpy as np
import re

def outputmaker(a):
    return ' '.join([a[i:i + 5] for i in range(0, len(a), 5)])

def keymaker(message,key):
    keychar = []
    if (len(message)>(len(key))):
        for i in range(len(message)):
            keychar.insert(len(keychar),ord(key[i%len(key)])%97)
    else:
        for characters in key:
            keychar.insert(len(keychar),ord(characters)%97)

    return keychar

def autokeymaker(message,key):
    keychar = []
    if (len(message)>(len(key))):
        for i in range(len(key)):
            keychar.insert(len(keychar),ord(key[i])%97)
        for i in range(len(key),len(message)):
            keychar.insert(len(keychar),ord(message[i-len(key)])%97)
    else:
        for characters in key:
            keychar.insert(len(keychar),ord(characters)%97)

    return keychar

def playfairkeymaker(key):
    key.replace('j','')
    keychar = []
    for i in range(len(key)):
        if (ord(key[i])%97) in keychar:
            continue
        else:
            keychar.insert(len(keychar),ord(key[i])%97)
    toInsert = 0
    while(len(keychar)<25):
        if (toInsert==9):
            toInsert += 1
            continue
        if (toInsert not in keychar):
            keychar.insert(len(keychar),toInsert)
        toInsert += 1

    pfkey = np.reshape(keychar,(5,5))
    return pfkey

'''def bytetextmaker(file):
    byte = file.read(1)
    textchar = []
    while byte:
        textchar.insert(len(textchar),ord(byte))
        byte = file.read(1)
    return textchar'''
    
def playfairtextmaker(message):
    message.replace('j','i')
    messagechar = []
    for characters in message:
        messagechar.insert(len(messagechar),ord(characters)%97)
    
    for i in range(1,len(messagechar)):
        if (messagechar[i]==messagechar[i-1]):
            messagechar.insert(i,23)
    if (len(messagechar)%2==1):
        messagechar.insert(len(messagechar),23)
        
    pftext = np.reshape(messagechar,(-1,2))
    return pftext

def vigenere_encrypt(message,key):
    keychar = keymaker(message,key)
    messagechar = []
    for characters in message:
        messagechar.insert(len(messagechar),ord(characters)%97)

    encrypted = messagechar
    for i in range(len(encrypted)):
        encrypted[i] = vigenere_matrice[keychar[i]][messagechar[i]]

    return encrypted

def full_vigenere_encrypt(message,key):
    np.random.shuffle(full_vigenere_matrice)
    keychar = keymaker(message,key)
    messagechar = []
    for characters in message:
        messagechar.insert(len(messagechar),ord(characters)%97)

    encrypted = messagechar
    for i in range(len(encrypted)):
        encrypted[i] = full_vigenere_matrice[keychar[i]][messagechar[i]]

    return encrypted

def autokey_vigenere_encrypt(message,key):
    keychar = autokeymaker(message,key)
    messagechar = []
    for characters in message:
        messagechar.insert(len(messagechar),ord(characters)%97)

    encrypted = messagechar
    for i in range(len(encrypted)):
        encrypted[i] = vigenere_matrice[keychar[i]][messagechar[i]]

    return encrypted

'''def extended_vigenere_encrypt(message,key):'''


def playfair_calculate(row,pfkey,encrypt):
    position_matrice = np.zeros((2,2), dtype=int)
    x, y, i, j, loop = 0, 0, 0, 0, 0
    while(loop!=2):
        if (j==5):
            i += 1
            j = -1
        elif (pfkey[i][j]==row[loop]):
            position_matrice[x][y] = i
            y += 1
            position_matrice[x][y] = j
            x += 1
            y, i, j = 0, 0, -1
            loop += 1
        j += 1
    if (encrypt):
        if (position_matrice[0][0]==position_matrice[1][0]):
            position_matrice[0][1] = (position_matrice[0][1] + 1) % 5
            position_matrice[1][1] = (position_matrice[1][1] + 1) % 5
        elif (position_matrice[0][1]==position_matrice[1][1]):
            position_matrice[0][0] = (position_matrice[0][0] + 1) % 5
            position_matrice[1][0] = (position_matrice[1][0] + 1) % 5
        else:
            swap = position_matrice[0][1]
            position_matrice[0][1] = position_matrice[1][1]
            position_matrice[1][1] = swap
    else:
        if (position_matrice[0][0]==position_matrice[1][0]):
            position_matrice[0][1] = (position_matrice[0][1] - 1) % 5
            position_matrice[1][1] = (position_matrice[1][1] - 1) % 5
        elif (position_matrice[0][1]==position_matrice[1][1]):
            position_matrice[0][0] = (position_matrice[0][0] - 1) % 5
            position_matrice[1][0] = (position_matrice[1][0] - 1) % 5
        else:
            swap = position_matrice[0][1]
            position_matrice[0][1] = position_matrice[1][1]
            position_matrice[1][1] = swap

    newrow = row
    newrow[0] = pfkey[position_matrice[0][0]][position_matrice[0][1]]
    newrow[1] = pfkey[position_matrice[1][0]][position_matrice[1][1]]
    return newrow 
        
def playfair(pftext,pfkey,encrypt):
    procctext = pftext
    for i in range(len(pftext)):
        procctext[i] = playfair_calculate(pftext[i],pfkey,encrypt)

    result = np.reshape(procctext,procctext.size)
    return result

def affine_encrypt(message,m,b):
    encryptchar = []
    for characters in message:
        encryptchar.insert(len(encryptchar),(((ord(characters)%97)*m)+b)%26)

    return encryptchar

def vigenere_decrypt(message,key):
    keychar = keymaker(message,key)
    messagechar = []
    for characters in message:
        messagechar.insert(len(messagechar),ord(characters)%97)

    decrypted = messagechar
    for i in range(len(decrypted)):
        decrypted[i] = vigenere_matrice[(keychar[i]*-1)%26][messagechar[i]]

    return decrypted

def full_vigenere_decrypt(message,key):
    keychar = keymaker(message,key)
    messagechar = []
    for characters in message:
        messagechar.insert(len(messagechar),ord(characters)%97)

    decrypted = messagechar
    for i in range(len(decrypted)):
        for j in range(26):
            if(messagechar[i]==full_vigenere_matrice[keychar[i]][j]):
                decrypted[i] = j
                break
                
    return decrypted

def autokey_vigenere_decrypt(plaintext,message,key):
    keychar = autokeymaker(plaintext,key)
    messagechar = []
    for characters in message:
        messagechar.insert(len(messagechar),ord(characters)%97)

    decrypted = messagechar
    for i in range(len(decrypted)):
        for j in range(26):
            if(messagechar[i]==vigenere_matrice[keychar[i]][j]):
                decrypted[i] = j
                break

    return decrypted

def inverse_mod(base,m):
    for i in range(1,base):
        if (((i*m)%base)==1):
            return i
        
def affine_decrypt(message,m,b):
    decryptchar = []
    for characters in message:
        decryptchar.insert(len(decryptchar),((inverse_mod(26,m)*((ord(characters)%97)-b))%26))

    return decryptchar

vigenere_matrice = \
    np.array([[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25],
              [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,0],
              [2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,0,1],
              [3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,0,1,2],
              [4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,0,1,2,3],
              [5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,0,1,2,3,4],
              [6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,0,1,2,3,4,5],
              [7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,0,1,2,3,4,5,6],
              [8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,0,1,2,3,4,5,6,7],
              [9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,0,1,2,3,4,5,6,7,8],
              [10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,0,1,2,3,4,5,6,7,8,9],
              [11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,0,1,2,3,4,5,6,7,8,9,10],
              [12,13,14,15,16,17,18,19,20,21,22,23,24,25,0,1,2,3,4,5,6,7,8,9,10,11],
              [13,14,15,16,17,18,19,20,21,22,23,24,25,0,1,2,3,4,5,6,7,8,9,10,11,12],
              [14,15,16,17,18,19,20,21,22,23,24,25,0,1,2,3,4,5,6,7,8,9,10,11,12,14],
              [15,16,17,18,19,20,21,22,23,24,25,0,1,2,3,4,5,6,7,8,9,10,11,12,14,15],
              [16,17,18,19,20,21,22,23,24,25,0,1,2,3,4,5,6,7,8,9,10,11,12,14,15,16],
              [17,18,19,20,21,22,23,24,25,0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16],
              [18,19,20,21,22,23,24,25,0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17],
              [19,20,21,22,23,24,25,0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18],
              [20,21,22,23,24,25,0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19],
              [21,22,23,24,25,0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20],
              [22,23,24,25,0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21],
              [23,24,25,0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22],
              [24,25,0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23],
              [25,0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24]])

full_vigenere_matrice = vigenere_matrice

''' akses matriks vigenere, vigenere_matrice[kunci][plainteks]'''

''' file input
file = open("./cap.JPG", 'rb')
byte = file.read(1)
print(byte)
textchar = []
while byte:
    print(byte)
    textchar.insert(len(textchar),byte)
    byte = file.read(1)
print(textchar)'''

'''        
message1 = input("input name\n")
message = message1.lower().replace(" ","")
key1 = input("insert key\n")
key = key1.lower().replace(" ","")

regex = re.compile('[^a-z]+')
regex.sub('',message)
regex.sub('',key)
'''

'''vigenere usage
cytext = autokey_vigenere_encrypt(message,key)
encrypted = ""
for elements in cytext:
    encrypted += chr(elements+97)
print(encrypted)

ptext = autokey_vigenere_decrypt(message,encrypted,key)
decrypted = ""
for elements in ptext:
    decrypted += chr(elements+97)
print(decrypted)'''

'''playfair usage
playfairkey = key.replace('j','')
pfkey = playfairkeymaker(playfairkey)
pftext = playfairtextmaker(message)
pfresult = playfair(pftext,pfkey,True)
encrypted = ""
for elements in pfresult:
    encrypted += chr(elements+97)
print(encrypted)

pfdecrypt = playfair(playfairtextmaker(encrypted),pfkey,False)
decrypted1=""
for elements in pfdecrypt:
    decrypted1 += chr(elements+97)
decrypted = decrypted1.replace("x","")
print(decrypted)'''

'''affine usage
m = int(input("isi m, m merupakan bilangan yang relatif prima dengan 26\n"))
b = int(input("isi b, b terserah\n"))

cytext = affine_encrypt(message,m,b)
encrypted = ""
for elements in cytext:
    encrypted += chr(elements+97)
print(encrypted)

ptext = affine_decrypt(encrypted,m,b)
decrypted = ""
for elements in ptext:
    decrypted += chr(elements+97)
print(decrypted)'''
