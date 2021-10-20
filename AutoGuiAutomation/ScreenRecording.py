import time
import webbrowser
import pyautogui
import json
from datetime import datetime

print("start")


def start():
    a_file = open("orarFacultate.json", "r")
    json_object = json.load(a_file)
    a_file.close()
    while True:
        now = datetime.now()
        for i in json_object["ore"]:
            if int(i["oraIncepere"][0]) == now.hour and int(i["oraIncepere"][1]) == now.minute:
                screenRecord(i["link"])
                time.sleep(10)
                stop()
                break


def stop():
    a_file = open("orarFacultate.json", "r")
    json_object = json.load(a_file)
    a_file.close()
    while True:
        now = datetime.now()
        for i in json_object["ore"]:
            if now.hour == int(i["oraTerminare"][0]) and now.minute == int(i["oraTerminare"][1]):
                terminareOra()
                break
            else:
                pass



def screenRecord(link):
    # run ScreenRecording
    pyautogui.hotkey('winleft', 'd')
    time.sleep(5)
    try:
        pyautogui.doubleClick("obs.png")
    except:
        pyautogui.doubleClick("obsClickedBG.png")

    time.sleep(5)
    pyautogui.getWindowsWithTitle("OBS 27.1.3")[0].maximize()
    time.sleep(5)
    pyautogui.click(1474, 857)
    pyautogui.click(1474, 878)
    time.sleep(2)
    pyautogui.click(1703, 876)
    time.sleep(5)
    # run FakeWebCam

    pyautogui.hotkey('winleft', 'd')
    time.sleep(5)
    try:
        pyautogui.doubleClick("obs.png")
    except:
        pyautogui.doubleClick("obsClickedBG.png")
    time.sleep(5)

    pyautogui.click(1113, 560)
    time.sleep(5)
    pyautogui.click(273, 929)

    pyautogui.click(1474, 836)  # ON FAKEWEBCAM
    pyautogui.click(1474, 857)  # OFF Audio
    pyautogui.click(1474, 878)  # OFF Screen
    pyautogui.click(1720, 896)  # ON virtualWebCamera

    webbrowser.open_new_tab(link)
    time.sleep(10)
    pyautogui.click("LaunchMeeting.png")
    # time.sleep(15)
    # pyautogui.getWindowsWithTitle("Zoom Meeting")[0].maximize()
    time.sleep(20)
    pyautogui.click(174, 985)  # Turn Camera ON


def terminareOra():
    try:
        pyautogui.click(1859, 993)  # buton LeaveChat
        time.sleep(5)
        pyautogui.click(1737, 917)  # buton LeaveChatConfirmation
    except:
        pass

    pyautogui.click("openOBS_AFTER.png")
    time.sleep(5)

    # pyautogui.click(1014,561)
    pyautogui.click(252, 927)  # select from 2 windows
    time.sleep(1)
    pyautogui.click(1474, 857)  # OFF Audio
    time.sleep(1)
    pyautogui.click(1474, 878)  # OFF Screen
    time.sleep(1)
    pyautogui.click(1703, 876)  # TurnOFF record
    time.sleep(1)
    # pyautogui.click(1150, 558)  # Confirmation TurnOFF
    time.sleep(1)
    pyautogui.click(1900, 11)  # exit program

    time.sleep(10)
    pyautogui.click("openOBS_AFTER.png")
    time.sleep(1)
    pyautogui.click(1474, 836)  # OFF FAKEWEBCAM
    time.sleep(1)
    pyautogui.click(1720, 896)  # TurnOFF virtualWebCamera
    time.sleep(1)
    # pyautogui.click(1150, 558)  # Confirmation TurnOFF
    time.sleep(1)
    pyautogui.click(1900, 11)  # exit program

#
# screenRecord("https://zoom.us/j/91230634292?pwd=UVNnazVLNXlUUEd6dlNnUDFYVnhDZz09&fbclid=IwAR3hxQo0ZxI5mLVbK2MGsKKyVZHc5DNxnZuMszMmxZq2-6lpyf64Q5q67BY#success")
# time.sleep(10)
#
# terminareOra()
# start()
# while True:
#     time.sleep(3)
#     print(pyautogui.position())
