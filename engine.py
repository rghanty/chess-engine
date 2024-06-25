
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

        