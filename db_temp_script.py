import sqlite3

# create sqlLite DB (sqlLite DB is usually a file)
connection = sqlite3.Connection('messaging_system.db')

cursor = connection.cursor()

create_table = "CREATE TABLE IF NOT EXISTS Users (id INTEGER, username text, password text,CONSTRAINT PK_User PRIMARY " \
               "KEY(Id)) "
cursor.execute(create_table)

create_table = "CREATE TABLE IF NOT EXISTS Messages( Id INTEGER NOT NULL,Sender INTEGER NOT NULL,Reciever INTEGER NOT " \
               "NULL,Subject TEXT,Content TEXT, IsReaded INTEGER, CreationDate NUMERIC NOT NULL, CONSTRAINT " \
               "PK_Message PRIMARY KEY(Id), CONSTRAINT FK_Messages_Sender FOREIGN KEY (Sender) REFERENCES Users(Id)," \
               "CONSTRAINT FK_Messages_Reciever FOREIGN KEY (Reciever) REFERENCES Users(Id)); "

cursor.execute(create_table)

connection.commit()
connection.close()
