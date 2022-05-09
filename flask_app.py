from flask import Flask, request
from dao import DAO
import json

app = Flask(__name__)

db_name = 'students.db'

@app.route('/')
def info():
    return "Здесь будет краткое руководство по API"


# добавить студента в таблицу
@app.route('/addStudent', methods=['POST'])
def addStudent():
    if request.method != 'POST':
        return 'Error. Post request is needed.'
    try:
        new_student = []
        new_student.append(request.form['FName'])
        new_student.append(request.form['LName'])
        new_student.append(request.form['VkId'])
        new_student.append(request.form['TelegrammId'])
        new_student.append(request.form['Group'])
    except KeyError:
        return 'KeyError'
    dao = DAO(db_name)
    dao.addToStudents(*new_student)
    return 'success'


# добавить сообщение в таблицы
@app.route('/addMessage', methods=['POST'])
def addMessage():
    if request.method != 'POST':
        return 'Error. Post request is needed.'
    try:
        new_message = []
        new_message.append(request.form['Text'])
        new_message.append(request.form['TargetId'])
    except KeyError:
        return 'KeyError'
    dao = DAO(db_name)
    try:
        if request.form['ToTelegramm']:
            dao.addToMessagesTelegramm(*new_message)
        if request.form['ToVk']:
            dao.addToMessagesTelegramm(*new_message)
    except KeyError:
        return "KeyError"
    return 'success'


# получить новые сообщения для ВК
@app.route('/newMessagesVk')
def newMessages():
    dao = DAO(db_name)
    messages = dao.getUnsendMessagesVk()
    response = []
    for i in messages:
        d = {}
        d['Id'] = i[0]
        d['Text'] = i[1]
        d['Date'] = i[2]
        d['IdTarget'] = i[3]
        response.append(d.copy())
    return json.dumps(response)


# получить новые сообщения для Телеграмма
@app.route('/newMessagesTelegramm')
def newMessages():
    dao = DAO(db_name)
    messages = dao.getUnsendMessagesTelegramm()
    response = []
    for i in messages:
        d = {}
        d['Id'] = i[0]
        d['Text'] = i[1]
        d['Date'] = i[2]
        d['IdTarget'] = i[3]
        response.append(d.copy())
    return json.dumps(response)


# пометить сообщение помеченным
@app.route('/sendMessage', methods=['POST'])
def sendMessage():
    pass


# получить список студентов
@app.route('/getStudents')
def getStudents():
    dao = DAO(db_name)
    students = dao.getStudentTable()
    return json.dumps(students)


