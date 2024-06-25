#   Carlos Salas Rosales Jr
#   AI Project 2
#   
#   I have neither given nor received unauthorized aid on this program as per the collaboration policy

from asyncio.windows_events import NULL
from json.encoder import INFINITY
from board import Board
from gamestate import GameState
from player import Player


class State(object):
    """
    Represents game state
    """
    def __init__(self, board, player):
        self.board = board
        self.player = player
        

    def __str__(self):
        return f'State: {self.board}, player={self.player}'

    def __repr__(self):
        return f'State({self.board}, {self.player})'

#Returns true if state is terminal, false if not
def isTerminal(state):
    if state.get_game_state() == GameState.IN_PROGRESS: return False
    return True

#Evaluates worth of a non-terminal state. Pos = max winning, neg = min winning. 
#Greater values correspond to more likelilhood of winning
def eval(state, winNum):
    value = 0
    ones = 0
    fives = 0
    tens = 0
    rows = state.to_2d_string().split("\n")
    matrix = [row.rstrip().split(" ") for row in rows[:len(rows) - 1]]
    # if player == max (X)
    if state.get_player_to_move_next() == Player.MIN:
        oS = False
        xS = 0
        for r in range(state.get_rows()):
            oS = False
            xS = 0
            colSlice = matrix[r: winNum + 1]

            for i in colSlice:
                #for works
                if i == "O": 
                    oS = True
                    break
                elif i == "X":
                    xS += 1                 
            
            if oS: value += 0
            elif xS == 3: tens += 10
            elif xS == 2: fives += 5
            elif xS == 1: ones += 1
            for c in range(state.get_cols() - winNum):
                oS = False
                xS = 0
                rowSlice = matrix[r][c: winNum + 1]

                for i in rowSlice:
                    #for works
                    if i == "O": 
                        oS = True
                        break
                    elif i == "X":
                        xS += 1 

                if oS: value += 0
                elif xS == 3: tens += 10
                elif xS == 2: fives += 5
                elif xS == 1: ones += 1
                
        value = ones + fives + tens
                
    #if player == min (O)
    elif state.get_player_to_move_next() == Player.MAX:
        for r in range(state.get_rows()):
            xS = False
            oS = 0
            colSlice = matrix[r: winNum + 1]

            for i in colSlice:
                #for works
                if i == "X": 
                    xS = True
                    break
                elif i == "O":
                    oS += 1 
            
            if xS: value += 0
            elif oS == 3: tens += 10
            elif oS == 2: fives += 5
            elif oS == 1: ones += 1

            for c in range(1, state.get_cols() - winNum):
                xS = False
                oS = 0

                rowSlice = matrix[r][c: winNum + 1]

                for i in rowSlice:
                    #for works
                    if i == "X": 
                        xS = True
                        break
                    elif i == "O":
                        oS += 1 

                if oS: value += 0
                elif xS == 3: tens += 10
                elif xS == 2: fives += 5
                elif xS == 1: ones += 1
                #if matrix[r][c] == "O" and matrix[r]:
                 #   pass
                #counts each 2 Os in a row that can become 4 in a row as 5
                #elif
                #counts each O piece that can become 4 in a row as 1
                #for i in range(winNum):

                 #   if matrix[r][c] == "O" and matrix[r][c + i] != "X":
                  #      ones += 1
        value = -1 * (ones + fives + tens)
    return value

#Returns the worth of a terminal state. pos = max win, neg = min win, 0 = draw
def utility(state):
    gameState = state.get_game_state()
    rows = state.get_rows()
    cols = state.get_cols()
    moves = state.get_number_of_moves()
    value = 0 

    #If min wins, value = -int(10000.0 * rows * cols / moves)
    if gameState == GameState.MIN_WIN:
        value = -int(10000.0 * rows * cols / moves)
    #If max wins, value = int(10000.0 * rows * cols / moves)
    if gameState == GameState.MAX_WIN:
        value = int(10000.0 * rows * cols / moves)
    
    return value

level = 0       #global variable for isCutoff

#returns true or false
def isCutoff(state, depth):
    pass

prunes = 0      #global variable for alphaBetaHeuristic() & alphaBetaSearch()


