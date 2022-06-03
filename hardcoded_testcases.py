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
# # board = KenKenBoard(3, cages)
# mstate = solve(cages, 4, 1)
# print(mstate)


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
# mstate = solve(cages, 3, 1)
# print("Solution:\n", mstate)

"""Test case No.5"""
# cages = [
#     Cage(operator=Operator.Divide, value=3, cells=[Cell(0,0), Cell(0,1)]),
#     Cage(operator=Operator.Constant, value=4, cells=[Cell(0,2)]),
#     Cage(operator=Operator.Constant, value=2, cells=[Cell(0,3)]),
#     Cage(operator=Operator.Add, value=6, cells=[Cell(1,0), Cell(2,0), Cell(2,1)]),
#     Cage(operator=Operator.Multiply, value=24, cells=[Cell(1,1), Cell(1,2), Cell(2,2), Cell(3,2)]),
#     Cage(operator=Operator.Add, value=8, cells=[Cell(1,3), Cell(2,3), Cell(3,3)]),
#     Cage(operator=Operator.Divide, value=2, cells=[Cell(3,0), Cell(3,1)]),
# ]
# mstate = solve(cages, 4, 1)
# print("Solution:\n", mstate)

"""Test case No.6"""
# cages = [
#     Cage(operator=Operator.Divide, value=2, cells=[Cell(0,0), Cell(1,0)]),
#     Cage(operator=Operator.Subtract, value=1, cells=[Cell(0,1), Cell(0,2)]),
#     Cage(operator=Operator.Add, value=8, cells=[Cell(0,3), Cell(1,3), Cell(2,3)]),
#     Cage(operator=Operator.Add, value=5, cells=[Cell(1,1), Cell(1,2), Cell(2,2)]),
#     Cage(operator=Operator.Add, value=5, cells=[Cell(2,0), Cell(3,0), Cell(3,1)]),
#     Cage(operator=Operator.Constant, value=3, cells=[Cell(2,1)]),
#     Cage(operator=Operator.Constant, value=4, cells=[Cell(3,2)]),
#     Cage(operator=Operator.Constant, value=2, cells=[Cell(3,3)]),
# ]
# mstate = solve(cages, 4, 1)
# print("Solution:\n", mstate)