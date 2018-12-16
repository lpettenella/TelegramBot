from Chat import Chat
class DataBase():
    
    lista_chat = list()
    chatList = list()

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
    
    def addFoto(self, chatid, file_id):
        for chats in self.lista_chat:
            if(chats.chat_id == chatid):
                if(chats.foto.__contains__(file_id)==False):
                    chats.foto.append(file_id)

