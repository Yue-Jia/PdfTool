from PyPDF2 import PdfFileMerger, PdfFileReader
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QListWidget, QListWidgetItem, QPushButton, QProgressBar
from PyQt5.QtCore import Qt, QUrl

class ListBoxWidget(QListWidget):
	def __init__(self,parent=None):
        	super().__init__(parent)
        	self.setAcceptDrops(True)
        	self.resize(600,600)
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
        	if event.mimeData().hasUrls():
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
		self.resize(1200,600)
		self.lstView = ListBoxWidget(self)
	#	print(dir(self.lstView))
		self.btn = QPushButton('Merge' ,self)
		self.btn.setGeometry(800,400,200,50)
       # 	self.btn.clicked.connect(lambda :print(self.getSelectedItem()))
		self.btn.clicked.connect(lambda : PT().pdfMerge(self.getItems()))
		self.btn1 = QPushButton('Delete' ,self)
		self.btn1.setGeometry(800,460,200,50)
		self.btn1.clicked.connect(lambda :self.lstView.takeItem(self.getItems().index(self.getSelectedItem())))

		self.setWindowTitle('PdfTool')
		self.pbar = QProgressBar(self)
		self.pbar.setRange(0,100)
		self.pbar.setValue(65)
		self.pbar.setGeometry(800,350,235,9)
	def getSelectedItem(self):
        	item = QListWidgetItem(self.lstView.currentItem())
        	return item.text()
	def getItems(self):
        	itt =[]
        	for i in range(self.lstView.count()):
            		itt.append(self.lstView.item(i).text())
        	return itt


class PT():
	if not sys.warnoptions:
        	import warnings
        	warnings.simplefilter("ignore")

	def pdfMerge(self,lst):
        	# Call the PdfFileMerger
        	mergedObject = PdfFileMerger()
        	print("Processing...") 
        # 	Loop through all of pdf files and append their pages
        	for fileName in lst:
            		mergedObject.append(PdfFileReader(fileName, 'rb'))
     
        # 	Write all the files into a file which is named as shown below
        	mergedObject.write("mergedfilesoutput.pdf")
        	print("Done.")
if __name__ =="__main__":
    
#    try:
#       last = sys.argv[1]
#        pdfMerge(int(last))
#    except Exception as e:
#        print(e)
	app = QApplication(sys.argv)
	tool = PdfTool()
	tool.show()
	sys.exit(app.exec_())
