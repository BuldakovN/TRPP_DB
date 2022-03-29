
# A very simple Flask Hello World app for you to get started with...

from flask import Flask, request
from dao import DAO
import json

app = Flask(__name__)

db_name = 'students.db'



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


@app.route('/addMessage', methods=['POST'])
def addMessage():
    if request.method != 'POST':
        return 'Error. Post request is needed.'

    try:
        new_message = []
        new_message.append(request.form['Text'])
        new_message.append(request.form['Id'])
        new_message.append(request.form['ToVk'])
        new_message.append(request.form['ToTelegramm'])
    except KeyError:
        return 'KeyError'

    dao = DAO(db_name)
    dao.addToMessages(*new_message)
    return 'success'


@app.route('/newMessages')
def newMessages():
    dao = DAO(db_name)
    messages = dao.getUnsendMessages()
    response = []
    for i in messages:
        d = {}
        d['Id'] = i[0]
        d['Text'] = i[1]
        d['Date'] = i[2]
        d['IdTarget'] = i[3]
        d['ToVk'] = i[4]
        d['ToTelegramm'] = i[5]
        response.append(d.copy())
    return json.dumps(response)


@app.route('/sendMessage', methods=['GET'])
def sendMessage():
    pass


@app.route('/getStudents')
def getStudents():
    dao = DAO(db_name)
    students = dao.getStudentTable()
    return json.dumps(students)


