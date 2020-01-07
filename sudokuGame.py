import pygame
import time
pygame.font.init()
class Board:
    board =[[0,3,9,0,0,0,0,0,7],
[2,0,0,4,0,0,6,1,0],
[1,0,0,0,0,5,0,0,0],
[0,0,0,0,3,0,0,6,0],
[0,5,2,0,1,0,4,7,0],
[0,6,0,0,5,0,0,0,0],
[0,0,0,7,0,0,0,0,1],
[0,1,3,0,0,8,0,0,9],
[5,0,0,0,0,0,8,3,0]]



    def __init__(self, rows, cols, width, height, win):
        self.rows = rows
        self.cols = cols
        self.cubes = [[Cube(self.board[x][y], x, y, width, height) for y in range(cols)] for x in range(rows)]
        self.width = width
        self.height = height
        self.model = [[self.cubes[x][y].value for y in range(self.cols)] for x in range(self.rows)]
        self.solved = [[self.cubes[x][y].value for y in range(self.cols)] for x in range(self.rows)]
        self.selRow = None
        self.selCol = None
        self.win = win
        
        solveSudoku(self.solved)

    def update_model(self,row,col,val):
        self.model[row][col] = val

    def update_cubes(self,row,col,val):
        self.cubes[row][col].set(val)

    def place(self, val):
        row = self.selRow
        col = self.selCol
        if self.cubes[row][col].value == 0:
            self.cubes[row][col].set(val)
            self.model[row][col] = val
                
            if (self.solved[row][col] == val):
                return True
            else:
                self.cubes[row][col].set(0)
                self.cubes[row][col].set_temp(0)
                self.model[row][col] = 0
                return False
            
    def sketch(self, val):
        row = self.selRow
        col = self.selCol
        self.cubes[row][col].set_temp(val)

    def draw(self, win):
        gap = self.width / self.rows
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

    def select(self, row, col):
        for x in range(self.rows):
            for y in range(self.cols):
                self.cubes[x][y].selected = False

        self.cubes[row][col].selected = True
        self.selRow = row
        self.selCol = col

    def clear(self):
        row = self.selRow
        col = self.selCol
        
        if self.cubes[row][col].given:
            self.cubes[row][col].set_temp(0)

    def click(self, pos):
        if pos[0] < self.width and pos[1] < self.height:
            gap = self.width / 9
            x = pos[0] // gap
            y = pos[1] // gap
            return (int(y),int(x))
        else:
            return None

    def is_finished(self):
        for x in range(self.rows):
            for y in range(self.cols):
                if self.cubes[x][y].value == 0:
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
        self.given = False if value == 0 else True

    def draw(self, win):
        fnt = pygame.font.SysFont(None, 40)

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

    def set(self, val):
        self.value = val

    def set_temp(self, val):
        self.temp = val

    def draw_change(self, win, g=True):
        fnt = pygame.font.SysFont(None, 40)

        gap = self.width / 9
        x = self.col * gap
        y = self.row * gap

        pygame.draw.rect(win, (255, 255, 255), (x, y, gap, gap), 0)

        text = fnt.render(str(self.value), 1, (0, 0, 0))
        win.blit(text, (x + (gap / 2 - text.get_width() / 2), y + (gap / 2 - text.get_height() / 2)))
        if g:
            pygame.draw.rect(win, (0, 255, 0), (x, y, gap, gap), 3)
        else:
            pygame.draw.rect(win, (255, 0, 0), (x, y, gap, gap), 3)

    def draw_done(self, win,done):
        fnt = pygame.font.SysFont(None, 40)

        gap = self.width / 9
        x = self.col * gap
        y = self.row * gap

        pygame.draw.rect(win, (255, 255, 255), (x, y, gap, gap), 0)

        text = fnt.render(str(self.value), 1, (0, 0, 0))
        win.blit(text, (x + (gap / 2 - text.get_width() / 2), y + (gap / 2 - text.get_height() / 2)))
        if done == 1:
            pygame.draw.rect(win, (0, 255, 0), (x, y, gap, gap), 3)
        elif done == 2:
            pygame.draw.rect(win, (255, 0, 0), (x, y, gap, gap), 3)
        else:
            pygame.draw.rect(win, (255,255,0), (x, y, gap, gap), 3)

class SolveButton():
    def __init__(self):
        self.color = (255,255,255)
        self.x = 5
        self.y = 545
        self.width = 100
        self.height = 50
        self.text = 'Solve'

    def draw(self,win):
        pygame.draw.rect(win, (0,0,0), (self.x-2,self.y-2,self.width+4,self.height+4),0)
        pygame.draw.rect(win, self.color, (self.x,self.y,self.width,self.height),0)
        font = pygame.font.SysFont(None, 40)
        text = font.render(self.text, 1, (0,0,0))
        win.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))

    def isOver(self, pos):
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True
        return False

