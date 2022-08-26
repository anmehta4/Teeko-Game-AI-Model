import random
import math
import copy

class TeekoPlayer:
    """ An object representation for an AI game player for the game Teeko.
    """
    board = [[' ' for j in range(5)] for i in range(5)]
    pieces = ['b', 'r']

    def __init__(self):
        """ Initializes a TeekoPlayer object by randomly selecting red or black as its
        piece color.
        """
        self.my_piece = random.choice(self.pieces)
        self.opp = self.pieces[0] if self.my_piece == self.pieces[1] else self.pieces[1]


    def check_drop_phase(self, state):
      my_count = 0
      opp_count = 0
      
      for i in range(len(state)):
        for j in range(len(state[0])):
          if(state[i][j] == self.my_piece):
            my_count += 1
          elif(state[i][j] == self.opp):
            opp_count += 1
      
      if (opp_count < 4 or my_count < 4):
        return True

      return False

    def succ(self, state):
      successors = []
      drop_phase = False
      my_count = 0
      opp_count = 0
      my_pos = []
      
      for i in range(len(state)):
        for j in range(len(state[0])):
          if(state[i][j] == self.my_piece):
            my_pos.append([i,j])
            my_count += 1
          elif(state[i][j] == self.opp):
            opp_count += 1
      
      if (opp_count< 4 or my_count<4):
        drop_phase = True

      if drop_phase:
        for i in range(len(state)):
          for j in range(len(state[0])):
            if(state[i][j] == ' '):
              successors.append([i,j])
      else:
        for pos in my_pos:
          r = [pos[0]-1, pos[0], pos[0]+1]
          c = [pos[1]-1, pos[1], pos[1]+1]
          for x in r:
            for y in c:
              if x>-1 and x<5 and y>-1 and y<5 and state[x][y] == ' ':
                successors.append([x,y, pos[0], pos[1]])

      random.shuffle(successors)
      return successors

    def heuristic_game_value(self, state,piece):
        terminal = self.game_value(state)
        if(terminal != 0):
            return terminal

        max_val = -math.inf
        min_val = math.inf

        # horizontal
        for row in state:
            for col in range(2):
                pieces = []
                for i in range(4):
                    pieces.append(row[col+i])
                max_val = max( max_val, pieces.count(self.my_piece)*0.2 )
                min_val = min( min_val, pieces.count(self.opp)*(-0.2))

        # vertical
        for col in range(5):
            for row in range(2):
                pieces = []
                for i in range(4):
                    pieces.append(state[row+i][col])
                max_val = max( max_val, pieces.count(self.my_piece)*0.2 )
                min_val = min( min_val, pieces.count(self.opp)*(-0.2))

        # \ diagonal
        for row in range(2):
            for col in range(2):
                pieces = []
                for i in range(4):
                    if(col+i < 5 and row+i < 5):
                        pieces.append( state[row+i][col+i] )
                max_val = max( max_val, pieces.count(self.my_piece)*0.2 )
                min_val = min( min_val, pieces.count(self.opp)*0.2*(-1) )
            
        # / diagonal
        for row in range(2):
            for col in range(3,5):
                pieces = list()
                for i in range(4):
                    if(col-i >= 0 and row+i < 5):
                        pieces.append( state[row+i][col-i] )
                max_val = max( max_val, pieces.count(self.my_piece)*0.2 )
                min_val = min( min_val, pieces.count(self.opp)*0.2*(-1) )
                
        # box
        for row in range(4):
            for col in  range(4):
                pieces = list()
                pieces.append(state[row][col])
                pieces.append(state[row][col+1])
                pieces.append(state[row+1][col])
                pieces.append(state[row+1][col+1])
                max_val = max( max_val, pieces.count(self.my_piece)*0.2 )
                min_val = min( min_val, pieces.count(self.opp)*(-0.2))

        return max_val + min_val

    def max_value(self, state, depth):
        if(self.game_value(state) != 0):
            return self.game_value(state)

        if(depth >= 1):
            return self.heuristic_game_value(state, self.my_piece)

        if (self.check_drop_phase(state)):
          alpha = -math.inf
          succ_list = self.succ(state)
          for r,c in succ_list:
            temp_state = copy.deepcopy(state)
            temp_state[r][c] = self.my_piece
            alpha = max(alpha,  self.min_value(temp_state, depth+1))

        else:
          alpha = -math.inf
          succ_list = self.succ(state)
          for r,c,rm,cm in succ_list:
            temp_state = copy.deepcopy(state)
            temp_state[r][c] = self.my_piece
            temp_state[rm][cm] = ' '
            alpha = max(alpha,  self.min_value(temp_state, depth+1))

        return alpha
    
    def min_value(self, state, depth):
        if(self.game_value(state) != 0):
            return self.game_value(state)

        if(depth >= 1):
            return self.heuristic_game_value(state, self.my_piece)

        if (self.check_drop_phase(state)):
          beta = math.inf
          succ_list = self.succ(state)
          for r,c in succ_list:
            temp_state = copy.deepcopy(state)
            temp_state[r][c] = self.opp
            beta = min(beta,  self.max_value(temp_state, depth+1))

        else:
          beta = math.inf
          succ_list = self.succ(state)
          for r,c,rm,cm in succ_list:
            temp_state = copy.deepcopy(state)
            temp_state[r][c] = self.opp
            temp_state[rm][cm] = ' '
            beta = min(beta,  self.max_value(temp_state, depth+1))

        return beta

    def make_move(self, state):

      drop_phase = self.check_drop_phase(state)   # TODO: detect drop phase

      
      move = []
      next_move = []
      
      if not drop_phase:
        succ_list = self.succ(state)
        max_suc_val = -math.inf
        for r,c,rm,cm in succ_list:
            temp_state = copy.deepcopy(state)
            temp_state[r][c] = self.my_piece
            temp_state[rm][cm] = ' '
            suc_val = self.max_value(temp_state, 0)
            if(suc_val > max_suc_val):
              next_move = [(r,c), (rm,cm)]
              max_suc_val = suc_val
        move = next_move
        return move
      else:
        succ_list = self.succ(state)
        max_suc_val = -math.inf
        for r,c in succ_list:
            temp_state = copy.deepcopy(state)
            temp_state[r][c] = self.my_piece
            suc_val = self.max_value(temp_state, 0)
            if(suc_val > max_suc_val):
              next_move = [r,c]
              max_suc_val = suc_val

      move.insert(0, (next_move[0], next_move[1]))
      return move
      

    def opponent_move(self, move):
        """ Validates the opponent's next move against the internal board representation.
        You don't need to touch this code.

        Args:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.
        """
        # validate input
        if len(move) > 1:
            source_row = move[1][0]
            source_col = move[1][1]
            if source_row != None and self.board[source_row][source_col] != self.opp:
                self.print_board()
                print(move)
                raise Exception("You don't have a piece there!")
            if abs(source_row - move[0][0]) > 1 or abs(source_col - move[0][1]) > 1:
                self.print_board()
                print(move)
                raise Exception('Illegal move: Can only move to an adjacent space')
        if self.board[move[0][0]][move[0][1]] != ' ':
            raise Exception("Illegal move detected")
        # make move
        self.place_piece(move, self.opp)

    def place_piece(self, move, piece):
        """ Modifies the board representation using the specified move and piece

        Args:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.

                This argument is assumed to have been validated before this method
                is called.
            piece (str): the piece ('b' or 'r') to place on the board
        """
        if len(move) > 1:
            self.board[move[1][0]][move[1][1]] = ' '
        self.board[move[0][0]][move[0][1]] = piece

    def print_board(self):
        """ Formatted printing for the board """
        for row in range(len(self.board)):
            line = str(row)+": "
            for cell in self.board[row]:
                line += cell + " "
            print(line)
        print("   A B C D E")

    def game_value(self, state):
        """ Checks the current board status for a win condition

        Args:
        state (list of lists): either the current state of the game as saved in
            this TeekoPlayer object, or a generated successor state.

        Returns:
            int: 1 if this TeekoPlayer wins, -1 if the opponent wins, 0 if no winner

        TODO: complete checks for diagonal and box wins
        """
        # check horizontal wins
        for row in state:
            for i in range(2):
                if row[i] != ' ' and row[i] == row[i+1] == row[i+2] == row[i+3]:
                    return 1 if row[i]==self.my_piece else -1

        # check vertical wins
        for col in range(5):
            for i in range(2):
                if state[i][col] != ' ' and state[i][col] == state[i+1][col] == state[i+2][col] == state[i+3][col]:
                    return 1 if state[i][col]==self.my_piece else -1

        # check \ diagonal wins
        for i in range(2):
          for j in range(2):
            if state[i][j] != ' ' and state[i][j] == state[i+1][j+1] == state[i+2][j+2] == state[i+3][j+3]:
              return 1 if state[i][j]==self.my_piece else -1

        # TODO: check / diagonal wins
        for i in range(2):
          for j in range(3,5):
            if state[i][j] != ' ' and state[i][j] == state[i+1][j-1] == state[i+2][j-2] == state[i+3][j-3]:
              return 1 if state[i][j]==self.my_piece else -1

        # TODO: check box wins
        for i in range(4):
            for j in range(4):
                if state[i][j] != ' ' and state[i][j] == state[i][j+1] == state[i+1][j] == state[i+1][j+1]:
                  return 1 if state[i][j]==self.my_piece else -1
        
        return 0 # no winner yet

    
