#Crystal Song
#cs5489
#Hyper Sudoku

'''
Apply forward checking and a backtracking search algorithm to solve hyper sudoku puzzle
Read in input file of 9x9 matrix and create output file with the solution.
0 represents a blank space.
'''
class Cell:
    def __init__(self, row, column, square, value):
        self.value = value
        if (value == None):
            self.assigned = False
            self.domain = [1,2,3,4,5,6,7,8,9]
        else:
            self.assigned = True
            self.domain = None
        self.row = row
        self.col = column
        self.square = square
        #number of unassigned neighbors each cell has
        #used for degree heuristic
        self.neighbors = 0

class Puzzle:
    def __init__(self):
        self.board = []
        self.cells = []
        #the current number of unassigned cells
        #used to end the recursion for backtracking
        self.unassigned = 0

'''return a list of indexes of squares that the given coordinates are in.
Square indexs are determined left to right, top to bottom with the original
9 squares bearing precedence. The indexes 10-13 represent the added squares
from hyper-sudoku rules.'''
def getSquare(row, col):
    #row/column indexes for each square
    opt1 = [1,2,3]
    opt2 = [4,5,6]
    opt3 = [7,8,9]
    opt4 = [2,3,4]
    opt5 = [6,7,8]

    squareIndex = []

    if row in opt1:
        if col in opt1: squareIndex.append(1)
        elif col in opt2: squareIndex.append(2)
        elif col in opt3: squareIndex.append(3)
    elif row in opt2:
        if col in opt1: squareIndex.append(4)
        elif col in opt2: squareIndex.append(5)
        elif col in opt3: squareIndex.append(6)
    elif row in opt3:
        if col in opt1: squareIndex.append(7)
        elif col in opt2: squareIndex.append(8)
        elif col in opt3: squareIndex.append(9)

    if row in opt4:
        if col in opt4: squareIndex.append(10)
        elif col in opt5: squareIndex.append(11)
    elif row in opt5:
        if col in opt4: squareIndex.append(12)
        elif col in opt5: squareIndex.append(13)

    return squareIndex

'''apply to cells that already have an assigned number
if any cell has an empty domain after applying forward checking
return no solution'''
def Forward_Checking(cells):
    for obj in cells:
        if obj.assigned == True:
            for cell in cells:
                #skip other assigned cells
                if cell.assigned == False:
                    #remove value of assigned cell from all neighbors
                    #remove value from cells in the same row
                    if (obj.row == cell.row) and (int(obj.value) in cell.domain):
                        cell.domain.remove(int(obj.value))
                        cell.neighbors += 1
                    #remove value from cells in the same column
                    if (obj.col == cell.col) and (int(obj.value) in cell.domain):
                        cell.domain.remove(int(obj.value))
                        cell.neighbors += 1
                    #remove value from cells in the same square
                    if len(obj.square) == 2:
                        if (obj.square[0] in cell.square) or (obj.square[1] in cell.square):
                            if(int(obj.value) in cell.domain):
                                cell.domain.remove(int(obj.value))
                                cell.neighbors += 1
                    elif len(obj.square) == 1:
                        if (obj.square[0] in cell.square) and (int(obj.value) in cell.domain):
                                cell.domain.remove(int(obj.value))
                                cell.neighbors += 1
                    #check if domain is empty after removal
                    if len(cell.domain) == 0:
                        return False
    return True

'''assign any cells that are currently unassigned
and have only one value in their domain'''
def assignSingles(puz):
    for obj in puz.cells:
        if obj.assigned == False:
            if len(obj.domain) == 1:
                puz.unassigned -= 1
                obj.value = obj.domain[0]
                obj.domain = None
                obj.assigned = True
    return

'''compare the given cell against all other cells in the puzzle
check if the value is not already in the same row/column/square'''
def isValid(puz, cell):
    for obj in puz.cells:
        #skip the identical cell
        if(obj.row == cell.row) and (obj.col == cell.col):
            continue
        #check for other values in the same row
        if cell.row == obj.row:
            if cell.value == obj.value:
                return False
        #check for other values in the same column
        elif cell.col == obj.col:
            if cell.value == obj.value:
                return False
        #check for other values in the same square
        if len(obj.square) == 2:
            if (cell.value == obj.value):
                if (obj.square[0] in cell.square) or (obj.square[1] in cell.square):
                    return False
            elif len(obj.square) == 1:
                if (cell.value == obj.value):
                    if obj.square[0] in cell.square:
                        return False
    return True

