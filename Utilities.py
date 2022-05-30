import enum
import numpy as np
from Generate import generate
from main_utilities import *

class KenKenBoard:
    def __init__(self, size, cages):
        self.size = size
        self.cages = cages
        self.mRowHash = np.full((size,size), False)
        self.mColHash = np.full((size,size), False)
        self.mstate = np.full((self.size, self.size), 0)
        rows,cols = (size,size)
        self.mDomain = [[0 for i in range(cols)] for j in range(rows)]
    
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

    """Initially fill all cells with all possible values and filling constants with its value only"""
    def init_domain_fill(self):
        default_domain = [x for x in range(1,self.size+1)]
        for cage in self.cages:
            if cage.operator == Operator.Constant:
                cage.cells[0].domain = [cage.value]
            else:
                for j in range(len(cage.cells)):
                    cage.cells[j].domain = default_domain

    def can_place(self, value, x, y):
        return not(self.mColHash[y][value-1] or self.mRowHash[x][value-1])

    def fill_freebie(self):
        filtered_list = list(self.cages)
        for cage in self.cages:
            if len(cage.cells) == 1:
                x_pos = cage.cells[0].x
                y_pos = cage.cells[0].y
                self.mstate[x_pos][y_pos] = cage.value
                self.mColHash[y_pos][cage.value - 1] = True
                self.mRowHash[x_pos][cage.value - 1] = True
                filtered_list.remove(cage)
        self.cages = filtered_list
        # print('Freebies selection:\n', self.mstate)

    def solve_with_backtracking(self):
        if np.all(self.mRowHash) and np.all(self.mColHash):
            # print('Final mstate:\n', self.mstate)
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
                            # print('Current mstate: \n', self.mstate)
                            # input('Press any key to continue')
                    return False

def solve(cages, size, algorithm):
    board = KenKenBoard(size=size, cages=cages)
    board.init_domain_fill()
    board.fill_freebie()
    if algorithm == 0:
        board.solve_with_backtracking()
        return board.mstate
    elif algorithm == 1:
        pass
    elif algorithm == 2:
        pass


"""Test case No.1"""
# sub1 = Cage(Operator.Constant, 2, [Cell(0, 0)])
# sub2 = Cage(Operator.Subtract, 2, [Cell(0, 1), Cell(1, 1)])
# sub3 = Cage(Operator.Subtract, 1, [Cell(0, 2), Cell(1, 2)])
# sub4 = Cage(Operator.Add, 6, [Cell(1, 0), Cell(2, 0), Cell(2, 1)])
# sub5 = Cage(Operator.Constant, 1, [Cell(2, 2)])
# Cages = [sub1, sub2, sub3, sub4, sub5]
# board = KenKenBoard(size = 3,cages = Cages)
# board.init_domain_fill()
# board.fill_freebie()
# board.solve_with_backtracking()

"""Test case No.2"""
# cages = [
#     Cage(operator=Operator.Divide, value=2, cells=[Cell(0,0), Cell(1,0)]),
#     Cage(operator=Operator.Add, value=6, cells=[Cell(0,1), Cell(1,1),Cell(2,1)]),
#     Cage(operator=Operator.Subtract, value=1, cells=[Cell(0,2), Cell(0,3)]),
#     Cage(operator=Operator.Multiply, value=12, cells=[Cell(1,2), Cell(1,3), Cell(2,3)]),
#     Cage(operator=Operator.Constant, value=1, cells=[Cell(2,0)]),
#     Cage(operator=Operator.Add, value=5, cells=[Cell(3,2), Cell(2,2), Cell(3,3)]),
#     Cage(operator=Operator.Subtract, value=1, cells=[Cell(3,0), Cell(3,1)])
# ]
# board = KenKenBoard(size = 4, cages = cages)
# board.init_domain_fill()
# board.fill_freebie()
# board.solve_with_backtracking()

