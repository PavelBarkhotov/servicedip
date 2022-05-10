import sys
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QWidget
import pyodbc

connection = pyodbc.connect('Driver={SQL Server};'
                            'Server=WIN-2Q4ROBLUEB1;'
                            'Database=barh_kurs;'
                            'Trusted_Connection=yes;')
global cur
cur = connection.cursor()


class WelcomeScreen(QDialog):
    def __init__(self):
        super(WelcomeScreen, self).__init__()
        loadUi("welcome.ui", self)
        self.passwordfield.setEchoMode(QtWidgets.QLineEdit.Password)
        self.login.clicked.connect(self.loginfunction)
        self.regbutton.clicked.connect(self.gotoreg)

    def gotoreg(self):
        reg = RegScreen()
        widget.addWidget(reg)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def loginfunction(self):
        user = self.emailfield.text()
        password = self.passwordfield.text()

        if len(user) == 0 and len(password) == 0:
            self.passerror.setText("*Введите данные об аккаунте")

        elif len(password) == 0:
            self.passerror.setText("*Введите ваш пароль")

        else:
            query = 'SELECT password FROM users WHERE email =\'' + user + "\'"
            cur.execute(query)

            result_pass = cur.fetchone()[0]
            if result_pass == password:
                print("Logged")
                main = MainScreen()
                widget.addWidget(main)
                widget.setCurrentIndex(widget.currentIndex() + 1)
            else:
                self.passerror.setText("*пароль введен неверно")


class RegScreen(QDialog):
    def __init__(self):
        super(RegScreen, self).__init__()
        loadUi("reg.ui", self)


class MainScreen(QDialog):
    def __init__(self):
        super(MainScreen, self).__init__()
        loadUi("main.ui", self)
        self.loaddata()
        self.delButton.clicked.connect(self.delete_button)
        self.addButton.clicked.connect(self.add_worker)
        self.editButton.clicked.connect(self.button_edit)
        self.autoButton.clicked.connect(self.auto_button)

        widget.setFixedHeight(694)
        widget.setFixedWidth(894)

    def add_worker(self):
        addscreen = AddScreen()
        widget.addWidget(addscreen)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def button_edit(self):
        editscreen = EditScreen()

        content = "SELECT * FROM workers"
        res = cur.execute(content)
        try:
            for row in enumerate(res):
                if row[0] == self.tableWidget.currentRow():
                    editscreen.label.setText(str(row[1][0]))
                    editscreen.fio.setText(row[1][1])
                    editscreen.good_r.setText(str(row[1][2]))
                    editscreen.bad_r.setText(str(row[1][3]))

        except Exception as error:
            print(error)

        widget.addWidget(editscreen)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def delete_button(self):

        content = "SELECT * FROM workers"
        res = cur.execute(content)
        try:
            for row in enumerate(res):
                if row[0] == self.tableWidget.currentRow():
                    print(row[1][0])
                    cur.execute(f"DELETE FROM workers WHERE id = {row[1][0]}")
                    connection.commit()
                    main = MainScreen()
                    widget.addWidget(main)
                    widget.setCurrentIndex(widget.currentIndex() + 1)
        except Exception as error:
            print(error)

    def loaddata(self):
        while self.tableWidget.rowCount() > 0:
            self.tableWidget.removeRow(0)
        content = "SELECT * FROM workers"
        res = cur.execute(content)
        for row_index, row_data in enumerate(res):
            self.tableWidget.insertRow(row_index)
            for colm_index, colm_data in enumerate(row_data):
                self.tableWidget.setItem(row_index, colm_index, QtWidgets.QTableWidgetItem(str(colm_data)))

        content2 = "SELECT * FROM services"
        res2 = cur.execute(content2)

        self.services = []
        for row_index, row_data in enumerate(res2):
            self.data = []
            self.services.append(self.data)

            for colm_index, colm_data in enumerate(row_data):
                self.data.append(colm_data)

        # print(self.services)

        for indx in range(1, 7, 1):
            title = getattr(self, "label_name_{}".format(indx))
            img = getattr(self, "label_{}".format(indx))

            # установка текста из массива с услугами
            title.setText(self.services[indx - 1][1])
            # установка изображений из массива с услугами
            pixmap = self.services[indx - 1][2]
            img.setPixmap(QPixmap(f"{pixmap}")) #путь в БД
            print(pixmap)

    def auto_button(self):
        autoscreen = AutoScreen()
        widget.addWidget(autoscreen)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class AddScreen(QDialog):

    def __init__(self):
        super(AddScreen, self).__init__()
        loadUi("add.ui", self)
        self.confirm.clicked.connect(self.add_button)

    def add_button(self):
        fio = "'" + self.surname.toPlainText() + ' ' + self.name.toPlainText() + ' ' + self.adname.toPlainText() + "'"
        self.surname.clear()
        self.name.clear()
        self.adname.clear()

        print(fio)

        try:
            cur = connection.cursor()
            cur.execute("INSERT INTO workers(FIO, reg_date)"
                        f"VALUES ({fio}, GETDATE())")
            connection.commit()
            main = MainScreen()
            widget.addWidget(main)
            widget.setCurrentIndex(widget.currentIndex() + 1)
        except Exception as error:
            print(error)


