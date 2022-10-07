        
class Compromisso():
    def __init__(self, nome, data, horario, convidados):
        self.nome = nome
        self.data = data
        self.horario = horario
        self.convidados = convidados
        
    def get(self, i):
        if i == "nome":
            return self.nome
        elif i == "data":
            return self.data
        elif i == "horario":
            return self.horario
        elif i == "convidados":
            return self.convidados
      
dictSam = {   
}  
        
thisdict = {
}

thisdict.update({"Sam" : ""})

comp = Compromisso(1,1,1,1)

thisdict["Sam"] = [dictSam]

print(thisdict)

thisdict.update({"Re" : dictSam })
thisdict.update({"Le" : "" })

dictSam.update({1: comp})
dictSam.update({2: comp})

print(thisdict)