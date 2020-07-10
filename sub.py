"""
ESAME DI STATO 2020 
@Author: Brugin Marco CLasse 5^AI 
Simulazione sistema di sensoristica basato su protocollo publisher/subscriber multithreading, in formato json con monitoraggio di CO2 e radioattività tramite doppia  dashboard: una fornita da Thingboard, un cloud MQTT,  e una implemetata  da me senza utilizzo di servizzi esterni, con salvataggio in database scolastico : 80.210.122.172
Server Broker: 80.210.122.173. 
Presente una misura di affidabilità consistente, grazie a un salvataggio in locale 
Presente inoltre sistema di notifica desktop in caso di allarme.
Presente inoltre crittografia Fernet e attivazione sistema via Telegram (bot_Token:1071297564:AAFJ9OH9WaNsPWsw_hnqmnmegnj3fs_qRmc). 
Quest'opera è stata rilasciata con licenza Creative Commons Attribuzione 3.0 Italia. Per leggere una copia della licenza visita il sito web
http://creativecommons.org/licenses/by/3.0/it/ o spedisci una lettera a Creative Commons, PO Box 1866, Mountain View, CA 94042, USA.
Python_Version:3.8.2
Version 2.3
"""
import paho.mqtt.client as m
from webbrowser import open_new_tab
import MySQLdb as p
import threading
import os
import platform
import json
import base64
import random
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes

def connect(client,userdata,flags,rc):
    print("Connect succefully with result code "+str(rc))
    client.subscribe("Esame2020/Brugin_M/#")
def message(client,userdata,msg):
    print(msg.topic+" "+msg.payload.decode())
    s=msg.topic.split("/")
    a=msg.payload.decode()
    print(s)
    #data=json.loads(msg.payload.decode())
    #print(data)
    sensore=s[2]
    oggetto=s[3]
    b=a[1:].encode("utf-8")
    c=f.decrypt(b)
    d=c.decode(encoding = 'utf-8')
    print("questo"+d)
    data=json.loads(d)
    print(data)
    dat=data[oggetto]
    ora=data["data"]
    print("dati"+dat)
    allarme=0
    if sensore=="1":
        ide=1
        if float(dat)>float(1000):
            allarme=1
            
    else:
        if float(dat)>float(100):
            allarme=1
            
        ide=2
    username="g4"
    pw="database"
    host="80.210.122.172"
    db="g4"
    try:
        connessione=p.connect(host,username,pw,db)
        cursor=connessione.cursor(p.cursors.DictCursor)
        query="Insert into Telemetria(valore,data,allarme,Cods) values('"+dat+"','"+ora+"','"+str(allarme)+"','"+str(ide)+"')"
        cursor.execute(query)
        connessione.commit()
        tabella=cursor.rowcount
        print(str(tabella))
        if tabella==1:
            print(str(tabella))
        else:
    	    print("Error")
    except Exception as r:
        print(str(r))
        print("Error")
   
def make_password(password, salt):
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=salt,
                iterations=100000,
                backend=default_backend()
            )
            return base64.urlsafe_b64encode(kdf.derive(password))	

    
    

