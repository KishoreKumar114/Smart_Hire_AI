s="hello"
rev=""
for ch in s:
   rev=ch + rev
print(rev)   
s="sswwrryy"
result=[]
for ch in s:
   if ch not in result:
      result.append(ch)
print(result)
s="madam"
result=(s==s[::-1])
print(result)
s="maass"
for ch in s:
   if s.count(ch)==1:
      print(ch)


s="Deepika"
freq={}
for ch in s:
   freq[ch]=freq.get(ch,0)+1
print(freq)   
