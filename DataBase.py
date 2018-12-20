from Chat import Chat
from Utente import Utente
from dbhelper import DBHelper

class DataBase():
    
    db = DBHelper()
    lista_chat = list()
    chatList = db.get_chat("chat")
    utenti = list()
    
    for chat_id in chatList:
        chat = Chat()
        chat.chat_id = chat_id
        mex = db.get_items("messaggi", "TESTO", chat_id)
        chat.messaggi = mex
        lista_chat.append(chat)

    def addChat_id(self, chatid, db):
        if(self.chatList.__contains__(chatid)==False):
            self.chatList.append(chatid)
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
                    if len(chats.messaggi) >= 1000:
                        nuova = chats.messaggi[len(chats.messaggi)//2:]
                        chats.messaggi = nuova
                        break;
                    
                    
    
    def addFoto(self, chatid, file_id, db):
        for chats in self.lista_chat:
            if(chats.chat_id == chatid):
                if(chats.foto.__contains__(file_id)==False):
                    chats.foto.append(file_id)
                    if len(chats.foto) >= 500:
                        nuova = chats.foto[len(chats.foto)//2:]
                        chats.foto = nuova
                        break;
                    
    def addUtente(self, id_utente):
        presente = False
        for utente in self.utenti:
            if utente.id == id_utente:
                presente = True
                utente.mex += 1
            if utente.mex % 10 == 0:
                utente.coin += 1
                break;
        if presente==False:
            utente = Utente()
            utente.id = id_utente
            utente.mex += 1
            self.utenti.append(utente)
            
            
