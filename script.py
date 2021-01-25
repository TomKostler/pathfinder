import sys
from qtpy import QtWidgets, QtTest
from qtpy import QtGui, QtCore
from mainwindow import Ui_MainWindow
from qtpy.QtWidgets import QPushButton, QMessageBox, QWidget, QGraphicsScene, QGraphicsView
from adjacencyList import adjacency
from bfs import bfsSearch
from aStar import *
#from animate import *
from qtpy.QtGui import QBrush, QPen, QColor
from qtpy.QtCore import Qt, QTimer



import random
import time
import math
import copy

app = QtWidgets.QApplication(sys.argv)

rows = 18
columns = 29 
widthNode = 50

normalBreite = columns * widthNode
normalHöhe = rows * widthNode

zoomLevel = 1






#class to Override the mouse event
class Scene(QtWidgets.QGraphicsScene):
    def __init__(self, parent=None):
        super(Scene, self).__init__(parent)

        self.zoom = 1
        self.mousePressed = 0
        self.widthNode = widthNode
        self.rows = rows
        self.columns = columns
        self.blackPen = QPen(Qt.black)
        self.blackPen.setWidth(2)



        pixmap = QtGui.QPixmap(self.columns * self.widthNode, self.rows * self.widthNode)
        pixmap.fill(QtCore.Qt.white)

        self.pixmap_item = self.addPixmap(pixmap)

        # random position
        self.pixmap_item.setPos(*random.sample(range(0, 2), 2))

    def mousePressEvent(self, event):
    	if window.ui.btnZoomOut.receivers(window.ui.btnZoomOut.clicked) > 0:
    		window.ui.btnZoomOut.clicked.disconnect()
    		window.ui.btnZoomIn.clicked.disconnect()
    	
    	items = self.items(event.scenePos())
    	for item in items:
    		if item is self.pixmap_item:
    			field = self.getField(item.mapFromScene(event.scenePos()))
    			if self.mousePressed < 2:
    				#set the start and end values
    				window.setPoints(field)
    			else:
    				window.makeWall(field)
    		super(Scene, self).mousePressEvent(event)


    	self.mousePressed += 1



    def mouseMoveEvent(self, event):
    	items = self.items(event.scenePos())
    	for item in items:
    		if item is self.pixmap_item:
    			x = int(item.mapFromScene(event.scenePos()).x())
    			y = int(item.mapFromScene(event.scenePos()).y())
    			if x < self.width() and y < self.height():
    				field = self.getField(item.mapFromScene(event.scenePos()))
    				window.makeWall(field)

    		super(Scene, self).mousePressEvent(event)


    def clear(self):
    	super(Scene, self).clear()

    	self.mousePressed = 0
    	pixmap = QtGui.QPixmap(window.columns * window.widthNode, window.rows * window.widthNode)
    	pixmap.fill(QtCore.Qt.white)

    	self.pixmap_item = self.addPixmap(pixmap)
    	self.pixmap_item.setPos(*random.sample(range(0, 2), 2))


    def getField(self, pos):
    	x, y = pos.x(), pos.y()

    	xField, yField = int(x/window.widthNode), int(y/window.widthNode)
    	return xField, yField