def inizio():
    
    message = """<!DOCTYPE html>
<html lang="it">
    <head>
        <title>Brugin Company</title>
        <meta charset="utf8">
        <meta name="viewport" content="width= device-width", initial-scale=1 , maxinum-scale=1>
        <link rel="icon" href="Senza_titolo.png">
		<meta http-equiv="refresh" content="3">
  
     <style>
        .button {
  transition-duration: 0.4s;
  box-shadow: 0 8px 16px 0 rgba(0,0,0,0.2), 0 6px 20px 0 rgba(0,0,0,0.19);
  border-radius: 15px;
  
}
.button:active {
  background-color: orange;
  box-shadow: 0 5px #666;
  transform: translateY(4px);
  
  }
.button:hover{ background-color: orange; /* Green */
  color: white;
   -webkit-transition: width 0.4s ease-in-out;
  transition: width 0.4s ease-in-out;
  box-shadow: 0 12px 16px 0 rgba(0,0,0,0.24), 0 17px 50px 0 rgba(0,0,0,0.19);
}
body {
    overflow: hidden;
}

#startLoader {
    background-image: url(index.gif);
    background-repeat: no-repeat;
    background-position: center center;
    background-color: #fff;
    text-align: center;
    position: fixed;
    top: 0;
    right: 0;
    bottom: 0;
    left: 0;
    z-index: 100000;
}
.buttons {
	position: relative;
	margin: 0 auto 20px auto;
	padding: 20px;
	float: left;
	display: block;
	background-color: #eee;
	border-radius: 4px;
}
.buttons:after {
	top: 100%;
	left: 50%;
	border: solid transparent;
	content: " ";
	height: 0;
	width: 0;
	position: absolute;
	pointer-events: none;
	border-color: rgba(238, 238, 238, 0);
	border-top-color: #eee;
	border-width: 10px;
	margin-left: -10px;
}
.button {
	padding: 10px 20px;
	font-weight: bold;
	letter-spacing: 5px;
	outline: none;
	cursor: pointer;
	color: white;
	background-color: #7F8C8D;
	border: none;
	border-radius: 4px;
}
#play-button {
	background-color: #2ECC71;
}
#play-button:hover {
	background-color: #27AE60;
}
#pause-button {
	background-color: #E67E22;
}
#pause-button:hover {
	background-color: #D35400;
}
#stop-button {
	background-color: #E74C3C;
}
#stop-button:hover {
	background-color: #C0392B;
}
#pause-button,
#stop-button {
	margin-left: 15px;
}

</style>
    </head>
    <body  style ="margin: 0;
    padding: 0;
    width: 100%;
    height: 100%;" >
  
  
         <div style="background-color:white;vertical-align: middle;  ; width: 100%; height: 100%;position:absolute;">
            <div style =" margin:auto; width:50%; ">
       		<h1 style ="  display:flex; ">Tabella misure CO2</h1>
            <h2 style="vertical-align:middle; "> La tabella &egrave; ordinata in senso crescente, secondo la data di emissione dati</h2>
          
		  <br>"""
    username="g4"
    pw="database"
    host="80.210.122.172"
    db="g4"
    print("------esco i dati !!------ ")#debug
    try:
        connessione=p.connect(host,username,pw,db)
        cursor=connessione.cursor(p.cursors.DictCursor)
        query="Select * from Telemetria where Cods=1 order by data desc limit 0,15 "
        cursor.execute(query)
        tabella=cursor.fetchall()
        connessione.close()
        a=cursor.rowcount
        ThreadLock = threading.Lock()
        ThreadLock.acquire()
        f = open('primo.html','w')
        if a==0:
            print("Nessun cliente presente")
            f.write(message)
            f.write("""<h2>Nessun dato presente</h2>""")
            f.close()
        else:
            f.write(message)
            f.write("""<table style="width:100%; text-align:center;"border=1>
                        <tr>
                        <td>Data</td>
                        <td>valore</td>
                        </tr>""")
            for i in tabella:
                a=i["valore"]
                b=i["data"]
                f.write("""
                            <tr>
                            <td>"""+str(b)+"""</td>
                            <td>"""+str(a)+"""</td>
                            </tr>""")
            f.write("""</table><br>""") 
            f.close() 
            ThreadLock.release()
            
    except Exception as e :
        print(str(e))
        print("Error")
        connessione.close()
