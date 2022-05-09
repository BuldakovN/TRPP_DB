import sqlite3
import time
import os.path

class DAO:
    def __init__(self, filename='test.db'):
        self.__filename = filename
        if not os.path.exists(self.__filename):
            f = open(self.__filename, 'w')
            f.close()
        
        self.__conn = sqlite3.connect(self.__filename)
        self.__cursor = self.__conn.cursor() 
        self.createTables()

    # очищение файла
    def deleteAll(self):
        f = open(self.__filename, 'w')
        f.close()


    def createTables(self):
        # таблица студентов
        # Id -- id студента
        # FName -- имя студента
        # LName -- фамилия студента
        # VkId -- id для вк (0 если отсутствует)
        # TelegrammId -- id для телеграмма (0 если отсутствует)
        # GroupName -- название группы
        self.__cursor.execute("""
            CREATE TABLE IF NOT EXISTS students(
            Id INT PRIMARY KEY,
            FName TEXT,
            LName TEXT,
            VkId TEXT,
            TelegrammId TEXT,
            GroupName TEXT);""")
        # таблица сообщений для телеграмма
        # Id -- id сообщения
        # Text -- текст сообщения
        # Date -- дата сообщения
        # IdTarget -- id адресата из таблицы студентов
        # Sent -- флаг отправленного сообщения (0 -- не отправлено, 1 -- отправленно)
        self.__cursor.execute("""
            CREATE TABLE IF NOT EXISTS messagesTelegramm(
            Id INT PRIMARY KEY, 
            Text TEXT,
            Date TEXT,
            IdTarget INT, 
            Sent INT);""")
        # таблица сообщений для ВК
        # Id -- id сообщения
        # Text -- текст сообщения
        # Date -- дата сообщения
        # IdTarget -- id адресата из таблицы студентов
        # Sent -- флаг отправленного сообщения (0 -- не отправлено, 1 -- отправленно)
        self.__cursor.execute("""
            CREATE TABLE IF NOT EXISTS messagesVk(
            Id INT PRIMARY KEY,
            Text TEXT,
            Date TEXT,
            IdTarget INT,
            Sent INT);""")
        self.__conn.commit()


    # добавление нового сообщения в таблицу messageVk
    def addToMessagesVk(self, Text, IdTarget):
        self.__cursor.execute("SELECT * FROM messagesVk")
        Id = len(self.__cursor.fetchall())
        message = (Id, Text, time.asctime(), IdTarget, 0)
        self.__cursor.execute("INSERT INTO messages VALUES(?, ?, ?, ?, ?);",
                              message)
        self.__conn.commit()

    # добавление нового сообщения в таблицу messagesTelegramm
    def addToMessagesVk(self, Text, IdTarget):
        self.__cursor.execute("SELECT * FROM messagesTelegramm")
        Id = len(self.__cursor.fetchall())
        message = (Id, Text, time.asctime(), IdTarget, 0)
        self.__cursor.execute("INSERT INTO messages VALUES(?, ?, ?, ?, ?);",
                              message)
        self.__conn.commit()


    # добавление нового студента
    def addToStudents(self, FName, LName, VkId, TelegrammId, Group):
        self.__cursor.execute("SELECT * FROM students")
        Id = len(self.__cursor.fetchall())
        student = (Id, FName, LName, VkId, TelegrammId, Group)
        self.__cursor.execute("INSERT INTO students VALUES(?, ?, ?, ?, ?, ?);",
                              student)
        self.__conn.commit()


    # отметить сообщение из ВК как отправленное
    def markAsSentVK(self, MessageId):
        self.__cursor.execute(
            'UPDATE messagesVk SET Sent = 1 WHERE Id = ?;',
            (MessageId,))
        self.__conn.commit()


    # отметить сообщение из телеграмма как отправленное
    def markAsSentVK(self, MessageId):
        self.__cursor.execute(
            'UPDATE messagesTelegramm SET Sent = 1 WHERE Id = ?;',
            (MessageId,))
        self.__conn.commit()


    # получить таблицу студентов
    def getStudentTable(self):
        self.__cursor.execute("SELECT * FROM students")
        result = self.__cursor.fetchall()
        return result


    # получить таблицу сообщения для ВК
    def getMessagesVkTable(self):
        self.__cursor.execute("SELECT * FROM messagesVk")
        result = self.__cursor.fetchall()
        return result


    # получить таблицу сообщения для Телеграмма
    def getMessagesTelegrammTable(self):
        self.__cursor.execute("SELECT * FROM messagesTelegramm")
        result = self.__cursor.fetchall()
        return result


    # получить неотправленные сообщения для ВК
    def getUnsendMessagesVk(self):
        self.__cursor.execute("SELECT * FROM messagesVk WHERE Sent = 0")
        result = self.__cursor.fetchall()
        return result


    # получить неотправленные сообщения для Телеграмма
    def getUnsendMessagesTelegramm(self):
        self.__cursor.execute("SELECT * FROM messagesTelegramm WHERE Sent = 0")
        result = self.__cursor.fetchall()
        return result

    # получить студента по id
    def getStudentById(self, Id):
        self.__cursor.execute("SELECT * FROM students WHERE Id = ?", (Id,))
        return self.__cursor.fetchone()


    # получить сообщение по id для ВК
    def getMessageVkById(self, Id):
        self.__cursor.execute("SELECT * FROM messagesVk WHERE Id = ?", (Id,))
        return self.__cursor.fetchone()


    # получить сообщение по id для Телеграмма
    def getMessageTelegrammById(self, Id):
        self.__cursor.execute("SELECT * FROM messagesTelegramm WHERE Id = ?", (Id,))
        return self.__cursor.fetchone()


    def __del__(self):
        self.__cursor.close()
        self.__conn.close()







  
