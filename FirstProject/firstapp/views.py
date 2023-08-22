import threading
from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from linebot import LineBotApi, WebhookParser, WebhookHandler
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextSendMessage, TextMessage
import sqlite3

# 設置 Channel Access Token
channel_access_token = settings.LINE_CHANNEL_ACCESS_TOKEN  # 從 Django 設定檔中取得 Channel Access Token
line_bot_api = LineBotApi(channel_access_token)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)  # 從 Django 設定檔中取得 Channel Secret
# 資料庫連接設定
db_connections = threading.local()

def get_db():
    if not hasattr(db_connections, 'connection'):
        db_connections.connection = sqlite3.connect('database.db', check_same_thread=False)
    return db_connections.connection

def get_cursor():
    return get_db().cursor()
#推送訊息
def send_push_message(user_id, message):
    try:
        line_bot_api.push_message(user_id, TextSendMessage(text=message))
        print("訊息推播成功！->"+message)
    except Exception as e:
        print("訊息推播失敗，錯誤訊息：", e)
"""
def send_push_message2(user_id, message):
    try:
        line_bot_api.push_message(user_id, TextSendMessage(text=message))
        print("訊息推播成功！->"+message)
    except Exception as e:
        print("訊息推播失敗，錯誤訊息：", e)
"""
#監聽是哪一個用戶並推播他訊息
def listen_terminal_input():
    while True:
        user_input = input("")
        if user_input.lower() == 'exit':
            break
        else:
            user_id = 'U9da5be2998d58f2054320507901301ed'  # 用戶的 Line ID
            send_push_message(user_id, user_input)

# 啟動監聽終端機輸入的線程
terminal_input_thread = threading.Thread(target=listen_terminal_input)
terminal_input_thread.start()

@csrf_exempt
def callback(request):
    if request.method == 'POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')
        
        try:
            events = parser.parse(body, signature)
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()


        
        for event in events:
            if isinstance(event, MessageEvent) and isinstance(event.message, TextMessage):
                print(event.source.user_id)
                print("已接收:"+event.message.text)
                handle_text_message(event)
                """
                print(event.source.user_id)
                print("已接收:"+event.message.text)
                line_bot_api.reply_message(event.reply_token, TextSendMessage("已接收"))
                """    


        # 等待終端機輸入線程結束
        #terminal_input_thread.join()

        return HttpResponse()
    else:
        return HttpResponseBadRequest()
    

# 處理文字訊息事件
def handle_text_message(event):
    user_message = event.message.text
    user_id = event.source.user_id
    data_type = type(user_id)
    print(data_type)
    event_reply_token=event.reply_token

    if user_message == "自訂名字":
        send_push_message(user_id, "請輸入想自訂的名字")
        set_user_status(user_id, "waiting_for_name")
    elif user_message == "自訂號碼":
        send_push_message(user_id, "請輸入想自訂的號碼")
        set_user_status(user_id, "waiting_for_number")
    else:
        user_status = get_user_status(str(user_id))
        if user_status == "waiting_for_name":
            insert_new_data(table="users1",column_name="name", value=user_message)
            send_push_message(user_id, "名字已更新")
            set_user_status(user_id, "active")
        elif user_status == "waiting_for_number":
            insert_new_data(table="users2",column_name="number",value=user_message)
            send_push_message(user_id, "號碼已更新")
            set_user_status(user_id, "active")
        else:
            send_push_message(user_id, "請輸入有效指令")

def insert_new_data(table, column_name,value):
    try:
        query = f"INSERT INTO {table} ({column_name}) VALUES (?)"
        get_cursor().execute(query, (value,))
        get_db().commit()
    except sqlite3.Error as e:
        print("新增資料到資料庫失敗:", e)

# 設定使用者狀態的函式
def set_user_status(user_id, status):
    try:
        connection = get_db()
        cursor = connection.cursor()

        # 確認這個id在status是否存在
        check_query = "SELECT id FROM status WHERE id = ?"
        cursor.execute(check_query, (user_id,))
        existing_user = cursor.fetchone()

        if existing_user:
            # 更新
            update_query = "UPDATE status SET thisid_status = ? WHERE id = ?"
            cursor.execute(update_query, (status, user_id))
        else:
            # 新增
            insert_query = "INSERT INTO status (id, thisid_status) VALUES (?, ?)"
            cursor.execute(insert_query, (user_id, status))

        connection.commit()
    except sqlite3.Error as e:
        print("設定使用者狀態失敗:", e)

# 取得使用者狀態的函式
def get_user_status(user_id):
    try:
        connection = get_db()
        cursor = connection.cursor()
        query = "SELECT thisid_status FROM status WHERE id = ?"
        cursor.execute(query, (user_id,))
        result = cursor.fetchone()
        print(print_status_table())
        print(user_id)
        print(result)
        if result:
            return result[0]
        return None
    except sqlite3.Error as e:
        print("取得使用者狀態失敗:", e)
        return None
    
def print_status_table():
    try:
        connection = get_db()
        cursor = connection.cursor()

        select_query = "SELECT thisid_status FROM status WHERE id = 'U9da5be2998d58f2054320507901301ed'"
        cursor.execute(select_query)
        rows = cursor.fetchall()

        print("Status Table:")
        for row in rows:
            print(f"ID: {row[0]}, Status: {row[0]}")

    except sqlite3.Error as e:
        print("打印資料表失敗:", e)