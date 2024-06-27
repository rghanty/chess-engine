
from move import Move

class GameState:

    def __init__(self):
        self.board = [["bR","bH","bB","bQ","bK","bB","bH","bR"],
                      ["bP","bP","bP","bP","bP","bP","bP","bP"],
                      ["--","--","--","--","--","--","--","--"],
                      ["--","--","--","--","--","--","--","--"],
                      ["--","--","--","--","--","--","--","--"],
                      ["--","--","--","--","--","--","--","--"],
                      ["wP","wP","wP","wP","wP","wP","wP","wP"],
                      ["wR","wH","wB","wQ","wK","wB","wH","wR"]]
        
        self.whiteTurn = True
        self.moveLog = [] 
    
    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move)
        self.whiteTurn = not self.whiteTurn 
    
    def undoMove(self):
        if (len(self.moveLog)!=0):
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteTurn = not self.whiteTurn
        
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
        
        if self.whiteTurn and row-1>=0:
            if self.board[row-1][col] == "--":
                moves.append(Move((row,col),(row-1,col),self.board))
            if row == 6 and self.board[row-2][col] == "--":
                moves.append(Move((row,col),(row-2,col),self.board))
            
            if col-1>=0 and self.board[row-1][col-1][0] == "b":
                moves.append(Move((row,col),(row-1,col-1),self.board))
            if col+1 <8 and self.board[row-1][col+1][0] == "b":
                 moves.append(Move((row,col),(row-1,col+1),self.board))
        
        if not self.whiteTurn and row + 1 >= 0:
            if self.board[row+1][col] == "--":
                moves.append(Move((row,col),(row+1,col),self.board))
            if row == 1 and self.board[row+2][col] == "--":
                moves.append(Move((row,col),(row+2,col),self.board))
            
            if col-1>=0 and self.board[row+1][col-1][0] == "w":
                moves.append(Move((row,col),(row+1,col-1),self.board))
            if col+1 <8 and self.board[row+1][col+1][0] == "w":
                moves.append(Move((row,col),(row+1,col+1),self.board))
        

    def generateRookMoves(self,row,col,moves):
        
        dirs = ((-1,0),(0,-1),(0,1),(1,0))
        self.generateMovesWithDirs(row,col,dirs,moves)
    
    def generateBishopMoves(self,row,col,moves):

        dirs = ((1,1),(1,-1),(-1,-1),(-1,1))
        self.generateMovesWithDirs(row,col,dirs,moves)

        
    def generateMovesWithDirs(self,row,col,dirs,moves):
        for dir in dirs:
            for i in range(1,8):
                endRow = row + dir[0]*i
                endCol = col + dir[1]*i
                if 0<=endRow < 8 and 0<= endCol < 8:
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
        possibles = [(row-2,col+1),         
                     (row-2,col-1),
                     (row-1,col+2),
                     (row+1,col+2),
                     (row-1,col-2),
                     (row+1,col-2),
                     (row+2,col+1),
                     (row+2,col-1)]
        possibles = list(filter(lambda pos: (0<=pos[0]<8 and 0<=pos[1]<8 and self.board[row][col][0] != self.board[pos[0]][pos[1]][0]), possibles))
        for i in possibles:
            moves.append(Move((row,col),(i[0],i[1]),self.board))
        

    def generateQueenMoves(self,row,col,moves):
        self.generateBishopMoves(row,col,moves)
        self.generateRookMoves(row,col,moves)

    def generateKingMoves(self,row,col,moves):
        dirs = ((0,1),(1,0),(1,1),(-1,-1),(0,-1),(-1,0),(1,-1),(-1,1))
        for i in dirs:
            endRow = row+i[0]
            endCol = col+i[1]   
            if 0<=endRow<8 and 0<=endCol<8:
                if self.board[row][col][0] != self.board[endRow][endCol][0]:
                    moves.append(Move((row,col),(endRow,endCol),self.board))
    
       


