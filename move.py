class Move:
    rankToRow = {str(i): 8-i for i in range(1,9)}           #{"1":7,"2":6 etc..}
    rowToRank = {v:k for k,v in rankToRow.items()}

    fileToCol = {chr(i+65):i for i in range(8)}             #{"a":0, "b":1 etc..}
    colToFile = {v:k for k,v in fileToCol.items()}

    def __init__(self, start, end, board):
        self.startRow, self.startCol = start
        self.endRow, self.endCol = end

        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
    
    def __eq__(self, other):
        if isinstance(other,Move):
            return self.startRow == other.startRow and self.startCol == other.startCol and self.endRow == other.endRow and self.endCol == other.endCol
    
    def notation(self):
        #can make this real chess notation
        return self.getRankFile(self.startRow,self.startCol) + "->" + self.getRankFile(self.endRow, self.endCol)       #if move is pawn from a2 to a4, returns a2a4


    def getRankFile(self,r,c):
        return self.colToFile[c] + self.rowToRank[r]