import math
import sys


class Node():
	def __init__(self, pos, vorgänger):
		self.position = pos
		self.vorgänger = vorgänger
		self.h_Cost = float('inf')
		self.g_Cost = float('inf')
		self.f_Cost = float('inf')
		self.x = 0
		self.y = 0


	def umrechnenInCoor(self, col, widthNode):
		y = math.floor(self.position / col)
		x = self.position - y*col
		return x, y




class aStarSearch():
	def __init__(self, rows, columns, start, end, walls, adjacency, widthNode):
		self.rows = rows
		self.columns = columns
		self.startPoint = start
		self.endPoint = end
		self.walls = walls
		self.adjacency = adjacency
		self.open = []
		self.closed = []
		self.widthNode = widthNode





	def add_to_open(self, neighbor):
	    for node in self.open:
	        if (neighbor == node and neighbor.g_Cost > node.g_Cost):
	            return False
	    return True


	def start(self):
		self.startNode = Node(self.columns * self.startPoint[0] + self.startPoint[1], None)
		endInd = self.columns * self.endPoint[0] + self.endPoint[1]
		self.open.append(self.startNode)

		xStart, yStart = self.startNode.umrechnenInCoor(self.columns, self.widthNode)
		xEnd, yEnd = self.endPoint[1], self.endPoint[0]
		
		while len(self.open) > 0:
			#get the node in visited with lowest f cost
			self.open.sort(key=lambda node: node.f_Cost)

			currentNode = self.open.pop(0)

			self.closed.append(currentNode)

			if currentNode.position == endInd:
				return currentNode, self.closed[1:-1]


			for neighborInd in self.adjacency[currentNode.position]:
				neighborNode = Node(neighborInd, currentNode)

				if len([i for i in self.closed if neighborNode.position == i.position]) > 0:
					continue


				#set the costs (g: vom Start, h: bis zum Ziel)
				xNeighbor, yNeighbor = neighborNode.umrechnenInCoor(self.columns, self.widthNode)


				neighborNode.g_Cost = abs(xNeighbor - xStart) + abs(yNeighbor - yStart)
				neighborNode.h_Cost = abs(xNeighbor - xEnd) + abs(yNeighbor - yEnd)
				neighborNode.f_Cost = neighborNode.h_Cost + neighborNode.g_Cost


				#check if node should be added ("Backtracking")
				if len([i for i in self.open if neighborNode.position == i.position]) > 0:
					continue

				#ansonsten soll er das adden
				self.open.append(neighborNode)


		return None, None




	def fastestWay(self, current):
		path = []

		while current != self.startNode:
			path.append(current.position)
			current = current.vorgänger

		path.reverse()
		return path






				

		


