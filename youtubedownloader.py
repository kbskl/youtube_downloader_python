from enum import Enum
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog, QMessageBox
import sys
from pytube import YouTube
import os
from threading import Thread
import datetime


class StaticVariables(Enum):
    download_suc = "Download completed successfully."
    download_started = "Download started."
    download_fail = "Download failed. Please check the link. Error:"
    storage_path = "storagepath"
    storage_path_saved = "Storage path saved"
    storage_path_saved_error = "An error occurred while saving the storage path. Error:"
    storage_path_loading_error = "An error occurred while loading the storage path. Error:"
    warning_empty_storage_path = "Please select storage path"
    warning_empty_url = "Please enter url"
    url_cleared = "Url input field cleared"
    warning_empty_url_status = "Url not entered"
    warning_empty_storage_path_status = "Storage path is empty"
    deleted_storage_path = "Storage path deleted"
    deleted_storage_path_error = "An error occurred while deleting the storage path. Error:"
    paste_process = "Pasting done from clipboard."


def download_thread(self, link, mypath, processType):
    try:
        yt = YouTube(link)
        title = yt.title
        self.label_4.setText(title)
        self.label_5.setText(str(datetime.timedelta(seconds=yt.length)))
        if processType == "mp3":
            filePath = yt.streams.filter(only_audio=True).first().download(output_path=mypath)
            os.rename(filePath, mypath + "/" + yt.title + ".mp3")
        elif processType == "mp4":
            ys = yt.streams.get_highest_resolution()
            ys.download(output_path=mypath)
        self.update_status_label(StaticVariables.download_suc.value)
    except Exception as e:
        self.update_status_label(StaticVariables.download_fail.value + str(e))
    finally:
        self.after_downloading()


