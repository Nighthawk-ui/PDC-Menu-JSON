import re

mystring = "hi 321 !  || 67322  9.22"

list = re.findall(r"\d+", mystring)

print(list)
