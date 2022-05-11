"""
#Документация для работы с удаленной БД

Все запросы посылаются по адресу:

    http://buldakovn.pythonanywhere.com/метод
"""

from flask import Flask, request
from dao import DAO
import json

app = Flask(__name__)

db_name = 'students.db'


@app.route('/')
def index():
    return "Сервер запущен, для работы ознакомьтесь с документацией"

@app.route('/addStudent', methods=['POST'])
def addStudent():
    """
    ##Добавить студента в таблицу
    На вход поступает POST на адрес **/addStudent** запрос в виде json-объекта вида

        {
            FName: имя студента,
            LName: фамилия студента,
            VkId: id вк студента (0, если отсутствует),
            TelegrammId: id телеграмма студента (0, если отсутствует),
            Group: группа студента (например, ИКБО-02-28)
        }
    """
    try:
        new_student = []
        new_student.append(request.form['FName'])
        new_student.append(request.form['LName'])
        new_student.append(request.form['VkId'])
        new_student.append(request.form['TelegrammId'])
        new_student.append(request.form['Group'])
    except KeyError as e:
        return 'KeyError: ' + e

    dao = DAO(db_name)
    dao.addToStudents(*new_student)
    return 'success'


@app.route('/addMessage', methods=['POST'])
def addMessage():
    """
    ##Добавить новое сообщение
    На вход поступает POST на адрес **/addMessage** запрос в виде json-объекта вида

        {
            Text: текст сообщения,
            TargetId: id студента из таблицы студентов,
            ToVk: 1 если отправить сообщение в ВК. 0 если нет,
            ToTelegramm: 1 если отправить сообщение в Телеграмм. 0 если нет
        }

    В случае успеха возращает сообщение success

    В случае ошибки возвращает сообщение KeyError
    """
    try:
        new_message = []
        new_message.append(request.form['Text'])
        new_message.append(request.form['TargetId'])
        to_vk = request.form['ToVk']
        to_tg = request.form['ToTelegramm']
    except KeyError as e:
        return 'KeyError: ' + e:
    dao = DAO(db_name)
    if to_vk:
        dao.addToMessagesVk(*new_message)
    elif to_tg:
        dao.addToMessagesTelegramm(*new_message)
    dao.addToMessages(*new_message)
    return 'success'


@app.route('/newMessagesVk')
def newMessagesVk():
    """
    ##Получить новые сообщения для ВК
    GET запрос на адрес **/newMessagesVk**

    В качестве ответа возвращается json-объект вида

        [
            {
                Id: id сообщения (понадобится, чтобы отметить его как отправленное),
                Text: текст сообщения,
                Date: дата добавления,
                IdTarget: id студента из таблицы
            },
        ]
    """
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


@app.route('/newMessagesTelegramm')
def newMessagesTelegramm():
    """
    ##Получить новые сообщения для Телеграмма
    GET запрос на адрес **/newMessagesTelegramm**

    В качестве ответа возвращается json-объект вида

        [
            {
                Id: id сообщения (понадобится, чтобы отметить его как отправленное),
                Text: текст сообщения,
                Date: дата добавления,
                IdTarget: id студента из таблицы
            },
        ]
    """
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



@app.route('/messagesVk')
def messagesVk():
    """
    ##Получить все сообщения для ВК
    GET запрос на адрес **/messagesVk**

    В качестве ответа возвращается json-объект вида

        [
            {
                Id: id сообщения
                Text: текст сообщения,
                Date: дата добавления,
                IdTarget: id студента из таблицы
                Sent: флаг отправленного сообщения(0 если не отправлено, иначе 1)
            },
        ]
    """
    dao = DAO(db_name)
    messages = dao.getMessagesVkTable()
    response = []
    for i in messages:
        d = {}
        d['Id'] = i[0]
        d['Text'] = i[1]
        d['Date'] = i[2]
        d['IdTarget'] = i[3]
        d['Sent'] = i[4]
        response.append(d.copy())
    return json.dumps(response)


@app.route('/messagesTelegramm')
def messagesTelegramm():
    """
    ##Получить все сообщения для Телеграмма
    GET запрос на адрес **/messagesTelegramm**

    В качестве ответа возвращается json-объект вида

        [
            {
                Id: id сообщения
                Text: текст сообщения,
                Date: дата добавления,
                IdTarget: id студента из таблицы
                Sent: флаг отправленного сообщения(0 если не отправлено, иначе 1)
            },
        ]
    """
    dao = DAO(db_name)
    messages = dao.getMessagesTelegrammTable()
    response = []
    for i in messages:
        d = {}
        d['Id'] = i[0]
        d['Text'] = i[1]
        d['Date'] = i[2]
        d['IdTarget'] = i[3]
        d['Sent'] = i[4]
        response.append(d.copy())
    return json.dumps(response)


@app.route('/sendMessage', methods=['POST'])
def sendMessage():
    """
    ##Сообщить о том, что сообщение доставлено
    На вход поступает POST запрос на адрес **/sendMessage** в виде json-объекта вида

        {
            Platform: платформа, с которой отправленно сообщение (Vk или Telegramm),
            Id: id сообщения из таблицы соответсвующей платформы
        }

        
    """
    try:
        platform = request.form['Platform']
        Id = request.form['Id']
    except KeyError as e:
        return 'KeyError: ' + e:
    dao = DAO(db_name)
    if platform == "Vk":
        dao.markAsSentVK(Id)
    elif platform == "Telegramm":
        dao.markAsSentTelegramm(Id)
    return 'success'


@app.route('/getStudents')
def getStudents():
    """
    ##Получить всех студентов
    Get-запрос на адрес **/getStudents**.

    В качестве ответа возвращается список json-объектов вида
    
        [
            {
                Id: id студента,
                FName: имя студента,
                LNmae: фамилия студента,
                VkId: id вк студента
                TelegrammId: id телеграмма студента
                Group: группа студента
            },
        ]
    """
    response = []
    dao = DAO(db_name)
    students = dao.getStudentTable()
    for s in students:
        d = {}
        d["Id"] = s[0]
        d["FName"] = s[1]
        d["LName"] = s[2]
        d["VkId"] = s[3]
        d["TelegramId"] = s[4]
        d["Group"] = s[5]
        response.append(d.copy())
    return json.dumps(response)


@app.route('/getStudentById', methods=["POST"])
def getStudentById():
    """
    ## Получить студента по его id
    На вход поступает POST-запрос на адрес **/getStudentById** с json-объектов вида

        {
            Id: id студента
        }

    В качестве ответа возращается json-объект вида

        {
            Id: id студента,
            FName: имя студента,
            LNmae: фамилия студента,
            VkId: id вк студента
            TelegrammId: id телеграмма студента
            Group: группа студента
        }
    """
    try:
        Id = request.form['Id']
    except KeyError as e:
        return 'KeyError: ' + e:
    dao = DAO(db_name)
    student = dao.getStudentById(Id)
    response["Id"] = student[0]
    response["FName"] = student[1]
    response["LName"] = student[2]
    response["VkId"] = student[3]
    response["TelegrammId"] = student[4]
    response["Group"] = student[5]
    return response
    

if __name__ == "__main__":
    app.run()