#Code for part C
def alphaBetaHeuristic(state, alpha, beta, depth, winNum, table):
    global prunes       #Instantiates global variable
    global level        #Instantiates global variable
    if state.__str__() in table:
        return [table[state], prunes]

    elif isTerminal(state):
        util = utility(state)
        info = (util, NULL)
        table[state.__str__()] = info     #adds state to transposition table along with info
        return [info, prunes]

    elif level >= depth:
        heuristic = eval(state, winNum)
        info = (heuristic, NULL)
        table[state.__str__()] = info
        return [info, prunes]

    #if player == min
    elif state.get_player_to_move_next() == Player.MAX:
        v = -INFINITY
        bestMove = NULL

        for i in range(state.get_cols()):
            #skip move if column full
            if state.is_column_full(i): continue

            childState = state.make_move(i)
            level += 1
            childInfo = alphaBetaHeuristic(childState, alpha, beta, depth + 1, winNum, table)[0]
            v2 = childInfo[0]
            #updates v and alpha if v2 > v
            if v2 > v:
                v = v2
                bestMove = i
                alpha = max(alpha, v)
            #prune
            if v >= beta:
                prunes += 1
                #level += 1
                return [(v, bestMove), prunes]

        info = (v, bestMove)
        table[state.__str__()] = info
        #level += 1
        return [info, prunes]

    #if player == Max
    elif state.get_player_to_move_next() == Player.MIN:
        v = INFINITY
        bestMove = NULL

        #go through each move
        for i in range(state.get_cols()):
            #skip move if column full
            if state.is_column_full(i): continue
            childState = state.make_move(i)
            level += 1
            childInfo = alphaBetaHeuristic(childState, alpha, beta, depth + 1, winNum, table)[0]
            v2 = childInfo[0]
            #updates v and beta if v2 < v
            if v2 < v:
                v = v2
                bestMove = i 
                beta = min(beta, v)
            #prunes
            if v <= alpha:
                prunes += 1
                #level += 1
                return [(v, bestMove), prunes]
                
        info = (v, bestMove)
        table[state.__str__()] = info
        #level += 1
        return [info, prunes]

#Does alpha beta pruning
#Code for part B
def alphaBetaSearch(state, alpha, beta, table):
    global prunes

    if state.__str__() in table:
        return [table[state.__str__()], prunes]

    elif isTerminal(state):
        util = utility(state)
        info = (util, NULL)
        table[state.__str__()] = info 
        return [info, prunes]

    #if current player is min
    elif state.get_player_to_move_next() == Player.MAX:
        v = -INFINITY
        bestMove = NULL

        #Goes through possible moves
        for i in range(state.get_cols()):
            #skip move if column full
            if state.is_column_full(i): continue

            childState = state.make_move(i)
            childInfo = alphaBetaSearch(childState, alpha, beta, table)[0]
            v2 = childInfo[0]
            #updates v and alpha if v2> v
            if v2 > v:
                v = v2
                bestMove = i
                alpha = max(alpha, v)
            #prune tree if v >= beta
            if v >= beta:
                prunes += 1
                return [(v, bestMove), prunes]
        info = (v, bestMove)
        table[state.__str__()] = info
        return [info, prunes]
    
    #if current player is max
    elif state.get_player_to_move_next() == Player.MIN:
        v = INFINITY
        bestMove = NULL

        #Go through each move
        for i in range(state.get_cols()):
            #skip move if column is ful
            if state.is_column_full(i): continue

            childState = state.make_move(i)
            childInfo = alphaBetaSearch(childState, alpha, beta, table)[0]
            v2 = childInfo[0]
            #update v and beta if v2<v
            if v2 < v:
                v = v2
                bestMove = i
                beta = min(beta, v)
            #prune
            if v <= alpha:
                prunes += 1
                return [(v, bestMove), prunes]
        info = (v, bestMove)
        table[state.__str__()] = info
        return [info, prunes]

#Code for part A
def miniMaxSearch(state, table):
    if state.__str__() in table:
        return table[state.__str__()]

    elif isTerminal(state):
        util = utility(state)
        info = (util, NULL)                 #minimaxInfo object stored as tuple
        table[state.__str__()] = info      #state added to transposition table
        return info                         #Returns info

    #If current player is min
    elif state.get_player_to_move_next() == Player.MAX:
        v = -INFINITY
        bestMove = NULL

        #Goes through possible moves
        for i in range(state.get_cols()): 

            #skips move if column is full
            if state.is_column_full(i):
                continue
                        
            childState = state.make_move(i)
            childInfo = miniMaxSearch(childState, table)
            v2 = childInfo[0]

            #Updates v and sets move as best if v2 is greater than v
            if v2 > v:
                v = v2
                bestMove = i

        info = (v, bestMove)                #minimaxInfo obj stored as tuple
        table[state.__str__()] = info      #state added to transposition table, with info
        return info                         #Returns info

    #If current player is Max
    elif state.get_player_to_move_next() == Player.MIN:
        v = INFINITY
        bestMove = NULL

        #Go through possible moves
        for i in range(state.get_cols()):
            
            #skips move if column is full
            if state.is_column_full(i):
                continue

            childState = state.make_move(i)
            childInfo = miniMaxSearch(childState, table)
            v2 = childInfo[0]

            #Updates v and sets move as best if v2 is less than v
            if v2 < v:
                v = v2
                bestMove = i

        info = (v, bestMove)                #minimaxInfo obj stored as tuple
        table[state.__str__()] = info      #state added to transposition table, with info
        return info                         #Returns info

