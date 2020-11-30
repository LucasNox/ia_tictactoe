import numpy
import pickle

class _MinMaxNode:
	#Cria o objeto de nó da árvore
	def __init__(self, depth, board, leaf, draw=False):
		#Adiciona parametros básicos
		self.depth = depth
		self.board = board
		self.leaf = leaf
		#Verifica se camada vai ser MAX ou MIN
		self.isMax = True if ((self.depth) % 2) == 0 else False
		#Caso nó não seja folha, cria nós com as posições em branco restantes
		if not leaf:
			indexes = self._getAvailablePosition()
			self.children = []
			marker = 1 if ((self.depth) % 2) == 0 else 2
			#Se faltar só uma posição, precisamos de uma análise diferenciada para caso de empate
			if len(indexes) == 1:
				new_board = numpy.copy(self.board)
				new_board[indexes[0,0],indexes[0,1]] = marker
				draw = self._checkVictory(new_board, indexes[0,0], indexes[0,1])
				new_node = _MinMaxNode(self.depth+1, new_board, True, not draw)
				self.children.append(new_node)
				return
			#Se faltar mais de uma posição, cicla por elas criando novos nós marcando com a marca do
			#jogador atual essas posições
			for i in indexes:
				new_board = numpy.copy(self.board)
				new_board[i[0],i[1]] = marker
				isLeaf = self._checkVictory(new_board, i[0], i[1])
				new_node = _MinMaxNode(self.depth+1, new_board, isLeaf)
				self.children.append(new_node)
		else:
			#Caso seja um nó folha, checa se o marcador de empate está ativo, se sim, pontuação é 0
			#senão, calcula a pontuação
			if draw:
				self.points = 0
			else:
				if not self.isMax:
					self.points = 1 / self.depth
				else:
					self.points = -1 / self.depth

	#Verifica se a jogada realizada em x e y cria uma vitória
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

	#Fornece uma lista de todas as posições que estão vazias
	def _getAvailablePosition(self):
		return numpy.argwhere(self.board == 0)

	#Procura e retorna melhor pontuação obtida neste nó, dependendo do tipo da camada
	#Utiliza algoritmo de poda alpha beta
	def searchInTree(self, alpha=float('-inf'), beta=float('inf')):
		# print('-------------------------------')
		# # print('MAX') if self.isMax else print('MIN')
		# print('Profundidade: ', self.depth)
		# print('Board:')
		# self.printBoard()
		
		position = None
		#Se for folha, retorna pontuação
		if self.leaf:
			return self.points, 0
		#Se for MAX, desce recursivamente pelos nós e com o resultado obtido, pega o maior valor
		if self.isMax:
			for child in self.children:
				new_value, _ = child.searchInTree(alpha, beta)
				if new_value > alpha:
					# print('Melhor valor encontrado: ', new_value)
					alpha = new_value
					position = self.children.index(child)
				else:
					# print('Valor encontrado: ', new_value)
					pass
				if alpha >= beta:
					break
			# print('-------------------------------')
			return alpha, position
		#Se for MIN, desce recursivamente pelos nós e com o resultado obtido, pega o menor valor
		else:
			for child in self.children:
				new_value, _ = child.searchInTree(alpha, beta)
				if new_value < beta:
					# print('Melhor valor encontrado: ', new_value)
					beta = new_value
					position = self.children.index(child)
				else:
					# print('Valor encontrado: ', new_value)
					pass
				if alpha >= beta:
					break
			# print('-------------------------------')
			return beta, position

	def printBoard(self):
		print(' {} | {} | {} \n'.format(self.board[0,0],self.board[0,1],self.board[0,2])
			+'-----------\n'
			+' {} | {} | {} \n'.format(self.board[1,0],self.board[1,1],self.board[1,2])
			+'-----------\n'
			+' {} | {} | {} \n'.format(self.board[2,0],self.board[2,1],self.board[2,2]))

class MinMaxTree:
	#Cria o objeto de raiz da árvore
	def __init__(self, save=False, path=""):
		#Verifica se foi passado um caminho
		if path:
			#Caso sim, verifica se há um arquivo lá para realizar um load da árvore e não perder tempo montando-a
			try:
				with open(path, 'rb') as f:
					self.root = pickle.load(f)
			except:
				#Se não achou, monta a árvore
				board = numpy.matrix([[0,0,0], [0,0,0], [0,0,0]])
				self.root = _MinMaxNode(0, board, False)
		else:
			#Se não tem caminho, monta a árvore
			board = numpy.matrix([[0,0,0], [0,0,0], [0,0,0]])
			self.root = _MinMaxNode(0, board, False)
		#Se tem caminho e tem save, salva a árvore no caminho
		if save and path:
			with open(path, 'wb') as f:
				pickle.dump(self.root, f)

	#Torna a raiz da árvore o nó que será movimentado para não perder tempo processando nós
	#de estados de tabuleiro não mais acessíveis
	def registerMove(self, x, y):
		#Escolher se mover para uma célula já caminhada fará com o movimento na árvore vá
		#para o primeiro da lista de filhos do nó atualmente raiz
		for node in self.root.children:
			if node.board[x,y] != 0:
				node_move = node
		#Registra o nó da árvore como o nó movido
		self.root = node_move

	#Usar esse se for um movimento da IA, pois a busca retorna a posição da movimentação dentro da lista
	#de filhos do nó, diferente da busca por x e y caso seja o jogador humano
	def registerMoveIA(self, position):
		self.root = self.root.children[position]

	def searchBestMove(self):
		_, position = self.root.searchInTree()
		return position

	# Retorna matriz que representa o board atual
	def getBoard(self):
		return self.root.board

	# Verifica se o board atual representa uma vitória
	# derrota ou empate.
	def getBoardState(self):
		state = self.root.board

		# Verifica linhas
		for i in range(0, 3):
			if(state[i,0] != 0 and (state[i,0] == state[i,1] == state[i,2])):
				return state[i,0], True

		# Verifica colunas
		for j in range(0, 3):
			if(state[0,j] != 0 and (state[0,j] == state[1,j] == state[2,j])):
				return state[0,i], True

		# Verifica diagonais
		if(state[0,0] != 0 and (state[0,0] == state[1,1] == state[2,2])):
			return state[0,0], True
		if(state[0,2] != 0 and (state[0,2] == state[1,1] == state[2,0])):
			return state[0,2], True			

		# Verifica empate
		for i in range(0, 3):
			for j in range(0, 3):
				if(state[i,j] == 0):
					return 0, False # Se ainda existe jogada disponível

		# Se não há ganhadores nem jogadas disponíveis,
		# retorna empate
		return 0, True

	# Verifica se movimento é válido
	def isValidMove(self, pos):
		state = self.root.board
		if(state[pos[0],pos[1]] != 0):
			return False
		else:
			return True

	def printBoard(self):
		board = self.root.board
		print(' {} | {} | {} \n'.format(board[0,0],board[0,1],board[0,2])
			+'-----------\n'
			+' {} | {} | {} \n'.format(board[1,0],board[1,1],board[1,2])
			+'-----------\n'
			+' {} | {} | {} \n'.format(board[2,0],board[2,1],board[2,2]))