'''use minimum remaining value heuristic and then degree heuristic to choose
the next variable assignment'''
def Select_Unassigned_Variable(cells):
    mrv = []
    degree = []
    minLen = 9
    maxNeighbors = 0
    
    #determine the minimum length of the domains
    for obj in cells:
        if obj.assigned == False:
            if len(obj.domain) < minLen:
                minLen = len(obj.domain)

    #add any domains of the minimum length to mrv
    for obj in cells:
        if obj.assigned == False:
            if len(obj.domain) == minLen:
                mrv.append(obj)

    #if there's only one cell in mrv, choose that cell for the next variable
    if len(mrv) == 1:
        return mrv[0]

    #else, apply degree heuristic to cells in mrv
    for obj in mrv:
        if obj.neighbors > maxNeighbors:
            maxNeighbors = obj.neighbors
            
    for obj in mrv:
        if obj.neighbors == maxNeighbors:
            degree.append(obj)

    #if degree only has one varible, assign that as the next
    #if degree has more than 1 variable left, arbitrarily choose the first in the list
    return degree[0]

#returns a solution or failure 
def Backtracking_Search(puz):
    return Backtrack(puz, {})

'''backtrack through the current unassigned variables to solve the puzzle
returns a solution or failure'''
def Backtrack(puz, assignment):
    #if complete, then end
    if puz.unassigned == 0:
        return True

    #choose next variable to assign through heuristics
    var = Select_Unassigned_Variable(puz.cells)

    #if the variable just has one value in the domain, assign that value
    if(len(var.domain) == 1):
        puz.unassigned -= 1
        var.assigned = True
        var.value = var.domain[0]
        return Backtrack(puz,assignment)

    #otherwise check values in the domain of the chosen variable
    for val in var.domain:
        #assign value as though it is correct
        var.value = val

        #if it is correct, keep the variable assignment
        if isValid(puz, var) == True:
            assignment[var] = val #add {var = value} to assignment
            puz.unassigned -= 1
            var.assigned = True
            var.value = val
            
            result = Backtrack(puz, assignment)
            if result != False:
                return result
            
            puz.unassigned += 1
            var.assigned = False
            var.value = None
            assignment.pop(var) #remove {var = value} from assignment
        #otherwise remove the assignment
        else:
            var.value = None
    return False

def solve(filename, outputFile):
    #read in starting puzzle
    puz = Puzzle()
    file = open(filename, 'r')
    for i in range(9):
        val = file.readline().strip().split(" ")
        if len(val) != 9:
            #check that the number of columns is correct, exit if not
            output = open(outputFile, 'w')
            output.write("invalid input")
            output.close()
            return
        puz.board.append(val)

    if len(puz.board) != 9:
        #check that the number of rows is correct, exit if not
        output = open(outputFile, 'w')
        output.write("invalid input")
        output.close()
        return

    file.close()

    #convert input board to list of Cell objects 
    for i in range(9):
        for j in range(9):
            if puz.board[i][j] != '0':
                val = int(puz.board[i][j])
            else:
                puz.unassigned += 1     #count the number of unassigned cells
                val = None
            sq = getSquare(i+1, j+1)    #add 1 to account for indexing of puz.board
            puz.cells.append(Cell(i+1,j+1,sq,val))

    #run forward checking algorithm to reduce cell domains
    #if the algorithm returns False, the board has no solution
    if(Forward_Checking(puz.cells) == False):
        output = open(outputFile, 'w')
        output.write("no solution")
        output.close()
        return

    singles = True

    #reduce the search space by automatically assigning cells with a single domain value
    #call Forward Checking again to re-establish domains after any changes
    while(singles):
        for obj in puz.cells:
            if obj.assigned == False:
                if len(obj.domain) == 1:
                    assignSingles(puz)
                    Forward_Checking(puz.cells)
                    continue
        singles = False

    #run the backtracking algorithm
    Backtracking_Search(puz)

    #print board to output file
    output = open(outputFile, 'w')
    counter = 0
    for obj in puz.cells:
        output.write(str(obj.value) + ' ')
        counter += 1
        if counter == 9:    
            output.write("\n")
            counter = 0
            
    output.close()
    
#call the function
#i.e. solve("Input1.txt", "Output1.txt")
