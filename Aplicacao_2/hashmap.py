from compromisso import *

TAM_MAP = 15

class Node:
    def __init__(self, key, value, ref):
        self.key = key
        self.value = value
        self.ref = ref
        self.next = None

class HashMap:
    def __init__(self, tam):
        self.store = [None for _ in range(tam)]
        
    def get(self, key):
        index = hash(key) & TAM_MAP 
        if self.store[index] is None:
            return None
        n = self.store[index]
        while True:
            if n.key == key:
                return n.value
            else:
                if n.next:
                    n = n.next
                else:
                    return None
                
    def put(self, key, value, id):
        nd = Node(key, value, id)
        index = hash(key) & TAM_MAP 
        n = self.store[index]
        if n is None:
            self.store[index] = nd
        else:
            if n.key == key:
                n.value = value
            else:
                while n.next:
                    if n.key == key:
                        n.value = value
                        return
                    else:
                        n = n.next
                n.next = nd
                
    def del_item(self, key):
        index = hash(key) & TAM_MAP 
        n = self.store[index]
        if n != None:
            self.store[index] = None
        else:
            print("Index não encontrado.")
        
