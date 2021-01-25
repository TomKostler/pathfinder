### algorythm pathfinding (zunächst BFS)


from queue import Queue
import time
from qtpy import QtGui, QtCore

class bfsSearch():
	#params: existing self.rows and self.columns in table
	def __init__(self, rows, columns, start, end, walls, adjacencyList):
		self.rows = rows
		self.columns = columns
		self.start = start
		self.end = end
		self.walls = walls
		self.adjacency = adjacencyList


	def bfs(self):
		self.qu = Queue()
		self.properties = [{"distance": None, "vorgänger": None} for x in range(len(self.adjacency))]
		self.visited = []


		self.startInd = (self.columns * self.start[0]) + self.start[1]
		self.endInd = (self.columns * self.end[0]) + self.end[1]
		self.qu.put(self.startInd)
		self.properties[self.startInd] = {"distance": 0, "vorgänger": -1}



		while not self.qu.empty():
			ind = self.qu.get() 
			if self.endInd == ind:
				return self.properties, self.visited
			for i in range(len(self.adjacency[ind])):				
				node = self.adjacency[ind][i]
				if self.properties[node]["distance"] == None:
					self.qu.put(node)
					self.properties[node]["distance"] = self.properties[ind]["distance"] + 1 
					self.properties[node]["vorgänger"] = ind
					self.visited.append(node)
			self.visited.append(";")

		#if there is no way
		return "There is no way", 0



	# hier wird der kürzeste Weg konstruiert
	def fastestWay(self):
		self.fastestWay = [self.endInd]
		#if self.properties[self.endInd]["distance"] == None:
		#	return "TThere is no wayy"

		distance = self.properties[self.endInd]["distance"]-1
		vorgänger = self.endInd


		while self.fastestWay[len(self.fastestWay)-1] != self.startInd:
			for i in range(len(self.properties)):
				if self.properties[i]["distance"] == distance: 
					if i == vorgänger+1 or i == vorgänger-1 or i == vorgänger+self.columns or i == vorgänger-self.columns:
						self.fastestWay.append(i)
						distance -= 1
						vorgänger = i
						break


		self.fastestWay.reverse()
		return self.fastestWay


		




