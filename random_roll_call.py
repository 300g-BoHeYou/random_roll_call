from os import system
from os.path import isfile
from PySide6.QtWidgets import QApplication,QLabel,QPushButton,QMainWindow,QMessageBox
from PySide6.QtCore import Qt,QTimer
from random import choice

class Main():
    def __init__(self):
        self.setup()
        self.loadNamelist()


    def setup(self):
        

        #初始化窗口
        self.window = QMainWindow()
        self.window.resize(300,300)
        self.window.move(200,200)
        self.window.setWindowTitle("随机点名")

        #初始化点名按钮
        self.pbtn_callroll = QPushButton("点名",self.window)
        self.pbtn_callroll.move(75,200)
        self.pbtn_callroll.resize(150,50)
        self.pbtn_callroll.clicked.connect(self.startCallRoll)

        #初始化点名结果
        self.lb_name = QLabel(self.window)
        self.lb_name.resize(200,40)
        self.lb_name.move(50,50)
        
        self.lb_name.setText("<font size=5>点击下方按钮点名</font>")
        self.timer = QTimer()

    def loadNamelist(self):
        #读取名单
        if isfile("namelist.txt"):
            with open("namelist.txt", "r", encoding="utf-8") as f:
                name_file = f.read()
                
            self.name_list = name_file.split("\n")
            self.names = self.name_list[:]
            
        else:  #名单不存在
            x = open("namelist.txt","x") #创建名单
            x.close()
            QMessageBox.warning(self.window,"名单不存在！","namelist.txt不存在，已自动创建，请填写")
            system(r'notepad namelist.txt')
            self.loadNamelist()
        for n in range(len(self.name_list)):
            if not self.name_list[n]: #空值
                del(self.name_list[n])
        if not self.name_list: #空名单
                QMessageBox.warning(self.window,"名单为空！","名单中没有名字，请将姓名填入namelist.txt")
                system(r'notepad namelist.txt')
                self.loadNamelist()
        
        # print(self.name_list)

    def next_name(self):
        name = choice(self.name_list)
        self.lb_name.setStyleSheet("font-size: 25pt;")
        self.lb_name.setAlignment(Qt.AlignCenter)
        self.lb_name.setText(name)
        # print(self.lb_name.text())
        self.timer.start(100)
        
    def startCallRoll(self):
        if self.name_list:
            self.pbtn_callroll.setText("停止")
            self.pbtn_callroll.clicked.connect(self.finishCallRoll)
            self.pbtn_callroll.clicked.disconnect(self.startCallRoll)
            self.timer.timeout.connect(self.next_name)
            self.timer.start(100)
            
            # print(name) #调试用
        else:
            QMessageBox.information(self.window,"提示","所有人都已回答过，将重新点名")
            self.name_list = self.names
            # print(self.names)

    def finishCallRoll(self):
        self.timer.stop()
        self.pbtn_callroll.clicked.disconnect(self.finishCallRoll)
        self.pbtn_callroll.clicked.connect(self.startCallRoll)
        self.pbtn_callroll.setText("点名")
        name = self.lb_name.text()
        print("name",name)
        self.name_list.remove(name)
        # self.lb_name.setStyleSheet("font-size: 25pt;")
        # self.lb_name.setAlignment(Qt.AlignCenter)
        # self.lb_name.setText(name)

if __name__ == "__main__":
    app = QApplication([])
    window = Main()
    window.window.show()
    app.exec_()