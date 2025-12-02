
"""class Student:
    def __init__(self,name,marks):
        self.name=name
        self.marks=marks
    def calculate_total(self):
        return sum(self.marks)
    def calculate_average(self):
        return self.calculate_total()/len(self.marks)
    def display_result(self):
        print(f"Name:{self.name}")
        print(f"Marks:{self.marks}")
        print(f"Total:{self.calculate_total()}")
        print(f"Average:{self.calculate_average():.2f}")


student1=Student("Mani",[98,99,100])
student1.display_result()

s="mada"
if s==s[::-1]:
    print("palindrome")
else:
    print("Not palindrome")

s="mani"
for i in range(len(s)):
    for j in range(i+1,len(s)+1):
        print(s[i:j])

a,b=0,1
for i in range(10):
    print(a,end="")
    a,b=b,a+b
def factorial(n):
    if n==1:
        return 1
    else:
        return n * factorial(n-1)
num=int(input("enter a number"))
print("Facorial of",num,"is",factorial(num))

s="mani"
print(s.upper())

text=int(input("Enter a sentence:"))
words=text.split()
longest=max(words,key=len)
print("The Longest Word;",longest)
print("length",longest(len))"""
lst=[20,30,40]
largest=max(lst)
lst.remove(largest)
second_largest=max(lst)
print(second_largest)
lst=[1,1,2,2,3,3,4,]
print(list(set(lst)))
