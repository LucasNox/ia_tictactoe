import sys
import numpy as np
from tree import MinMaxTree

# Exibição do resultado do jogo
def result(player, ai):
	if(player):
		print("\n--------------- RESULTADO ---------------\n")
		print("|\tGanhador: Jogador")
		print("|\tParabéns! Você ganhou da IA!")
		print("\n-----------------------------------------\n")
	elif(ai):
		print("\n--------------- RESULTADO ---------------\n")
		print("|\tGanhador: PC")
		print("|\tQue pena, parece que você perdeu.")
		print("\n-----------------------------------------\n")
	else:
		print("\n--------------- RESULTADO ---------------\n")
		print("|\tEmpate!")
		print("|\tVocê empatou com o computador.")
		print("\n-----------------------------------------\n")

# Exibição e execução do turno da IA
def ia_move(tree, starting):
	# Registra board antes da IA mover
	start = tree.getBoard()
	# Realiza melhor movimento
	tree.registerMoveIA(tree.searchBestMove())
	# Registra board após movimento
	end = tree.getBoard()

	diff = np.subtract(start, end)
	pos = np.array(np.argwhere(diff)[0])

	print("--------------- TURNO: IA ---------------\n")
	print("Linha: " + str(pos[0]))
	print("Coluna: " + str(pos[1]))
	print("\n-----------------------------------------")
	return tree.getBoardState()

# Exibição e execução do turno do jogador
def player_move(tree, starting):
	row = -1
	column = -1

	while((row < 0 or row > 2) or (column < 0 or column > 2)):
		print("------------- TURNO: JOGADOR ------------\n")
		row = int(input("Linha (0-2): "))
		column = int(input("Coluna (0-2): "))
		print("\n-----------------------------------------")

		if((row >= 0 and row <= 2) and (column >= 0 and column <= 2)):
			if(tree.isValidMove((row,column))):
				tree.registerMove(row,column)
				return tree.getBoardState()
			else:
				print("\n-----------------------------------------")
				print("\tJOGADA INVÁLIDA")
				print("-----------------------------------------\n")
				row = -1
				column = -1
		else:
			print("\n-----------------------------------------")
			print("\tJOGADA INVÁLIDA")
			print("-----------------------------------------\n")
			row = -1
			column = -1

# Início e loop de execução do jogo
def play(tree):
	done = False
	order = 4

	while(order < 1 or order > 3):
		print("------------ ORDEM DE JOGADA ------------\n")
		print("Opções:")
		print("[1] Jogador começa")
		print("[2] Computador começa")
		print("[3] Cancelar")
		op = int(input("Seleção: "))
		print("\n-----------------------------------------")

		# Jogador começa
		if(op == 1):
			# Loop do jogo
			while(not done):
				tree.printBoard()
				winner, done = player_move(tree, True)
				if(done):
					break
				tree.printBoard()
				winner, done = ia_move(tree, False)

			tree.printBoard()
			if(winner == 1):
				result(True, False)
			elif(winner == 2):
				result(False, True)
			else:
				result(False, False)
		# Computador começa
		elif(op == 2):
			# Loop do jogo
			while(not done):
				tree.printBoard()
				winner, done = ia_move(tree, True)
				if(done):
					break
				tree.printBoard()
				winner, done = player_move(tree, False)

			tree.printBoard()
			if(winner == 1):
				result(False, True)
			elif(winner == 2):
				result(True, False)
			else:
				result(False, False)
		# Cancelar
		elif(op == 3):
			return op

		if(done):
			print("\nOpções:")
			print("[1] Novo jogo")
			print("[2] Sair")
			op = int(input("Seleção: "))
			print("\n-----------------------------------------")
			if(op == 1):
				tree.restart()
				done = False
				order = 4
			elif(op == 2):
				return op

def main():
	op = 3

	while(op < 1 or op > 2):
		print("------------- JOGO DA VELHA -------------\n")
		print("Opções:")
		print("[1] Novo jogo")
		print("[2] Sair")
		op = int(input("Seleção: "))
		print("\n-----------------------------------------")

		if(op == 1):
			tree = MinMaxTree(True, './minmaxtree.bin')
			op = play(tree)
		elif(op == 2):
			sys.exit()

if __name__ == "__main__":
	main()

