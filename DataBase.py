from Chat import Chat
from Utente import Utente
from dbhelper import DBHelper

class DataBase():
    
    db = DBHelper()
    lista_chat = list()
    chatList = db.get_chat("chat", "ID")
    utents = db.get_chat("utenti", "ID")
    utenti = list()
    clans = list()
    
    for chat_id in chatList:
        chat = Chat()
        chat.chat_id = chat_id
        mex = db.get_items("messaggi", "TESTO", chat_id)
        foto = db.get_items("foto", "TESTO", chat_id)
        chat.messaggi = mex
        chat.foto = foto
        lista_chat.append(chat)
        
    for utente_id in utents:
        utente = Utente()
        coin = db.get_item("utenti", "COIN", utente_id)
        utente.id = utente_id
        utente.coin = coin
        utenti.append(utente)
        
    def addUserName(self, text, id_utente, db):
        for utente in self.utenti:
            if utente.id == id_utente:
                if utente.username == None:
                    utente.username = text
                    db.add_username(text, id_utente)

    def addChat_id(self, chatid, db):
        if(self.chatList.__contains__(chatid)==False):
            self.chatList.append(chatid)
            print("fatto")
            db.add_chat("chat", chatid)
            chat = Chat()
            chat.chat_id = chatid
            self.lista_chat.append(chat)
    
    
    def addMex(self, chatid, mex, db):
        for chats in self.lista_chat:
            if(chats.chat_id == chatid):
                if(chats.messaggi.__contains__(mex)==False):
                    chats.messaggi.append(mex)
                    db.add_item("messaggi", mex, chatid)
                    print("fatto")
                    if len(chats.messaggi) >= 1000:
                        db.delete_items("messaggi", chatid)
                        nuova = chats.messaggi[len(chats.messaggi)//2:]
                        chats.messaggi = nuova
                        break;
                    
                    
    
    def addFoto(self, chatid, file_id, db):
        for chats in self.lista_chat:
            if(chats.chat_id == chatid):
                if(chats.foto.__contains__(file_id)==False):
                    chats.foto.append(file_id)
                    db.add_item("foto", file_id, chatid)
                    if len(chats.foto) >= 500:
                        nuova = chats.foto[len(chats.foto)//2:]
                        chats.foto = nuova
                        break;
                    
    def addUtente(self, id_utente, db, chat_type):
        presente = False
        for utente in self.utenti:
            if utente.id == id_utente:
                presente = True
                utente.mex += 1
                print("mex addato")
                if (utente.mex % 10 == 0) & (chat_type == "supergroup"):
                    utente.coin += 1
                    db.add_utente(id_utente, 1, "COIN")
                    break
        if presente==False:
            utente = Utente()
            utente.id = id_utente
            utente.mex += 1
            self.utenti.append(utente)
            db.add_chat("utenti", id_utente)
            
            
