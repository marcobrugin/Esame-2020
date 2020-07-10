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
from primo import *
from secondo import *
import datetime
import os
import time
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
import base64
import sys
import telepot
import MySQLdb as q
from telepot.loop import MessageLoop
import paho.mqtt.client as p
import paho.mqtt.publish as m 
import json
import os
import platform
from random import uniform 
from random import randint 
from threading import Thread
import threading
def azione(msg):
    tipo,chat_type,chat_id=telepot.glance(msg)
    if tipo=="text":	
        commando=msg['text']
        print("Commando: "+str(commando))
        if commando=="/ciao":
            bot.sendMessage(chat_id,str("Buongiorno sono Brugin bot il tuo Bot"))
            bot.sendMessage(chat_id,str("Scrivi /command per avere i comandi "))
        elif commando=="/command":
            bot.sendMessage(chat_id,str("-------Hai selezionato commandi!!!--------"))
            bot.sendMessage(chat_id,str("Scrivi /1 per Visualizzare la co2 !!"))
            bot.sendMessage(chat_id,str("Scrivi /2 per Visualizzare le radioattività!"))
            bot.sendMessage(chat_id,str("Scrivi /3 per Visualizzare entrambe!!"))
        elif commando=="/1":
            Primo()
            
                
            sensore("1",randint(5,10),"kyQkPRHxzd7Cp0DkLbXw",chat_id)
        elif commando=="/2":
            Secondo()  
            sensore("2",randint(5,10),"EYm5oo1RnMrBmiOO9E2C",chat_id)
        elif commando=="/3":
            Primo()
            sensore("1",randint(5,10),"kyQkPRHxzd7Cp0DkLbXw",chat_id)
            Secondo()
            sensore("2",randint(5,10),"EYm5oo1RnMrBmiOO9E2C",chat_id)
        else:
            print("Commando non assegnato!!!")
            bot.sendMessage(chat_id,str("Commando non assegnato, scrivi /ciao!!!"))		
    else:
        print("------------Not string!!!!!!!!!!--------------")
	

class sensore(Thread):
    def __init__(self,nome,a,token,ide):
        Thread.__init__(self)
        self.sensore=nome
        self.intervallo=a
        self.token=token
        self.ide=ide
        self.start()
    def run(self):
        ThreadLock = threading.Lock()
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
        
        thing="demo.thingsboard.io"
        min=0
        max=0
        if self.sensore=="1":
            oggetto='CO2'
            min=900
            max=1200
        else:
            oggetto='Radioattivita'
            min=80
            max=110
        dati={oggetto :0}
        date={oggetto :"","data": ""}
        pausa=time.time()
        client=p.Client()
        client1=p.Client()
        client.username_pw_set(self.token)
        client1.connect("80.210.122.173",1883,60)
        client.connect(thing,1883,60)
        client.loop_start()
        
        
        try:
            for i in range (0,15):
                t=round(uniform(min,max),2)
                #giorno=datetime.datetime.now().strftime("%d/%m/%Y,%H:%M:%S")
                giorno=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                dati[oggetto]=t
                #print(dati[oggetto])
                client.publish('v1/devices/me/telemetry', json.dumps(dati), 1)
                f = Fernet(key)
                print(f.encrypt(str(t).encode("utf-8")))#debug
                date[oggetto]=str(f.encrypt(str(t).encode("utf-8")))
                a=date[oggetto][1:].encode("utf-8")#debug
                date[oggetto]=str(t)
                date["data"]=giorno
                a=str(f.encrypt(json.dumps(date).encode("utf-8")))
                b=a[1:].encode("utf-8")#debug
                c=f.decrypt(b)#debug
                d=c.decode(encoding = 'utf-8')#debug
                print("questo"+d)#debug
                """
                print(a)
                b=f.decrypt(a)
                print("decriptato"+str(b[1:]))
                """
                client1.publish("Esame2020/Brugin_M/"+self.sensore+"/"+oggetto+"/", a.encode(), 1)
                #client1.publish("Esame2020/Brugin_M/"+self.sensore+"/"+oggetto+"/", json.dumps(date).encode(), 1)
                #m.single("Esame2020/Brugin/"+self.sensore+"/",str(dati[oggetto]).encode(),hostname="80.210.122.173")
                
                ThreadLock.acquire()
                if os.path.isfile(self.sensore+".txt"):
                    r=open(self.sensore+".txt","r")
                    c=r.readlines()
                    r.close()
                    m=open(self.sensore+".txt","w")
                    for i in c:
                        m.write(i)
                        m.flush()
                    s=self.sensore+"#"+str(t)+"#"+giorno+"#"+"\n"
                    m.write(s)
                    m.flush()
                    m.close()
                else:
                    m=open(self.sensore+".txt","w") 
                    s=self.sensore+"#"+str(t)+"#"+giorno+"#"+"\n"
                    m.write(s)
                    m.flush()
                    m.close()
                ThreadLock.release()
                pausa+=self.intervallo
                if pausa-time.time()>0:
        	        time.sleep(pausa-time.time())
        except Exception as e:
            print(str(e))
            client.loop_stop()
            client.disconnect()
            
        client.loop_stop()
        client.disconnect()
def definition():
    system=platform.system()
    if system=="Windows":
        return "cls"
    else:
        return "clear"
def screen():
    b=definition()
    os.system(b)
print("Strat")
TOKEN="1071297564:AAFJ9OH9WaNsPWsw_hnqmnmegnj3fs_qRmc"
bot=telepot.Bot(TOKEN)
print(bot.getMe())
MessageLoop(bot,azione).run_as_thread()
screen()
while 1:
	time.sleep(15)

