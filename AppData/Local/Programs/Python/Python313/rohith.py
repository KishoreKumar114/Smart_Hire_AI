"""class car:
    def __init__(self,brand,model):
        self.brand=brand
        self.model=model

    def move(self):
        print("drive")
        
class boat:
    def __init__(self,brand,model):
        self.brand=brand
        self.model=model

    def move(self):
        print("float")

class plane:
    def __init__(self,brand,model):
        self.brand=brand
        self.model=model

    def move(self):
        print("fly")

car1=car("BMW","2025")
boat1=boat("shirakh","2023")
for x in (car1,boat1):
    x.move()"""
"""password=""
while password!=("python123"):
    password=("Enter a password:")
    print("Vada ulla")"""
s="ilamanikandan"
max_char=max(s,key=s.count)
unique=""
for ch in s:
    if ch not in unique:
        unique+=ch
result=max_char+unique.replace(max_char,"")
print(result)




