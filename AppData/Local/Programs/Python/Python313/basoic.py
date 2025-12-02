"""s = "xyxzwxwyzyww"
result=""
for ch in s:
    if ch not in result:
        result+=ch
print(result)        
s="I love python"
reversed_s=' '.join(s.split()[::-1])
print(reversed_s)
s="xyxzwywzxyw"
result=""
for ch in s:
    if ch not in result:
        result+=ch
print(result)
class BankAccount:
    def __init__(self,owner,balance):
        self.owner=owner
        self.balance=balance

    def deposit(self,amt):
        self.balance+=amt
        return self.balance

    def widthraw(self,amt):
        if amt > self.balanace:
            return "insuffient balance"
        self.balance-=amt
        return self.balance

acc=BankAccount("Mani",1000)
print(acc.deposit(500))
s="bananana"
res=""
for ch in s:
    if ch not in res:
        res+=ch
print(res)        

s="deepika"
freq={}
for ch in s:
    freq[ch]=freq.get(ch,0)+1
print(max(freq , key=freq.get) )


s1,s2="mani","inam"
print(sorted (s1)==sorted (s2))

s="ilamanikandan"
vowels="aeiou"
result=""
for ch in s:
    if ch in vowels:
        result+=ch
print(result)
s="fizz"
for ch in s:
    if s.count(ch)==1:
        print(ch)
        break"""
"""s="********"
for i in range (len(s)):
    for j in range(i+1,len(s)+1):
        print(s[i:j])
lst=[1,2,3,4]
rev=[]
for i in lst:
    rev =[i]+rev
print(rev)"""
class Actor:
    def movie(self):
        print("some movie")
class Vijay(Actor):
    def movie(self):
        print("Ghilli")
class SK (Actor):
    def movie(self):
        print("Amaran")
class Ajith(Actor):
    def movie (self):
        print("Billa")

Vijay().movie()
SK().movie()
Ajith().movie()

class BankAccount:
    def __init__(self,owner,balance=0):
        self.owner=owner
        self.balance=balance
    def widthraw(self,amt):
        self.balance+=amt
        return self.balance
    def deposit(self,amt):
        if self.balance > amt:
            return "insufficient"
        self.balance-=amt
        return self.balance
acc=BankAccount("Mani",1000)
print(acc.deposit(500))
        













    



