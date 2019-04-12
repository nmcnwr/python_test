import datetime
import re


dd_d5000    = datetime.timedelta(days=5000)
dd_d10000   = datetime.timedelta(days=10000)


gg=[]
print(gg)
gg.append(datetime.date(1975,8,29))
gg.append(datetime.date(1975,8,16))
gg.append(datetime.date(2001,3,21))
gg.append(datetime.date(2013,6,6))
print(gg)

for n in gg:
    print(n,n+dd_d5000,n+dd_d10000)






my_today    = datetime.date.today()
my_birthday = datetime.date(1975,8,29)
my_delta    = datetime.timedelta(days=30)

my_today_plus_my_delta = my_today+my_delta
print(my_today_plus_my_delta)

my_today_minus_my_birthday=my_today-my_birthday

print(my_today_minus_my_birthday)



class Person:
    def __init__(self,fname,lname,birthday):
        self.fname=fname
        self.lname=lname
        self.birthday=birthday
    def age(self):
        fname=self.fname
        lname=self.lname
        birthday=self.birthday


        result = re.findall(r'(\d+)-(\d+)-(\d+)', birthday)



        print(result)

        # now = datetime.datetime.now()
        # then = datetime.datetime(by,bm,bd)

        print("Hello " + fname +" "+lname + ". You were born at "+birthday + ". Your age is:")

hero1 = Person("Paul","Smith","1975-08-29")
hero1.age()

#
#
# d = datetime.datetime(2017, 3, 5, 12, 30, 10)
#
#
# print(d.year)  # 2012
# print(d.month)  # 12
# print(d.day)  # 14
#
# print(d.hour) # 12
# print(d.minute) # 10
# print(d.second) # 10
#
# a = datetime.datetime.today()
# print(a)
#
# b = datetime.datetime.now()
# print(b)
#
# today = datetime.datetime.today()
# print(today.strftime("%Y-%m-%d-%H.%M.%S"))
#
#
# #--------------------------
# now = datetime.datetime.now()
# then = datetime.datetime(1975, 8, 29)
#
# # Кол-во времени между датами.
# delta = now - then
# print(delta.days/365)

