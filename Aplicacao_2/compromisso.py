from datetime import date
from datetime import datetime
from datetime import timedelta
        
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
    
dictNomes = {}  
dictRef = {}


# data_e_hora_atuais = datetime.now()
# data_e_hora_em_texto = data_e_hora_atuais.strftime("%H:%M")
      
# ---------------------------      
# Using current time
# ini_time_for_now = datetime.now()
# notfica = ini_time_for_now + \
#                         timedelta(minutes = 3)
 
# print('notificao:', str(notfica))
# data_e_hora_em_texto = notfica.strftime("%H:%M")
# print(data_e_hora_em_texto)

# if str(data_e_hora_em_texto) == "12:13":
#     print("LEgal")
 