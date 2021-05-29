from PyQt5.QtWidgets import QApplication, QMainWindow,QTableWidgetItem
from gui import Ui_MainWindow
from PyQt5 import QtCore
from data import *
import sys, csv, re
class MyApp(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.threads = {}
        self.crawl = CrawlTele(self)
        self.ui.pushButton.clicked.connect(self.startWork)
        self.ui.pushButton_2.clicked.connect(self.stopWork)
        self.ui.pushButton_3.clicked.connect(self.exactCSV)
    def startWork(self):
        self.threads[1] = self.crawl
        self.threads[1].listWidgetUpdate.connect(self.updateListWidget)
        self.threads[1].tableWidgetUpdate.connect(self.updateTableWidget)
        self.threads[1].resetRow.connect(self.resetRowPos)
        self.threads[1].start()
        self.ui.setEnableLineEdit()
        self.ui.pushButton.setEnabled(False)
    def stopWork(self):
        self.threads[1].flag = False
        self.threads[1].stop()
        self.ui.setEnableLineEdit(True)
        self.ui.pushButton.setEnabled(True)
        self.ui.pushButton.setText(QtCore.QCoreApplication.translate("MainWindow", "START"))
    def updateListWidget(self,value):
        self.ui.listWidget.addItem(value)
    def resetRowPos(self):
        self.ui.tableWidget.setRowCount(0)
    def updateTableWidget(self,value1,value2):
        rowPosition = self.ui.tableWidget.rowCount()
        self.ui.tableWidget.insertRow(rowPosition)        
        self.ui.tableWidget.setItem(rowPosition,0,QTableWidgetItem(str(value1)))
        self.ui.tableWidget.setItem(rowPosition,1,QTableWidgetItem(str(value2)))
    def exactCSV(self):
        rowPosition = self.ui.tableWidget.rowCount()
        # colPosition = 2
        fileName = re.findall("me/(.*)",str(self.ui.lineEdit_13.text()))[0]
        path = f"{str(fileName)}_chats.csv"
        with open(path,"w",encoding='UTF-8') as f:
            writer = csv.writer(f,delimiter=",",lineterminator="\n")
            writer.writerow(['username','count'])
            for row in range(rowPosition):
                writer.writerow([self.ui.tableWidget.item(row, 0).text(),self.ui.tableWidget.item(row, 1).text()])
if __name__ == "__main__":
    app = QApplication(sys.argv)
    apps = MyApp()
    apps.show()
    sys.exit(app.exec())