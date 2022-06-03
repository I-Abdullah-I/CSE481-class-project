from datetime import datetime
import enum
from math import fabs
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
        self.queue = []
    
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
        elif cage.operator == Operator.Constant :
            return True

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

    def solve_with_backtracking(self, arc_consistency= False):
        if np.all(self.mRowHash) and np.all(self.mColHash):
            # print('Final mstate:\n', self.mstate)
            return True
        for cage in self.cages:
            for cell in cage.cells:
                x_pos = cell.x
                y_pos = cell.y
                if self.mstate[x_pos][y_pos] == 0:
                    old_domain = cell.domain
                    for val in old_domain:
                        if self.can_place(val, x_pos, y_pos):
                            cell.domain = [val]
                            self.mColHash[y_pos][val - 1] = True
                            self.mRowHash[x_pos][val - 1] = True
                            self.mstate[x_pos][y_pos] = val
                            
                            if cell == cage.cells[-1]:
                                
                                cage_validated = self.validate_cage_constraint(cage)
                            else:
                                cage_validated = True
                            
                            if cage_validated:
                                if arc_consistency:
                                    self.generate_queue(cell=cell, cage=cage)
                                    if self.AC3():
                                        result = self.solve_with_backtracking(arc_consistency=True)
                                    else :
                                        result = False
                                else :
                                    result = self.solve_with_backtracking()
                            elif not cage_validated:
                                result = False

                            if not result:
                                cell.domain = old_domain
                                self.mColHash[y_pos][val - 1] = False
                                self.mRowHash[x_pos][val - 1] = False
                                self.mstate[x_pos][y_pos] = 0
                            elif result:
                                return True
                            # print('Current mstate: \n', self.mstate)
                            # input('Press any key to continue')
                    return False



            
    def generate_queue(self, cage, cell, filter = False, cell2 = None):
        # for cage in self.cages :
        #     for cell in cage.cells:
        for cage1 in self.cages :
            for cell1 in cage1.cells:

                if (cell == cell1) or (filter and (cell1 == cell2)):
                    continue

                if (cage == cage1) and (len(cage.cells) == 2) and ((cage,cell),cell1) not in self.queue:
                    self.queue.append(((cage,cell),cell1))
                    continue
                
                if (cell1.x != cell.x and cell1.y == cell.y) or (cell1.x == cell.x and cell1.y != cell.y) and ((cage,cell),cell1) not in self.queue:
                    self.queue.append(((cage,cell),cell1))

                        

  
        # x1 = cell.x
        # y1 = cell.y
        
        # domain = cell.domain

        
        # if(len(domain) > 1):
        #     return 0
        # elif (len(domain) == 0) :
        #     return -1
        
        # if len(cage.cells) == 2 : #Has two elements
        #     index_of_cell = cage.cells.where(cage.cells == cell)

        #     if cage.operation == Operator.Multiply :
        #         expected = cage.value / cell.domain[0]
        #         if expected == cell.domain[0] :
        #             return -1
        #         domain_neighbour = cage.cells[1-index_of_cell].domain
        #         cage.cells[1-index_of_cell].domain = intersection(cage.cells[1-index_of_cell].domain, [expected])
        #         v = self.check_constraints(cage, cage.cells[1-index_of_cell])
        #         if v == -1:
        #             cage.cells[1-index_of_cell].domain = domain_neighbour
        #             return -1
        #     elif cage.operation == Operator.Add :
        #         expected = cage.value - cell.domain[0]
                
        #         domain_neighbour = cage.cells[1-index_of_cell].domain
        #         cage.cells[1-index_of_cell].domain = intersection(cage.cells[1-index_of_cell].domain, [expected])
        #         v = self.check_constraints(cage, cage.cells[1-index_of_cell])
        #         if v == -1:
        #             cage.cells[1-index_of_cell].domain = domain_neighbour
        #             return -1
        #     elif cage.operation == Operator.Subtract :
        #         expected = cage.value + cell.domain[0]
        #         if expected > self.size :
        #             expected = cage.value - cell.domain[0]
        #             if expected > self.size :
        #                 return -1
        #         if expected == cell.domain[0] :
        #             return -1
        #         domain_neighbour = cage.cells[1-index_of_cell].domain
        #         cage.cells[1-index_of_cell].domain = intersection(cage.cells[1-index_of_cell].domain, [expected])
        #         v = self.check_constraints(cage, cage.cells[1-index_of_cell])
        #         if v == -1:
        #             cage.cells[1-index_of_cell].domain = domain_neighbour
        #             return -1
        #     elif cage.operation == Operator.Divide :
        #         expected = cage.value * cell.domain[0] #Numerator
        #         if expected > self.size :
        #             expected = cell.domain[0] / self.size
        #             if expected > self.size :
        #                 return -1
        #         if expected == cell.domain[0] :
        #             return -1
        #         domain_neighbour = cage.cells[1-index_of_cell].domain
        #         cage.cells[1-index_of_cell].domain = intersection(cage.cells[1-index_of_cell].domain, [expected])
        #         v = self.check_constraints(cage, cage.cells[1-index_of_cell])
        #         if v == -1:
        #             cage.cells[1-index_of_cell].domain = domain_neighbour
        #             return -1


        # #Row and col
        # for c in self.cages:
        #     for ce in c.cells:
            
        #         dom = ce.domain
        #         v = None
        #         if ce.x != x1 and ce.y == y1 : #Same Column
        #             next = Diff(dom, domain)
        #             if ce.domain == next:
        #                 return 0
        #             ce.domain = next
        #             if len(c.cells) == 1 :
        #                 # self.mstate[ce.x][ce.y] = cage.value
        #                 # self.mColHash[ce.y][cage.value - 1] = True
        #                 # self.mRowHash[ce.x][cage.value - 1] = True
        #                 cage.cells[0].domain = [cage.value]
        #             v = self.check_constraints(c, ce)
        #         # elif ce.x == (x1+2) % 3  and ce.y == y1 :
        #         #     ce.domain = np.setdiff1d(ce.domain, domain)
        #         #     if len(c.cells) == 1 :
        #         #         # self.mstate[ce.x][ce.y] = cage.value
        #         #         # self.mColHash[ce.y][cage.value - 1] = True
        #         #         # self.mRowHash[ce.x][cage.value - 1] = True
        #         #         cage.cells[0].domain = np.array([cage.value])
        #         #     v = self.check_constraints(c, ce)
        #         elif ce.x == x1  and ce.y != y1 : #Same Row
                    
        #             next = Diff(dom, domain)
        #             if ce.domain == next:
        #                 return 0
        #             ce.domain = next
        #             if len(c.cells) == 1 :
        #                 # self.mstate[ce.x][ce.y] = cage.value
        #                 # self.mColHash[ce.y][cage.value - 1] = True
        #                 # self.mRowHash[ce.x][cage.value - 1] = True
        #                 cage.cells[0].domain = [cage.value]
        #             v = self.check_constraints(c, ce)
        #         # elif ce.x == x1  and ce.y == (y1+2)%3 :
        #         #     ce.domain = np.setdiff1d(ce.domain, domain)
        #         #     if len(c.cells) == 1 :
        #         #         # self.mstate[ce.x][ce.y] = cage.value
        #         #         # self.mColHash[ce.y][cage.value - 1] = True
        #         #         # self.mRowHash[ce.x][cage.value - 1] = True
        #         #         cage.cells[0].domain = np.array([cage.value])
        #         #     v = self.check_constraints(c, ce)
                
        #         if v == -1  :
        #             ce.domain = dom
        #             return -1
        
        # return 1

    def remove_inconsistent_values(self, cage, cell1, cell2):
        removed = False

        # to_be_removed = False

        #only compare to single element domain in cell2
        if len(cell2.domain) == 1:
            if (cell1.x != cell2.x and cell1.y == cell2.y) or (cell1.x == cell2.x and cell1.y != cell2.y) :
                virtual_domain = cell1.domain
                for domain in cell1.domain:
                    if domain == cell2.domain[0]:
                        virtual_domain.remove(domain)
                        removed = True
        
                cell1.domain = virtual_domain
        return removed

    def AC3(self):
        while len(self.queue) != 0:
            binary_arc = self.queue[0]
            self.queue = self.queue[1:]
            cage = binary_arc[0][0]
            cell = binary_arc[0][1]
            cell1 = binary_arc[1]
            old_domain = [] + cell.domain
            if self.remove_inconsistent_values(cage, cell, cell1):
                if len(cell.domain) == 0 :
                    cell.domain = old_domain
                    return False
                self.generate_queue(cage, cell, filter=True, cell2 = cell1)
        return True

