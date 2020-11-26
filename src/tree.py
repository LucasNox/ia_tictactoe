import numpy

class _MinMaxNode:
	def __init__(self, depth, board, leaf):
		self.depth = depth
		self.board = board
		self.leaf = leaf
		self.children = []
		if not leaf:
			marker = 1 if ((self.depth + 1) % 2) == 0 else 2
			indexes = self._getAvailablePosition()
			for i in indexes:
				new_board = numpy.copy(self.board)
				new_board[i[0],i[1]] = marker
				isLeaf = self._checkVictory(board, i[0], i[1])
				new_node = _MinMaxNode(self.depth+1, new_board, isLeaf)
				self.children.append(new_node)

	def _checkVictory(self, board, x, y):
		#Vertical
		if board[0,y] == board[1,y] == board [2,y]:
			return True
		#Horizontal
		if board[x,0] == board[x,1] == board [x,2]:
			return True
		#Diagonal principal
		if x == y and board[0,0] == board[1,1] == board [2,2]:
			return True
		#Diagonal secundária
		if x + y == 2 and board[0,2] == board[1,1] == board [2,0]:
			return True
		return False 

	def _getAvailablePosition(self):
		return numpy.argwhere(self.board == 0)
		

class MinMaxTree:
	def __init__(self):
		board = numpy.matrix([[0,0,0], [0,0,0], [0,0,0]])
		self.root = _MinMaxNode(0, board, False)