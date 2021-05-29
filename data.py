from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSignal, QThread,QCoreApplication
from telethon.sync import TelegramClient
# from telethon import TelegramClient
import csv
from collections import Counter


class CrawlTele(QThread):
    listWidgetUpdate = pyqtSignal(str)
    tableWidgetUpdate = pyqtSignal([int,int])
    resetRow = pyqtSignal()
    def __init__(self,args):
        QThread.__init__(self)
        self.args = args
        self.api_id = self.args.ui.lineEdit_11.text()
        self.api_hash = self.args.ui.lineEdit_12.text()
        self.phone = self.args.ui.lineEdit_15.text()
        self.chat = self.args.ui.lineEdit_13.text()
    def run(self):
        self.api_id = self.args.ui.lineEdit_11.text()
        self.api_hash = self.args.ui.lineEdit_12.text()
        self.phone = self.args.ui.lineEdit_15.text()
        self.chat = self.args.ui.lineEdit_13.text()
        # api_id = 5861698
        # api_hash = '4b4ccb3c3cf5db0501f8c4679d731b60'
        # phone = '+84393856999'
        # client = TelegramClient(phone, api_id, api_hash)
        client = TelegramClient(self.phone, self.api_id, self.api_hash)
        client.connect()
        self.args.ui.pushButton.setText(QCoreApplication.translate("MainWindow", "Continue"))
        if not client.is_user_authorized():
            client.send_code_request(self.phone)
            self.args.ui.lineEdit_14.setEnabled(True)
            self.args.ui.pushButton.setEnabled(True)
            self.flag = True
            while self.flag:
                if (self.args.ui.pushButton.isChecked()) or self.args.ui.pushButton_2.isChecked():
                    self.args.ui.lineEdit_14.setEnabled(False)
                    self.flag = False
            
            client.sign_in(self.phone, int(self.args.ui.lineEdit_14.text()))
        client.start()
        self.args.ui.lineEdit_14.setEnabled(False)
        self.args.ui.pushButton.setText(QCoreApplication.translate("MainWindow", "Starting"))
        # chat = "https://t.me/LinkCacc"
        # chat = 1244930062
        # count = 0
        arr = []
        for message in client.iter_messages(self.chat, reverse=True):
            # count+=1
            # if count > 1000:
            #     break
            arr.append(message.sender_id)
            self.listWidgetUpdate.emit(f"{message.sender_id} : {message.text}")
            a = Counter(arr)
            QtCore.QThread.msleep(100)
            # self.resetRow.emit()
            self.args.ui.tableWidget.setRowCount(0)
            for item in a:
                self.tableWidgetUpdate.emit(item,a[item])
        self.args.ui.pushButton.setText(QCoreApplication.translate("MainWindow", "Done"))
        self.exec_()
    def stop(self):
        self.terminate()