"""Test case No.3"""
# cages = [
#     Cage(operator=Operator.Subtract, value=1, cells=[Cell(0,0), Cell(1,0)]),
#     Cage(operator=Operator.Add, value=6, cells=[Cell(0,1), Cell(1,1), Cell(2,1)]),
#     Cage(operator=Operator.Multiply, value=8, cells=[Cell(0,2), Cell(0,3), Cell(1, 2)]),
#     Cage(operator=Operator.Divide, value=2, cells=[Cell(2,0), Cell(3,0)]),
#     Cage(operator=Operator.Constant, value=4, cells=[Cell(3,1)]),
#     Cage(operator=Operator.Add, value=8, cells=[Cell(3,2), Cell(2,2), Cell(3,3)]),
#     Cage(operator=Operator.Subtract, value=3, cells=[Cell(1,3), Cell(2,3)])
# ]
# mstate = solve(cages, 4, 0)
# print("Solution:\n", mstate)

"""Test case No.4"""
# cages = [
#     Cage(operator=Operator.Add, value=6, cells=[Cell(0,0), Cell(0,1), Cell(1,1)]),
#     Cage(operator=Operator.Add, value=6, cells=[Cell(0,2), Cell(1,2), Cell(2,2)]),
#     Cage(operator=Operator.Add, value=6, cells=[Cell(1,0), Cell(2,0), Cell(2,1)]),
# ]
# mstate = solve(cages, 3, 0)
# print("Solution:\n", mstate)

"""Test case No.5"""
# cages = [
#     Cage(operator=Operator.Multiply, value=4, cells=[Cell(0,1), Cell(0,2), Cell(1,2)]),
#     Cage(operator=Operator.Add, value=10, cells=[Cell(0,3), Cell(1,3), Cell(2,3), Cell(2,2)]),
#     Cage(operator=Operator.Add, value=12, cells=[Cell(1,0), Cell(1,1), Cell(2,1), Cell(3,1)]),
#     Cage(operator=Operator.Divide, value=2, cells=[Cell(2,0), Cell(3,0)]),
#     Cage(operator=Operator.Constant, value=3, cells=[Cell(3,3)]),
# ]
# mstate = solve(cages, 4, 0)
# print("Solution:\n", mstate)

"""Test case No.5"""
# cages = [
#     Cage(operator=Operator.Multiply, value=420, cells=[Cell(0,0), Cell(0,1), Cell(1,0), Cell(1,1)]),
#     Cage(operator=Operator.Multiply, value=10, cells=[Cell(0,2), Cell(0,3), Cell(0,4)]),
#     Cage(operator=Operator.Multiply, value=84, cells=[Cell(1,2), Cell(1,3), Cell(1,4)]),
#     Cage(operator=Operator.Subtract, value=5, cells=[Cell(0,5), Cell(1,5)]),
#     Cage(operator=Operator.Multiply, value=72, cells=[Cell(0,6), Cell(0,7)]),
#     Cage(operator=Operator.Divide, value=2, cells=[Cell(0,8), Cell(1,8)]),
#     Cage(operator=Operator.Multiply, value=288, cells=[Cell(2,0), Cell(3,0), Cell(4,0)]),
#     Cage(operator=Operator.Add, value=3, cells=[Cell(2,1), Cell(2,2)]),
#     Cage(operator=Operator.Multiply, value=12, cells=[Cell(2,3), Cell(2,4)]),
#     Cage(operator=Operator.Multiply, value=168, cells=[Cell(2,3), Cell(2,4)]),
#     Cage(operator=Operator.Constant, value=4, cells=[Cell(3,1)]),
#     Cage(operator=Operator.Add, value=8, cells=[Cell(3,2), Cell(2,2), Cell(3,3)]),
#     Cage(operator=Operator.Subtract, value=3, cells=[Cell(1,3), Cell(2,3)])
# ]
# board = KenKenBoard(size = 4, cages = cages)
# board.init_domain_fill()
# board.fill_freebie()
# board.solve_with_backtracking()

"""Random Testcase"""
size = 4
cages, solution = generate(size)
cells_count = 0
for cage in cages:
#     print(type(cage.cells[0]))
    cells_count += len(cage.cells)
    print('Cage operator: {} \t cage value: {} \t cage cells: {}'.format(cage.operator, cage.value, [(cell.x, cell.y) for cell in cage.cells]))
print(cells_count)
print("Solution\n", solution)
print("My solution:\n", solve(cages, size, 0))