#!C:\BeelineProgFiles\python\python.exe


from mako.template import Template
# Импорт модулей для обработки CGI
import cgi, cgitb

# Создание экземпляра FieldStorage
form = cgi.FieldStorage()

# Получение данных из полей
first_name = form.getvalue('first_name')
last_name = form.getvalue('last_name')


mytemplate = Template(filename='template.txt')

print("Content-type: text/html\n\n")
print()
print("Hello :", first_name, last_name)
print("<h2>Привет  %s %s</h2>" % (first_name, last_name))

#print(mytemplate.render(topics=(first_name, last_name)))
print(mytemplate.render(topics=("Python вап GUIs","Python IDEs","Python web scrapers")))