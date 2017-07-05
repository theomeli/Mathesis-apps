# mathesis.cup.gr course with title "Introduction to Python"
# Project: Tic Tac Toe

import random
import time

marker = {'Player 1': 'X', 'Player 2': 'O', }

def display_board(board): 
    #it prints the tic tac toe's state
    cell = 0
    for i in range(3):
        firstLine = '+'
        for j in range(53):
            firstLine += '-'
        firstLine += '+'

        secondLine = ''
        for j in range(3):
            cell += 1
            secondLine += '|' + str(cell)
            for k in range(15):
                secondLine += ' '
        secondLine += '|'

        thirdLine = ''
        for j in range(3):
            thirdLine += '|'
            for k in range(8):
                thirdLine += ' '
            c = 3 * (i - 1) + j - 6
            thirdLine += board[c]
            for k in range(7):
                thirdLine += ' '
        thirdLine += '|'

        fourthLine = ''
        for j in range(3):
            fourthLine += '|'
            for k in range(16):
                fourthLine += ' '
        fourthLine += '|'

        fifthLine = '\n+'
        for j in range(53):
            fifthLine += '-'
        fifthLine += '+\n'

        print(firstLine, '\n', secondLine, '\n', thirdLine, '\n', fourthLine, fifthLine)

def choose_first():
    # it drews which player is going to play first
    # it returns 'Player 1' or 'Player 2'
    player = random.randint(1, 2)
    return 'Player ' + str(player)

def display_score(score):
    # it prints the final score
    print('FINAL SCORE\nPlayer 1: {}\nPlayer 2: {}'.format(score.get('Player 1', 0), score.get('Player 2', 0)))

def place_marker(board, marker, position):
    # it places the variable marker into board's position
    board[position] = marker

def win_check(board,mark):
    # it returns True if symbol mark has formed a tic tac toe
    return (board[1] == mark and board[5] == mark and board[9] == mark) or \
           (board[3] == mark and board[5] == mark and board[7] == mark) or \
           (board[2] == mark and board[5] == mark and board[8] == mark) or \
           (board[4] == mark and board[5] == mark and board[6] == mark) or \
           (board[7] == mark and board[8] == mark and board[9] == mark) or \
           (board[1] == mark and board[2] == mark and board[3] == mark) or \
           (board[1] == mark and board[4] == mark and board[7] == mark) or \
           (board[3] == mark and board[6] == mark and board[9] == mark)

def board_check(board):
    # it returns False if there are still empty squares
    # and True in the opposite case.
    board[0] = '0'
    for b in board:
        if b == ' ':
            return False
    return True
 
def player_choice(board, turn):
    # The player that variable turn represents, chooses a square
    # It returns an integer in the space [1, 9]
    # Here will be checked if there is already a value inside the square
    while True:
        number = input(turn + '[ ' + marker[turn] + ' ]: Choose a square: (1-9) ')
        # it is checked if input is an int
        try:
            numberInt = int(number)
        except:
            continue
        else:
            # it is checked if it belongs in the allowed space
            if numberInt < 1 or numberInt > 9:
                continue
            number = int(number)
            # finally it is checked if the corresponding cell is empty
            if board[number] == ' ':
                return number
            else:
                print('The chosen square is occupied')

def replay():
    # it asks the user if he wants to play again and it returns True if it is so 
    while True:
        ans = input('Do you want to play again? (Yes/No)').lower().strip()
        if ans == 'yes':
            return True
        elif ans == 'no':
            return False

def next_player(turn):
    # it returns the next player that plays
    split = turn.split()
    if split[1] == '1':
        return split[0] + ' 2'
    return split[0] + ' 1'

def main():
    score = {} # a dictionary with the players' score
    print('Let\'s start!\nBecomes lottery ', end = '')
    for t in range(10):
        print(".", flush='True', end=' ')
        time.sleep(0.2)
    print()
    # variable turn is referred to the player that plays 
    turn = choose_first() 
    print("\n" + turn + ' plays first.')
    # variable first is referred to the player that played first
    first = turn 
    game_round = 1 # game round
    while True:
        # new game
        theBoard = [' '] * 10 
        game_on = True  # game starts
        while game_on:
            display_board(theBoard) # display tic tac toe
            # player turn chooses a position
            position = player_choice(theBoard, turn) 
            # is placed his choice
            place_marker(theBoard, marker[turn], position)
            if win_check(theBoard, marker[turn]): # a check if he has won
                display_board(theBoard)
                print(turn + ' won')
                score[turn] = score.get(turn, 0) + 1
                game_on = False
            # a check if tableau has filled without a winner
            elif board_check(theBoard): 
                display_board(theBoard)
                print('Draw!')
                game_on = False
            else: # else we continue with next player's move
                turn = next_player(turn)
        if not replay():
            ending = ''
            if game_round>1 : ending = 's'
            print("After {} round{}".format(game_round, ending))
            display_score(score) # exit ... final score
            break
        else :
            game_round += 1
            # in next game the other player begins
            turn = next_player(first) 
            first = turn
main()
