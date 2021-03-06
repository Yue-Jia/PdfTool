from PyPDF2 import PdfFileMerger, PdfFileReader, PdfFileWriter
import sys
import asyncio
from PyQt5.QtWidgets import QApplication, QMainWindow, QListWidget, QListWidgetItem, QPushButton, QProgressBar, QFileDialog, QLabel, QLineEdit, QRadioButton
from PyQt5 import QtGui
from PyQt5.QtCore import Qt, QUrl
import os
import re

class ListBoxWidget(QListWidget):
	def __init__(self,parent=None):
		super().__init__(parent)
		self.setAcceptDrops(True)
		self.resize(600,600)
		self.setStyleSheet(
			'''
			border-color: #00008B;
			border-style: outset;
			border-width: 2px;
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
		plst = []
		#self.resize(900,600)
		self.setFixedSize(900,600)
		self.lstView = ListBoxWidget(self)
		self.lstView.setGeometry(300,0,600,600)
		self.txt = QLineEdit(self)
		self.txt.setAlignment(Qt.AlignCenter)
		self.txt.setGeometry(50,140,200,50)
		self.radi = QRadioButton('Retrieve Page')
		self.radi.setGeometry(50,100,60,10)
		self.btn = QPushButton('Merge' ,self)
		self.btn.setGeometry(50,400,200,50)
		self.btn.clicked.connect(lambda : self.pdfMerge(self.getItems(),self.msg()))
		self.btn1 = QPushButton('Delete' ,self)
		self.btn1.setGeometry(50,460,200,50)
		self.btn1.clicked.connect(lambda :self.removeItem())
		self.btn2 = QPushButton('Split',self)
		self.btn2.setGeometry(50,200,200,50)
		self.btn2.clicked.connect(lambda : self.pdf_splitter(self.getSelectedItem(),plst,self.msg()))
		self.setWindowTitle('PdfTool')
		self.setStyleSheet('''
				QPushButton {
				    padding: 5px;
				    border-color: #00008B;
				    border-style: outset;
				    border-width: 2px;
				}
				QPushButton:hover{
					background-color: #637383;
					color:#F0F8FF;
				};
				font:23px;
				color: #00008B;
				background-color: #F0F8FF;
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
 
	def pdf_splitter(self,path,plst,direc):
		plst = self.getPages()
		try:
			fname = os.path.splitext(os.path.basename(path))[0]
			pdf = PdfFileReader(path)
			totalP = pdf.getNumPages()
			if plst[0]<plst[1] and plst[1]<totalP:
				
				pdf_writer = PdfFileWriter()
				for page in range(plst[0]-1,plst[1]):
					pdf_writer.addPage(pdf.getPage(page))
		 
				output_filename = direc #'{}_page_{}.pdf'.format(fname, str(plst[0])+'_'+str(plst[1]))
	 
				with open(output_filename, 'wb') as out:
					pdf_writer.write(out)
					 
				self.notif.setText('Created:{}'.format(output_filename))
			elif plst[0] == plst[1]:
				if plst[0]>0:
					pdf_writer = PdfFileWriter()
					pdf_writer.addPage(pdf.getPage(plst[0]-1))
					output_filename = direc #'{}_page.pdf'.format(fname)
					with open(output_filename, 'wb') as out:
						pdf_writer.write(out)

					self.notif.setText('Created: {}'.format(output_filename))
				else:
					pdf_writer = PdfFileWriter()
					for page in range(0,-plst[0]-1):
						pdf_writer.addPage(pdf.getPage(page))
					for page in range(-plst[0],totalP):
						pdf_writer.addPage(pdf.getPage(page))
					output_filename = direc #'{}_page.pdf'.format(fname)
					with open(output_filename,'wb') as out:
						pdf_writer.write(out)

					self.notif.setText('Created: {}'.format(output_filename))
			elif plst[0]>plst[1] and plst[0]<totalP:
				pdf_writer = PdfFileWriter()
				for page in range(0,plst[1]-1):
					pdf_writer.addPage(pdf.getPage(page))
				for page in range(plst[0],totalP):
					pdf_writer.addPage(pdf.getPage(page))
				output_filename = direc #'{}_page_{}.pdf'.format(fname, str(plst[0])+'_'+str(plst[1]))
				with open(output_filename, 'wb') as out:
					pdf_writer.write(out)
				self.notif.setText('Created: {}'.format(output_filename))
			else:
				self.notif.setText('error')


		except Exception as e:
			print(e)
	def getPages(self):
		try:
			plst=[]
			startp=0
			endp=0
			content = self.txt.text().strip()
			splitPages = re.split(':',content)
			if len(splitPages)==1:
				startp = endp = int(splitPages[0])
			elif len(splitPages)==2:
				startp = int(splitPages[0])
				endp = int(splitPages[1])
			else:
				print('should be less than 3 numbers')
			plst.append(startp)
			plst.append(endp)
			return plst

		except Exception as e:
			print(e)
					



if __name__ =="__main__":
    
	app = QApplication(sys.argv)
	tool = PdfTool()
	tool.show()
	sys.exit(app.exec_())
