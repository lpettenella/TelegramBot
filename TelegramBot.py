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
from Utente import Utente
from dbhelper import DBhelper

bot = telepot.Bot('670588262:AAG069-aIzJwzp6bo8G-H78HvOTgm04eyxs')
dataBase = DataBase()
domande = list()
insulti = list()
insulti.append("stronzo") 
insulti.append("gay")
insulti.append("coglione")
epiteti = list()
epiteti.append("Parli tu")
complimenti = list()
complimenti.append("ti amo")

def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    print(content_type, chat_type, chat_id)
    db = DBhelper()

    dataBase.addChat_id(chat_id, db)
    dataBase.addUtente(msg['from']['id'])
    if(content_type == 'text'):
        dataBase.addMex(chat_id, msg['text'], db)
               
        if(msg['text'] == "ciao"):
            bot.sendMessage(chat_id, "afangul")
            
        if "?" in msg['text']:
            metti = True
            mex = msg['text'].lower()
            for domanda in domande:
                if (domanda.domanda == mex):
                    metti = False
                    r = randint(-1, len(domanda.risposte)-1)
                    if(len(domanda.risposte))>0:
                        bot.sendMessage(chat_id, domanda.risposte[r], reply_to_message_id = msg['message_id'])
                        break
            if(metti):
                domanda = Domanda()
                domanda.domanda = mex
                domande.append(domanda)
                print (domande[0].domanda)
                
        if ("gay" in msg['text']) | ("Gay" in msg['text']):
            for utente in dataBase.utenti:
                if msg['from']['id'] == utente.id:
                    utente.coin+=1
                    break
                
        for insulto in insulti:
                if (insulto in msg['text'].lower()) & (("è" in msg['text'])==False) & (("È" in msg['text'])==False):
                    utenteInsultato = Utente()
                    
        if (msg['text'] == "jjm coin") | (msg['text'] == "Jjm coin"):
            for utente in dataBase.utenti:
                if msg['from']['id'] == utente.id:
                    bot.sendMessage(chat_id,"Hai "+str(utente.coin)+" jjm coin.", reply_to_message_id= msg['message_id'])
                    break;
        
        if msg['text'] == "lista":
            for utente in dataBase.utenti:
                print (utente.id)
                
        if (msg['text'] == "/insulto"):
            if(msg['from']['id'] == 660824842):
                if (insulti.__contains__(msg['reply_to_message']['text'].lower()))==False:
                    insulti.append(msg['reply_to_message']['text'].lower())
            else: 
                bot.sendMessage(chat_id, "Chiedi il permesso a @ermanichino", reply_to_message_id= msg['message_id'])
                
        if (msg['text'] == "/complimento"):
            if(msg['from']['id'] == 660824842):
                if (complimenti.__contains__(msg['reply_to_message']['text'].lower()))==False:
                    complimenti.append(msg['reply_to_message']['text'].lower())
            else: 
                bot.sendMessage(chat_id, "Chiedi il permesso a @ermanichino", reply_to_message_id= msg['message_id'])
                
        if (msg['text'] == "/epiteto"):
            if (msg['from']['id'] == 660824842):
                if (epiteti.__contains__(msg['reply_to_message']['text']))==False:
                    epiteti.append(msg['reply_to_message']['text'])
            else: 
                bot.sendMessage(chat_id, "Chiedi il permesso a @ermanichino", reply_to_message_id= msg['message_id'])  
                
        if (msg['text'] == "addCoin") & (msg['from']['id'] == 660824842):
            for utente in dataBase.utenti:
                if utente.id == 660824842:
                    utente.coin+=1000
                    break
            
        if ('reply_to_message' in msg):
            print ("cacca")
            for domanda in domande:
                if domanda.domanda == msg['reply_to_message']['text'].lower():
                    domanda.addRisp(msg['text'])
                    print (domanda.risposte[0])
                    break
            for insulto in insulti:
                if (insulto in msg['text'].lower()) & (("è" in msg['text'])==False) & (("È" in msg['text'])==False):
                    utenteInsultato = Utente()
                    for utente in dataBase.utenti:
                        if utente.id == msg['reply_to_message']['from']['id']:
                            utenteInsultato = utente
                            if utente.coin >= 300:
                                r = randint(-1, len(epiteti)-1)
                                bot.sendMessage(chat_id, epiteti[r], reply_to_message_id= msg['message_id'])
                        if utente.id == msg['from']['id']:
                            if (utenteInsultato.coin >= 300) & (utente.coin >= 5):
                                utenteInsultato.coin+=5;
                                utente.coin-=5
            if(chat_type == 'supergroup') & (msg['reply_to_message']['from']['id']!=msg['from']['id']): 
                for complimento in complimenti:
                    if (complimento == msg['text'].lower()):
                        for utente in dataBase.utenti:
                            if utente.id == msg['from']['id']:
                                utente.coin+=5
                                break
                               
                    
        
        if((msg['text'] == "rfoto") | (msg['text'] == "Rfoto") | (msg['text'] == "/rfoto")):
            for chat in dataBase.lista_chat:
                if(chat.chat_id == chat_id):
                    if(len(chat.foto)>0):
                        for utente in dataBase.utenti:
                            if (utente.id == msg['from']['id']):
                                if (utente.coin>=2):
                                    utente.coin-=2
                                    r = randint(-1, len(chat.messaggi)-1)
                                    r2 = randint(-1, len(chat.foto)-1)
                                    bot.sendPhoto(chat_id, chat.foto[r2], chat.messaggi[r])
                                    break
                                else:
                                    bot.sendMessage(chat_id, "Non hai abbastanza jjm coin per questa funzione.", reply_to_message_id= msg['message_id'])
                                    break
                    else:
                        bot.sendMessage(chat_id, "Non sono ancora state inviate immagini su questo gruppo.")
                        break
            
    if(content_type == 'photo'):
        file_id = msg['photo'][-1]['file_id']
        dataBase.addFoto(chat_id, file_id)
        
MessageLoop(bot, handle).run_as_thread()

while 1:
    time.sleep(10)