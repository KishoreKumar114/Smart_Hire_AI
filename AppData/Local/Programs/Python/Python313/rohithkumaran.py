
"""n, fact = 5, 1
for i in range(1, n+1): fact *= i
print(fact)

# recursion
def fact(n): return 1 if n==0 else n*fact(n-1)
print(fact(5))

s="ilamanikandan"
res=""
for ch in s:
    if s.count(ch)==1:
        res+=ch
print((res))

    
s="yxyzxxywyz"
max_char=max(s,key=s.count)
unique=""
for ch in s:
    if ch not in unique:
        unique+=ch
result=max_char+unique.replace(max_char,"")
print(result)

    
s="swiss"
res=""
for ch in s:
    if ch not in res:
        res+=ch

print(max(res))

s1="mani"
s2="inam"
print(sorted(s1)==sorted(s2))

s="madam"
if s==s[::-1]:
    print("palindrome")
else:
    print("not palindrome")

def most_repeated_char(s):
    freq={}
    for ch in  s:
        freq[ch]=freq.get(ch,0)+1
    return max(freq, key=freq.get)
s="banana"
print(most_repeated_char(s))
nums=[1,2,3,4,5]
print(nums[::-1])

def reverse_list(lst):
    rev=[]
    for i in range(len(lst)-1,-1,-1):
        rev.append(lst[i])
    return rev    
print(reverse_list([1,2,3,4,5]))"""

s="ilamanikandan"
vowels="aeiou"
result=""
for ch in s:
    if ch in vowels:
        result+=ch
print(result)
a,b=0,1
for i in range(12):
    print(a,end="")
    a,b=b,a+b    
def factorial(n):
    if num==0:
        return 0
    else:
        return n*factorial(n-1)

num=int(input("enter a number"))
print("Factorial",num,"is",factorial(num))
    
    
    
