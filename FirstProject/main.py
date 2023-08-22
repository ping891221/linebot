import speech_recognition
import pyttsx3
from connect import w

def speech(setupword):
    #識別器
    r = speech_recognition.Recognizer()
    #不斷無限循環偵測是否有語音輸入
    while True:

        try:
            #創建麥克風對象來錄製語音輸入
            with speech_recognition.Microphone() as mic:
                #調整環境噪音，duration參數指定調整環境噪音的時間（以秒為單位）
                r.adjust_for_ambient_noise(mic,duration=0.2)
                #識別我們何時開始說話和停止說話
                audio = r.listen(mic)
                #轉換成文字
                text = r.recognize_google(audio,language='en')
                #文本轉換為小寫
                text = text.lower()

                print(f"Recognized {text}")
                for word in setupword:
                    if word in text:
                        print("success")
                        break
                        #就回傳甚麼給硬體
                        #return
        #發生未知錯誤
        except speech_recognition.UnknownValueError as e:
            print(f"Error: {e}")
            r = speech_recognition.Recognizer()
            #重新開始
            continue
        except KeyboardInterrupt:
            print("User interrupted. Exiting...")
            break  # 退出無限循環



def line(data): 
    lineword = []   
    for item in data:
        lineword.append(item) 
    print(lineword)
    speech(lineword)

combined_values = w()
line(combined_values)