def vai():
    
    message = """<!DOCTYPE html>
<html lang="it">
    <head>
        <title>Brugin Company</title>
        <meta charset="utf8">
        <meta name="viewport" content="width= device-width", initial-scale=1 , maxinum-scale=1>
        <link rel="icon" href="Senza_titolo.png">
		<meta http-equiv="refresh" content="3">
  
     <style>
        .button {
  transition-duration: 0.4s;
  box-shadow: 0 8px 16px 0 rgba(0,0,0,0.2), 0 6px 20px 0 rgba(0,0,0,0.19);
  border-radius: 15px;
  
}
.button:active {
  background-color: orange;
  box-shadow: 0 5px #666;
  transform: translateY(4px);
  
  }
.button:hover{ background-color: orange; /* Green */
  color: white;
   -webkit-transition: width 0.4s ease-in-out;
  transition: width 0.4s ease-in-out;
  box-shadow: 0 12px 16px 0 rgba(0,0,0,0.24), 0 17px 50px 0 rgba(0,0,0,0.19);
}
body {
    overflow: hidden;
}

#startLoader {
    background-image: url(index.gif);
    background-repeat: no-repeat;
    background-position: center center;
    background-color: #fff;
    text-align: center;
    position: fixed;
    top: 0;
    right: 0;
    bottom: 0;
    left: 0;
    z-index: 100000;
}
.buttons {
	position: relative;
	margin: 0 auto 20px auto;
	padding: 20px;
	float: left;
	display: block;
	background-color: #eee;
	border-radius: 4px;
}
.buttons:after {
	top: 100%;
	left: 50%;
	border: solid transparent;
	content: " ";
	height: 0;
	width: 0;
	position: absolute;
	pointer-events: none;
	border-color: rgba(238, 238, 238, 0);
	border-top-color: #eee;
	border-width: 10px;
	margin-left: -10px;
}
.button {
	padding: 10px 20px;
	font-weight: bold;
	letter-spacing: 5px;
	outline: none;
	cursor: pointer;
	color: white;
	background-color: #7F8C8D;
	border: none;
	border-radius: 4px;
}
#play-button {
	background-color: #2ECC71;
}
#play-button:hover {
	background-color: #27AE60;
}
#pause-button {
	background-color: #E67E22;
}
#pause-button:hover {
	background-color: #D35400;
}
#stop-button {
	background-color: #E74C3C;
}
#stop-button:hover {
	background-color: #C0392B;
}
#pause-button,
#stop-button {
	margin-left: 15px;
}

</style>
    </head>
    <body  style ="margin: 0;
    padding: 0;
    width: 100%;
    height: 100%;" >
  
  
         <div style="background-color:white;vertical-align: middle;  ; width: 100%; height: 100%;position:absolute;">
            <div style =" margin:auto; width: 50%; height: 100%; ">
       		<h1 style ="  display:flex; ">Tabella misure radioativit&agrave;</h1>
            <h2 style="vertical-align:middle; "> La tabella &egrave; ordinata in senso crescente, secondo la data di emissione dati</h2>
          
		  <br>"""
    username="g4"
    pw="database"
    host="80.210.122.172"
    db="g4"
    print("------esco i dati !!------ ")#debug
    try:
        connessione=p.connect(host,username,pw,db)
        cursor=connessione.cursor(p.cursors.DictCursor)
        query="Select * from Telemetria where Cods=2 order by data desc limit 0,15 "
        cursor.execute(query)
        tabella=cursor.fetchall()
        a=cursor.rowcount
        connessione.close()
        ThreadLock = threading.Lock()
        ThreadLock.acquire()
        f = open('secondo.html','w')
        if a==0:
            print("Nessun cliente presente")
            f.write(message)
            f.write("""<h2>Nessun dato presente</h2>""")
            f.close()
        else:
            
            f.write(message)
            f.write("""<table style="width:100%; text-align:middle;text-align:center; font-size=20px;"border=1>
                        <tr>
                        <td>Data</td>
                        <td>valore</td>
                        </tr>""")
            for i in tabella:
                a=i["valore"]
                b=i["data"]
                f.write("""
                            <tr>
                            <td>"""+str(b)+"""</td>
                            <td>"""+str(a)+"""</td>
                            </tr>""")
            f.write("""</table><br>""") 
            f.close()               
            ThreadLock.release()
    except Exception as e :
        connessione.close()
        print(str(e))
        print("Error")      
def make_password(password, salt):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    return base64.urlsafe_b64encode(kdf.derive(password)) 
def definition():
    system=platform.system()
    if system=="Windows":
        return "cls"
    else:
        return "clear"
def screen():
    b=definition()
    os.system(b)  
print("STart")

inizio()
vai()
open_new_tab("index.html")



screen()
username="g4"
pw="database"
host="80.210.122.172"
db=""
def make_password(password, salt):
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=salt,
                iterations=100000,
                backend=default_backend()
            )
            return base64.urlsafe_b64encode(kdf.derive(password))
        

PASSWORD = b"BrUgIoSeGuGiO"
#
SALT = '9'
SALT_byte = SALT.encode("utf-8")
key = make_password(PASSWORD,SALT_byte)
print(key)
f = Fernet(key)
print(f)
#screen()	
	
try:
    client=m.Client()
    client.on_connect=connect
    client.on_message=message
    client.connect("80.210.122.173",1883,60)	
    client.loop_forever()
except Exception as f :
	print(str(f))
	print("Error")
