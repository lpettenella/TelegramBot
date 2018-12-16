import telepot
from telepot.loop import MessageLoop
import time
import DataBase
import Chat
import Domanda
from Chat import Chat
from DataBase import DataBase
from pprint import pprint
from random import randint
from Domanda import Domanda

bot = telepot.Bot('670588262:AAG069-aIzJwzp6bo8G-H78HvOTgm04eyxs')
dataBase = DataBase()
domande = list()

def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    print(content_type, chat_type, chat_id)
    pprint (msg)

    dataBase.addChat_id(chat_id)
    if(content_type == 'text'):
        dataBase.addMex(chat_id, msg['text'])
        if(msg['text'] == "lista"):
            for chat in dataBase.lista_chat:
                print ("heibhyh")
               
        if(msg['text'] == "ciao"):
            bot.sendMessage(chat_id, "afangul")
            
        if "?" in msg['text']:
            metti = True
            for domanda in domande:
                if domanda.domanda == msg['text']:
                    metti = False
                    r = randint(-1, len(domanda.risposte)-1)
                    bot.sendMessage(chat_id, domanda.risposte[r], reply_to_message_id = msg['message_id'])
                    break;
            if(metti):
                domanda = Domanda()
                domanda.domanda = msg['text']
                domande.append(domanda)
                print (domande[0].domanda)
            
        if 'reply_to_message' in msg:
            for domanda in domande:
                if domanda.domanda == msg['reply_to_message']['text']:
                    domanda.risposte.append(msg['text'])
                    print (domanda.risposte[0])
                    
        
        if((msg['text'] == "rfoto") | (msg['text'] == "Rfoto")):
            for chat in dataBase.lista_chat:
                if((chat.chat_id == chat_id) & (len(chat.foto)>0)):
                    r = randint(-1, len(chat.messaggi)-1)
                    r2 = randint(-1, len(chat.foto)-1)
                    bot.sendPhoto(chat_id, chat.foto[r2], chat.messaggi[r])
            
    if(content_type == 'photo'):
        file_id = msg['photo'][-1]['file_id']
        dataBase.addFoto(chat_id, file_id)
        
MessageLoop(bot, handle).run_as_thread()

while 1:
    time.sleep(10)