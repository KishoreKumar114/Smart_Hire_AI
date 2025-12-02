s = "abcabcadef"
dup = ""
seen = ""

for ch in s:
    if ch in seen and ch not in dup:
        dup += ch
    else:
        seen += ch

print(dup) 
