import sqlite3

class DBHelper:
    def __init__(self, dbname="bottestt.sqlite"):
        self.dbname = dbname
        self.conn = sqlite3.connect(dbname)

    def setup(self, name):
        stmt = "CREATE TABLE IF NOT EXISTS "+name+" (description text)"
        self.conn.execute(stmt)
        self.conn.commit()

    def add_item(self, tabella, item_text, chat_id):
        stmt = "INSERT INTO "+tabella+" (ID, TESTO) VALUES (?, ?)"
        args = (chat_id, item_text,)
        self.conn.execute(stmt, args)
        self.conn.commit()

    def add_domanda(self, text):
        stmt = "INSERT INTO domande (TESTO) VALUES (?)"
        args = (text, )
        self.conn.execute(stmt, args)
        self.conn.commit()
        
    def add_username(self, username, id):
        stmt = "UPDATE utenti SET USER = ? WHERE ID = "+str(id)
        args = (username, )
        self.conn.execute(stmt, args)
        self.conn.commit()

    def add_chat(self, tabella, chat_id):
        if tabella == "utenti":
            stmt = "INSERT INTO "+tabella+" (ID, COIN) VALUES (?, ?)"
            args = (chat_id, 0, )
        elif (tabella == "insulti") | (tabella == "complimenti"):
            stmt = "INSERT INTO "+tabella+" (TEXT) VALUES (?)"
            args = (chat_id, )
        else:
            stmt = "INSERT INTO "+tabella+" (ID) VALUES (?)"
            args = (chat_id, )

        self.conn.execute(stmt, args)
        self.conn.commit()

    def add_utente(self, id, int, item):
        stmt = "UPDATE utenti SET "+item+" = "+item+" + "+str(int)+" WHERE ID = "+str(id)
        self.conn.execute(stmt)
        self.conn.commit()

    def delete_items(self, tabella, item_text):
        i = 0
        while i<500:
            stmt = "DELETE FROM messaggi WHERE ID = (?)"
            args = (item_text, )
            self.conn.execute(stmt, args)
            self.conn.commit()
            i+=1

    def delete_photo(self, id):
        stmt = "DELETE FROM foto WHERE TESTO = (?)"
        args = (id, )
        self.conn.execute(stmt, args)
        self.conn.commit()

    def get_items(self, tabella, tipo, id):
        stmt = "SELECT "+tipo+" FROM "+tabella+" WHERE ID="+str(id)
        return[x[0] for x in self.conn.execute(stmt)]

    def get_chat(self, tabella, item):
        stmt = "SELECT "+item+" FROM "+tabella
        return[x[0] for x in self.conn.execute(stmt)]

    def get_item(self, tabella, item, id):
        stmt = "SELECT "+item+" FROM "+tabella+" WHERE ID="+str(id)
        cursor= self.conn.cursor()
        cursor.execute(stmt)
        return cursor.fetchone()[0]

    def get_id(self, tabella, item, text):
        stmt = "SELECT "+item+" FROM "+tabella+" WHERE TESTO= (?)"
        args = (text, )
        cursor= self.conn.cursor()
        cursor.execute(stmt, args)
        return cursor.fetchone()[0]

    def get_n(self, id):
        stmt = "SELECT Count(*) FROM messaggi WHERE ID= (?)"
        args = (id, )
        return self.conn.execute(stmt, args)