############################################################################
#
# THE FOLLOWING CODE IS FOR SAMPLE GAMEPLAY ONLY
#
############################################################################
def main():
    print('Hello, this is Samaritan')
    ai = TeekoPlayer()
    piece_count = 0
    turn = 0

    # drop phase
    while piece_count < 8 and ai.game_value(ai.board) == 0:

        # get the player or AI's move
        if ai.my_piece == ai.pieces[turn]:
            ai.print_board()
            move = ai.make_move(ai.board)
            ai.place_piece(move, ai.my_piece)
            print(ai.my_piece+" moved at "+chr(move[0][1]+ord("A"))+str(move[0][0]))
        else:
            move_made = False
            ai.print_board()
            print(ai.opp+"'s turn")
            while not move_made:
                player_move = input("Move (e.g. B3): ")
                while player_move[0] not in "ABCDE" or player_move[1] not in "01234":
                    player_move = input("Move (e.g. B3): ")
                try:
                    ai.opponent_move([(int(player_move[1]), ord(player_move[0])-ord("A"))])
                    move_made = True
                except Exception as e:
                    print(e)

        # update the game variables
        piece_count += 1
        turn += 1
        turn %= 2

    # move phase - can't have a winner until all 8 pieces are on the board
    while ai.game_value(ai.board) == 0:

        # get the player or AI's move
        if ai.my_piece == ai.pieces[turn]:
            ai.print_board()
            move = ai.make_move(ai.board)
            ai.place_piece(move, ai.my_piece)
            print(ai.my_piece+" moved from "+chr(move[1][1]+ord("A"))+str(move[1][0]))
            print("  to "+chr(move[0][1]+ord("A"))+str(move[0][0]))
        else:
            move_made = False
            ai.print_board()
            print(ai.opp+"'s turn")
            while not move_made:
                move_from = input("Move from (e.g. B3): ")
                while move_from[0] not in "ABCDE" or move_from[1] not in "01234":
                    move_from = input("Move from (e.g. B3): ")
                move_to = input("Move to (e.g. B3): ")
                while move_to[0] not in "ABCDE" or move_to[1] not in "01234":
                    move_to = input("Move to (e.g. B3): ")
                try:
                    ai.opponent_move([(int(move_to[1]), ord(move_to[0])-ord("A")),
                                    (int(move_from[1]), ord(move_from[0])-ord("A"))])
                    move_made = True
                except Exception as e:
                    print(e)

        # update the game variables
        turn += 1
        turn %= 2

    ai.print_board()
    if ai.game_value(ai.board) == 1:
        print("AI wins! Game over.")
    else:
        print("You win! Game over.")


if __name__ == "__main__":
    main()

