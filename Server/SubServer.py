#sub server
import threading
import time
import os
import socket
import random
print("請依照網頁提供的指示操作ngrok")
print("操作完成請依照網頁指示輸入ngrok的ip在此")
ip = input()
print("請依照網頁指示提供主伺服器ip")
ip2 = socket.gethostbyname(input())
print("請依照網頁指示提供主伺服器port")
port = input()
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((ip2, port))
s.send("ServerCreated".encode())
s.recv(1024)
s.send(ip.encode())
s.recv(1024)
s.close()
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("0.0.0.0", 7000))
def game_server():
    PlayerData = []
    Map = []
    a = []
    while len(Map)<500:
        Map.append([])
    for i in Map:
        while len(i)<500:
            i.append(["",0])
    i = 0
    temp_a = []
    while i<50000:
        a1 = random.randint(0, 499)
        a2 = random.randint(0, 499)
        Map[a1][a2] = ["grass",0]
        i+=1
    i=0
    while i<7500:
        a1 = random.randint(0, 499)
        a2 = random.randint(0, 499)
        Map[a1][a2] = ["add_water_station",100]
        i+=1
    i=0
    while i<75000:
        a1 = random.randint(0, 499)
        a2 = random.randint(0, 499)
        Map[a1][a2] = ["wall",100]
        i+=1
    i=0
    while i<8: 
        a1 = random.randint(0, 499)
        a2 = random.randint(0, 499)
        if [a1,a2] not in temp_a: 
            if Map[a1][a2] == ['',0]:
                Map[a1][a2] = ['player',80]
                i+=1
                temp_a.append([a1,a2])
                continue
            if Map[a1][a2] == ['grass',0]:
                Map[a1][a2] = ['player','grass',80]
                i+=1
                temp_a.append([a1,a2])
                continue
            if Map[a1][a2] == ['add_water_station',100]:
                continue
            if Map[a1][a2] == ['wall',100]:
                continue
        else:
            continue
    server.accept()

game_server()