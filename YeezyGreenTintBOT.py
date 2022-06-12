from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import concurrent.futures
import time
import multiprocessing

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QPixmap, QIcon
import sys

def newProc(x):
	try:
		options = Options()
		options.add_argument('--disable-gpu')
		driver = webdriver.Chrome(executable_path='./selenium/webdriver/chromedriver.exe', options=options)
		driver.minimize_window()
		wait = WebDriverWait(driver, 43200)
		url = "https://www.adidas.co.id/Originals/yeezy.html"

		print("Tab", x, "Opened")
		driver.get(url)
		print("Tab", x, "Loaded")
		
		try:
			wait.until(EC.visibility_of_element_located((By.ID, "MainPart_lbQueueNumber")))

			que = driver.find_element_by_id('MainPart_lbQueueNumber')
			print("Tab", x, "Queue Number:", que.text)

			time.sleep(20)
			
			if int(que.text) > 5000 :
				driver.close()
				print("Tab", x, "closing. Above limit number")
		except:
			print("Tab", x, "error. Autoclose Canceled!")
	except:
		print("Tab", x, "error. Switching to Manual")
	finally:
		time.sleep(43200)
	


class MyWindow(QMainWindow):
	def __init__(self):
		super(MyWindow, self).__init__()
		self.setGeometry(710, 300, 500, 500)
		self.setWindowTitle("GreenTint Yeezy BOT")
		self.initUI()

	def initUI(self):
		self.logo = QtWidgets.QLabel(self)
		self.pixmap = QPixmap("logo.png")
		self.pixmap = self.pixmap.scaled(128, 128, QtCore.Qt.KeepAspectRatio)
		self.logo.setPixmap(self.pixmap)
		self.logo.move(175, 50)
		self.logo.resize(self.pixmap.width(), self.pixmap.height())

		self.label2 = QtWidgets.QLabel(self)
		self.label2.setText("Input How Many Tab :")
		self.label2.setAlignment(QtCore.Qt.AlignCenter)
		self.label2.move(186,170)
		self.label2.adjustSize() 
		self.tab = QtWidgets.QLineEdit(self)
		self.tab.setAlignment(QtCore.Qt.AlignCenter)   
		self.tab.move(200,205)
		self.tab.resize(100,30)

		self.label = QtWidgets.QLabel(self)
		self.label.setText("Click the Button below to open")
		self.label.setAlignment(QtCore.Qt.AlignCenter)
		self.label.move(166,260)
		self.label.adjustSize()

		self.but = QtWidgets.QPushButton(self)
		self.but.setText("Open Tab")
		self.but.clicked.connect(self.clicked)
		self.but.move(200, 300)

	def clicked(self):
		self.label.setText("Opening Magic Tab...")
		self.label.move(185,260)
		self.update()

		tabval = self.tab.text()
		x = int(tabval)
		openTab(x)

		self.label.setText("All Tab Opened")
		self.label.move(205,260)
		self.update()

	def update(self):
		self.label.adjustSize()

def window():
	app = QApplication(sys.argv)
	app_icon = QIcon("logo.ico")
	app.setWindowIcon(app_icon)

	win = MyWindow()

	win.show()
	sys.exit(app.exec_())


processes = []

if __name__ == "__main__":
	multiprocessing.freeze_support()
	def openTab(tab):	
		for x in range(tab):
			p = multiprocessing.Process(target=newProc,args=[x])
			p.start()
			processes.append(p)
			time.sleep(3)

	window()

for p in processes:
	p.join()