class Ui_MainWindow(object):

    def save_path(self):
        try:
            with open(StaticVariables.storage_path.value, "w") as text_file:
                text_file.write(self.textEdit_2.toPlainText().strip())
            self.update_status_label(StaticVariables.storage_path_saved.value)
        except Exception as e:
            self.update_status_label(StaticVariables.storage_path_saved_error.value + str(e))

    def path_process(self):
        if self.checkBox.isChecked():
            if self.textEdit_2.toPlainText().strip() != "":
                self.save_path()

            else:
                self.warning_messages(StaticVariables.warning_empty_storage_path.value)
                self.update_status_label(StaticVariables.warning_empty_storage_path_status.value)
                self.checkBox.setChecked(False)
        else:
            try:
                os.remove(StaticVariables.storage_path.value)
                self.update_status_label(StaticVariables.deleted_storage_path.value)
            except Exception as e:
                self.update_status_label(StaticVariables.deleted_storage_path_error.value + str(e))

    def update_status_label(self, message):
        self.label_8.setText(message)
        self.label_8.adjustSize()

    def warning_messages(self, messages):
        QMessageBox.warning(self.centralwidget, "Warning", messages, QMessageBox.Ok)

    def paste_clipboard(self):
        cb = QtWidgets.QApplication.clipboard()
        self.textEdit.setText(cb.text())
        self.update_status_label(StaticVariables.paste_process.value)

    def before_downloading(self):
        self.update_status_label(StaticVariables.download_started.value)
        self.label_4.setText("-")
        self.label_5.setText("-")
        self.pushButton.setEnabled(False)
        self.pushButton_2.setEnabled(False)
        self.pushButton_3.setEnabled(False)
        self.textEdit_2.setEnabled(False)
        self.textEdit.setEnabled(False)
        self.pushButton_4.setEnabled(False)
        self.checkBox.setEnabled(False)

    def after_downloading(self):
        self.pushButton.setEnabled(True)
        self.pushButton_2.setEnabled(True)
        self.pushButton_3.setEnabled(True)
        self.textEdit_2.setEnabled(True)
        self.textEdit.setEnabled(True)
        self.pushButton_4.setEnabled(True)
        self.checkBox.setEnabled(True)

    def download(self):
        if self.textEdit.toPlainText().strip() != "":
            if self.textEdit_2.toPlainText().strip() != "":
                self.before_downloading()
                mypath = self.textEdit_2.toPlainText()
                link = self.textEdit.toPlainText()
                processType = "mp4" if self.radioButton.isChecked() else "mp3"
                threadObject = Thread(target=download_thread, args=(self, link, mypath, processType))
                threadObject.start()
            else:
                self.update_status_label(StaticVariables.warning_empty_storage_path_status.value)
                self.warning_messages(StaticVariables.warning_empty_storage_path.value)
        else:
            self.update_status_label(StaticVariables.warning_empty_url_status.value)
            self.warning_messages(StaticVariables.warning_empty_url.value)

    def delete_url(self):
        self.update_status_label(StaticVariables.url_cleared.value)
        self.textEdit.setText("")

    def select_download_path(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName = QFileDialog.getExistingDirectory(self.centralwidget, "QFileDialog.getOpenFileName()", "")
        if fileName:
            self.textEdit_2.setText(fileName)

    def control_savedpath(self):
        if os.path.isfile(StaticVariables.storage_path.value):
            self.checkBox.setChecked(True)
            try:
                with open(StaticVariables.storage_path.value, 'r') as reader:
                    self.textEdit_2.setText(reader.readline())
            except Exception as e:
                self.update_status_label(StaticVariables.storage_path_loading_error.value + str(e))
                self.checkBox.setChecked(False)

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(619, 331)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(20, 50, 491, 31))
        self.textEdit.setObjectName("textEdit")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(20, 20, 131, 31))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.radioButton = QtWidgets.QRadioButton(self.centralwidget)
        self.radioButton.setGeometry(QtCore.QRect(20, 90, 100, 20))
        self.radioButton.setChecked(True)
        self.radioButton.setObjectName("radioButton")
        self.radioButton_2 = QtWidgets.QRadioButton(self.centralwidget)
        self.radioButton_2.setGeometry(QtCore.QRect(110, 90, 100, 20))
        self.radioButton_2.setObjectName("radioButton_2")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(20, 120, 170, 32))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.download)
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(520, 40, 81, 51))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(self.delete_url)
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(200, 90, 41, 16))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(200, 110, 51, 16))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(270, 90, 231, 16))
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(270, 110, 91, 16))
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(20, 190, 60, 16))
        self.label_6.setObjectName("label_6")
        self.textEdit_2 = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit_2.setGeometry(QtCore.QRect(20, 210, 491, 31))
        self.textEdit_2.setObjectName("textEdit_2")
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(520, 200, 81, 51))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.clicked.connect(self.select_download_path)
        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_4.setGeometry(QtCore.QRect(520, 90, 81, 51))
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_4.clicked.connect(self.paste_clipboard)
        self.checkBox = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox.setGeometry(QtCore.QRect(20, 250, 161, 20))
        self.checkBox.setObjectName("checkBox")
        self.checkBox.clicked.connect(self.path_process)
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(20, 290, 51, 16))
        self.label_7.setObjectName("label_7")
        self.label_8 = QtWidgets.QLabel(self.centralwidget)
        self.label_8.setGeometry(QtCore.QRect(70, 290, 531, 16))
        self.label_8.setObjectName("label_8")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 619, 24))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.control_savedpath()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Youtube Downloader"))
        self.label.setText(_translate("MainWindow", "Youtube link"))
        self.radioButton.setText(_translate("MainWindow", "MP4"))
        self.radioButton_2.setText(_translate("MainWindow", "MP3"))
        self.pushButton.setText(_translate("MainWindow", "Download"))
        self.pushButton_2.setText(_translate("MainWindow", "Delete"))
        self.label_2.setText(_translate("MainWindow", "Title:"))
        self.label_3.setText(_translate("MainWindow", "Length:"))
        self.label_4.setText(_translate("MainWindow", "-"))
        self.label_5.setText(_translate("MainWindow", "-"))
        self.label_6.setText(_translate("MainWindow", "Storage Path"))
        self.label_6.adjustSize()
        self.pushButton_3.setText(_translate("MainWindow", "Select"))
        self.pushButton_4.setText(_translate("MainWindow", "Paste"))
        self.checkBox.setText(_translate("MainWindow", "Save storage path"))
        self.label_7.setText(_translate("MainWindow", "Status:"))
        self.label_8.setText(_translate("MainWindow", "Application started"))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ex = Ui_MainWindow()
    w = QtWidgets.QMainWindow()
    ex.setupUi(w)
    w.show()
    sys.exit(app.exec_())
