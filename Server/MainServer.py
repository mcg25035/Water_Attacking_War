#main server
import threading
import socket
import time
import os
IP = '0.0.0.0'
PORT = 7001
Servers = []
Player_Data = []
Item_Data = {"WaterGun":100,"WaterTower":3600,"WaterTowerWithPressMotor":4800,"Pipe":50,"Battery":500,"Bottle":20,"Ballon":100,"Sprinkler":5000,"Shovel":800}
#player_data : [{"PlayerName":字串,"Inventory":[道具]}]
#Servers : [{"ip":字串,"Status":數字,"PlayerNum":數字}]
#status : 進行中:1 遊戲中:2 等待中:3
ServerMaxID = 0
Servers = 0
PlayerToken = 0
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((IP, PORT))
server.listen(5)
def talk_to_client():
    global Servers
    global Player_Data
    conn,addr = server.accept()
    data = conn.recv(1024).decode()
    #NewServerCreateInit
    while True:
        if data == "ServerCreated":
            conn.send("ip_request".encode())
            data = conn.recv(1024).decode()
            Temp_JSON = {"ip":data,"players":0,"status":0,"players_data":[]}
            Servers.append(Temp_JSON)
            conn.send("ok_now_break_conn".encode())
            continue
        #PlayerLoginInit
        elif data == "PlayerRegister":
            conn.send("register data request".encode())
            data1 = conn.recv(1024).decode()
            data2 = conn.recv(1024).decode()
            data3 = conn.recv(1024).decode()
            if os.path.isfile("./player_password/"+data1):
                conn.send("ERR.REGED".encode())
                continue
            else:
                f = open("./player_password/"+data1,"w")
                f.write(data2)
                f.close()
                f = open("./player_data/"+data1,"w")
                f.write(str({"PlayerName":data3,"Win":0,"Lose":0,"money":0,"Level":0,"Inventory":[{"hand",0},{"move",0}]}))
                f.close()
        elif data == "buy_something":
            conn.send("username_request")
            conn.send("wanna_buy")
            data1 = conn.recv(1024).decode()
            data2 = conn.recv(1024).decode()
            if os.path.isfile("./player_data/"+data):
                f.open("./player_data/"+data,"r+")
                data = f.read()
                f.close()
                if data["money"] >= ItemData[data2]:
                    f.open("./player_data/"+data,"w")
                    data["Inventory"].append(data2)
                    data["money"]-=ItemData[data2]
                    f.write(data)
                    f.close()
                    conn.send("ok".encode())
                else:
                    conn.send("money_not_enough".encode())
                continue
        elif data == "change_playername":
            conn.send("username_request")
            conn.send("passwrd_request")
            conn.send("changeTo_request")
            data1 = conn.recv(1024).decode()
            data2 = conn.recv(1024).decode()
            data3 = conn.recv(1024).decode("utf-8")
            if os.path.isfile("./player_password/"+data1):
                f = open("./player_password/"+data1,"r+")
                psd = f.read()
                f.close()
                if data2 == psd:
                    f = open("./player_data/"+data1,"r+")
                    data = eval(f.read())
                    f.close()
                    data["PlayerName"] = data3
                    f = open("./player_data/"+data1,"w")
                    f.write(data)
                    f.close()
                    conn.send("ok".encode())
                else:
                    conn.send("passwrd_err",encode())
            continue
        elif data == "PlayerLogin":
            conn.send("usrnme_request".encode())
            data1 = conn.recv(1024).decode()
            conn.send("psd_request".encode())
            data2 = conn.recv(1024).decode()
            temp_bool = False
            for i in Player_Data:
                if i["username"] == data1:
                    conn.send("ERR_logined".encode())
                    temp_bool = True
                    break
            if temp_bool == True:
                continue
            elif os.path.isfile("./player_password/"+data1):
                f.open("./player_password/"+data1,"r+")
                psd = f.read()
                f.close()
                if psd == data2:
                    f.open("./player_data/"+data1,"r+")
                    player_data = f.read()
                    f.close()
                    conn.send(player_data.encode('utf-8'))
                    player_data = eval(player_data)
                    Player_Data.append(player_data)
                    continue
                else:
                    conn.send("err_login".encode())
                    continue
        #ListenPlayerConnectServer
        elif data == "PlayerConnectServer":
            conn.send(str(Servers).encode())
        #ListenServerBreakConnect
        elif data == "ServerClose":
            conn.send("ip request".encode())
            data = conn.recv(1024).decode()
            temp_bool = False
            for i in Servers:
                if i["ip"] == data:
                    Servers.remove(i)
                    temp_bool = True
                    break
            if temp_bool:
                conn.send("ok".encode())
                continue
        elif data == "editPlayerData":
            conn.send("player_name request")
            data = conn.recv(1024).decode()
            conn.send("type request")
            data1 = conn.recv(1024).decode()
            f = open("./player_data/"+data,"r+")
            data2 = eval(f.read())
            f.close()
            if data1 == "Win":
                data2["Win"]+=1
                data2["Level"]+=0.5
            if data2 == "Lose":
                data2["Lose"]+=1
                data2["Level"]-=0.25
            f = open("./player_data/"+data,"w")
            f.write(data2)
            f.close()
        #ListenServerRequestPlayerData
        elif data == "PlayerDataRequest":
            conn.send("player_name request")
            data = conn.recv(1024).decode()
            f = open("./player_data/"+data,"r+")
            data2 = f.read()
            f.close()
            conn.send(data2.encode('utf-8'))
a = []
i = 0
while i<=100:
    a.append(threading.Thread(target = talk_to_client))
    i+=1

for i in a:
    i.start()

while True:
    a = input(">>>")
    eval(a)
