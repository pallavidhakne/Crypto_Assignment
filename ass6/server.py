import socket

def encrypt_block(m):
    c = pow(m, e, n)  #m to the pow e mod n
    return c

def encrypt_string(s):
    return ''.join([chr(encrypt_block(ord(x))) for x in list(s)])

s = socket.socket() 
host='127.0.0.1'
port = 12345               
s.bind((host, port))
s.listen()            
client, addr = s.accept()    
print ('Got connection from', addr )
e=int(client.recv(1024).decode())
n=int(client.recv(1024).decode())

msg = input("Enter a message to encrypt: ")
print("\nPlain message: " + msg + "\n")
enc = encrypt_string(msg)
print("Encrypted string: " +enc)
client.send(f'{enc}'.encode())





