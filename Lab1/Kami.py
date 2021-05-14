import sys, threading,difflib,random,os
from PyQt5 import QtWidgets, QtGui, QtCore
import speech_recognition as sr
from src.KamiInterface import Ui_MainWindow
from src.WeatherInteface import CheckWeather
from src.MusicInterface import PlayMusic
import time

r = sr.Recognizer()
_translate = QtCore.QCoreApplication.translate

# 检测s1和s2的相似度
def similar(s1,s2):
    return difflib.SequenceMatcher(None, s1, s2).quick_ratio()

class myWindow(QtWidgets.QMainWindow,Ui_MainWindow):
    def __init__(self,driverPath):
        super(myWindow, self).__init__()
        self.setupUi(self)
        self.inNote = False  # 标志是否在说明页面
        self.isAct = False  # 标志是否在激活状态
        self.driverPath=str(driverPath) # chromedriver.exe path
        self.setWindowIcon(QtGui.QIcon('../resource/icon/siri.png'))

    # 点击x结束程序
    def closeEvent(self,event):
        os._exit(0)

    def failRecog(self):
        self.helloLabel.setVisible(False)
        self.noteLabel.setVisible(False)
        self.siriFig.setVisible(False)
        self.failLabel.setVisible(True)
        time.sleep(1.2)
        self.failLabel.setVisible(False)
        self.helloLabel.setVisible(True)
        self.noteLabel.setVisible(True)
        self.siriFig.setVisible(True)

    def _recog(self):
        mic = sr.Microphone()
        with mic as source:
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source)
            return audio


    def siriRecog(self):
        print("------------------进入主页面识别函数-------------")
        audio=self._recog()

        global timer
        try:
            com=r.recognize_sphinx(audio) #识别出用户语音命令
        except:
            self.failRecog()
            print("主页面激活语音识别失败！")

            print("准备按照基本流程执行未识别到语音后的siri")
            timer = threading.Timer(2.1, self.siriRecog)  # 之后是2.1s执行一次
            timer.start()
        else:
            self.isAct=True
            print('The statement you said is "{}".'.format(com))
            s=similar(com,"Kami")
            print("similar: {}".format(s))
            if self.inNote==False and s>0.1: # 激活成功
                self.successAwake()
            else: # 激活失败
                self.failAwake()
            timer = threading.Timer(0.1, self.siriRecog)
            timer.start()

            self.isAct=False

    # 唤醒成功后显示提示信息
    # 并在0.1秒后进行语音识别功能
    def successAwake(self):
        self.helloLabel.setVisible(False)
        self.noteLabel.setVisible(False)

        print("激活成功")
        # 结束主页面计时
        global timer
        timer.cancel()

        self.actLabel.setVisible(True)
        self.siriFig.setVisible(True)
        audio=self._recog()

        try:
            com=r.recognize_sphinx(audio) #识别出用户语音命令
        except:
            self.failRecog()
            print("识别失败")
        else:
            print("用户功能调用")
            self.guessLabel.setVisible(True)
            self.siriFig.setVisible(False)
            time.sleep(1.5)

            self.actLabel.setVisible(False)
            self.siriFig.setVisible(False)
            keyWord=com[:4] # 检查命令的前四个字母

            proCom=[similar(keyWord,"play"), similar(keyWord,"chec"),similar(keyWord,"visi")]
            maxPro=max(proCom)
            print(proCom)

            index=2
            if maxPro<0.2:
                print("I guess you want to ...")
                index=random.randint(1,3)
            else:
                index=proCom.index(maxPro)+1

            self.guessLabel.setVisible(False)
            index=2
            if index==1:
                print("I am listening music!")
                if self.driverPath=="":
                    os.startfile(r"../resource/music/Creep-Damien Rice .mp3")
                    self.reply1Label.setText(_translate("MainWindow","Playing Creep"))
                    self.reply1Label.setVisible(True)
                else:
                    songName='creep'
                    if com[4:]:
                        songName=com[4:]
                    self.reply1Label.setText(_translate("MainWindow","Playing "+songName))
                    self.reply1Label.setVisible(True)
                    m=PlayMusic(songName,self.driverPath)
                    m.play()
                time.sleep(4)
                self.reply1Label.setVisible(False)
            if index==2 :
                print("I am check weather of Shanghai!")
                c=CheckWeather("上海")
                report=c.weather()
                print(report)

                self.reply2Label.setVisible(True)
                self.ansLabel.setText(_translate("MainWindow",report))
                self.ansLabel.setVisible(True)

                time.sleep(4)
                self.reply2Label.setVisible(False)
                self.ansLabel.setVisible(False)
            if index==3:
                print("visit bilibili")
                self.reply3Label.setText(_translate("MainWindow","Showing Bilibili"))
                self.reply3Label.setVisible(True)
                os.startfile("https://bilibili.com")
                time.sleep(4)
                self.reply3Label.setVisible(False)

        self.helloLabel.setVisible(True)
        self.noteLabel.setVisible(True)
        self.actLabel.setVisible(False)
        self.siriFig.setVisible(True)

        # 休眠后回到主页面
        print("执行结束功能后执行新一轮的siri")




    # 唤醒失败后显示提示信息
    # 并在2.1 秒后显示初始页面label并且调用识别功能
    def failAwake(self):
        print("激活失败")
        if self.inNote==False:
            self.helloLabel.setVisible(False)
            self.noteLabel.setVisible(False)
            self.failLabel.setVisible(True)
            self.siriFig.setVisible(False)

            # 结束主页面计时
            global timer
            timer.cancel()
            time.sleep(2)

            self.failLabel.setVisible(False)
            self.helloLabel.setVisible(True)
            self.noteLabel.setVisible(True)
            self.siriFig.setVisible(True)

        print("激活失败后执行新一轮的siri识别")


    def mouseDoubleClickEvent(self,event):
        # 激活状态点击无效
        if self.isAct==True:
            return

        self.helloLabel.setVisible(self.inNote)
        self.siriFig.setVisible(self.inNote)
        self.noteLabel.setVisible(self.inNote)

        if self.inNote==True:# 若原本在说明页面，返回主页面
            self.inNote=False
        else: # 进入说明页面
            self.inNote=True

        self.func1Label.setVisible(self.inNote)
        self.func2Label.setVisible(self.inNote)
        self.func3Label.setVisible(self.inNote)
        self.com1Label.setVisible(self.inNote)
        self.com2Label.setVisible(self.inNote)
        self.com3Label.setVisible(self.inNote)


if __name__=="__main__":
    app = QtWidgets.QApplication(sys.argv)
    path="" #chromedriver.exe path
    if len(sys.argv)>1:
        path=sys.argv[1]
    window=myWindow(path)
    window.show()

    timer = threading.Timer(0.2, window.siriRecog)  # 第一次执行0.1s后开始
    timer.start()

    sys.exit(app.exec())
