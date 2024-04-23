import numpy as np
from operator import itemgetter
#import time
#import sys

class AIPlayer:
    def __init__(self, player_number):
        self.player_number = player_number
        self.type = 'ai'
        self.player_string = 'Player {}:ai'.format(player_number)


    def countv(self, board, num, player_num):
        nwins = 0 
        wc = '{0}' * num 
        wc = wc.format(player_num)
        sc = lambda a: ''.join(a.astype(str))

        def countr(b):
            count = 0
            for row in b:
                if wc in sc(row):
                    count += sc(row).count(wc) 
            return count

        def countc(b):
            return countr(b.T)

        def countcrs(b):
            count = 0 
            for op in [None, np.fliplr]:
                op_board = op(b) if op else b
                main_diag = np.diagonal(op_board, offset=0).astype(np.int64)
                if wc in sc(main_diag):
                    count += sc(main_diag).count(wc) 

                for i in range(1, b.shape[1]-3):
                    for offset in [i, -i]:
                        diag = np.diagonal(op_board, offset=offset)
                        diag = sc(diag.astype(np.int64))
                        if wc in diag:
                            count += diag.count(wc) 
            return count 
        nwins = countr(board) + countc(board) + countcrs(board) 
        return nwins

    def possiblevalidMoves(self, board):
        move = []
        no_column=7
        no_rows=5
        for col in range(no_column):
            for row in range(no_rows,-1,-1):
                if board[row][col] == 0:
                    move.append([row, col])
                    break
        return move

    def get_alpha_beta_move(self, board):
        """
        Given the current state of the board, return the next move based on
        the alpha-beta pruning algorithm

        This will play against either itself or a human player

        INPUTS:
        board - a numpy array containing the state of the board using the
                following encoding:
                - the board maintains its same two dimensions
                    - row 0 is the top of the board and so is
                      the last row filled
                - spaces that are unoccupied are marked as 0
                - spaces that are occupied by player 1 have a 1 in them
                - spaces that are occupied by player 2 have a 2 in them

        RETURNS:
        The 0 based index of the column that represents the next move
        """
        values = []
        def alphabeta( board, depth, alpha, beta, player, player_2):
            for row, col in self.possiblevalidMoves(board):
                board[row][col] = player
                alpha = max(alpha, min_value(board,alpha, beta,depth + 1 , player, player_2))
                #print('alpha = ' + str(alpha))
                values.append((alpha,col))
                board[row][col] = 0
            #print("Key = itemgetter(1)  " + str(itemgetter(1)))
            maxvalue = (max(values,key=itemgetter(1))[0])
            #print("MaxValue = " + str(maxvalue))
            for item in values:
                if maxvalue in item:
                    maxindex = item[1]
                    break
                
            return (maxindex)

        def min_value(board,alpha,beta,depth,player, player_2):
            #start_timcle = time.time()
            time_limit = 1
            valid_moves = self.possiblevalidMoves(board)
            if(depth == 4 or not valid_moves):
                return (self.evaluation_function(board))
            for row,col in valid_moves:
                board[row][col] = player_2 
                result = max_value(board, alpha, beta, depth+1, player, player_2)
                beta = min (beta, result)
                board[row][col] = 0
                if beta<= alpha:
                    return beta 
                '''if time.time() - start_time >= time_limit:
                    #print("TimeLimit Reached::"+ str(time.time()-start_time))
                    continue'''
            return beta
        def max_value(board,alpha, beta, depth, player, player_2):
            #start_time = time.time()
            time_limit = 1
            valid_moves = self.possiblevalidMoves(board)
            if(depth == 4 or not valid_moves):
                return (self.evaluation_function(board))
            for row, col in valid_moves:
                board[row][col] = player 
                result = min_value(board,alpha,beta,depth+1, player, player_2)
                alpha = max(alpha, result)
                board[row][col] = 0
                if alpha >= beta:
                    return alpha
                '''if time.time() - start_time >= time_limit:
                    #print('Inside max_value')
                    #print("TimeLimit Reached::"+ str(time.time()-start_time))
                    continue'''
            return alpha

        player = self.player_number
        #print("Player : " + str(player))
        if (player == 1): 
            player_2 = 2
        else: 
            player_2 = 1
        return (alphabeta(board, 0, -float('inf'), float('inf'), player, player_2)) 
        raise NotImplementedError('Whoops I don\'t know what to do')

    def get_expectimax_move(self, board):
        """
        Given the current state of the board, return the next move based on
        the expectimax algorithm.

        This will play against the random player, who chooses any valid move
        with equal probability

        INPUTS:
        board - a numpy array containing the state of the board using the
                following encoding:
                - the board maintains its same two dimensions
                    - row 0 is the top of the board and so is
                      the last row filled
                - spaces that are unoccupied are marked as 0
                - spaces that are occupied by player 1 have a 1 in them
                - spaces that are occupied by player 2 have a 2 in them

        RETURNS:
        The 0 based index of the column that represents the next move
        """

        values = []
        def expectimax(board, depth, player, player_2):
            alpha = -float('inf')
            for row, col in self.possiblevalidMoves(board):
                board[row][col] = player
                alpha = max(alpha, exp_val(board,depth - 1 , player, player_2))
                #print('alpha + ==' + str(alpha))
                values.append((alpha,col))
                board[row][col] = 0
            
            #print("Key = itemgetter(1) in expectimax " + str(itemgetter(1)))
            maxvalue = (max(values,key=itemgetter(1))[0]) 
            for item in values:
                if maxvalue in item:
                    maxindex = item[1]
                    break

            return (maxindex)
        def max_val(board, depth, player,player_2):
            valid_moves = self.possiblevalidMoves(board)
            if (depth == 0 or not valid_moves): 
                return (self.evaluation_function(board))
            bestValue = -float('inf')
            for row,col in valid_moves:
                board[row][col] = player 
                val = exp_val(board, depth - 1, player, player_2)
                bestValue = max(bestValue, val);
                #print('bestValue + ==' + str(bestValue))

            return bestValue
        def exp_val(board, depth, player, player_2): 
            valid_moves = self.possiblevalidMoves(board)
            lengthmoves = len(valid_moves)
            print (lengthmoves)
            if (depth == 0 or not valid_moves): 
                return (self.evaluation_function(board))
            expectedValue = 0
            for row,col in valid_moves:
                board[row][col] = player_2 
                val = max_val(board , depth-1, player, player_2)
                expectedValue += val


            return (expectedValue/lengthmoves)

        player = self.player_number
        if (player == 1): 
            player_2 = 2
        else: 
            player_2 = 1
        return (expectimax(board, 8 , player, player_2))

        raise NotImplementedError('Whoops I don\'t know what to do')




    def evaluation_function(self, board):
        """
        Given the current stat of the board, return the scalar value that 
        represents the evaluation function for the current player
       
        INPUTS:
        board - a numpy array containing the state of the board using the
                following encoding:
                - the board maintains its same two dimensions
                    - row 0 is the top of the board and so is
                      the last row filled
                - spaces that are unoccupied are marked as 0
                - spaces that are occupied by player 1 have a 1 in them
                - spaces that are occupied by player 2 have a 2 in them

        RETURNS:
        The utility value for the current board
        """
        utility_value = 0
        p = self.player_number
        if (p == 1): 
            p2 = 2
        else: 
            p2 = 1

        utility_value = self.countv( board, 4, p) * 1000
        utility_value += self.countv( board, 3, p) * 100
        utility_value += self.countv( board, 2, p) * 10
        #print("outcome + " + str(outcome) + " " + str(player))
        utility_value -= self.countv( board, 4, p2) * 1100
        utility_value -= self.countv( board, 3, p2) * 110
        utility_value -= self.countv( board, 2, p2) * 10

        return utility_value
       

