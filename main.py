import pygame
from engine import GameState
from move import Move


WIDTH = HEIGHT = 560                #can be adjustable
DIMENSION = 8
SIZE = WIDTH // DIMENSION
FPS = 15                            #fps for animation
IMAGES = {}

#Images should be loaded only once. Stored in IMAGES dict
def loadImages():
    pieces = ["bB","bH","bK","bP","bQ","bR","wB","wH","wK","wP","wQ","wR"]
    for i in pieces:
        IMAGES[i] = pygame.transform.scale(pygame.image.load("media/"+i+".png"),(SIZE,SIZE))

#Driver function
def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH,HEIGHT))
    pygame.display.set_caption("Chess Engine")
    clock = pygame.time.Clock()
    screen.fill(pygame.Color("white"))
    game = GameState()
    loadImages()
    running = True
    sqSelected = ()
    squares = []
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                position = pygame.mouse.get_pos()
                col = position[0]//SIZE
                row = position[1]//SIZE

                if sqSelected == (row,col):
                    sqSelected = ()
                    squares = []
                else:
                    sqSelected = (row,col)
                    squares.append(sqSelected)
                    if len(squares) == 2:
                        
                        move = Move(squares[0],squares[1],game.board)
                        game.makeMove(move)

                        sqSelected = ()
                        squares = []
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_z and pygame.key.get_mods() & pygame.KMOD_LCTRL:
                    game.undoMove()
        

        drawGame(screen,game)
        
        clock.tick(FPS)
        pygame.display.flip()

#Draw the current game state
def drawGame(screen,game):
    drawBoard(screen)
    drawPieces(screen,game)


#draw the board
def drawBoard(screen):
    colors = [pygame.Color("white"),pygame.Color("gray")]
    for i in range(DIMENSION):
        for j in range(DIMENSION):
            color = colors[(i+j)%2]
            pygame.draw.rect(screen,color,pygame.Rect(j*SIZE,i*SIZE,SIZE,SIZE))

#draw the pieces on the board depending on the game state
def drawPieces(screen,game):
    board = game.board
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            if board[row][col] != "--":
                screen.blit(IMAGES[board[row][col]],(col*SIZE,row*SIZE))




if __name__ == "__main__":
    main()