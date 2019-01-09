from dbhelper import DBHelper

class Domanda():
    def __init__(self):
        self.domanda = None
        self.risposte = list()
        
    def addRisp(self, text, id, db):
        if self.risposte.__contains__(text)==False:
            self.risposte.append(text)
            db.add_item("risposte", text, id)
            
