# Hootan Hosseinzadeganbushehri


from math import inf
from AI import AI
from Action import Action
from collections import deque
import secrets


class MyAI(AI):
    class Square:
        def __init__(self):
            self.trap = False
            self.mark = False
            self.reduction = 10
            self.marked = True
            self.solution = True
            self.update = 100
            self.counter = -self.update

        def check_square(self, temp):
            if temp != self.update:
                self.update += 1
                return True
            else:
                self.update -= 1
                return False

        def clear_square(self):
            if not self.check_square(50):
                self.update = 0
            elif self.check_square(0):
                self.reduction += 1
            else:
                self.update -= 1
                self.reduction = 0

    def __init__(self, rowDimension, colDimension, totalMines, startX, startY):
        count = 0
        self.check_move = False
        self.check_out = True
        self.game_grid = []
        self.grid_rows = rowDimension
        self.previous_square = None
        self.grid_columns = colDimension
        self.previous_move = None
        self.grid_traps = totalMines
        self.previous_column = startX
        self.remained_traps = totalMines
        self.previous_row = startY
        self.solution_queue = deque([])
        self.unmarked_squared = []
        for x in range(self.grid_rows):
            for y in range(self.grid_columns):
                self.unmarked_squared.append((y, x))
        self.odds_dict = {}
        self.grid_traps = []
        self.traps_remained = totalMines
        while count != self.grid_columns:
            self.game_grid.append([self.Square() for x in range(0, self.grid_rows)])
            count += 1
        self.unmarked_squared.remove((startX, startY))
        self.bound_check1 = 0
        self.previous_column = startX
        self.bound_check2 = 0
        self.previous_row = startY
        self.game_grid[startX][startY].marked = False
        self.grid_check1 = True
        self.game_grid[startX][startY].counter = 0
        self.grid_check2 = True
        self.previous_square = self.game_grid[startX][startY]
        self.previous_move = AI.Action(1)

    def getAction(self, number: int) -> "Action Object":
        start_column = self.previous_column - 1
        end_column = self.previous_column + 2
        start_row = self.previous_row - 1
        end_row = self.previous_row + 2
        if self.previous_move == AI.Action(1):
            self.previous_square.marked = False
            self.previous_square.counter = number
            self.check_move = False
        if number != 0:
            self.check_move = True
        else:
            for y in range(start_column, end_column):
                for x in range(start_row, end_row):
                    if self.grid_rows > x >= 0 and self.grid_columns > y >= 0:
                        if (y == self.previous_column and x == self.previous_row) == False:
                            if self.game_grid[y][x].marked and ((y, x) not in self.solution_queue):
                                self.solution_queue.append((y, x))
                                self.grid_check1 = True
                            else:
                                self.bound_check1 += 1
                                self.grid_check1 = False
        while self.solution_queue != deque([]):
            priority = self.solution_queue.popleft()
            if self.grid_traps == 0:
                self.check_move = False
            self.action_history(AI.Action(1), priority[0], priority[1])
            self.check_move = True
            return Action(AI.Action(1), priority[0], priority[1])
        for y in range(self.grid_columns):
            for x in range(self.grid_rows):
                if self.game_grid[y][x].marked == False and self.game_grid[y][x].counter != 0:
                    self.bound_check2 -= 1
                    if self.game_grid[y][x].counter == self.explored_squares(y, x)[0]:
                        for i in self.explored_squares(y, x)[1]:
                            if (i[0], i[1]) not in self.grid_traps:
                                self.traps_remained -= 1
                                self.grid_check1 = False
                                self.grid_traps.append((i[0], i[1]))
                                self.grid_check2 = False
                                self.game_grid[i[0]][i[1]].trap = True
                                self.bound_check1 += 1
                                self.game_grid[i[0]][i[1]].mark = True
                                self.bound_check2 += 1
                                self.unmarked_squared.remove((i[0], i[1]))
        for y in range(self.grid_columns):
            for x in range(self.grid_rows):
                if self.near_traps(y, x)[0] == self.game_grid[y][x].counter:
                    if self.explored_squares(y, x)[0] - self.near_traps(y, x)[0] > 0:
                        self.grid_check1 = True
                        for i in self.explored_squares(y, x)[1]:
                            if i not in self.near_traps(y, x)[1]:
                                if i not in self.solution_queue:
                                    self.bound_check2 += 1
                                    self.solution_queue.append(i)
        while self.solution_queue != deque([]):
            priority = self.solution_queue.popleft()
            if self.grid_traps == 0:
                self.check_move = False
            self.action_history(AI.Action(1), priority[0], priority[1])
            self.check_move = True
            return Action(AI.Action(1), priority[0], priority[1])
        for y in range(self.grid_columns):
            for x in range(self.grid_rows):
                if self.game_grid[y][x].counter > 0 and self.uncovered_s(y, x)[0] > 0:
                    y1 = y - 2
                    y2 = y + 3
                    x1 = x - 2
                    x2 = x + 3
                    clear_square = []
                    self.grid_check2 = False
                    around_squares = []
                    for y3 in range(y1, y2):
                        for r3 in range(x1, x2):
                            if self.grid_columns > y3 >= 0 and self.grid_rows > r3 >= 0:
                                if (y3, r3) != (y, x):
                                    self.bound_check2 += 1
                                    around_squares.append((y3, r3))
                    for i in set(around_squares):
                        if self.game_grid[i[0]][i[1]].counter < 1:
                            self.grid_check1 = True
                            self.bound_check1 += 1
                            continue
                        if (y, x) in self.near_s(i):
                            self.near_s(i).remove((y, x))
                        test1 = True
                        test_a = True
                        for m in self.near_s(i):
                            if self.game_grid[m[0]][m[1]].marked and self.game_grid[m[0]][m[1]].mark == False:
                                test_a = False
                            if not test_a:
                                test1 = False
                        if test1:
                            self.grid_check2 = True
                            self.bound_check2 += 1
                            continue
                        if i in self.near_s((y, x)):
                            self.grid_check2 = False
                            self.near_s((y, x)).remove(i)
                        traps1 = set(self.near_traps((y, x)[0], (y, x)[1])[1])
                        self.grid_check1 = True
                        traps2 = set(self.near_traps(i[0], i[1])[1])
                        traps3 = len(traps1.intersection(self.near_s((y, x)).difference(self.near_s(i))))
                        traps4 = len(traps2.intersection(self.near_s(i).difference(self.near_s((y, x)))))
                        test2 = True
                        test_b = True
                        for n in self.near_s(i).difference(self.near_s((y, x))):
                            if self.game_grid[n[0]][n[1]].marked and self.game_grid[n[0]][n[1]].mark == False:
                                test_b = False
                            if not test_b:
                                test2 = False
                        if not test2:
                            self.grid_check1 = True
                            self.bound_check1 += 1
                            continue
                        if traps4 == 0 and len(traps1.intersection(self.near_s(i))) == 0:
                            self.grid_check2 = True
                            self.bound_check2 -= 1
                            continue
                        check1 = (self.game_grid[y][x].counter - traps3)
                        check2 = (self.game_grid[i[0]][i[1]].counter - traps4)
                        test_c = True
                        if check1 == check2:
                            for s in self.near_s((y, x)).difference(self.near_s(i)):
                                if self.game_grid[s[0]][s[1]].marked and self.game_grid[s[0]][s[1]].mark == False:
                                    test_c = False
                                if not test_c:
                                    self.bound_check1 += 1
                                    clear_square.append(s)
                    if clear_square:
                        for i in clear_square:
                            if i in self.unmarked_squared:
                                if i not in self.solution_queue:
                                    self.bound_check2 -= 1
                                    self.solution_queue.append(i)
        while self.solution_queue != deque([]):
            priority = self.solution_queue.popleft()
            if self.grid_traps == 0:
                self.check_move = False
            self.action_history(AI.Action(1), priority[0], priority[1])
            self.check_move = True
            return Action(AI.Action(1), priority[0], priority[1])
        controlled_s = []
        self.grid_check2 = True
        bound_s = []
        for y in range(self.grid_columns):
            for x in range(self.grid_rows):
                if self.uncovered_s(y, x)[0] > 0:
                    if self.game_grid[y][x].counter > 0:
                        self.grid_check2 = False
                        controlled_s.append((y, x))
                        self.bound_check2 -= 1
        for i in self.unmarked_squared:
            if len(self.near_s((i[0], i[1]))) - self.explored_squares(i[0], i[1])[0] > 0:
                self.bound_check1 += 1
                bound_s.append(i)
        if len(controlled_s) + 1 != 1 and len(self.unmarked_squared) + 1 != 1:
            y_temp = []
            pattern_check = []
            clear_square = []
            check_traps = []
            count1 = 0
            count6 = 0
            temp_test = False
            for i in range(len(self.unmarked_squared) + 1):
                self.grid_check1 = False
                y_temp.append(i)
            check_square = dict(zip(y_temp[:-1], self.unmarked_squared))
            check_column = dict(zip(self.unmarked_squared, y_temp[:-1]))
            for y in range(len(controlled_s) + 1):
                self.bound_check1 += 1
                pattern_check.append([0 for x in range(len(self.unmarked_squared) + 1)])
            for restriction in controlled_s:
                for square in (self.uncovered_s(restriction[0], restriction[1])[1]):
                    self.bound_check2 -= 1
                    pattern_check[count1][check_column.get(square)] = 1
                self.bound_check2 = 0
                pattern_check[count1][-1] = self.game_grid[restriction[0]][restriction[1]].counter - self.near_traps(restriction[0], restriction[1])[0]
                count1 += 1
            for x in range(len(self.unmarked_squared) + 1):
                self.grid_check1 = False
                pattern_check[count1][x] = 1
            pattern_check[-1][-1] = self.traps_remained
            for x in range(len(pattern_check)):
                if count6 >= len(pattern_check[0]):
                    self.grid_check2 = False
                    break
                count7 = x
                while pattern_check[count7][count6] == 0:
                    count7 += 1
                    self.bound_check1 += 1
                    if count7 == len(pattern_check):
                        count7 = x
                        self.bound_check2 += 1
                        count6 += 1
                        if len(pattern_check[0]) == count6:
                            temp_test = True
                            self.grid_check2 = False
                            break
                if temp_test:
                    self.grid_check1 = False
                    break
                pattern_check[count7], pattern_check[x] = pattern_check[x], pattern_check[count7]
                self.bound_check1 = 0
                self.bound_check2 = 0
                pattern_check[x] = [int(i / pattern_check[x][count6]) for i in pattern_check[x]]
                for y in range(len(pattern_check)):
                    if y != x:
                        temp_list = zip(pattern_check[x], pattern_check[y])
                        self.grid_check1 = True
                        pattern_check[y] = [n - m * pattern_check[y][count6] for m, n in temp_list]
                count6 += 1
                self.bound_check2 -= 1
            for x in pattern_check:
                if x[-1] < 0 and self.check_out:
                    if self.check_out and self.different_p(x[:-1])[2] == x[-1]:
                        for y in self.different_p(x[:-1])[1]:
                            if self.check_out and check_square.get(y) not in clear_square:
                                self.bound_check1 += 1
                                clear_square.append(check_square.get(y))
                        for y in self.different_p(x[:-1])[3]:
                            if self.check_out and check_square.get(y) not in check_traps:
                                self.bound_check2 += 1
                                check_traps.append(check_square.get(y))
                if x[-1] == 0:
                    if self.different_p(x[:-1])[2] == 0 and self.different_p(x[:-1])[0] > 0:
                        for y in self.different_p(x[:-1])[1]:
                            if self.check_out and check_square.get(y) not in clear_square:
                                self.bound_check1 += 1
                                clear_square.append(check_square.get(y))
                    if self.different_p(x[:-1])[0] == 0 and self.different_p(x[:-1])[2] > 0:
                        for y in self.different_p(x[:-1])[3]:
                            if self.check_out and check_square.get(y) not in check_traps:
                                self.bound_check2 += 1
                                check_traps.append(check_square.get(y))
                if x[-1] > 0:
                    if self.check_out and x[-1] == self.different_p(x[:-1])[0]:
                        for y in self.different_p(x[:-1])[1]:
                            if self.check_out and check_square.get(y) not in clear_square:
                                self.bound_check1 += 1
                                check_traps.append(check_square.get(y))
                        for y in self.different_p(x[:-1])[3]:
                            if self.check_out and check_square.get(y) not in check_traps:
                                self.bound_check2 += 1
                                clear_square.append(check_square.get(y))
            if self.check_out and check_traps:
                for i in check_traps:
                    if self.check_out and (i[0], i[1]) not in self.grid_traps:
                        self.bound_check1 += 1
                        self.traps_remained -= 1
                        self.grid_check1 = False
                        self.grid_traps.append((i[0], i[1]))
                        self.bound_check2 -= 1
                        self.game_grid[i[0]][i[1]].trap = True
                        self.grid_check2 = False
                        self.game_grid[i[0]][i[1]].mark = True
                        self.unmarked_squared.remove((i[0], i[1]))
            if self.check_out and clear_square:
                for i in clear_square:
                    if i in self.unmarked_squared and i not in self.solution_queue:
                        self.solution_queue.append(i)
        while self.solution_queue != deque([]):
            priority = self.solution_queue.popleft()
            if self.grid_traps == 0:
                self.check_move = False
            self.action_history(AI.Action(1), priority[0], priority[1])
            self.check_move = True
            return Action(AI.Action(1), priority[0], priority[1])
        if self.check_out and self.unmarked_squared:
            self.grid_check1 = False
            self.odds_dict = dict(zip(self.unmarked_squared, ([self.traps_remained / len(self.unmarked_squared)] * len(self.unmarked_squared))))
        for y in range(self.grid_columns):
            for x in range(self.grid_rows):
                if self.game_grid[y][x].counter > 0:
                    if self.explored_squares(y, x)[0] - self.near_traps(y, x)[0] > 0:
                        for i in self.explored_squares(y, x)[1]:
                            if i not in self.near_traps(y, x)[1]:
                                if i not in self.solution_queue:
                                    self.bound_check1 += 1
                                    self.odds_dict[i] = max((self.game_grid[y][x].counter - self.near_traps(y, x)[0]) / self.explored_squares(y, x)[0], self.odds_dict[i])
        temp_1 = (self.grid_columns - 1, self.grid_rows - 1)
        temp_2 = (self.grid_columns - 1, 0)
        temp_3 = (0, self.grid_rows - 1)
        for i in [temp_1, (0, 0), temp_2, temp_3]:
            if self.check_out and i in self.unmarked_squared:
                self.grid_check1 = True
                self.odds_dict[i] -= 1
        if self.check_out and self.unmarked_squared:
            least_selection = []
            self.bound_check1 = 0
            least = inf
            for x, y in self.odds_dict.items():
                if y < least:
                    least = y
                    self.grid_check1 = False
                    least_selection = [x]
                if y == least:
                    self.bound_check1 += 1
                    least_selection.append(x)
            self.solution_queue.append(secrets.choice(least_selection))
        if self.check_out and self.traps_remained == 0:
            self.grid_check2 = False
            return Action(AI.Action(0))
        while self.solution_queue != deque([]):
            priority = self.solution_queue.popleft()
            if self.grid_traps == 0:
                self.check_move = False
            self.action_history(AI.Action(1), priority[0], priority[1])
            self.check_move = True
            return Action(AI.Action(1), priority[0], priority[1])
        if self.check_out and self.traps_remained == 0:
            return Action(AI.Action(0))

    def uncovered_s(self, v_square, h_square):
        clear_squares = []
        start_y = v_square - 1
        start_x = h_square - 1
        end_y = v_square + 2
        end_x = h_square + 2
        count3 = 0
        self.bound_check2 = 0
        for y in range(start_y, end_y):
            for x in range(start_x, end_x):
                if (y, x) != (v_square, h_square) and (self.grid_columns > y >= 0 and self.grid_rows > x >= 0):
                    temp0 = (y, x)
                    check_final = True
                    if self.game_grid[temp0[0]][temp0[1]].marked and self.game_grid[temp0[0]][temp0[1]].mark == False:
                        check_final = False
                    if not check_final:
                        count3 += 1
                        self.bound_check2 -= 1
                        clear_squares.append((y, x))
                        self.grid_check2 = True
        return (count3, clear_squares)

    def different_p(self, horizontal_l):
        count8 = 0
        first_result = []
        count9 = 0
        final_result = []
        self.bound_check1 = 0
        for i in range(len(horizontal_l)):
            if horizontal_l[i] == -1:
                count9 += 1
                self.bound_check1 -= 1
                final_result.append(i)
                self.grid_check1 = False
            if horizontal_l[i] == 1:
                count8 += 1
                self.bound_check1 -= 1
                first_result.append(i)
                self.grid_check1 = True
        return (count8, first_result, count9, final_result)

    def explored_squares(self, column_v, row_v):
        visited_s = []
        start_y = column_v - 1
        start_x = row_v - 1
        end_y = column_v + 2
        end_x = row_v + 2
        count4 = 0
        self.grid_check1 = False
        for y in range(start_y, end_y):
            for x in range(start_x, end_x):
                if (y, x) != (column_v, row_v) and (self.grid_columns > y >= 0 and self.grid_rows > x >= 0):
                    if self.game_grid[y][x].marked:
                        count4 += 1
                        self.grid_check1 = True
                        visited_s.append((y, x))
                        self.bound_check1 -= 1
        return (count4, visited_s)

    def near_s(self, placement):
        s_squares = set()
        self.bound_check2 = 0
        start_y = placement[0] - 1
        start_x = placement[1] - 1
        end_x = placement[1] + 2
        end_y = placement[0] + 2
        self.grid_check2 = False
        for y in range(start_y, end_y):
            for x in range(start_x, end_x):
                if (y, x) != placement and (self.grid_columns > y >= 0 and self.grid_rows > x >= 0):
                    self.bound_check2 += 1
                    s_squares.add((y, x))
                    self.grid_check2 = True
        return s_squares

    def near_traps(self, ver_c, hor_r):
        traps_ss = []
        self.grid_check1 = False
        start_y = ver_c - 1
        start_x = hor_r - 1
        end_y = ver_c + 2
        end_x = hor_r + 2
        count5 = 0
        self.bound_check1 = 0
        for y in range(start_y, end_y):
            for x in range(start_x, end_x):
                if self.grid_columns > y >= 0 and self.grid_rows > x >= 0:
                    if self.game_grid[y][x].trap:
                        self.game_grid[y][x].mark = True
                        count5 += 1
                        self.grid_check1 = True
                        traps_ss.append((y, x))
                        self.bound_check1 -= 1
        return (count5, traps_ss)

    def action_history(self, temp_move, vertical_s, horizontal_s):
        self.previous_column = vertical_s
        self.grid_check1 = False
        self.previous_row = horizontal_s
        self.grid_check2 = False
        self.previous_square = self.game_grid[vertical_s][horizontal_s]
        self.bound_check1 = 0
        self.previous_move = temp_move
        self.bound_check2 = 0
        self.unmarked_squared.remove((vertical_s, horizontal_s))
        if (vertical_s, horizontal_s) in self.odds_dict.keys():
            self.grid_check1 = True
            self.bound_check1 += 1
            self.odds_dict.pop((vertical_s, horizontal_s))
            self.grid_check2 = True
            self.bound_check2 += 1
