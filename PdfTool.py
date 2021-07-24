from PyPDF2 import PdfFileMerger, PdfFileReader
import sys
import asyncio
from PyQt5.QtWidgets import QApplication, QMainWindow, QListWidget, QListWidgetItem, QPushButton, QProgressBar, QFileDialog, QLabel, QLineEdit
from PyQt5 import QtGui
from PyQt5.QtCore import Qt, QUrl

class ListBoxWidget(QListWidget):
	def __init__(self,parent=None):
		super().__init__(parent)
		self.setAcceptDrops(True)
		self.resize(600,600)
		self.setStyleSheet(
			'''
			background-color:#637383;
			
			''')
	def dragEnterEvent(self, event):
		if event.mimeData().hasUrls:
			event.accept()
		else:
			event.ignore()
	def dragMoveEvent(self, event):
		if event.mimeData().hasUrls():
			event.setDropAction(Qt.CopyAction)
			event.accept()
		else:
			event.ignore()
	def dropEvent(self, event):
		if event.mimeData().hasUrls() and event.mimeData().urls()[-1].toString().endswith('.pdf'):
			event.setDropAction(Qt.CopyAction)
			event.accept()

			links= []
			for url in event.mimeData().urls():
				if url.isLocalFile():
					links.append(str(url.toLocalFile()))
				else:
					links.append(str(url.toString()))
			self.addItems(links)
		else:
			event.ignore()


class PdfTool(QMainWindow):
	def __init__(self):
		super().__init__()
		directory ='mergedFile.pdf'
		#self.resize(900,600)
		self.setFixedSize(900,600)
		self.lstView = ListBoxWidget(self)
		self.lstView.setGeometry(300,0,600,600)
		self.txt = QLineEdit(self)
		self.txt.setGeometry(50,140,200,50)

		self.btn = QPushButton('Merge' ,self)
		self.btn.setGeometry(50,400,200,50)
		self.btn.clicked.connect(lambda : self.pdfMerge(self.getItems(),self.msg()))
		self.btn1 = QPushButton('Delete' ,self)
		self.btn1.setGeometry(50,460,200,50)
		self.btn1.clicked.connect(lambda :self.removeItem())
		self.btn2 = QPushButton('Split',self)
		self.btn2.setGeometry(50,200,200,50)

		self.setWindowTitle('PdfTool')
		self.setStyleSheet('''
				QPushButton {
				    padding: 5px;
				    border-color: #00FA9A;
				    border-style: outset;
				    border-width: 2px;
				};
				font:23px;
				color: #00FA9A;
				background-color: #778899;
				''')
		self.setWindowIcon(QtGui.QIcon('PT.png'))
		self.notif = QLabel('',self)
		self.notif.setGeometry(50,300,200,20)

	def getSelectedItem(self):
        	item = QListWidgetItem(self.lstView.currentItem())
        	return item.text()
	def getItems(self):
        	itt =[]
        	for i in range(self.lstView.count()):
            		itt.append(self.lstView.item(i).text())
        	return itt
	def removeItem(self):
		try:
			if self.getSelectedItem():
				self.lstView.takeItem(self.getItems().index(self.getSelectedItem()))
			else:
				self.lstView.clear()
		except Exception as e:
			print(e)
	def msg(self):
		try:
			directory = QFileDialog.getSaveFileName(self, "Set Path","./","PDF Files (*.pdf)")
			return directory[0]
		except Exception as e:
			print(e)
	
	def pdfMerge(self,lst,directory):
		if not sys.warnoptions:
			import warnings
			warnings.simplefilter("ignore")
		try:
			# Call the PdfFileMerger
			mergedObject = PdfFileMerger()
			if lst:
				print("Processing...")
				self.notif.setText('Processing...')
			# 	Loop through all of pdf files and append their pages
				for fileName in lst:
					mergedObject.append(PdfFileReader(fileName, 'rb'))
				
			# 	Write all the files into a file which is named as shown below
				mergedObject.write(directory)
				print("Done.")
				self.notif.setText('Done.')
			else:
				self.notif.setText('Select a file first')
		except Exception as e:
			print(e)
			self.notif.setText(e)


if __name__ =="__main__":
    
	app = QApplication(sys.argv)
	tool = PdfTool()
	tool.show()
	sys.exit(app.exec_())
