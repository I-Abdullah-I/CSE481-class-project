# cages = List<UDD:Cage>
# UDD Cage:
#   operator
#   value
#   List<UDD:Point>

import enum
from webbrowser import Opera
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
    def __init__(self, operator, value, cells):
        self.operator = operator
        self.value = value
        self.cells = cells



# class Cage:
#     def __init__(self, list_sub_cages):
#         self.list_sub_cages =

class KenKenBoard:
    def __init__(self, size, cages):
        self.size = size
        self.cages = cages
        self.mRowHash = np.full((size,size),False)
        self.mColHash = np.full((size,size),False)
        self.mstate = np.empty((0, self.size), np.int32)
        rows,cols = (size,size)
        self.mDomain = [[0 for i in range(cols)] for j in range(rows)]

    # Initially fill all cells with all possible values and filling constants with its value only
    def init_domain_fill(self):
        default_domain = [x for x in range(1,self.size+1)]
        for cage in self.cages:
            if cage.operator == Operator.Constant:
                index_x = cage.cells[0].x
                index_y = cage.cells[0].y
                self.mDomain[index_x][index_y] = [cage.value]
            else:
                index_x = [x1.x for x1 in cage.cells]
                index_y = [y1.y for y1 in cage.cells]
                for j in range(len(index_x)):
                    self.mDomain[index_x[j]][index_y[j]] = default_domain
        # print(self.mDomain)

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