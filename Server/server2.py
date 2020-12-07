import socket
import time

UDP_IP = "192.168.0.17"
UDP_PORT= 8888
DEST_IP ="192.168.0.3"
DEST_PORT= 7777
 
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP,UDP_PORT))

#i=0
 

while(1): #Main Loop
    """
    if i%2==0:
        message =b"temp"
    else:
        message=b"humi"
    """
    message =b"tempe"    
    print("I am asking:",message)
    print("\n")
    sock.sendto(message,(DEST_IP,DEST_PORT))
    data, addr = sock.recvfrom(4096)
    data = data.decode()
    print("recieved message",data)
    print("\n")
    print(addr)
    print("\n")

    message =b"light"    
    print("I am asking:",message)
    print("\n")
    sock.sendto(message,(DEST_IP,DEST_PORT))
    data, addr = sock.recvfrom(4096)
    data = data.decode()
    print("recieved message",data)
    print("\n")
    print(addr)
    print("\n")

    message =b"sound"    
    print("I am asking:",message)
    print("\n")
    sock.sendto(message,(DEST_IP,DEST_PORT))
    data, addr = sock.recvfrom(4096)
    data = data.decode()
    print("recieved message",data)
    print("\n")
    print(addr)
    print("\n")
            
    """            
    if len(data):
        print("recieved message",data)
        print(addr)
        i=i+1
    """

    time.sleep(5)
        
    