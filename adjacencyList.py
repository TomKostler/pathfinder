class adjacency():
	def __init__(self, rows, columns, start, end, walls):
		self.start = start
		self.end = end
		self.rows = rows
		self.columns = columns
		self.walls = walls



	def getAdjacency(self):
		#generate the self.adjacency list of the tableWidget
		rangeObj = self.columns * self.rows
		self.adjacency = [[] for x in range(rangeObj)]


		#eine eindeutige Zuordnung einer Zelle ist Tupel (0, 0)
		#anfangen mit dem durchlaufen eine Zelle oben drüber und dann Uhrzeigersinn
		ind = 0
		for i in range(self.rows):
			for j in range(self.columns):
				ind = self.columns * i + j

				#wenn die Wall schon der Ind ist
				if self.walls[ind] == 1:
					continue
				#links und rechts
				if ind - (self.columns*i) - 1 >= 0 and self.walls[ind-1] != 1:
					self.adjacency[ind].append(ind - 1)
				if ind - (self.columns*i) + 1 <= self.columns-1 and self.walls[ind+1] != 1:
					self.adjacency[ind].append(ind + 1) 

				#unten und oben
				if ind - self.columns >= 0 and self.walls[ind-self.columns] != 1:
					self.adjacency[ind].append(ind - self.columns)
				if ind + self.columns <= len(self.adjacency)-1 and self.walls[ind+self.columns] != 1:
					self.adjacency[ind].append(ind + self.columns)

				ind += 1

		#but set the value of the end index to 0
		endInd = self.columns*self.end[0] + self.end[1]
		self.adjacency[endInd] = []

		#print(self.adjacency)

		return self.adjacency