class RandomPlayer:
    def __init__(self, player_number):
        self.player_number = player_number
        self.type = 'random'
        self.player_string = 'Player {}:random'.format(player_number)

    def get_move(self, board):
        """
        Given the current board state select a random column from the available
        valid moves.

        INPUTS:
        board - a numpy array containing the state of the board using the
                following encoding:
                - the board maintains its same two dimensions
                    - row 0 is the top of the board and so is
                      the last row filled
                - spaces that are unoccupied are marked as 0
                - spaces that are occupied by player 1 have a 1 in them
                - spaces that are occupied by player 2 have a 2 in them

        RETURNS:
        The 0 based index of the column that represents the next move
        """
        valid_cols = []
        for col in range(board.shape[1]):
            if 0 in board[:,col]:
                valid_cols.append(col)

        return np.random.choice(valid_cols)


class HumanPlayer:
    def __init__(self, player_number):
        self.player_number = player_number
        self.type = 'human'
        self.player_string = 'Player {}:human'.format(player_number)

    def get_move(self, board):
        """
        Given the current board state returns the human input for next move

        INPUTS:
        board - a numpy array containing the state of the board using the
                following encoding:
                - the board maintains its same two dimensions
                    - row 0 is the top of the board and so is
                      the last row filled
                - spaces that are unoccupied are marked as 0
                - spaces that are occupied by player 1 have a 1 in them
                - spaces that are occupied by player 2 have a 2 in them

        RETURNS:
        The 0 based index of the column that represents the next move
        """

        valid_cols = []
        for i, col in enumerate(board.T):
            if 0 in col:
                valid_cols.append(i)

        move = int(input('Enter your move: '))

        while move not in valid_cols:
            print('Column full, choose from:{}'.format(valid_cols))
            move = int(input('Enter your move: '))

        return move
