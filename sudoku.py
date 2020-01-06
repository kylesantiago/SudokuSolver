import math

def printTable(arr):
    for x in range(n):
        for y in range(n):
            print(arr[x][y], end=" ")
        print()

def checkForEmptySpace(arr,holder):
    for x in range(n):
        for y in range(n):
            if(arr[x][y] == 0):
                holder[0] = x
                holder[1] = y
                return True

    return False

def checkRow(arr,row,num):
    for i in range(n):
        if(arr[row][i] == num):
            return False
    return True

def checkCol(arr,col,num):
    for i in range(n):
        if(arry[i][col] == num):
            return False
    return True

def checkBlock(arr,col,row,num):

    rowStart = row-row%int(math.sqrt(n))
    colStart = col-col%int(math.sqrt(n))
    
    for x in range(int(math.sqrt(n))):
        for y in range(int(math.sqrt(n))):
            if(arr[rowStart+x][colStart+y] == num):
                return False
    return True
        
def checkLocation(arr,col,row,num):
    return checkRow(arr,row,num) and checkCol(arr,col,num) and checkBlock(arr,col,row,num)

def solveSudoku(arr):
    holder = [0,0]

    if(not checkForEmptySpace(arry,holder)):
        return True

    row = holder[0]
    col = holder[1]
    
    for num in range(1,n+1):
        if (checkLocation(arr,col,row,num)):
            arr[row][col] = num

            if(solveSudoku(arr)):
                return True

            arr[row][col] = 0

    return False

n = 9
arry = [[5,0,4,2,0,0,0,0,0], 
        [0,0,3,0,0,0,0,0,0], 
        [8,0,0,0,9,0,6,0,0], 
        [4,0,0,0,0,1,9,7,2], 
        [0,0,0,7,0,5,0,0,0], 
        [3,1,7,9,0,0,0,0,5], 
        [0,0,8,0,3,0,0,0,4], 
        [0,0,0,0,0,0,2,0,0], 
        [0,0,0,0,0,6,1,0,7]] 

if(solveSudoku(arry)):
    printTable(arry)
else:
    print("No solution")