class MainWindow(QtWidgets.QMainWindow):
	def __init__(self, parent = None):
		super().__init__(parent)
		self.ui = Ui_MainWindow()
		self.ui.setupUi(self)

		self.rows = rows
		self.columns = columns
		self.normalHöhe = normalHöhe
		self.normalBreite = normalBreite
		self.widthNode = widthNode
		self.widthNodeStart = copy.deepcopy(self.widthNode)
		self.startPoint = None
		self.endPoint = None
		self.walls = [0 for x in range(self.rows*self.columns)]
		self.fastestWay = []
		self.toAnimate = []
		self.speed = self.ui.horizontalSliderSpeed.value()
		self.pastRects = []
		self.algo = "A*"
		self.start = True
		self.zoomLevel = zoomLevel




		#setup the grid
		self.scene = Scene()
		self.blackPen = QPen(Qt.black)
		self.blackPen.setWidth(2)
		self.greenColor = QBrush(Qt.green)
		self.redColor = QBrush(Qt.red)
		self.blackColor = QBrush(Qt.black)
		self.yellowColor = QBrush(Qt.yellow)
		self.cyanColor = QBrush(Qt.cyan)


		self.view = QGraphicsView(self.scene, self)
		self.view.setGeometry(0, 80, self.columns * self.widthNode, self.rows * self.widthNode)
		self.drawTheGrid()
		self.view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
		self.view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

		self.ui.horizontalSliderSpeed.valueChanged.connect(self.setSpeed)
		self.ui.pushButtonDelete.clicked.connect(self.deleteMap)
		self.ui.btnChangeAlgo.clicked.connect(self.changeAlgo)

		self.ui.labelAlgo.setText("You are currently using " + self.algo)

		self.ui.labelColorStart.setStyleSheet("background-color: lightgreen")
		self.ui.labelColorEnd.setStyleSheet("background-color: red")


		self.ui.btnZoomOut.clicked.connect(self.zoomOut)
		self.ui.btnZoomIn.clicked.connect(self.zoomIn)





		self.setWindowTitle("Pathfinding Visualizer")




		#init the the message Boxes
		self.msgError = QMessageBox()
		self.msgError.setIcon(QMessageBox.Information)
		self.msgError.setText("Es konnte kein Pfad gefunden werden.")
		self.msgError.setWindowTitle("No Path")
		self.msgError.setStandardButtons(QMessageBox.Ok)


		self.msgStartP = QMessageBox()
		self.msgStartP.setIcon(QMessageBox.Information)
		self.msgStartP.setText("Bitte wählen Sie zuerst den Start-Punkt, indem sie auf ein Feld klicken.")
		self.msgStartP.setWindowTitle("Start Punkt wählen")
		self.msgStartP.setStandardButtons(QMessageBox.Ok)


		self.msgEndP = QMessageBox()
		self.msgEndP.setIcon(QMessageBox.Information)
		self.msgEndP.setText("Bitte wählen Sie nun den End-Punkt aus, indem sie auf ein Feld klicken.")
		self.msgEndP.setWindowTitle("End Punkt wählen")
		self.msgEndP.setStandardButtons(QMessageBox.Ok)

		

		self.msgStartP.exec()




	def createLabyrinth(self):
		#das geht nur nachdem start und end gewählt wurde
		rects = self.columns * self.rows
		for i in range(int(rects * 1/6 * 0.8)):
			ind = int(random.random() * rects)
			x, y = self.indToCoor(ind)
			xRect = ind * self.widthNode
			yRect = ind * self.widthNode			
			if self.startPoint[0] != xRect or self.startPoint[1] != yRect:
				if self.endPoint[0] != yRect or self.endPoint[1] != xRect:
					self.scene.addRect(x, y, self.widthNode, self.widthNode, self.blackPen, self.blackColor)
					self.walls[ind] = 1 






		
	def zoomOut(self):
		self.scene.clear()
		self.zoomLevel = 0.95
		self.widthNode = self.zoomLevel*self.widthNode

		self.rows = int(normalHöhe / self.widthNode)
		self.columns = int(normalBreite / self.widthNode)

		self.walls = [0 for x in range(self.rows*self.columns)]

		#draw the grid with new widthNode
		self.drawTheGrid()
		self.scene.update()




	def zoomIn(self):
		self.scene.clear()
		self.zoomLevel = 1.05
		self.widthNode = self.zoomLevel*self.widthNode

		self.rows = int(normalHöhe / self.widthNode)
		self.columns = int(normalBreite / self.widthNode)

		self.walls = [0 for x in range(self.rows*self.columns)]

		#draw the grid with new widthNode
		self.drawTheGrid()
		

	def setSpeed(self, value):
		maximum = self.ui.horizontalSliderSpeed.maximum()
		self.speed = maximum - value



	def deleteMap(self):
		self.scene.clear()
		self.ui.labelState.setText('<html><head/><body><p><span style=" font-style:italic;">Mode:</span><span style=" font-weight:600; font-style:italic;"> Start</span></p></body></html>')

		self.properties = []
		self.visited = []
		self.scene.mousePressed = 0
		self.startPoint = None
		self.endPoint = None
		self.walls = [0 for x in range(self.rows*self.columns)]
		self.fastestWay = []
		self.toAnimate = []

		self.drawTheGrid()
		self.msgStartP.exec()		
		

	def drawTheGrid(self):
		x = 0
		y = 0

		for i in range(self.rows):
			for j in range(self.columns):
				self.scene.addRect(x, y, self.widthNode, self.widthNode, self.blackPen)
				x += self.widthNode

			x = 0
			y += self.widthNode



	def setPoints(self, pos):
		x, y = pos
		if self.startPoint == None:
			self.ui.labelState.setText('<html><head/><body><p><span style=" font-style:italic;">Mode:</span><span style=" font-weight:600; font-style:italic;"> Config</span></p></body></html>')
			self.drawRect(x, y, color="green")
			
			self.startPoint = (y, x)

			self.msgEndP.exec()



		else:
			self.drawRect(x, y, color="red")

			self.endPoint = (y, x)

			if self.start:
				self.ui.btnStart.setStyleSheet("background-color : blue")
				self.ui.btnStart.clicked.connect(self.algorythm)
				self.start = False

			self.ui.btnCreateLabyrinth.clicked.connect(self.createLabyrinth)



	def drawRect(self, x, y, color):
		x = x * self.widthNode
		y = y * self.widthNode
		if color == "green":
			self.scene.addRect(x, y, self.widthNode, self.widthNode, self.blackPen, self.greenColor)
		else:
			self.scene.addRect(x, y, self.widthNode, self.widthNode, self.blackPen, self.redColor)



	def makeWall(self, pos):
		x, y = pos
		if self.startPoint[1] != x or self.startPoint[0] != y:
			if self.endPoint[1] != x or self.endPoint[0] != y:  
				ind = self.columns * y + x
				x = x * self.widthNode
				y = y * self.widthNode
				self.scene.addRect(x, y, self.widthNode, self.widthNode, self.blackPen, self.blackColor)
				self.walls[ind] = 1 
		

	def changeAlgo(self):
		if self.algo == "BFS":
			self.algo = "A*"
			self.ui.labelAlgo.setText("You are currently using " + self.algo)

		else:
			self.algo = "BFS"
			self.ui.labelAlgo.setText("You are currently using " + self.algo)



	def algorythm(self):
		#start the algorythm
		self.ui.labelState.setText('<html><head/><body><p><span style=" font-style:italic;">Mode:</span><span style=" font-weight:600; font-style:italic;"> Running</span></p></body></html>')
		adjacencyObj = adjacency(self.rows, self.columns, self.startPoint, self.endPoint, self.walls)
		adjacencyList = adjacencyObj.getAdjacency()

		
		if self.algo == "BFS":

			pathfinder = bfsSearch(self.rows, self.columns, self.startPoint, self.endPoint, self.walls, adjacencyList)
			properties, self.visited = pathfinder.bfs()

			if properties != "There is no way":
				#self.visited.reverse()

				self.fastestWay = pathfinder.fastestWay()[1:-1]
				#print(self.fastestWay)

				self.clearConnections()
				self.animateWayBfs()
				self.setConnections()


			else:
				self.msgError.exec()
		else:
			#A*
			pathfinder = aStarSearch(self.rows, self.columns, self.startPoint, self.endPoint, self.walls, adjacencyList, widthNode)
			node, self.close = pathfinder.start()

			
			if node == None:
				self.msgError.exec()

			else:	
				self.fastestWay = pathfinder.fastestWay(node)[:-1]
				#print(self.fastestWay)
				
				#visualize the way
				self.clearConnections()
				self.animateWayAStar()
				self.setConnections()




	

	def clearConnections(self):
		self.ui.pushButtonDelete.disconnect()
		self.ui.btnStart.disconnect()
		self.ui.btnCreateLabyrinth.disconnect()


	def setConnections(self):
		self.ui.pushButtonDelete.clicked.connect(self.deleteMap)
		self.ui.btnStart.clicked.connect(self.algorythm)
		self.ui.btnZoomOut.clicked.connect(self.zoomOut)
		self.ui.btnZoomIn.clicked.connect(self.zoomIn)


	def animateWayAStar(self):
		for ind in self.close:
			x, y = self.indToCoor(ind.position)
			rect = self.scene.addRect(x, y, self.widthNode, self.widthNode, self.blackPen, QColor(255, 102, 153))
			QtTest.QTest.qWait(1.5*self.speed)

		self.visualizeFastestWay()	



	def animateWayBfs(self):
		#non recursive
		pastRects = []
		endInd = self.coorToInd(self.endPoint)
		for ind in self.visited:
			if ind != endInd and ind != ";":
				x, y = self.indToCoor(ind)
				rect = self.scene.addRect(x, y, self.widthNode, self.widthNode, self.blackPen, QColor(255, 102, 153))
				pastRects.append(rect)
				QtTest.QTest.qWait(1.2*self.speed)
			else:
				for rect in pastRects:
					rect.setBrush(self.cyanColor)
				pastRects = []
		self.visualizeFastestWay()

	
				


	def visualizeFastestWay(self):
		if len(self.fastestWay) > 0:
			node = self.fastestWay.pop(0)
			self.x, self.y = self.indToCoor(node)
			rect = self.scene.addRect(self.x, self.y, self.widthNode, self.widthNode, self.blackPen, self.yellowColor)
			QtTest.QTest.qWait(1.2 * self.speed)
			self.visualizeFastestWay()





	def indToCoor(self, ind):
		y = math.floor(ind / self.columns) * self.widthNode
		x = ind * self.widthNode - y*self.columns
		return x, y






	def coorToInd(self, coor):
		y, x = coor
		ind = y * self.columns + x
		return ind

window = MainWindow()
window.show()
sys.exit(app.exec_())