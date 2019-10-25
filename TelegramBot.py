import telepot
from telepot.loop import MessageLoop
import time
import DataBase
import Chat
import Domanda
import datetime
from Chat import Chat
from DataBase import DataBase
from pprint import pprint
from random import randint
from Domanda import Domanda
from Utente import Utente
from dbhelper import DBHelper
import urllib3

db = DBHelper()
bot = telepot.Bot('670588262:AAG069-aIzJwzp6bo8G-xxxxxxxxxxxxx')
dataBase = DataBase()
domande_L = db.get_chat("domande", "TESTO")
domande_id = db.get_chat("domande", "ID")
domande = list()
insulti = db.get_chat("insulti", "TEXT")
insulti.append("stronzo")
insulti.append("gay")
insulti.append("coglione")
epiteti = db.get_chat("epiteti", "TEXT")
epiteti.append("Parli tu")
complimenti = db.get_chat("complimenti", "TEXT")
complimenti.append("ti amo")
scherzo = False
global giochi
giochi = 0


i=1
for domanda in domande_L:
    domands = Domanda()
    domands.domanda = domanda
    risposte = db.get_items("risposte", "TESTO", i)
    domands.risposte = risposte
    domande.append(domands)
    i+=1

updates = bot.getUpdates(100000001)

if updates:
    last_update_id = updates[-1]['update_id']
    bot.getUpdates(offset=last_update_id+1)

