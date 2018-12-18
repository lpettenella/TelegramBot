from Chat import Chat
from Utente import Utente
class DataBase():
    
    lista_chat = list()
    chatList = list()
    utenti = list()

    def addChat_id(self, chatid):
        if(self.chatList.__contains__(chatid)==False):
            self.chatList.append(chatid)
            chat = Chat()
            chat.chat_id = chatid
            self.lista_chat.append(chat)
    
    
    def addMex(self, chatid, mex):
        for chats in self.lista_chat:
            if(chats.chat_id == chatid):
                if(chats.messaggi.__contains__(mex)==False):
                    chats.messaggi.append(mex)
                    if len(chats.messaggi) >= 1000:
                        nuova = chats.messaggi[len(chats.messaggi)//2:]
                        chats.messaggi = nuova
                        break;
                    
                    
    
    def addFoto(self, chatid, file_id):
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
            
            
