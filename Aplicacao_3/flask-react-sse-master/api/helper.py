import uuid
import random
# from faker import Faker
# fake = Faker()

lista_users = list()
lista_comps = list()

# def get_data():
#     data = list()
#     for _ in range(10):
#         data.append({'userId': uuid.uuid4(), 'id': random.randrange(1, 100), 'name': fake.name(), 'address': fake.address()})
#     return data

def post_newUser(nome, address):
    
    lista_comps = list()
    lista_users.append({'name': nome, 'address': address, 'compromissos': lista_comps})
    
    id = len(lista_users)
    
    return id

def post_newComp(id, comp):
                                   
    comps = lista_users[id]
    comps.append({comp})
    
    return 0

def post_alerta():
    return 0

def delete_comp(id, comp):
    
    comps = lista_users[id][comp]
    comps.append({comp})
    
    return 0

def delete_alerta():
    return 0

def get_comp(id):
    
    comps = lista_users[id][comps]
    
    return comps

def get_schd_time():
    return random.randrange(5,20)