def name(s):
    r=""
    i=0
    while i<len(s):
        if s[i].isdigit():
            r=r+int(s[i])+90
        elif s[i].isalpha():
            if s[i].isupper():
                r=r+s[i].lower()
            else:
                r=r+s[i].upper()
        else:
            r=r+"#"
    return r
s=input("Enter a string")
q= name(s)
print(q)
      
    