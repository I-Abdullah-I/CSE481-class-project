import numpy as np
from Generate import generate
from main_utilities import *
import copy
import timeit


class KenKenBoard:
    def __init__(self, size, cages):
        self.size = size
        self.cages = cages
        self.mRowHash = np.full((self.size, self.size), False)
        self.mColHash = np.full((self.size, self.size), False)
        self.mstate = np.full((self.size, self.size), 0)
        """Two dimensional array holding the available domain values per each cell in the board"""
        self.mDomain = [[[0] for i in range(self.size)] for j in range(self.size)]
    
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
        default_domain = [x for x in range(1, self.size+1)]
        for cage in self.cages:
            if cage.operator == Operator.Constant:
                cage.cells[0].domain = [cage.value] # should be removed
                index_x = cage.cells[0].x
                index_y = cage.cells[0].y
                self.mDomain[index_x][index_y] = [cage.value]
            else:
                for cell in cage.cells:
                    self.mDomain[cell.x][cell.y] = default_domain
                # should be removed
                for j in range(len(cage.cells)):
                    cage.cells[j].domain = default_domain
        # print(self.mDomain)

    def can_place(self, value, x, y):
        return not(self.mColHash[y][value-1] or self.mRowHash[x][value-1])

    def forward_checking(self, value, x_pos, y_pos, mDomain, freebie_domain=False):
        mDomain_temp = copy.deepcopy(mDomain)
        for col_iter in range(self.size):
            if not col_iter == y_pos:
                domain_temp = list(mDomain_temp[x_pos][col_iter])
                if value in domain_temp:
                    domain_temp.remove(value)
                    mDomain_temp[x_pos][col_iter] = domain_temp
        for row_iter in range(self.size):
            if not row_iter == x_pos: 
                domain_temp = list(mDomain_temp[row_iter][y_pos])
                if value in domain_temp:
                    domain_temp.remove(value)
                    mDomain_temp[row_iter][y_pos] = domain_temp
        
        if freebie_domain == True:
            mDomain_temp[x_pos][y_pos] = [-1]
        else:
            domain_temp = list(mDomain_temp[x_pos][y_pos])
            domain_temp.remove(value)
            mDomain_temp[x_pos][y_pos] = domain_temp
        return mDomain_temp

    def fill_freebie(self, algorithm = 0):
        filtered_list = list(self.cages)
        for cage in self.cages:
            if len(cage.cells) == 1:
                x_pos = cage.cells[0].x
                y_pos = cage.cells[0].y
                self.mstate[x_pos][y_pos] = cage.value
                self.mColHash[y_pos][cage.value - 1] = True
                self.mRowHash[x_pos][cage.value - 1] = True
                filtered_list.remove(cage)
                if algorithm == 1:
                    self.mDomain = self.forward_checking(cage.value, x_pos, y_pos, self.mDomain, True)
        self.cages = filtered_list
        # print('mDomain after freebie filling:\n', self.mDomain)
        # print('mstate after freebie filling:\n', self.mstate)

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

    def solve_with_backtracking_and_forward_checking(self, var_domains):
        if np.all(self.mRowHash) and np.all(self.mColHash):
            # print('Final mstate:\n', self.mstate)
            return True
        for cage in self.cages:
            for cell in cage.cells:
                x_pos = cell.x
                y_pos = cell.y
                if self.mstate[x_pos][y_pos] == 0:
                    for val in var_domains[x_pos][y_pos]:
                        if self.can_place(val, x_pos, y_pos):
                            self.mColHash[y_pos][val - 1] = True
                            self.mRowHash[x_pos][val - 1] = True
                            self.mstate[x_pos][y_pos] = val
                            new_var_domains = self.forward_checking(val, x_pos, y_pos, var_domains)

                            if cell == cage.cells[-1]:
                                cage_validated = self.validate_cage_constraint(cage)
                            else:
                                cage_validated = True
                            
                            if cage_validated:
                                result = self.solve_with_backtracking_and_forward_checking(new_var_domains)
                            elif not cage_validated:
                                result = False

                            if not result:
                                self.mColHash[y_pos][val - 1] = False
                                self.mRowHash[x_pos][val - 1] = False
                                self.mstate[x_pos][y_pos] = 0
                            elif result:
                                # print('Backtracked')
                                return True
                            # print('Current mstate: \n', self.mstate)
                            # input('Press any key to continue')
                    return False

def solve(cages, size, algorithm):
    """
    algorithm = 0   => normal backtracking
    algorithm = 1   => backtracking with forward checking
    algorithm = 2   => backtracking with arc consistency
    """
    board = KenKenBoard(size=size, cages=cages)
    board.init_domain_fill()
    if algorithm == 0:
        board.fill_freebie(algorithm)
        board.solve_with_backtracking()
        print("My solution:\n", board.mstate)
        return board.mstate
    elif algorithm == 1:
        board.fill_freebie(algorithm)
        board.solve_with_backtracking_and_forward_checking(board.mDomain)
        print("My solution:\n", board.mstate)
        return board.mstate
    elif algorithm == 2:
        pass

"""Random Testcase"""
size = 3
cages, solution = generate(size)
cells_count = 0
for cage in cages:
    cells_count += len(cage.cells)
    print('Cage operator: {} \t cage value: {} \t\t cage cells: {}'.format(cage.operator, cage.value, [(cell.x, cell.y) for cell in cage.cells]))
print(cells_count)
print("Ready solution\n", solution)
t = timeit.timeit(lambda: solve(cages, size, 1), number=1)
print('backtracking with forward checking: ', t)
t = timeit.timeit(lambda: solve(cages, size, 0), number=1)
print('backtracking only: ', t)
# print("My solution:\n", solve(cages, size, 1))
# solve(cages, size, 1)