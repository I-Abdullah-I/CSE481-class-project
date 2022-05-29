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


class Cage:
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


    def validate_cage_constraint(self, cage):
     
        expansion_of_cage = list()
        for cell in cage.cells:
            expansion_of_cage.append(self.mstate[cell.x][cell.y])

        if cage.operator == Operator.Add :
            return sum(expansion_of_cage) == cage.value
        elif cage.operator == Operator.Subtract : #Subtract Cages is only 2 cells
            """
            Subtract Cages is only 2 cells
            Because order of subrtacting among more than 2 cells will be distinctive
            """
            if len(expansion_of_cage) != 2 :
                return False
            return abs(expansion_of_cage[0]-expansion_of_cage[1]) == cage.value

        elif cage.operator == Operator.Multiply :
            return np.prod(expansion_of_cage) == cage.value

        elif cage.operator == Operator.Divide : #Division Cages is only 2 cells
            """
            Subtract Cages is only 2 cells
            Because order of subrtacting among more than 2 cells will be distinctive
            """
            if(expansion_of_cage[0] > expansion_of_cage[1]):
                return (expansion_of_cage[0] / expansion_of_cage[1]) == cage.value
            elif(expansion_of_cage[0] < expansion_of_cage[1]):
                return (expansion_of_cage[1] / expansion_of_cage[0]) == cage.value








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

    

    def solve_with_backtracking(self):
        if np.all(self.mRowHash) and np.all(self.mColHash):
            print('Final mstate: \n', self.mstate)
            return True
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
                            
                            if cell == cage.cells[-1]:
                                
                                cage_validated = self.validate_cage_constraint(cage)
                            else:
                                cage_validated = True
                            
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

            

# sub1 = Cage(Operator.Constant, 2, [Cell(0, 0)])
# sub2 = Cage(Operator.Subtract, 2, [Cell(0, 1), Cell(1, 1)])
# sub3 = Cage(Operator.Subtract, 1, [Cell(0, 2), Cell(1, 2)])
# sub4 = Cage(Operator.Add, 6, [Cell(1, 0), Cell(2, 0), Cell(2, 1)])
# sub5 = Cage(Operator.Constant, 1, [Cell(2, 2)])


# Cages = [sub1, sub2, sub3, sub4, sub5]
# board = KenKenBoard(size = 3,cages = Cages)
# board.fill_board()
# board.print_board()

cages = [Cage(operator=Operator.Divide, value=2, cells=[Cell(0,0), Cell(1,0)])
, Cage(operator=Operator.Add, value=6, cells=[Cell(0,1), Cell(1,1),Cell(2,1)])
, Cage(operator=Operator.Subtract, value=1, cells=[Cell(0,2), Cell(0,3)])
, Cage(operator=Operator.Multiply, value=12, cells=[Cell(1,2), Cell(1,3), Cell(2,3)])
, Cage(operator=Operator.Constant, value=1, cells=[Cell(2,0)])
, Cage(operator=Operator.Add, value=5, cells=[Cell(3,2), Cell(2,2), Cell(3,3)])
, Cage(operator=Operator.Subtract, value=1, cells=[Cell(3,0), Cell(3,1)])]

board = KenKenBoard(size = 4, cages = cages)

board.print_board()


board.init_domain_fill()
board.fill_freebie()
board.solve_with_backtracking()