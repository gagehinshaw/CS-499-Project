import pygame
from solver import solve, valid, print_board

pygame.font.init()

class Board:
    # sudoku board
    grid = [[6,7,2,0,0,8,0,0,1],
        [8,3,0,0,0,5,6,0,0],
        [0,4,0,6,3,0,8,0,7],
        [0,2,0,0,1,6,0,0,4],
        [0,0,0,4,9,0,1,8,0],
        [0,1,5,3,8,0,0,0,2],
        [0,0,7,0,0,0,0,0,6],
        [3,0,6,0,5,0,0,1,8],
        [0,0,0,0,0,9,7,5,3]
    ]

    def __init__(self, rows, cols, width, height):
        self.rows = rows
        self.cols = cols
        self.cubes =[[Cube(self.grid[i][j], i, j, width, height) for j in range(cols)] for i in  range(rows)]
        self.width = width
        self.height = height
        self.model = None
        self.selected = None

    def update_model(self):
        self.model = [[self.cubes[i][j].value for j in range(self.cols)] for i in range(self.rows)]

    def place(self, val): # placing a value
        row, col = self.selected
        if self.cubes[row][col].value == 0:
            self.cubes[row][col].set(val)
            self.update_model()

            if valid(self.model, val, (row,col)) and solve(self.model):
                return True
            else:
                self.cubes[row][col].set(0)
                self.cubes[row][col].set_temp(0)
                self.update_model()
                return False
    
    def sketch(self, val): # setting the value entered into the cell
        row, col = self.selected
        self.cubes[row][col].set_temp(val)

    def draw(self, win): # drawing the board
        gap = self.width / 9
        for i in range(self.rows+1):
            if i % 3 == 0 and i != 0:
                thick = 4
            else:
                thick = 1
            pygame.draw.line(win, (0,0,0), (0, i*gap), (self.width, i*gap), thick)
            pygame.draw.line(win, (0, 0, 0), (i * gap, 0), (i * gap, self.height), thick)

        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].draw(win)

    def select(self, row, col): # selecting a cell
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].selected = False

        self.cubes[row][col].selected = True
        self.selected = (row, col)

    def click(self, pos): # returning the clicked cell if valid
        if pos[0] < self.width and pos[1] < self.height:
            gap = self.width / 9
            x = pos[0] // gap
            y = pos[1] // gap
            return (int(y),int(x))
        else:
            return None

    def is_finished(self): # checking if the board is complete
        for i in range(self.rows):
            for j in range(self.cols):
                if self.cubes[i][j].value == 0:
                    return False
        return True


class Cube:
    rows = 9
    cols = 9

    def __init__(self, value, row, col, width ,height):
        self.value = value
        self.temp = 0
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        self.selected = False

    def draw(self, win): # drawing the cubes
        fnt = pygame.font.SysFont("timesnewroman", 40)

        gap = self.width / 9
        x = self.col * gap
        y = self.row * gap

        if self.temp != 0 and self.value == 0:
            text = fnt.render(str(self.temp), 1, (128,128,128))
            win.blit(text, (x+5, y+5))
        elif not(self.value == 0):
            text = fnt.render(str(self.value), 1, (0, 0, 0))
            win.blit(text, (x + (gap/2 - text.get_width()/2), y + (gap/2 - text.get_height()/2)))

        if self.selected:
            pygame.draw.rect(win, (255,0,0), (x,y, gap ,gap), 3)

    def set(self, val): # setting a value
        self.value = val

    def set_temp(self, val):
        self.temp = val


def redraw_window(win, board): # update window
    win.fill((255,255,255))
    fnt = pygame.font.SysFont("comicsans", 40)
    # Draw grid and board
    board.draw(win)

def main(): # game loop
    win = pygame.display.set_mode((540, 540)) # window
    pygame.display.set_caption("Sudoku") # caption
    board = Board(9, 9, 540, 540) # create board
    key = None
    run = True
    while run:
           # grabbing keyboard and mouse input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    key = 1
                if event.key == pygame.K_2:
                    key = 2
                if event.key == pygame.K_3:
                    key = 3
                if event.key == pygame.K_4:
                    key = 4
                if event.key == pygame.K_5:
                    key = 5
                if event.key == pygame.K_6:
                    key = 6
                if event.key == pygame.K_7:
                    key = 7
                if event.key == pygame.K_8:
                    key = 8
                if event.key == pygame.K_9:
                    key = 9
                if event.key == pygame.K_RETURN: # checks if input is valid when entering a value
                    i, j = board.selected
                    if board.cubes[i][j].temp != 0:
                        if board.place(board.cubes[i][j].temp):
                            print("Success")
                        else:
                            print("Wrong")
                        key = None

                        if board.is_finished():
                            print("Game over")
                            run = False

            if event.type == pygame.MOUSEBUTTONDOWN: # mouse click input 
                pos = pygame.mouse.get_pos()
                clicked = board.click(pos)
                if clicked:
                    board.select(clicked[0], clicked[1])
                    key = None

        if board.selected and key != None: # entering the value
            board.sketch(key)

        redraw_window(win, board)
        pygame.display.update()



# display puzzle in terminal
puzzle = Board.grid
print_board(puzzle)

# menu
print("==============")
print("Choose an option: ")
print("1: Solve Board")
print("2: Attempt Puzzle")
answer = int(input(""))
while True:
    if answer == 1: # solve board and display result
        solve(puzzle)
        main()
        pygame.quit()
        break
    elif answer == 2: # run game loop
        main()
        pygame.quit()
        break
    pygame.quit()