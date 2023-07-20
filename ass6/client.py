import socket 
import random
from sympy import mod_inverse
s = socket.socket()
port = 12345            
s.connect(('127.0.0.1', port))
def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

def coprimes(a):
    l = []
    for x in range(2, a):
        if gcd(a, x) == 1 and mod_inverse(x, phi) != None:
            l.append(x)
    for x in l:
        if x == mod_inverse(x, phi):
            l.remove(x)
    return l

def decrypt_block(c):
    m = pow(c, d, n)
    return m

def decrypt_string(s):
    return ''.join([chr(decrypt_block(ord(x))) for x in list(s)])
p=17
q=19
n = p * q
phi = (p - 1) * (q - 1)
l=coprimes(phi)
e =  random.choice(l)
d = mod_inverse(e, phi)
print("\nYour public key is a pair of numbers (e=" + str(e) + ", n=" + str(n) + ").\n")
print("Your private key is a pair of numbers (d=" + str(d) + ", n=" + str(n) + ").\n")
s.send(f'{e}'.encode())
s.send(f'{n}'.encode())
ct=s.recv(1024).decode()
print("Received String: "+ct)
m=decrypt_string(ct)
print("Decoded string: "+m)
s.close()