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
from dbhelper import DBHelper
from Clan import Clan

db = DBHelper()
bot = telepot.Bot('548040088:AAFs8Y1Msb4367WkDth_HF30hM2j-yXenNQ')
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

i=1
for domanda in domande_L:
    domands = Domanda()
    domands.domanda = domanda
    risposte = db.get_items("risposte", "TESTO", i)
    domands.risposte = risposte
    domande.append(domands)
    i+=1


def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    print(content_type, chat_type, chat_id)
    db = DBHelper()
    pprint(msg)


    dataBase.addChat_id(chat_id, db)
    dataBase.addUtente(msg['from']['id'], db, chat_type)
    if(content_type == 'text'):
        dataBase.addMex(chat_id, msg['text'], db)

        if ("/ann" in msg['text']) & (msg['from']['id'] == 660824842):
            for chat in dataBase.lista_chat:
                bot.sendMessage(chat.chat_id, msg['text'][5:])

        if(msg['text'] == "ciao"):
            bot.sendMessage(chat_id, "afangul")

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


        for utente in dataBase.utenti:
            if (utente.id == msg['from']['id']) & (utente.scherzo == True):
                utente.mex_scherzo += 1
                if(utente.mex_scherzo >=15):
                    utente.mex_scherzo = 0
                    utente.scherzo = False
                r = randint(-1, len(insulti)-1)
                insulto = insulti[r]
                bot.sendMessage(chat_id, msg['text']+" e sono"+" "+insulto)


        if(("gay" in msg['text']) | ("Gay" in msg['text'])) & (chat_type == "supergroup"):
            for utente in dataBase.utenti:
                if msg['from']['id'] == utente.id:
                    utente.coin+=1
                    db.add_utente(msg['from']['id'], 1, "COIN")
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
                if(msg['from']['id'] == 660824842):
                    if (insulti.__contains__(msg['reply_to_message']['text'].lower()))==False:
                        insulti.append(msg['reply_to_message']['text'].lower())
                        db.add_chat("insulti", msg['reply_to_message']['text'].lower())
                else:
                    bot.sendMessage(chat_id, "_Chiedi il permesso a_ @ermanichino", reply_to_message_id= msg['message_id'], parse_mode='Markdown')
            else:
                bot.sendMessage(chat_id, insulti)

        if (msg['text'] == "/complimento"):
            if ('reply_to_message' in msg):
                if(msg['from']['id'] == 660824842):
                    if (complimenti.__contains__(msg['reply_to_message']['text'].lower()))==False:
                        complimenti.append(msg['reply_to_message']['text'].lower())
                        db.add_chat("complimenti", msg['reply_to_message']['text'].lower())
                else:
                    bot.sendMessage(chat_id, "_Chiedi il permesso a_ @ermanichino", reply_to_message_id= msg['message_id'], parse_mode='Markdown')
            else:
                bot.sendMessage(chat_id, complimenti)

        if (msg['text'] == "/epiteto") :
            if ('reply_to_message' in msg):
                if (msg['from']['id'] == 660824842):
                    if (epiteti.__contains__(msg['reply_to_message']['text']))==False:
                        epiteti.append(msg['reply_to_message']['text'])
                        db.add_chat("epiteti", msg['reply_to_message']['text'].lower())
                else:
                    bot.sendMessage(chat_id, "_Chiedi il permesso a_ @ermanichino", reply_to_message_id= msg['message_id'], parse_mode='Markdown')
            else:
                bot.sendMessage(chat_id, epiteti)

        if (msg['text'] == "addCoin") & (msg['from']['id'] == 660824842):
            for utente in dataBase.utenti:
                if utente.id == 660824842:
                    utente.coin+=1000
                    db.add_utente(utente.id, 1000, "COIN")
                    break
                
        if (("/crea_clan" in msg['text']) & (len(msg['text'])>=12)):
            for utente in dataBase.utenti:
                if utente.id == msg['from']['id']:
                    if utente.coin >= 300:
                        utente.coin -= 300
                        db.add_utente(utente.id, -300, "COIN")
                        text = msg['text'][11:]
                        isDisponibile = True
                        for clan in dataBase.clans:
                            if clan.nome == text:
                                isDisponibile = False
                        if(isDisponibile):
                            clanew = Clan()
                            clanew.nome = text
                            utente.clan = text
                            bot.sendMessage(chat_id, "Clan '"+text+"' creato con successo.")
                    else:
                        bot.sendMessage(chat_id, "Non hai abbastanza coin")
                
                            
        if (msg['text'] == "/myclan"):
            for utente in dataBase.utenti:
                if utente.id == msg['from']['id']:
                    if utente.clan != None:
                        bot.sendMessage(chat_id, "Il tuo clan: "+utente.clan, reply_to_message_id=msg['message_id'])
                    else:
                        bot.sendMessage(chat_id, "Non hai ancora un clan.", reply_to_message_id=msg['message_id'])
                
                    

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
                                    db.add_utente(utenteInsultato.id, 50, "COIN")
                                    if utente.coin < 50:
                                        utente.coin = 0
                                    else:
                                        utente.coin-=50
                                        db.add_utente(utente.id, -50, "COIN")

            if(chat_type == 'supergroup') & (msg['reply_to_message']['from']['id']!=msg['from']['id']):
                for complimento in complimenti:
                    if (complimento == msg['text'].lower()):
                        for utente in dataBase.utenti:
                            if utente.id == msg['from']['id']:
                                utente.coin+=10
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
                    db.add_utente(utentePagante.id, int("-"+num), "COIN")
                    utentePagato.coin += int(num)
                    db.add_utente(utentePagato.id, int(num), "COIN")
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
                    db.add_utente(msg['from']['id'], -200, "COIN")
                    utenteScherzato.scherzo = True
                elif utenteScherzato.scherzo == True:
                    bot.sendMessage(chat_id, "Lascia sto stu puveret che è già sotto scherz!", reply_to_message_id= msg['message_id'])
                else:
                    bot.sendMessage(chat_id, "Non hai abbastanza soldi per sta bravata!", reply_to_message_id= msg['message_id'])


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
        dataBase.addFoto(chat_id, file_id, db)

MessageLoop(bot, handle).run_as_thread()

while 1:
    time.sleep(10)