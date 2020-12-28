import socket
import time
import random
import sqlite3

UDP_IP = "192.168.0.17"
UDP_PORT= 8888
DEST_IP ="192.168.0.3"
DEST_PORT= 7777
 
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
sock.bind((UDP_IP,UDP_PORT))

dbname='/var/www/piapp/dbfolder/sensorsData.db'
sampleFreq = 1*3# time in seconds ==> Sample each 1 min


# get data from DHT sensor
def getRoomData():   
    message =b"tempe"    
    #print("I am asking:",message)
    #print("\n")
    sock.sendto(message,(DEST_IP,DEST_PORT))
    data, addr = sock.recvfrom(4096)
    data = data.decode()
    tempe = float(data)
    #print("recieved message",data)
    #print("\n")
    #print(addr)
    #print("\n")

    message =b"light"    
    #print("I am asking:",message)
    #print("\n")
    sock.sendto(message,(DEST_IP,DEST_PORT))
    data, addr = sock.recvfrom(4096)
    data = data.decode()
    light = float(data)
    #print("recieved message",data)
    #print("\n")
    #print(addr)
    #print("\n")

    message =b"sound"    
    #print("I am asking:",message)
    #print("\n")
    sock.sendto(message,(DEST_IP,DEST_PORT))
    data, addr = sock.recvfrom(4096)
    data = data.decode()
    sound = float(data)
    #print("recieved message",data)
    #print("\n")
    #print(addr)
    #print("\n")
    
    co2value = round(random.uniform(250,400000),2)
    #print("Co2 value: ")
    #print(co2value)
    #print("\n")
    
    covalue = round(random.uniform(0,12800),2)
    #print("Co value: ")
    #print(covalue)
    #print("\n")
    
    humvalue = round(random.uniform(0,100),2)
    #print("Humidity: ")
    #print(humvalue)
    #print("\n")
    return tempe, light, sound, co2value, covalue, humvalue
 

# log sensor data on database
def insertData (tempe, light, sound, co2value, covalue, humvalue):
    conn=sqlite3.connect(dbname,check_same_thread=False)
    curs=conn.cursor()
    curs.execute("INSERT INTO Room_data values(datetime('now'), (?), (?),(?),(?),(?),(?))", (tempe, light,sound,co2value,covalue,humvalue))
    conn.commit()
    conn.close()    




# main function
def arduino():
    while True:
        tempe, light, sound, co2value, covalue, humvalue = getRoomData()
        insertData (tempe, light, sound, co2value, covalue, humvalue)
        time.sleep(sampleFreq)

# ------------ Execute program 
#main()
        

