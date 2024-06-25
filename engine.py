
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
                        if type == "P":
                            self.generatePawnMoves(row,col,allMoves)
                        elif type == "R":
                            self.generateRookMoves(row,col,allMoves)
    
       


