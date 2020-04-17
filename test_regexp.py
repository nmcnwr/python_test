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

# file = 'kpistat_5csv\dwhdb_MSK_202003241000_er_3g_15min.res'
# # (yy, mm, dd, hh) = re.search(r'_(\d{4})(\d{2})(\d{2})(\d{2})', file)
# # print(yy, mm, dd, hh)
#
#
# input_example = 'MSK_202003241000_er_3g_15min'
# # regexp_1 = re.compile(r'(?P<day>\w+) at (?P<time>(\d+):(\d+) (\w+)) on (?P<place>\w+)')
# regexp_1 = re.compile(r'_(?P<yyyy>(\d{4}))(?P<mm>(\d{2}))(?P<dd>(\d{2}))')
# re_match = regexp_1.match(input_example)
# print(list(re_match.groups()))
# print(re_match.group('yyyy'))
# print(re_match.group('mm'))
# print(re_match.group('dd'))


import re

for statement in ("I love Mary",
                  "Ich liebe Margot",
                  "Je t'aime Marie",
                  "Te amo Maria"):

    if m := re.match(r"I love (\w+)", statement):
        print("He loves", m.group(1))

    elif m := re.match(r"Ich liebe (\w+)", statement):
        print("Er liebt", m.group(1))

    elif m := re.match(r"Je t'aime (\w+)", statement):
        print("Il aime", m.group(1))

    else:
        print()

file = r"kpistat_5csv\dwhdb_MSK_202003241000_er_3g_15min.res"
m = re.match(r'(MSK_\d+)', file)
if m:
    print("Date=", m.group(1))



statement ="kpistat_5csv\dwhdb_MSK_202003241000_er_3g_15min.res"
if m := re.match(r".*_(\d{4})(\d{2})(\d{2})(\d{4}).*", statement):
    period1 = m.group(1)+'-'+m.group(2)+'-'+m.group(3)+' '+m.group(4)
    print(period1)
    # yy = m.group(1)
    # mm = m.group(2)
    # dd = m.group(3)
    # time = m.group(4)

m0 = re.match(".*_(\d{4})(\d{2})(\d{2})(\d{4})_.*", statement)
if m0:
    period1_start = m.group(1) + '-' + m.group(2) + '-' + m.group(3) + ' ' + m.group(4)
    print("period1_start", period1_start)



