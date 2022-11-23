from datetime import date
from datetime import datetime
from datetime import timedelta

import binascii

from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto import Random
from Crypto.Signature import pkcs1_15
        
class Compromisso():
    def __init__(self, nome, data, horario, convidados, convidados_alerta):
        self.nome = nome
        self.data = data
        self.horario = horario
        self.convidados = convidados
        self.convidados_alerta = convidados_alerta
        
    def get(self, i):
        if i == "nome":
            return self.nome
        elif i == "data":
            return self.data
        elif i == "horario":
            return self.horario
        elif i == "convidados":
            return self.convidados
        elif i == "alerta":
            return self.convidados_alerta
        
    def set_alerta(self, i):
        self.convidados_alerta = i
    
dictNomes = {}  
dictRef = {}
