import re
result = re.match(r'AV', 'AV Analytics Vidhya AV')
print(result)

result = re.split(r'a', 'Analytics')

print(result)



result = re.match(r'AV', 'AV Analytics Vidhya AV')
print (result.group(0))


result = re.split(r'i', 'Analytics Vidhya',maxsplit=1)
print(result)


result = re.sub(r'India', 'the World', 'AV is largest Analytics community of India')
print(result)


text="hello world"
result = re.findall(r'\s(\w{5})', text)
print(result)