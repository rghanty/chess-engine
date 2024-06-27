
from move import Move

class GameState:

    def __init__(self):
        self.board = [["bR","bN","bB","bQ","bK","bB","bN","bR"],
                      ["bP","bP","bP","bP","bP","bP","bP","bP"],
                      ["--","--","--","--","--","--","--","--"],
                      ["--","--","--","--","--","--","--","--"],
                      ["--","--","--","--","--","--","--","--"],
                      ["--","--","--","--","--","--","--","--"],
                      ["wP","wP","wP","wP","wP","wP","wP","wP"],
                      ["wR","wN","wB","wQ","wK","wB","wN","wR"]]
        
        self.pieceFuncs = {"P":self.generatePawnMoves, "R": self.generateRookMoves, "N": self.generateKnightMoves,
                           "B":self.generateBishopMoves, "K": self.generateKingMoves, "Q": self.generateQueenMoves}
        self.whiteTurn = True
        self.moveLog = [] 
        self.whiteKing = (7,4)
        self.blackKing = (0,4)
        self.rivals = {True:"b", False:"w"}     #if it is white's turn, its rival is black and vice versa
        self.allies = {True:"w", False:"b"}
        
        self.inCheck = False
        self.pins = []
        self.checks = []

    
    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move)
        self.whiteTurn = not self.whiteTurn 
        if move.pieceMoved == "wK":
            self.whiteKing = (move.endRow,move.endCol)
        if move.pieceMoved == "bK":
            self.blackKing = (move.endRow,move.endCol)
    
    def undoMove(self):
        if (len(self.moveLog)!=0):
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteTurn = not self.whiteTurn
        if move.pieceMoved == "wK":
            self.whiteKing = (move.startRow,move.startCol)
        if move.pieceMoved == "bK":
            self.blackKing = (move.startRow,move.startCol)

    def generateValidMoves(self):
        moves = []
        self.inCheck, self.pins, self.checks = self.pinsAndChecks()
        print(self.checks)
        if self.whiteTurn:
            kingRow = self.whiteKing[0]
            kingCol = self.whiteKing[1]
        else:
            kingCol = self.blackKing[1]
            kingRow = self.blackKing[0]

        if self.inCheck:
            
            if len(self.checks) == 1:
                moves = self.generateAllMoves()
                check = self.checks[0]
                checkRow = check[0]
                checkCol = check[1]
                validSquares = []       #Consists of the squares a piece can move to under a check
                piece = self.board[checkRow][checkCol]
                if piece[1] == "N":                     #Cannot block the knight, we can either capture it or move the king
                    validSquares = [(checkRow,checkCol)]
                else:
                    for i in range(1,8):                #Go in the direction of the check
                        endRow = kingRow + check[2]*i
                        endCol = kingCol + check[3]*i
                        validSquares.append((endRow,endCol))        #Add every square in that direction and stop after reaching the checking piece
                        if endRow == checkRow and endCol == checkCol:
                            break 
                for i in range(len(moves)-1,-1,-1):     #Remove all moves that do not move the king or block the check
                    if moves[i].pieceMoved[1] != "K":
                        if (moves[i].endRow,moves[i].endCol) not in validSquares:
                            moves.remove(moves[i])
            else:       #More than one piece is checking the king, need to move the king
                self.generateKingMoves(kingRow,kingCol,moves)
        else:       #Not in check, all moves are valid
            moves = self.generateAllMoves()
        
      
        
        return moves

    def pinsAndChecks(self):
        pins = []
        checks = []
        inCheck = False
        if self.whiteTurn:
            startRow = self.whiteKing[0]
            startCol = self.whiteKing[1]
        else:
            startCol = self.blackKing[1]
            startRow = self.blackKing[0]
        enemy = self.rivals[self.whiteTurn]
        ally = self.allies[self.whiteTurn]
        
        dirs = ((-1,0),(0,1),(1,0),(0,-1),(-1,-1),(-1,1),(1,-1),(1,1))              
        for i in range(len(dirs)):
            dir = dirs[i]
            possiblePin = ()        #checking for possible pins in any direction.
            for j in range(1,8):
                endRow = startRow + dir[0]*j
                endCol = startCol + dir[1]*j
                if 0<=endRow<8 and 0<=endCol<8:
                    endPiece = self.board[endRow][endCol]
                
                    if endPiece[0] == ally and endPiece[1] != "K":  #Kinda hard to explain the second condition, it is done to make sure a king's future move is not protected by the current king's position 
                        
                        if possiblePin == ():       
                            possiblePin = (endRow,endCol,dir[0],dir[1])     #if we find an allied piece, add it to our possible pin
                        else:               # 2nd allied piece in the same direction, not a pin
                            break
                    elif endPiece[0] == enemy:
                        piece = endPiece[1]
                    
                        if (0<=i<=3 and piece == "R") or (4<=i<=7 and piece=="B") or \
                            (j == 1 and piece == "P" and ((enemy == "w" and 6<=i<=7) or (enemy == "b" and 4<=i<=5))) or \
                            (piece == "Q") or (j == 1 and piece == "K"):

                            if possiblePin == ():           #if no allied piece blocking our king, then it is a check
                                inCheck = True
                                checks.append((endRow, endCol, dir[0],dir[1]))
                            else:
                                pins.append(possiblePin)    # otherwise, add to list of our pins
                                break
                        else:  #empty square
                            break
                else:       #out of bounds
                    break
        
        knightDirs = ((-2,1),(-2,-1),(1,2),(1,-2),(-1,2),(-1,-2),(2,1),(2,-1))
        for i in knightDirs:
            endRow  = startRow + i[0]
            endCol = startRow + i[1]

            if 0<=endRow<8 and 0<=endCol<8:
                piece = self.board[endRow][endCol]

                if piece[1] == "N" and piece[0]==enemy:
                    inCheck = True
                    checks.append((endRow,endCol,i[0],i[1]))
        
        return inCheck, pins, checks





        
    
    #Returns true if the current player's king is under attack (check)
    def check(self):
        if self.whiteTurn:
            return self.isUnderAttack(self.whiteKing[0], self.whiteKing[1])
        else:
            return self.isUnderAttack(self.blackKing[0],self.blackKing[1])
    

    # Returns true if the piece at row, col on the board is under attack by an enemy piece
    def isUnderAttack(self, row, col):                          
        self.whiteTurn = not self.whiteTurn                 # we want to generate all moves from the opponent's perspective
        oppMoves = self.generateAllMoves()
        self.whiteTurn = not self.whiteTurn                 # switch back to the original turn of the player
        for move in oppMoves:
            if row == move.endRow and col == move.endCol:
                return True
        return False

    def generateAllMoves(self):
        allMoves = []
        for row in range(len(self.board)):
            for col in range(len(self.board[0])):
                if self.board[row][col] != "--":
                    piece = self.board[row][col]
                    colour,type = piece[0],piece[1]
                    if self.whiteTurn and colour =="w" or (not self.whiteTurn and colour=="b"):
                        self.pieceFuncs[type](row,col,allMoves)
        return allMoves

    def generatePawnMoves(self,row,col,moves):
        piecePinned = False
        pinDirection = ()

        for i in range(len(self.pins)-1,-1,-1):
            if self.pins[i][0] == row and self.pins[i][1] == col:
                piecePinned = True
                pinDirection = (self.pins[i][2],self.pins[i][3])
                self.pins.remove(self.pins[i])
                break


        if self.whiteTurn:
            if self.board[row-1][col] == "--":
                if not piecePinned or pinDirection == (-1,0):
                    moves.append(Move((row,col),(row-1,col),self.board))
                    if row == 6 and self.board[row-2][col] == "--":
                        moves.append(Move((row,col),(row-2,col),self.board))
            
            if col-1>=0 and self.board[row-1][col-1][0] == "b" and (not piecePinned or pinDirection == (-1,-1)):
                moves.append(Move((row,col),(row-1,col-1),self.board))
            if col+1 <8 and self.board[row-1][col+1][0] == "b" and (not piecePinned or pinDirection == (-1,1)):
                 moves.append(Move((row,col),(row-1,col+1),self.board))
        
        if not self.whiteTurn:
            if self.board[row+1][col] == "--":
                if not piecePinned or pinDirection == (1,0):
                    moves.append(Move((row,col),(row+1,col),self.board))
                    if row == 1 and self.board[row+2][col] == "--":
                        moves.append(Move((row,col),(row+2,col),self.board))
            
            if col-1>=0 and self.board[row+1][col-1][0] == "w" and (not piecePinned or pinDirection == (1,-1)):
                moves.append(Move((row,col),(row+1,col-1),self.board))
            if col+1 <8 and self.board[row+1][col+1][0] == "w" and (not piecePinned or pinDirection == (1,1)):
                moves.append(Move((row,col),(row+1,col+1),self.board))
        

    def generateRookMoves(self,row,col,moves):
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins)-1,-1,-1):
            if self.pins[i][0] == row and self.pins[i][1] == col:
                piecePinned = True
                pinDirection = (self.pins[i][2],self.pins[i][3])
                if self.board[row][col][1] != "Q":
                    self.pins.remove(self.pins[i])
                break
        dirs = ((-1,0),(0,-1),(0,1),(1,0))
        self.generateMovesWithDirs(row,col,dirs,moves,piecePinned,pinDirection)
    
    def generateBishopMoves(self,row,col,moves):
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins)-1,-1,-1):
            if self.pins[i][0] == row and self.pins[i][1] == col:
                piecePinned = True
                pinDirection = (self.pins[i][2],self.pins[i][3])    
                self.pins.remove(self.pins[i])
                break
        dirs = ((1,1),(1,-1),(-1,-1),(-1,1))
        self.generateMovesWithDirs(row,col,dirs,moves,piecePinned,pinDirection)

        
    def generateMovesWithDirs(self,row,col,dirs,moves,isPinned,pinDirection):
        for dir in dirs:
            for i in range(1,8):
                endRow = row + dir[0]*i
                endCol = col + dir[1]*i
                if 0<=endRow < 8 and 0<= endCol < 8:
                    if not isPinned or pinDirection == dir or pinDirection == (-dir[0],-dir[1]):
                        if self.board[endRow][endCol] == "--":
                            moves.append(Move((row,col),(endRow,endCol),self.board))
                        elif self.board[endRow][endCol][0] != self.board[row][col][0]:
                            moves.append(Move((row,col),(endRow,endCol),self.board))
                            break
                        else:
                            break
                else:
                    break


        

    def generateKnightMoves(self,row,col,moves):
        piecePinned = False 
        for i in range(len(self.pins)-1,-1,-1):
            if self.pins[i][0] == row and self.pins[i][1] == col:
                piecePinned = True
                self.pins.remove(self.pins[i])
                break
        possibles = [(row-2,col+1),         
                     (row-2,col-1),
                     (row-1,col+2),
                     (row+1,col+2),
                     (row-1,col-2),
                     (row+1,col-2),
                     (row+2,col+1),
                     (row+2,col-1)]
        for i in possibles:
            if 0<=i[0]<8 and 0<=i[1]<8:
                if not piecePinned:
                    endPiece = self.board[i[0]][i[1]]
                    if endPiece[0] != self.allies[self.whiteTurn]:
                        moves.append(Move((row,col),(i[0],i[1]),self.board))
        

    def generateQueenMoves(self,row,col,moves):
        self.generateBishopMoves(row,col,moves)
        self.generateRookMoves(row,col,moves)

    def generateKingMoves(self,row,col,moves):
        dirs = ((0,1),(1,0),(1,1),(-1,-1),(0,-1),(-1,0),(1,-1),(-1,1))
        ally = self.allies[self.whiteTurn]
        
        for i in dirs:
            endRow = row+i[0]
            endCol = col+i[1]   
            if 0<=endRow<8 and 0<=endCol<8:
                if self.board[row][col][0] != self.board[endRow][endCol][0]:
                    if ally == "w":
                        self.whiteKing = (endRow, endCol)
                    else:
                        self.blackKing = (endRow,endCol)
                    
                    inCheck, pins, checks = self.pinsAndChecks() #Want to make sure the position we move the king to is not being attacked
                    print(inCheck)
                    if not inCheck:
                        moves.append(Move((row,col),(endRow,endCol),self.board))
                    
                    if ally == "w":
                        self.whiteKing = (row,col)
                    else:
                        self.blackKing = (row,col)
                

