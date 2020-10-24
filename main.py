from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QApplication , QMainWindow, QWidget
import sys
import sqlite3



conn = sqlite3.connect("users.db")
c = conn.cursor()

c.execute("""SELECT count(name) FROM sqlite_master WHERE type='table' and name = 'Users'""")
if c.fetchone()[0] == 0:
    c.execute("""CREATE TABLE Users (
        Username text,
        Password text
    
    )""")





def window():

    app = QApplication(sys.argv)
    win = Create()
    win.show()
    sys.exit(app.exec_())


class Login(QMainWindow):


    def __init__(self, parent= None):
        super(Login,self).__init__(parent)
        self.length = 400
        self.width = 200
        self.setFixedSize(self.length, self.width)
        self.setWindowTitle("Pypass")
        self.win = UserWin()
        self.UI()

    def UI(self):
        self.label = QtWidgets.QLabel(self)
        self.label.setText("LOGIN")
        self.label.resize(self.length, 40)
        self.label.setAlignment(QtCore.Qt.AlignCenter)

        self.userinput = QtWidgets.QLineEdit(self)
        self.userinput.move(60, 60)
        self.userinput.resize(280, 20)

        self.passinput = QtWidgets.QLineEdit(self)
        self.passinput.move(60, 100)
        self.passinput.resize(280, 20)
        self.passinput.setEchoMode(QtWidgets.QLineEdit.Password)

        self.b1 = QtWidgets.QPushButton(self)
        self.b1.setText("Login")
        self.b1.resize(100, 25)
        self.b1.move(150, 150)
        self.b1.clicked.connect(self.Userwinbutton)

        self.b2 = QtWidgets.QPushButton(self)
        self.b2.setText("Create")
        self.b2.resize(80, 25)
        self.b2.move(310, 170)
        self.b2.clicked.connect(self.createacc)


    def Userwinbutton(self):
        user = self.userinput.text(), self.passinput.text()
        if user[0] != '' and user[1] != '':
            c.execute("SELECT * FROM Users WHERE Username = ? AND Password = ?",user)
            result = c.fetchall()
            if len(result) == 1:
                self.win.username = user[0]
                self.win.password = user[1]
                self.win.UI()
                self.win.show()
            if len(result) == 0:
                self.b1.setText("TRY AGAIN")
        else:
            self.b1.setText("TRY AGAIN")

    def createacc(self):
        self.close()
        Create(self).show()



class UserWin(QWidget):
    def __init__(self):
        super().__init__()
        self.length = 400
        self.width = 200
        self.setFixedSize(self.length, self.width)
        self.setWindowTitle("Pypass")
        self.password = ""
        self.username = ""
        self.add = Addaccount()

    def UI(self):
        self.table = texttonum((self.username,self.password))
        self.add.table = self.table

        items = {}
        num = 0
        y = 50


        c.execute("SELECT * FROM " + self.table)
        try:
            for item in c.fetchall():
               items[f"items1{num}"] = QtWidgets.QLabel(self)
               items[f"items1{num}"].setText(item[0])
               items[f"items1{num}"].move(20,y)

               items[f"items2{num}"] = QtWidgets.QLabel(self)
               items[f"items2{num}"].setText(item[1])
               items[f"items2{num}"].move(60, y)

               items[f"items3{num}"] = QtWidgets.QLabel(self)
               items[f"items3{num}"].setText(item[2])
               items[f"items3{num}"].move(90, y)

               num +=1
               y += 20
        except Exception as e:
            print(e)


        self.b1 = QtWidgets.QPushButton(self)
        self.b1.setText("Create Account")
        self.b1.resize(100, 25)
        self.b1.clicked.connect(self.addaccount)
        self.b1.move(150, 150)


    def addaccount(self):
            self.add.show()



class Addaccount(QWidget):
    def __init__(self):
        super().__init__()
        self.table = ""
        self.length = 400
        self.width = 200
        self.setFixedSize(self.length, self.width)
        self.setWindowTitle("Pypass")
        self.UI()



    def UI(self):
        self.email = QtWidgets.QLineEdit(self)
        self.email.move(60,60)
        self.username = QtWidgets.QLineEdit(self)
        self.username.move(60, 90)
        self.password = QtWidgets.QLineEdit(self)
        self.password.move(60, 120)
        self.enterbutton = QtWidgets.QPushButton(self)
        self.enterbutton.clicked.connect(self.enter)


    def enter(self):
        c.execute("INSERT INTO " + self.table + " VALUES (?,?,?)",(
            self.email.text(),self.username.text(),self.password.text()
        ))
        conn.commit()





class Create(QMainWindow):
    def __init__(self, parent=None):
        super(Create, self).__init__(parent)
        self.length = 400
        self.width = 200
        self.setFixedSize(self.length,self.width)
        self.win = UserWin()
        self.setWindowTitle("Pypass")
        self.UI()

    def UI(self):
        self.label = QtWidgets.QLabel(self)
        self.label.setText("CREATE")
        self.label.resize(self.length,40)
        self.label.setAlignment(QtCore.Qt.AlignCenter)

        self.userinput = QtWidgets.QLineEdit(self)
        self.userinput.move(60,60)
        self.userinput.resize(280,20)

        self.passinput = QtWidgets.QLineEdit(self)
        self.passinput.move(60, 100)
        self.passinput.resize(280, 20)
        self.passinput.setEchoMode(QtWidgets.QLineEdit.Password)

        self.b1 = QtWidgets.QPushButton(self)
        self.b1.setText("Create Account")
        self.b1.resize(100, 25)
        self.b1.clicked.connect(self.Userwinbutton)
        self.b1.move(150, 150)

        self.b2 = QtWidgets.QPushButton(self)
        self.b2.setText("Login")
        self.b2.resize(80, 25)
        self.b2.clicked.connect(self.loginButton)
        self.b2.move(310, 170)



    def loginButton(self):
        self.close()
        Login(self).show()

    def Userwinbutton(self):
        user = self.userinput.text(), self.passinput.text()
        c.execute("""SELECT count(name) FROM sqlite_master WHERE type='table' and name = '""" + texttonum(user) + """' """)
        if c.fetchone()[0] == 0:
            if user[0] != '' and user[1] != '':
                self.createtableval(texttonum(user))
                c.execute("""INSERT INTO Users VALUES (?,?)""",user)
                conn.commit()
                self.close()
                self.win.username = user[0]
                self.win.password = user[1]
                self.win.UI()
                self.win.show()


            else:
                self.b1.setText("TRY AGAIN")
        else:
            self.b1.setText("Account Made")



    def createtableval(self,string):
        c.execute("""CREATE TABLE """ + string + """ (
            Email text,
            Username text,
            Password text
        
        )""")


def texttonum(user):
    string = user[0] + "," + user[1]
    returnstring = "T"

    for l in string:
        returnstring += str(ord(l))

    return returnstring

if "__main__" == __name__:
    window()

