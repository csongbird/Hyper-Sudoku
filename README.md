# Hyper-Sudoku
A rough implementation of a hyper sudoku solver

Hyper Sudoku differs from the classic Sudoku in that four overlapping regions are defined in addition to
the regular regions, as described below. The rules of the game are:
* The game board consists of 9 × 9 cells divided into 3 × 3 non-overlapping regions. 
Four additional overlapping regions are defined. The game board therefore contains 9 non-overlapping 
regions and 4 overlapping regions, with each region containing 3 × 3 cells. 
Some of the cells already have numbers (1 to 9) assigned to them initially.
* The goal is to find assignments (1 to 9) for the empty cells so that every row, column, 
nonoverlapping region and overlapping region contains all the digits from 1 to 9. Each of the
9 digits, therefore, can only appear once in every row, column, non-overlapping region and
overlapping region. 

The program first applies Forward Checking to cells that already have a number
assigned to them and reduce the domain of their neighbors. If any cell has an empty domain after
applying Forward Checking, then the puzzle does not have a solution and the program can stop and
exit. 

Next, a Backtracking Algorithm is run to solve for a solution.
The function selects the next unassigned variable using the minimum remaining
value heuristic and then the degree heuristic. If there are more than one variables left after applying
the two heuristics, it arbitrarily chooses a variable to work on next. 

Input and output files: The program reads in the initial game board configuration from an
input text file and produces an output text file that contains the solution. The input file contains 9
rows (or lines) of integers. Each row contains 9 integers ranging from 0 to 9, separated by blank
spaces. Digits 1-9 represent the cell values and 0’s represent blank cells. 

***This project is done for the class CS 4613 at NYU Tandon in the Fall of 2020***