def handleStrikes(strikes):
    temp = ""
    if(strikes < 4):
        for i in range(strikes):
            temp += "X"
    else:
        temp = "X " + str(strikes)
        
    return temp
    
def redraw_window(win, board, time, strikes, button):
    win.fill((255,255,255))
    fnt = pygame.font.SysFont(None, 40)
    text = fnt.render("Time: " + format_time(time), 1, (0,0,0))
    win.blit(text, (340, 560))
    text = fnt.render(handleStrikes(strikes), 1, (255, 0, 0))
    win.blit(text, (140, 560))
    board.draw(win)
    button.draw(win)

def format_time(secs):
    sec = secs%60
    minute = secs//60
    hour = minute//60

    mat = ""
    
    if(hour < 10):
        mat+= "0"+str(hour)
    else:
        mat+= str(hour)
        
    mat+=":"
    
    if(minute < 10):
        mat+= "0"+str(minute)
    else:
        mat+= str(minute)

    mat+=":"

    if(sec < 10):
        mat+= "0"+str(sec)
    else:
        mat+= str(sec)

    return mat


def main():
    win = pygame.display.set_mode((540,600))
    pygame.display.set_caption("Sudoku")
    board = Board(9, 9, 540, 540, win)
    button = SolveButton()
    key = None
    run = True
    doneVal = False
    start = time.time()
    strikes = 0
    while run:
        
        play_time = round(time.time() - start)
        
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
                if event.key == pygame.K_DELETE:
                    board.clear()
                    key = None
                if event.key == pygame.K_RETURN:
                    x = board.selRow
                    y = board.selCol
                    if board.cubes[x][y].temp != 0:
                        if not board.place(board.cubes[x][y].temp):
                            strikes += 1
                        key = None

                        if board.is_finished():
                            doneVal = True
                            done(board,1)

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                clicked = board.click(pos)
                if clicked:
                    board.select(clicked[0], clicked[1])
                    key = None
                elif button.isOver(pos) and not doneVal:
                    redraw_window(win, board, play_time, strikes, button)
                    doneVal = True
                    visualSolve(board)
                    done(board,3)
                    

        if board.selRow != None and board.selCol != None and key != None:
            board.sketch(key)

        if not doneVal:
            redraw_window(win, board, play_time, strikes, button)
            
        pygame.display.update()

def checkForEmptySpace(arr,holder):
    for x in range(9):
        for y in range(9):
            if(arr[x][y] == 0):
                holder[0] = x
                holder[1] = y
                return True

    return False

def checkRow(arr,row,num):
    for i in range(9):
        if(arr[row][i] == num):
            return False
    return True

def checkCol(arr,col,num):
    for i in range(9):
        if(arr[i][col] == num):
            return False
    return True

def checkBlock(arr,col,row,num):

    rowStart = row-row%3
    colStart = col-col%3
    
    for x in range(3):
        for y in range(3):
            if(arr[rowStart+x][colStart+y] == num):
                return False
    return True

def checkLocation(arr,col,row,num):
    return checkRow(arr,row,num) and checkCol(arr,col,num) and checkBlock(arr,col,row,num)

def solveSudoku(arr):
    holder = [0,0]

    if(not checkForEmptySpace(arr,holder)):
        return True

    row = holder[0]
    col = holder[1]
    
    for num in range(1,10):
        if (checkLocation(arr,col,row,num)):
            arr[row][col] = num
            
            if(solveSudoku(arr)):
                return True

            arr[row][col] = 0

    return False

def checkLocationGame(arr,col,row,num):
    for i in range(9):
        if arr[row][i] == num and col != i:
            return False
        
    for i in range(9):
        if arr[i][col] == num and row != i:
            return False

    rowStart = row-row%3
    colStart = col-col%3
    
    for x in range(3):
        for y in range(3):
            if arr[rowStart+x][colStart+y] == num and x != row and y != col:
                return False

    return True

    
def visualSolve(board):
    holder = [0,0]

    if(not checkForEmptySpace(board.model,holder)):
        return True

    board.select(holder[0],holder[1])
    row = board.selRow
    col = board.selCol
    
    for num in range(1,10):
        if (checkLocationGame(board.model,col,row,num)):
            #if(board.place(num)):
                #visualSolve(board)
            board.update_model(row,col,num)
            board.update_cubes(row,col,num)
            board.cubes[row][col].draw_change(board.win, True)
            pygame.display.update()
            pygame.time.delay(50)
        
            if visualSolve(board):
                return True

            board.update_model(row,col,0)
            board.update_cubes(row,col,0)
            board.cubes[row][col].draw_change(board.win, False)
            pygame.display.update()
            pygame.time.delay(50)
            
    return False

def done(board,val):
    for x in range(9):
        for y in range(9):
            board.cubes[x][y].draw_done(board.win,val)

main()
pygame.quit()
