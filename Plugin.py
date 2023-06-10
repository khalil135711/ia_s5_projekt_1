import os.path
import pickle
import pandas as pd
import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from Writer import Writer



class ExcelProcessor:

    def replaceNaN(self,data_frame):
        for columnName in data_frame.columns:
            sommeNan = data_frame[columnName].isnull().sum()
            if (sommeNan != 0):
                mean = pd.to_numeric(data_frame[columnName], errors='coerce').mean()
                data_frame[columnName] = data_frame[columnName].fillna(mean)
        return data_frame

    def cleanData(self,data_frame):
        for columnName in data_frame.columns:
            for index in range(len(data_frame[columnName])):
                formated_str = str(data_frame[columnName][index]).replace(",", ".")
                data_frame[columnName].iloc[index] = formated_str
        return data_frame

    def __init__(self,fileName):

        drop_columns_table = ['dernier_WindDirection[deg]','moy_WindDirection[deg]','Date/heure','ETP quotidien [mm]']

        try:
            self.fileName = fileName
            data_frame = pd.read_excel(self.fileName)

            #Drop Features
            for to_drop in drop_columns_table:
                if to_drop in data_frame.columns:
                    data_frame = data_frame.drop(to_drop, axis=1)
            data_frame = self.replaceNaN(data_frame)
            self.data_frame = self.cleanData(data_frame)
        except:
            raise ValueError("[ - ] - File incompatible")
    def get_data(self):
        XPredict = self.data_frame.to_numpy()

        data = {
            "columns":self.data_frame.columns,
            "data":XPredict
        }

        return data

    def save(self,data,columns,output="output.xlsx"):
        new_data = pd.DataFrame(data,columns=columns)
        new_data.to_excel(output, sheet_name='Sheet1')
        return output

class AIPredict:
    def __init__(self):
        self.model = pickle.load(open("models/mymodel.pckl","rb"))

    def predict(self,X):
        return self.model.predict(X)


class Ui_MainWindow(object):
    def __init__(self,model:AIPredict):
        self.model = model
        self.writer = Writer()

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(821, 615)
        MainWindow.setStyleSheet("background-color:qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(255, 178, 102, 255), stop:0.55 rgba(235, 148, 61, 255), stop:0.98 rgba(0, 0, 0, 255), stop:1 rgba(0, 0, 0, 0))")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.fileLocation = QtWidgets.QTextEdit(self.centralwidget)
        self.fileLocation.setGeometry(QtCore.QRect(10, 220, 581, 41))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.fileLocation.setFont(font)
        self.fileLocation.setStyleSheet("background-color:rgb(255, 255, 255)")
        self.fileLocation.setObjectName("fileLocation")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(80, 300, 631, 51))
        font = QtGui.QFont()
        font.setFamily("Algerian")
        font.setPointSize(18)
        self.pushButton.setFont(font)
        self.pushButton.setStyleSheet("background-color:rgb(255, 255, 255)")
        self.pushButton.setObjectName("pushButton")
        self.statusFixed = QtWidgets.QLabel(self.centralwidget)
        self.statusFixed.setGeometry(QtCore.QRect(80, 400, 81, 31))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.statusFixed.setFont(font)
        self.statusFixed.setStyleSheet("background-color:rgb(255, 255, 255)")
        self.statusFixed.setObjectName("statusFixed")
        self.statusPrinter = QtWidgets.QLabel(self.centralwidget)
        self.statusPrinter.setGeometry(QtCore.QRect(180, 400, 481, 31))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(16)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.statusPrinter.setFont(font)
        self.statusPrinter.setStyleSheet("background-color:rgb(255, 255, 255)")
        self.statusPrinter.setText("")
        self.statusPrinter.setObjectName("statusPrinter")
        self.browseButton = QtWidgets.QPushButton(self.centralwidget)
        self.browseButton.setGeometry(QtCore.QRect(600, 220, 171, 41))
        
        font = QtGui.QFont()
        font.setFamily("Algerian")
        font.setPointSize(18)
        self.browseButton.setFont(font)
        self.browseButton.setStyleSheet("background-color:rgb(255, 255, 255)")
        self.browseButton.setObjectName("browseButton")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)


        # If you want to replace design copy this to your new code
        self.browseButton.clicked.connect(self.getfiles)
        self.pushButton.clicked.connect(self.processExcel)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "Predict"))
        self.statusFixed.setText(_translate("MainWindow", "Status"))
        self.browseButton.setText(_translate("MainWindow", "Browse"))




        
    # If you want to replace design copy this to your new code
    def getfiles(self):
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(None, 'Single File', '', '*.xlsx')
        self.fileLocation.setText(fileName)

    def processExcel(self):
        fileName = self.fileLocation.toPlainText()
        try:
            if not os.path.exists(fileName):
                raise ValueError("[ - ] - File Not found")

            self.writer.writeSuccess("[ + ] - Processing the file")
            excelProcessor = ExcelProcessor(fileName)
            dictionary = excelProcessor.get_data()

            XData = dictionary['data']
            columns_of_feature = dictionary['columns']

            yPredict = self.model.predict(XData)
            newTable = np.column_stack((XData,yPredict))
            fileName = excelProcessor.save(newTable,np.append(columns_of_feature,"ETP Quotidien"),"predictions.xlsx")

            status = f"Datapredicted in the name {fileName}"
            self.writer.writeSuccess("[ + ] - File Processed")
        except ValueError as e:
            error_string = str(e)
            self.writer.writeError(error_string)
            status = error_string

        self.statusPrinter.setText(status)








def launch(aiPredicter: AIPredict):
    app = QtWidgets.QApplication(sys.argv)
    windows = QtWidgets.QMainWindow()
    diabete = Ui_MainWindow(aiPredicter)
    diabete.setupUi(windows)
    diabete.retranslateUi(windows)
    windows.show()
    sys.exit(app.exec_())

