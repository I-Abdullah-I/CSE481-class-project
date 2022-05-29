# cages = List<UDD:Cage>
# UDD Cage:
#   operator
#   value
#   List<UDD:Point>

import enum
from unittest import result
# from webbrowser import Opera
import numpy as np

class Operator(enum.Enum):
    Add = 0
    Subtract = 1
    Multiply = 2
    Divide = 3
    Constant = 4


class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.domain = np.empty((0),np.int32)


class SubCage:
    def __init__(self, operator, value, cells=[], solutions=[]):
        self.operator = operator
        self.value = value
        self.cells = cells
        # self.solutions = solutions

class KenKenBoard:
    def __init__(self, size, cages):
        self.size = size
        self.cages = cages
        self.mRowHash = np.full((size,size), False)
        self.mColHash = np.full((size,size), False)
        self.mstate = np.full((self.size, self.size), 0)
        rows,cols = (size,size)
        self.mDomain = [[0 for i in range(cols)] for j in range(rows)]
        self.current_x = 0
        self.current_y = 0

    # Initially fill all cells with all possible values and filling constants with its value only
    def init_domain_fill(self):
        default_domain = [x for x in range(1,self.size+1)]
        for cage in self.cages:
            if cage.operator == Operator.Constant:
                cage.cells[0].domain = [cage.value]
                index_x = cage.cells[0].x
                index_y = cage.cells[0].y
                self.mDomain[index_x][index_y] = [cage.value]
            else:
                index_x = [x1.x for x1 in cage.cells]
                index_y = [y1.y for y1 in cage.cells]
                for j in range(len(index_x)):
                    self.mDomain[index_x[j]][index_y[j]] = default_domain
                    cage.cells[j].domain = default_domain
        print(self.mDomain)

    def can_place(self, value, x, y):
        return not(self.mColHash[y][value-1] or self.mRowHash[x][value-1])

    def fill_freebie(self):
        for cage in self.cages:
            # Freebie case
            if len(cage.cells) == 1:
                x_pos = cage.cells[0].x
                y_pos = cage.cells[0].y
                self.mstate[x_pos][y_pos] = cage.value
                self.mColHash[y_pos][cage.value - 1] = True
                self.mRowHash[x_pos][cage.value - 1] = True
                self.cages.remove(cage)
        print('Freebies selection: ', self.mstate)

    def validate_cage_constraint(self):
        return 0

    def solve_with_backtracking(self):
        if np.all(self.mRowHash) and np.all(self.mColHash):
            print('Final mstate: \n', self.mstate)
            return 'success'
        for cage in self.cages:
            for cell in cage.cells:
                x_pos = cell.x
                y_pos = cell.y
                if self.mstate[x_pos][y_pos] == 0:
                    for val in cell.domain:
                        if self.can_place(val, x_pos, y_pos):
                            self.mColHash[y_pos][val - 1] = True
                            self.mRowHash[x_pos][val - 1] = True
                            self.mstate[x_pos][y_pos] = val
                            
                            if cage.cells.index(cell) == len(cage.cells) - 1:
                                cage_validated = self.validate_cage_constraint()
                            
                            if cage_validated:
                                result = self.solve_with_backtracking()
                            elif not cage_validated:
                                result = False

                            if not result:
                                self.mColHash[y_pos][val - 1] = False
                                self.mRowHash[x_pos][val - 1] = False
                                self.mstate[x_pos][y_pos] = 0
                            elif result:
                                return True
                            print('Current mstate: \n', self.mstate)
                            # input('Press any key to continue')
                    return False
                

    # def create_solutions(self):
    #     for cage in self.cages:
    #         num_of_cells = len(cage.cells)


    
    def print_board(self):
        print(self.mstate)

            

sub1 = SubCage(Operator.Constant, 2, [Cell(0, 0)])
sub2 = SubCage(Operator.Subtract, 2, [Cell(0, 1), Cell(1, 1)])
sub3 = SubCage(Operator.Subtract, 1, [Cell(0, 2), Cell(1, 2)])
sub4 = SubCage(Operator.Add, 6, [Cell(1, 0), Cell(2, 0), Cell(2, 1)])
sub5 = SubCage(Operator.Constant, 1, [Cell(2, 2)])
Cages = [sub1, sub2, sub3, sub4, sub5]
board = KenKenBoard(size = 3,cages = Cages)
# board.fill_board()
# board.print_board()
board.init_domain_fill()
board.fill_freebie()
board.solve_with_backtracking()