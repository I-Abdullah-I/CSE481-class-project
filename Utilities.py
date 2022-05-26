# cages = List<UDD:Cage>
# UDD Cage:
#   operator
#   value
#   List<UDD:Point>

import enum

class Operator(enum.Enum):
    Add = 0
    Subtract = 1
    Multiply = 2
    Divide = 3
    Constant = 4

class Cell:
    def __init__(self, x, y, value):
        self.x = x
        self.y = y
        self.value = value

class SubCage:
    def __init__(self, operator, value, cells):
        self.operator = operator
        self.value =  value
        self.cells = cells

# class Cage:
#     def __init__(self, list_sub_cages):


class KenKenBoard:
    def __init__(self, size, cages):
        self.size = size
        self.cages = cages
