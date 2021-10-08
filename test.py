import enum


s = """hello 27\" rims 34" deep"""

print(s)

temp = ""
for i, c in enumerate(s):
    if c == '"':
        temp += '""'
    else:
        temp += c

print(temp)
