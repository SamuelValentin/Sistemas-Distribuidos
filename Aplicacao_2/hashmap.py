class Node:
    def __init__(self, key, value, id):
        self.key = key
        self.value = value
        self.id = id
        self.next = None

class HashMap:
    def __init__(self, tam):
        self.store = [None for _ in range(tam)]
        
    def get(self, key):
        index = hash(key) & 15
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
        index = hash(key) & 15
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

hm = HashMap(14)
hm.put("1", "sachin", "a")
hm.put("2", "sehwag", "a")
hm.put("3", "ganguly", "a")
hm.put("4", "srinath", "a")
hm.put("5", "kumble", "a")
hm.put("6", "dhoni", "a")
hm.put("7", "kohli", "a")
hm.put("8", "pandya", "a")

print(hm.get("1"))
print(hm.get("2"))
print(hm.get("3"))
print(hm.get("4"))
print(hm.get("5"))
print(hm.get("6"))
print(hm.get("7"))
print(hm.get("8"))

