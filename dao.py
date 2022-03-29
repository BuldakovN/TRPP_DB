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

        
    def deleteAll(self):
        f = open(self.__filename, 'w')
        f.close()


    def createTables(self):
        self.__cursor.execute("""
            CREATE TABLE IF NOT EXISTS students(
            Id INT PRIMARY KEY,
            FName TEXT,
            LName TEXT,
            VkId TEXT,
            TelegrammId TEXT,
            GroupName TEXT);""")
        self.__cursor.execute("""
            CREATE TABLE IF NOT EXISTS messages(
            Id INT PRIMARY KEY,
            Text TEXT,
            Date TEXT,
            IdTarget INT,
            ToVk TEXT,
            ToTelegramm TEXT,
            Sent INT);""")
        self.__conn.commit()

        
    def addToMessages(self, Text, IdTarget, ToVk, ToTelegramm):
        self.__cursor.execute("SELECT * FROM messages")
        Id = len(self.__cursor.fetchall())
        message = (Id, Text, time.asctime(), IdTarget, ToVk, ToTelegramm, 0)
        self.__cursor.execute("INSERT INTO messages VALUES(?, ?, ?, ?, ?, ?, ?);",
                              message)
        self.__conn.commit()

        
    def addToStudents(self, FName, LName, VkId, TelegrammId, Group):
        self.__cursor.execute("SELECT * FROM students")
        Id = len(self.__cursor.fetchall())
        student = (Id, FName, LName, VkId, TelegrammId, Group)
        self.__cursor.execute("INSERT INTO students VALUES(?, ?, ?, ?, ?, ?);",
                              student)
        self.__conn.commit()


    def markAsSent(self, MessageId):
        self.__cursor.execute(
            'UPDATE messages SET Sent = 1 WHERE Id = ?;',
            (MessageId,))
        self.__conn.commit()

        
    def getStudentTable(self):
        self.__cursor.execute("SELECT * FROM students")
        result = self.__cursor.fetchall()
        return result


    def getMessagesTable(self):
        self.__cursor.execute("SELECT * FROM messages")
        result = self.__cursor.fetchall()
        return result


    def getUnsendMessages(self):
        self.__cursor.execute("SELECT * FROM messages WHERE Sent = 0")
        result = self.__cursor.fetchall()
        return result


    def getStudentById(self, Id):
        self.__cursor.execute("SELECT * FROM students WHERE Id = ?", (Id,))
        return self.__cursor.fetchone()


    def getMessageById(self, Id):
        self.__cursor.execute("SELECT * FROM messages WHERE Id = ?", (Id,))
        return self.__cursor.fetchone()


    def __del__(self):
        self.__cursor.close()
        self.__conn.close()







  
