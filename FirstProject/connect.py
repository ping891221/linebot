import threading
import sqlite3
"""
def w():
    #如果使用者是想要加入航班號碼的話呼叫航班的資料表
    #(先加入航班的資料表)
    #if
    ######
    #如果要改偵測詞從這裡改
    ######
    for
        s=space("g12345")
    #如果使用者是想要加入名字
    #(先加入名字的資料表)
    return s
"""
# 資料庫連接設定
db_connections = threading.local()
def get_db():
    if not hasattr(db_connections, 'connection'):
        db_connections.connection = sqlite3.connect('database.db', check_same_thread=False)
    return db_connections.connection
def get_cursor():
    return get_db().cursor()

def get_and_process_names():
    query = "SELECT name FROM users1"
    cursor = get_cursor()
    cursor.execute(query)
    rows = cursor.fetchall()
    names = []
    for row in rows:
        name = row[0]
        names.append(name)
    print("NAME:",names)
    return names
def get_and_process_numbers():
    query = "SELECT number FROM users2"
    cursor = get_cursor()
    cursor.execute(query)
    rows = cursor.fetchall()
    numbers = []
    for row in rows:
        number = row[0]
        processed_number = space(number)
        numbers.append(processed_number)
    print("NUMBER:",numbers)
    return numbers
#如果使用者是想要加入航班號碼的話呼叫
def space(value):
    #value = str(value)
    vl = ""
    for i in value:
        vl += " " + i
    vl = vl.strip()
    
    return vl

def w():
    numbers = get_and_process_numbers()
    names = get_and_process_names()
    return numbers + names

