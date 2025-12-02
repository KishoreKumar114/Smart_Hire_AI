i = 1
while i <= 5:
    print(i)
    i += 1
total=0
for i in range(1,11):
    total+=i
    print(total)
class vehicle:
    def bike(self):
        print("BMW")
    def start(self):
        print("wroom wroom")
v=vehicle()
v.bike()
v.start()
def factorial(n):
    if n == 0 or n == 1:
        return 1
    return n * factorial(n-1)
print(factorial(5))

num=[1,2,2,3,3,5,5,7,7,8]
unique=list(set(num))
print(unique)
d1={"mani"}
d2={"Deepi"}
d1.update(d2)
print(d1)
s="ram"
vowels="a,e,i,o,u"
count=sum(1 for ch in s if ch in vowels)
print(count)       
for i in range(1,51):
    if i%3==0 and i%5!=0:
        print(i,end=" ")
s="hello"
print(s[::-1])
s="madam"
if (s[::-1]):
    print("palindrom")
else:
    print("Not palindrom")
def factorial(n):   
    if n==1:
        return 1
    return n*factorial (n-1)
print (factorial(5))
nums=[1,2,3,4,5]
second_largest= sorted(nums)[-2] 
print("Second largest:",second_largest)
a,b=5,6
b,a=a,b
print(a,b)
num=[1,1,2,2,3,4,4,5,5,6,6]
unique=list(set(num))
print(unique)
text="this is a mani,this is deepi"
words=text.split()
freq={}
for w in words:
    freq[w]=freq.get(0,1)+1
print(freq)
s="hello"
reverse=(s[::-1])
print(reverse)
def factorial (n):
    if n==1:
        return 1
    return n*factorial(n-1)
print(factorial(6))
n = 7
a, b = 0, 1
for _ in range(n):
    print(a, end=" ")
    a, b = b, a+b
sentence="mani ila"
words=sentence.split()
reverse_words=words[::-1]
result=" ".join(reverse_words)
print(result)

    
    

   
    