def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    print(content_type, chat_type, chat_id)
    db = DBHelper()
    pprint(msg)


    dataBase.addChat_id(chat_id, db)
    dataBase.addUtente(msg['from']['id'], db, chat_type, msg['from']['username'], msg['from']['first_name'])
    if(content_type == 'text'):
        dataBase.addMex(chat_id, msg['from']['id'], msg['text'], db)

        if ("/ann" in msg['text']) & (msg['from']['id'] == 223772637):
            for chat in dataBase.lista_chat:
                try:
                    bot.sendMessage(chat.chat_id, msg['text'][5:])
                    print("message sent")
                except telepot.exception.BotWasBlockedError:
                    print("user block the bot")

        if('reply_to_message' in msg) & (msg['text'].lower() == "fugo nome"):
            last_name = ""
            if 'last_name' in msg['reply_to_message']['from']:
                last_name = msg['reply_to_message']['from']['last_name']

            bot.sendMessage(chat_id, "si chiama: "+msg['reply_to_message']['from']['first_name']+" "+last_name, reply_to_message_id = msg['message_id'])

        if(msg['text'] == "ciao"):
            bot.sendMessage(chat_id, "afangul")

        if(msg['text'].lower() == "buonanotte"):
            n = randint(0, 6)
            print (n)
            now = datetime.datetime.now()
            print (now)
            if(now.hour >= 18-2) & (now.hour <= 20-2) & (n <= 3):
                bot.sendMessage(chat_id, "mamma mia che poppante ahasha", reply_to_message_id = msg['message_id'])
            elif(now.hour > 20-2) & (now.hour <= 22-2) & (n <= 3):
                bot.sendMessage(chat_id, "di già", reply_to_message_id = msg['message_id'])
            elif(now.hour >= 22-2) & (now.hour <= 2) & (n <= 4):
                bot.sendMessage(chat_id, "buonanotte °^°", reply_to_message_id = msg['message_id'])

        if(msg['text'] == "/start"):
            bot.sendMessage(chat_id, "Ciao, per conoscere tutte le funzionalità di questo bot digita /help")

        if(msg['text'] == "/help"):
            bot.sendMessage(chat_id, "Questo bot è in grado di rispondere ad alcune domande postegli. E possiede alcuni comandi speciali: \n\n» /rfoto o rfoto/Rfoto: manda una foto casuale con didascalia casuale inviate nel gruppo stesso al costo di 2 jjm coin, per rimuovere una foto non gradita rispondere alla stessa digitando il comando /rimuovi \n\n» \"Jjm scherzo\" (in risposta a un utente): al costo di 200 jjm coin farà un bello scherzetto all'utente scelto\n\n» \"jjm coin\": mostrerà i coin che possiedi.\n\nPer conoscere ulteriori informazioni riguardo ai coin premi /help_coin")

        if(msg['text'] == "/help_coin"):
            bot.sendMessage(chat_id, "I coin vengono guadagnati: \n 1 ogni 10 messaggi inviati\n 10 ogni complimento fatto a un utente (premere /complimento per la lista dei complimenti)\n\nI coin vengono persi:\n -50 ogni insulto fatto a un utente VIP (premere /insulto per la lista degli insulti)\n\nSe si vuole donare dei coin a un altro utente basta premere in risposta a un utente /dona seguito da uno spazio e l'importo che si vuole donare. Es: /dona 100\n\nQuando un utente raggiunge 1000 coin diventa Vip, il che significa che verrà difeso dal bot in caso di insulti da parte di altri utenti e guadagnerà 50 coin ad ogni insulto ricevuto, prelevati direttamente dall'utente che lo ha insultato.")

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
                db.add_domanda(mex)
                print (domande[0].domanda)


        for chat in dataBase.lista_chat:
            if(chat.chat_id == chat_id):
                if(chat.gioco == True):
                    for sol in chat.gioco_soluzione:
                        if (sol.lower() in msg['text'].lower()):
                            for utente in dataBase.utenti:
                                if msg['from']['id'] == utente.id:
                                    chat.gioco = False
                                    del chat.gioco_soluzione[:]
                                    #giochi = giochi-1
                                    utente.coin+=50
                                    bot.sendMessage(chat_id, "BRAVO HAI VINTOOO 50 jjm COIN!", reply_to_message_id = msg['message_id'])
                                    db.add_utente_coin(msg['from']['id'], 50, "COIN")
                                    break

        if(msg['text'] == "gioco reset") | (msg['text'] == "/gioco_reset"):
            for chat in dataBase.lista_chat:
                if(chat.chat_id == chat_id):
                    if(chat.gioco == True):
                        chat.gioco = False
                        del chat.gioco_soluzione[:]
                        bot.sendMessage(chat_id, "_gioco resettato_", parse_mode='Markdown')
                        break;
                    else:
                        bot.sendMessage(chat_id, "_nessun gioco in corso_", parse_mode='Markdown')


        for utente in dataBase.utenti:
            if (utente.id == msg['from']['id']) & (utente.scherzo == True):
                utente.mex_scherzo += 1
                if(utente.mex_scherzo >=7):
                    utente.mex_scherzo = 0
                    utente.scherzo = False
                r = randint(-1, len(insulti)-1)
                insulto = insulti[r]
                bot.sendMessage(chat_id, msg['text']+" e sono"+" "+insulto)

        if(("gay" in msg['text']) | ("Gay" in msg['text'])) & (chat_type == "supergroup"):
            for utente in dataBase.utenti:
                if msg['from']['id'] == utente.id:
                    utente.coin+=1
                    db.add_utente_coin(msg['from']['id'], 1, "COIN")
                    break

        if (msg['text'] == "jjm coin") | (msg['text'] == "Jjm coin"):
            for utente in dataBase.utenti:
                if msg['from']['id'] == utente.id:
                    bot.sendMessage(chat_id,"Hai *"+str(utente.coin)+" jjm coin*.", reply_to_message_id= msg['message_id'], parse_mode='Markdown')
                    break;

        if msg['text'] == "lista":
            for utente in dataBase.utenti:
                print (utente.id)


        if (msg['text'] == "/insulto"):
            if ('reply_to_message' in msg):
                if(msg['from']['id'] == 223772637):
                    if (insulti.__contains__(msg['reply_to_message']['text'].lower()))==False:
                        insulti.append(msg['reply_to_message']['text'].lower())
                        db.add_chat("insulti", msg['reply_to_message']['text'].lower())
                else:
                    bot.sendMessage(chat_id, "_Chiedi il permesso a_ @ermanichino", reply_to_message_id= msg['message_id'], parse_mode='Markdown')
            else:
                bot.sendMessage(chat_id, insulti)

        if (msg['text'] == "/complimento"):
            if ('reply_to_message' in msg):
                if(msg['from']['id'] == 223772637):
                    if (complimenti.__contains__(msg['reply_to_message']['text'].lower()))==False:
                        complimenti.append(msg['reply_to_message']['text'].lower())
                        db.add_chat("complimenti", msg['reply_to_message']['text'].lower())
                else:
                    bot.sendMessage(chat_id, "_Chiedi il permesso a_ @ermanichino", reply_to_message_id= msg['message_id'], parse_mode='Markdown')
            else:
                bot.sendMessage(chat_id, complimenti)

        if (msg['text'] == "/epiteto") :
            if ('reply_to_message' in msg):
                if (msg['from']['id'] == 223772637):
                    if (epiteti.__contains__(msg['reply_to_message']['text']))==False:
                        epiteti.append(msg['reply_to_message']['text'])
                        db.add_chat("epiteti", msg['reply_to_message']['text'].lower())
                else:
                    bot.sendMessage(chat_id, "_Chiedi il permesso a_ @ermanichino", reply_to_message_id= msg['message_id'], parse_mode='Markdown')
            else:
                bot.sendMessage(chat_id, epiteti)

        if (msg['text'] == "addCoin") & (msg['from']['id'] == 223772637):
            for utente in dataBase.utenti:
                if utente.id == 223772637:
                    utente.coin+=10000
                    db.add_utente_coin(utente.id, 10000, "COIN")
                    break

        if ('reply_to_message' in msg):
            if('photo' in msg['reply_to_message']):
                if(msg['text']=="/rimuovi"):
                    for chat in dataBase.lista_chat:
                        if chat.chat_id == chat_id:
                            id_foto = msg['reply_to_message']['photo'][-1]['file_id']
                            if(id_foto in chat.foto):
                                chat.foto.remove(id_foto)
                                db.delete_photo(id_foto)
                                bot.sendMessage(chat_id, "_Foto rimossa_", parse_mode='Markdown')
                            else:
                                bot.sendMessage(chat_id, "_Foto già rimossa o non presente_", parse_mode='Markdown')

            elif('animation' in msg['reply_to_message']):
                0
            else:
                for domanda in domande:
                    if domanda.domanda == msg['reply_to_message']['text'].lower():
                        id_d = db.get_id("domande", "ID", msg['reply_to_message']['text'].lower())
                        domanda.addRisp(msg['text'], id_d, db)
                        print (domanda.risposte[0])
                        break
                for insulto in insulti:
                    if (insulto in msg['text'].lower()) & (("è" in msg['text'])==False) & (("È" in msg['text'])==False) & (msg['reply_to_message']['from']['is_bot'] == False):
                        utenteInsultato = Utente()
                        for utente in dataBase.utenti:
                            if utente.id == msg['reply_to_message']['from']['id']:
                                utenteInsultato = utente
                                if utente.coin >= 1000:
                                    r = randint(-1, len(epiteti)-1)
                                    bot.sendMessage(chat_id, epiteti[r], reply_to_message_id= msg['message_id'])
                        if utente.id == msg['from']['id']:
                                if (utenteInsultato.coin >= 1000):
                                    utenteInsultato.coin+=50;
                                    db.add_utente_coin(utenteInsultato.id, 50, "COIN")
                                    if utente.coin < 50:
                                        utente.coin = 0
                                    else:
                                        utente.coin-=50
                                        db.add_utente_coin(utente.id, -50, "COIN")

            if(chat_type == 'supergroup') & (msg['reply_to_message']['from']['id']!=msg['from']['id']) & (msg['reply_to_message']['from']['is_bot']==False):
                for complimento in complimenti:
                    if (complimento == msg['text'].lower()):
                        for utente in dataBase.utenti:
                            if utente.id == msg['from']['id']:
                                utente.coin+=10
                                db.add_utente_coin(utente.id, 10, "COIN")
                                break

            if ("/componi" in msg['text']):
                for chat in dataBase.lista_chat:
                    if(chat.chat_id == chat_id):
                        for utente in dataBase.utenti:
                            if (utente.id == msg['from']['id']):
                                if (utente.coin>=10):
                                    utente.coin-=10
                                    mex = msg['reply_to_message']['text'].lower()
                                    m_words = mex.split()
                                    last_word = m_words[-1]
                                    list_mex = list()
                                    list_one = list()
                                    trovato = False
                                    for message in chat.messaggi:
                                        mess = message.lower()
                                        list_m = mess.split()
                                        if(last_word in list_m) & (len(list_m) > 1) & (mex != mess):
                                            if(list_m[0] == last_word):
                                                list_m.remove(last_word)
                                            list_mex.append(list_m)
                                            trovato = True
                                    if (trovato):
                                        r2 = randint(-1, len(list_mex)-1)
                                        mex1 = list_mex[r2]
                                        mex2 = ""
                                        for m in mex1:
                                            mex2 = mex2 + " " + m
                                        bot.sendMessage(chat_id, ""+mex+""+mex2)
                                        break
                                    elif(trovato == False):
                                        for message in chat.messaggi:
                                            mess = message.lower()
                                            list_m = mess.split()
                                            i = 0
                                            for w in reversed(m_words):
                                                list_m2 = m_words
                                                if(len(m_words)/2):
                                                    if(i == 3):
                                                        break
                                                if(w in list_m) & (len(list_m) > 1) & (mex != mess):
                                                    del list_m2[list_m2.index(w):]
                                                    del list_m[0:list_m.index(w)]
                                                    list_mex.append(list_m)
                                                    list_one.append(list_m2)
                                                    break
                                                i+=1
                                        r1 = randint(-1, len(list_mex)-1)
                                        mex1 = list_one[r1]
                                        mex2 = list_mex[r1]
                                        m1 = ""
                                        for m in mex1:
                                            m1 = m1 + " " + m
                                        m2 = ""
                                        for m in mex2:
                                            m2 = m2 + " " + m
                                        bot.sendMessage(chat_id, ""+m1+""+m2)
                                        break
                                    else:
                                        bot.sendMessage(chat_id, "trovato un cazz o non hai 10 coin")
                                        break


            if ("/dona" in msg['text']) & (msg['text'].__contains__("-") == False):
                num = msg['text'][6:]
                pagato = False
                utentePagante = Utente()
                utentePagato = Utente()
                for utente in dataBase.utenti:
                    if utente.id == msg['from']['id']:
                        if utente.coin >= int(num):
                            pagato = True
                            utentePagante = utente
                        else:
                            bot.sendMessage(chat_id, "Uaglio non hai tutti sti soldi!", reply_to_message_id= msg['message_id'])
                            break
                    if utente.id == msg['reply_to_message']['from']['id']:
                        utentePagato = utente
                if pagato:
                    utentePagante.coin -= int(num)
                    db.add_utente_coin(utentePagante.id, int("-"+num), "COIN")
                    utentePagato.coin += int(num)
                    db.add_utente_coin(utentePagato.id, int(num), "COIN")
                    bot.sendMessage(chat_id, "Hai donato *"+num+" coin* a _"+msg['reply_to_message']['from']['first_name']+"_ con successo.", reply_to_message_id= msg['message_id'], parse_mode='Markdown')

            if(msg['text'] == "jjm scherzo") | (msg['text'] == "Jjm scherzo") :
                utenteInfame = Utente()
                utenteScherzato = Utente()
                for utente in dataBase.utenti:
                    if utente.id == msg['from']['id']:
                        utenteInfame = utente
                    if utente.id == msg['reply_to_message']['from']['id']:
                        utenteScherzato = utente
                if (utenteInfame.coin >= 200) & (utenteScherzato.scherzo == False):
                    utenteInfame.coin -= 200
                    db.add_utente_coin(msg['from']['id'], -200, "COIN")
                    utenteScherzato.scherzo = True
                elif utenteScherzato.scherzo == True:
                    bot.sendMessage(chat_id, "Lascia sto stu puveret che è già sotto scherz!", reply_to_message_id= msg['message_id'])
                else:
                    bot.sendMessage(chat_id, "Non hai abbastanza soldi per sta bravata!", reply_to_message_id= msg['message_id'])

        if((msg['text'] == "rgioco") | (msg['text'] == "Rgioco") | (msg['text'] == "/rgioco")):
            for chat in dataBase.lista_chat:
                if(chat.chat_id == chat_id):
                    if(chat.gioco == False) & (len(chat.mex_gioco)>50):
                        chat.gioco = True
                        #giochi = giochi+1
                        n = 0

                        n = randint(-1, len(chat.mex_gioco)-1)
                        mex = chat.mex_gioco[n]
                        utente_sol = chat.mex_utenti[n]
                        username_utente = db.get_item("utenti", "USERNAME", utente_sol)
                        firstname_utente = db.get_item("utenti", "FIRST_NAME", utente_sol)
                        if (username_utente != None):
                            chat.gioco_soluzione.append(username_utente)
                        chat.gioco_soluzione.append(firstname_utente)
                        bot.sendMessage(chat_id, "*Indovina chi ha mandato il messaggio:*\n\n"+mex+"\n\n_Per rispondere digita il nome/username della persona._", parse_mode='Markdown')
                        #bot.sendMessage(chat_id, username_utente+" "+firstname_utente)
                        break
                    elif(len(chat.mex_gioco)<50):
                        bot.sendMessage(chat_id, "_troppi pochi messaggi per iniziare il gioco..._", parse_mode='Markdown')
                    else:
                        bot.sendMessage(chat_id, "_c'è già un gioco in corso_", parse_mode='Markdown')


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
                                    bot.sendMessage(chat_id, "Non hai abbastanza *jjm coin* per questa funzione.", reply_to_message_id= msg['message_id'], parse_mode='Markdown')
                                    break
                    else:
                        bot.sendMessage(chat_id, "_Non sono ancora state inviate immagini su questo gruppo._", parse_mode='Markdown')
                        break

    if(content_type == 'photo'):
        file_id = msg['photo'][-1]['file_id']
        dataBase.addFoto(chat_id, file_id, db, msg['from']['id'])

MessageLoop(bot, handle).run_as_thread()

while 1:
    time.sleep(10)
