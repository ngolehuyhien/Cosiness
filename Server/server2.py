import socket
import time
import random

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
    
    co2value = round(random.uniform(250,400000),2)
    print("Co2 value: ")
    print(co2value)
    print("\n")
    
    covalue = round(random.uniform(0,12800),2)
    print("Co value: ")
    print(covalue)
    print("\n")
    
    humvalue = round(random.uniform(0,100),2)
    print("Humidity: ")
    print(humvalue)
    print("\n")
    
            
    """            
    if len(data):
        print("recieved message",data)
        print(addr)
        i=i+1
    """

    time.sleep(5)
        
    