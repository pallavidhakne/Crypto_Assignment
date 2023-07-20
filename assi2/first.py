#for encrption 
import socket 
s=socket.socket()
print("socket created")
port=12345
s.bind(('',port))