class EditScreen(QDialog):
    def __init__(self):
        super(EditScreen, self).__init__()
        loadUi("edit.ui", self)

        self.edit.clicked.connect(self.editbutton)

    def editbutton(self):
        id = self.label.text()
        print(id)
        FIO = self.fio.toPlainText()
        print(FIO)
        good_rates = self.good_r.toPlainText()
        print(good_rates)
        bad_rates = self.bad_r.toPlainText()
        print(bad_rates)
        try:
            cur = connection.cursor()

            cur.execute(
                f"UPDATE workers SET FIO='{FIO}', good_rates={good_rates}, bad_rates={bad_rates} WHERE id = {id}")
            connection.commit()
            main = MainScreen()
            widget.addWidget(main)
            widget.setCurrentIndex(widget.currentIndex() + 1)
        except Exception as error:
            print(error)


class AutoScreen(QDialog):
    def __init__(self):
        super(AutoScreen, self).__init__()
        loadUi("auto.ui", self)
        widget.setFixedHeight(671)
        widget.setFixedWidth(671)
        self.backButton.clicked.connect(self.back_button)

        self.a = []
        self.b = []
        self.maxs = []
        self.loaddata()
        self.raiting()

    def back_button(self):
        try:
            main = MainScreen()
            widget.addWidget(main)
            widget.setCurrentIndex(widget.currentIndex() + 1)
        except Exception as error:
            print(error)

    def raiting(self):
        while self.raitingWidget.rowCount() > 0:
            self.raitingWidget.removeRow(0)
        krit = [0, 1, -1, 1, -0.5, -0.5]
        rate = []

        for i in range(0, 5, 1):
            sum = 0

            self.raitingWidget.insertRow(i)
            for j in range(1, 6, 1):
                sum = sum + (int(self.a[i][j]) / int(self.maxs[j])) * int(krit[j])
            rate.append([])
            rate[i].append(self.a[i][0])
            rate[i].append(sum)

            for n in range(0, 2, 1):
                self.raitingWidget.setItem(i, n, QtWidgets.QTableWidgetItem(str(rate[i][n])))
            print(rate[i])

    def loaddata(self):
        while self.tableWidget.rowCount() > 0:
            self.tableWidget.removeRow(0)
        content = (
            "SELECT FIO as ФИО, good_rates as Положительные, bad_rates as Отрицательные, DATEDIFF(DAY, reg_date, GETDATE()) as Время_работы_в_компании, avg(DATEDIFF(DAY,start_time, end_time)) as Среднее_время, Count(*) as Количество_попыток FROM workers, works WHERE workers.id = works.worker_id GROUP BY workers.id, workers.FIO, workers.good_rates, workers.bad_rates, workers.reg_date, worker_id, order_id ")
        res = cur.execute(content)

        for row_index, row_data in enumerate(res):
            self.tableWidget.insertRow(row_index)
            self.b = []
            self.a.append(self.b)

            for colm_index, colm_data in enumerate(row_data):
                self.tableWidget.setItem(row_index, colm_index, QtWidgets.QTableWidgetItem(str(colm_data)))
                self.b.append(colm_data)

        print(self.a)

        while self.maxtableWidget.rowCount() > 0:
            self.maxtableWidget.removeRow(0)
        content = (
            "SELECT MAX(FIO), MAX(good_rates), MAX(bad_rates), MAX(DATEDIFF(DAY, reg_date, GETDATE())), MAX(max_aa), MAX(max_bb)  from workers, (select avg(DATEDIFF(DAY,start_time, end_time))as max_aa from works group by worker_id) as max_a, (select Count(*) as max_bb from works group by worker_id) as msx_b")
        res = cur.execute(content)

        for row_index, row_data in enumerate(res):
            self.maxtableWidget.insertRow(row_index)
            for colm_index, colm_data in enumerate(row_data):
                self.maxtableWidget.setItem(row_index, colm_index, QtWidgets.QTableWidgetItem(str(colm_data)))
                self.maxs.append(colm_data)
        print(self.maxs)


# main
app = QApplication(sys.argv)
welcome = WelcomeScreen()
widget = QStackedWidget()
widget.addWidget(welcome)
widget.setFixedHeight(514)
widget.setFixedWidth(875)
widget.show()
try:
    sys.exit(app.exec_())
except:
    print("Exiting")
