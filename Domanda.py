
class Domanda():
    def __init__(self):
        self.domanda = None
        self.risposte = list()
        
    def addRisp(self, text):
        if self.risposte.__contains__(text)==False:
            self.risposte.append(text)