def solve(cages, size, algorithm):
    # sub1 = Cage(Operator.Constant, 2, [Cell(0, 0)])
    # sub2 = Cage(Operator.Subtract, 2, [Cell(0, 1), Cell(1, 1)])
    # sub3 = Cage(Operator.Subtract, 1, [Cell(0, 2), Cell(1, 2)])
    # sub4 = Cage(Operator.Add, 6, [Cell(1, 0), Cell(2, 0), Cell(2, 1)])
    # sub5 = Cage(Operator.Constant, 1, [Cell(2, 2)])
    # cages = [sub1, sub2, sub3, sub4, sub5]
    board = KenKenBoard(size=size, cages=cages)
    board.init_domain_fill()
    
    # algorithm = 2
    if algorithm == 0:
        board.fill_freebie()
        board.solve_with_backtracking()
        return board.mstate
    elif algorithm == 1:
        pass
    elif algorithm == 2:
        board.solve_with_backtracking(arc_consistency=True)
        return board.mstate



def intersection(lst1, lst2):
    return list(set(lst1) & set(lst2))


def Diff(li1, li2):
    return list(set(li1) - set(li2))








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
size = 6
cages, solution = generate(size)
cells_count = 0
for cage in cages:
#     print(type(cage.cells[0]))
    cells_count += len(cage.cells)
    print('Cage operator: {} \t cage value: {} \t cage cells: {}'.format(cage.operator, cage.value, [(cell.x, cell.y) for cell in cage.cells]))
print(cells_count)
print("Solution\n", solution)
t1 = datetime.now()
print("My solution:\n", solve(cages, size, 0))
print(datetime.now() - t1)