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
        
    def add_chat(self, tabella, chat_id):
        stmt = "INSERT INTO "+tabella+" (ID) VALUES (?)"
        args = (chat_id, )
        self.conn.execute(stmt, args)
        self.conn.commit()
    
    def delete_item(self, tabella, item_text):
        stmt = "DELETE FROM "+tabella+" WHERE description = (?)"
        args = (item_text, )
        self.conn.execute(stmt, args)
        self.conn.commit()
        
    def get_items(self, tabella, tipo, id):
        stmt = "SELECT "+tipo+" FROM "+tabella+" WHERE ID="+str(id)
        args = ("TESTO", )
        return[x[0] for x in self.conn.execute(stmt)]
        
    def get_chat(self, tabella):
        stmt = "SELECT ID FROM "+tabella
        return[x[0] for x in self.conn.execute(stmt)] 
        