def main():
    global prunes
    game = input("Hi! Would you like to run part A, B or C? (0 to quit) ")      #part to run    

    while game != "":

        deb = input("Would you like me to include debugging info? (y/n) ")
        row = int(input("Enter rows: "))
        col = int(input("Enter columns: "))
        winNum = int(input ("Enter number in a row to win: "))

        board = Board(row, col, winNum)     #Creates board to user's specifications
        transTable = {}                     #Creates transposition table as dictionary (empty for now)

        print()

        if game == "A" or game == "a":
            info = miniMaxSearch(board, transTable)
            result = info[0]
            print("Transposition table has  " + str(transTable.__len__()) + " states.")    #prints size of transposition table
            
            #Handles printing out results
            if result > 0: print("1st player has a garunteed win, assuming perfect play.")
            elif result == 0: print("Game will result in a tie, assuming perfect play")
            elif result < 0: print("2nd player has a garunteed win, assuming perfect play")

            if deb == "y":
                print("Transposition table: ")
                print(transTable)
            print()
            playGame(board, transTable, game, 0, winNum)

        elif game == "B" or game == "b":
            prunes = 0
            info = alphaBetaSearch(board, -INFINITY, INFINITY, transTable)
            result = info[0][0]
            print("Transposition table has " + str(transTable.__len__()) + " states.")

            #Handles printing out results
            if result > 0: print("1st player has a garunteed win, assuming perfect play.")
            elif result == 0: print("Game will result in a tie, assuming perfect play")
            elif result < 0: print("2nd player has a garunteed win, assuming perfect play")

            print(str(info[1]) + " prunings")

            #prints debugging info
            if deb == "y":
                print("Transposition table: ")
                print(transTable)
            print()
            playGame(board, transTable, game, 0, winNum)

        elif game == "C" or game == "c":
            prunes = 0
            depth = int(input("How far should I look ahead (depth)? "))
            info = alphaBetaHeuristic(board, -INFINITY, INFINITY, depth, winNum, transTable)
            result = info[0][0]
            print("Transposition table has " + str(transTable.__len__()) + " states.")

            #prints debugging info
            if deb == "y":
                print("Transposition table: ")
                print(transTable)
            print()
            playGame(board, transTable, game, depth, winNum)
        elif game == "0": break
        else:
            game = input("Sorry, I don't understand. Would you like to run part A, B or C? (0 to quit) ")
            if game == "0": break
            continue
        game = input("Would you like to run part A, B, or C? (0 to quit) ")     #update game so no loop-ti-doop
        if game == "0": break

def playGame(board, table, mode, depth, winNum):
    agent = input("Who plays first? (1 = human, 2 = computer) ")
    stateValue = table[board.__str__()][0]
    bestMove = table[board.__str__()][1]
    player = "Max"

    print(board.to_2d_string())
    print("Minimax value for this state: " + str(stateValue) + " Best move: " + str(bestMove))
    print("It's " + player + "'s turn!")
    print()

    while board.get_game_state() == GameState.IN_PROGRESS:
        
        if agent == "1":
            move = int(input("Enter move: "))   #Gets player move
            board = board.make_move(move)

            if board.__str__() not in table and (mode == "B" or mode == "b"):
                print(board.to_2d_string())
                print("This is a state that was previously pruned. Re-running alphabeta from here.")
                table = {}
                info = alphaBetaSearch(board, -INFINITY, INFINITY, table)

            elif board.__str__() not in table and (mode == "C" or mode == "c"):
                print(board.to_2d_string())
                print("This is a state that was previously pruned. Re-running alphabeta from here.")
                table = {}
                info = alphaBetaHeuristic(board, -INFINITY, INFINITY, depth, winNum, table)

            stateValue = table[board.__str__()][0]
            bestMove = table[board.__str__()][1] 
            print(board.to_2d_string())         #prints board
            print("Minimax value for this state: " + str(stateValue) + " Best move: " + str(bestMove))
            agent = "2"
            if player == "Max": 
                player = "Min"
                print("It's " + player + "'s turn!")
            elif player == "Min": 
                player = "Max"
                print("It's " + player + "'s turn!")

        elif agent == "2":
            print("Computer chooses move " + str(bestMove))
            board = board.make_move(bestMove)

            if board.__str__() not in table and (mode == "b" or mode == "B"):
                print(board.to_2d_string())
                print("This is a state that was previously pruned. Re-running alphabeta from here.")
                table = {}
                info = alphaBetaSearch(board, -INFINITY, INFINITY, table)
                
            elif board.__str__() not in table and (mode == "C" or mode == "c"):
                print(board.to_2d_string())
                print("This is a state that was previously pruned. Re-running alphabeta from here.")
                table = {}
                info = alphaBetaHeuristic(board, -INFINITY, INFINITY, depth, winNum, table)
                
            stateValue = table[board.__str__()][0]
            bestMove = table[board.__str__()][1]
            print(board.to_2d_string())
            print("Minimax value for this state: " + str(stateValue) + " Best move: " + str(bestMove))
            print()
            agent = "1"
            if player == "Max": 
                player = "Min"
                print("It's " + player + "'s turn!")
            elif player == "Min": 
                player = "Max"
                print("It's " + player + "'s turn!")

    print("Game Over!")
    print(board.to_2d_string())
    if board.get_game_state() == GameState.TIE:
        print("This game is a tie!")
    else:
        if player == "Min": player = "Max"
        if player == "Max": player = "Min"
        if agent == "2": agent = "(human)"
        if agent == "1": agent = "(computer)"
        print("The winner is " + player + " " + agent)

    


main()