#Copyright CB, 2021
#config
obvious_small_wins = True	#Fills small boards with winning symbol.
player_symbols = ["X", "O"]
always_three_in_a_row = False	#Determines weather to always count 3 in a row as a win. Only applicible to games with more than 2 players. When false, board_side_length in a row is considered a win.
##TODO: responsive board size for infinite players
#setup
import string
board = []	#[0] is not visible, & represents the overall state of the board. [x][0] is also invisible & represents the overall state of board x.
board_side_length = len(player_symbols)+1
board_length = (board_side_length**2)+1
for a in range(board_length):	#Fill board with boards filled with spaces.
	tmp_board = []
	for b in range(board_length):
		tmp_board.append(" ")
	board.append(tmp_board)
end = False	#Is the game over?
current_turn = 0	#The index of the current player in player_symbols
big_move = 0	#The player's input for the desired board to mark. Potentially non-numerical index.
small_move = 0	#The player's input for the desired cell to mark. Potentally non-numerical index.
big_move_index = 0	#Numerical index equivilent of big_move.
small_move_index = 0	#Numerical index of small_move.
win_print = ""	#A status message telling the players that a board has been won, displayed after the completion of a turn, as necessary.
end_print = ""	#A status message informing players of the final outcome of the game, displayed at the end of the game.
print("Copyright CB, 2021\n\nThis is a turn-based strategy game in which each player has influence over their opponent's next turn. This game is known as Ultimate Tic Tac Toe because it is played on a large Tic Tac Toe board (a 3x3 grid) in which each cell of the board contains a smaller Tic Tac Toe board. The objective is to win three boards which form a line (horizontal, vertical, or diagonal). A board is won by marking three cells which form a line. As in regular Tic Tac Toe, both players take turns marking cells of the board. During the first turn, the player is free to mark any of the 81 cells. On most subsequent turns (including player 2's first turn), the player must mark the board that corresponds to the cell in which the previous mark was made. For example, if player 1 marked cell 7 of board 3, player 2 would be required to make their next mark in board 7. Both players are subject to this, so if player 2 then marked cell 2 (of board 7), player 1 is required to make the next mark in board 2. Neither player may mark a completed board (a board which is full or won by either player). If your opponent's previous mark requires you to do so, you must disregard that requirement & choose an incomplete board to mark.\n")
#functions
def check_full(check_board_index): #Checks if the given board is full.
	global board, end, end_print
	if " " in board[check_board_index][1:]:	#Checks for any spaces in the visible section.
		return False	#If there are any spaces, it's not full.
	board[0][check_board_index] = ""
	if check_board_index == 0:
		end = True
		end_print = "All boards are full. It's a tie."
	else:
		check_full(0)	#Check if that filled the main board.
	return True
def handle_win(win_board_index):
	global board, player_symbols, current_turn, end, win_print, end_print
	board[0][win_board_index] = player_symbols[current_turn]
	if obvious_small_wins:
		for a in range(len(board[win_board_index])):	#Turns every space to the winner's symbol. Uses range() because direct iteration is immutable.
			board[win_board_index][a] = player_symbols[current_turn]
	if win_board_index == 0:
		end = True
		end_print = "Player " + player_symbols[current_turn] + " wins!"
	else:
		win_print = "Player " + player_symbols[current_turn] + " wins board " + str(win_board_index) + "."
		if not check_win(0):
			check_full(0)
	return True
def check_win(check_board_index):
	global board, end
	if always_three_in_a_row:
	for a in range(1, board_length-board_side_length+1, board_side_length):
		if board[check_board_index][a] == board[check_board_index][a+1] == board[check_board_index][a+2] == player_symbols[current_turn]:
			return handle_win(check_board_index)
	for b in range(1, 4):
		if board[check_board_index][b] == board[check_board_index][b+3] == board[check_board_index][b+6] == player_symbols[current_turn]:
			handle_win(check_board_index)
			return True
	if ((board[check_board_index][1] == board[check_board_index][5] == board[check_board_index][9] == player_symbols[current_turn]) or (board[check_board_index][3] == board[check_board_index][5] == board[check_board_index][7] == player_symbols[current_turn])):
		handle_win(check_board_index)
		return True
	check_full(check_board_index)
	return False
def get_input(big_index, initial_prompt, illegal_reprompt):
	#TODO: back option
	global board, board_length
	new_input = 0
	while new_input == 0:
		new_input = input(initial_prompt)
		if len(new_input) != 1:
			new_input = 0
			print("You must enter one character.")
		elif new_input not in string.printable[1:board_length]:
			print("You must enter a value from the numbered grid above. (case sensitive)")
			new_input = 0
		elif board[big_index][string.printable.find(new_input)] != " ":
			new_input = 0
			print(illegal_reprompt)
		else:
			return new_input
#main loop
while not(end):
	for a in range(1, board_length, board_side_length):
		for b in range(board_side_length):
			print(string.printable[a+b], end = "")
			if b != (board_side_length - 1):
				print("|", end = "")
			elif a < (board_length - board_side_length):
				print()
				for c in range(board_side_length-1):
					print("-+", end = "")
				print("-")
	print("\n")
	big_move = small_move
	big_move_index = small_move_index
	small_move = 0
	small_move_index = 0
	if win_print:
		print(win_print)
		win_print = ""
	if (big_move == 0) or (board[0][big_move_index] != " "):
		big_move = get_input(0, "Player " + player_symbols[current_turn] + ", which board will you be marking? ", "That board is already complete. You must choose a board containing legal moves.")
	big_move_index = string.printable.find(big_move)
	small_move = get_input(big_move_index, "Player " + player_symbols[current_turn] + ", which cell of board " + str(big_move) + " will you be marking? ", "That cell is taken. You must choose an empty cell.")
	small_move_index = string.printable.find(small_move)
	board[big_move_index][small_move_index] = player_symbols[current_turn]
	check_win(big_move_index)
	print()
	if not obvious_small_wins:
		for a in range(1, 8, 3):
			for b in range(3):
				if board[0][a+b] == "":
					print(" ", end = "")
				else:
					print(board[0][a+b], end="")
				if b != 2:
					print("|", end = "")
				elif a != 7:
					print("\n-+-+-")
		print("\n")
	for a in range(1, 8, 3):
		for b in range(1, 8, 3):
			for c in range(3):
				for d in range(3):
					print(board[a+c][b+d], end = "")
					if d != 2:
						print("|", end = "")
					elif c != 2:
						print(" || ", end = "")
					elif (b != 7):
						print("\n-+-+- || -+-+- || -+-+-")
					if (a != 7) and (b == 7) and (c == 2) and (d == 2):
						print("\n      ||       ||\n------++-------++------\n------++-------++------\n      ||       ||")
	print("\n")
	current_turn = not current_turn
print(end_print)
input("Press return to exit. ")
#Ultimate Tac Tac Toe is Public Domain.