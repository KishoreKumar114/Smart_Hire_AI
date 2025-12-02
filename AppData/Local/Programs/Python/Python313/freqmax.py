s="xxyzwyx"
freq={}
for ch in s:
    freq[ch]=freq.get(ch,0)+1
max_char=max(freq,key=freq.get)
unique=""
for ch in s:
    if ch not in unique:
        unique+=ch
result=max_char
for ch in unique:
    if ch !=max_char:
        result+=ch
print(result)    



s = "xxyzxwxwyz"

max_char = max(s, key=s.count)

unique = ""
for ch in s:
    if ch not in unique:
        unique += ch


result = max_char + unique.replace(max_char, "")
print(result)
