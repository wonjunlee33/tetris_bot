from board import Direction, Rotation, Action, Shape
from random import Random
import time

class Player:
    def print_board(self, board):
        print("--------")
        for y in range(24):
            s = ""
            for x in range(10):
                if (x,y) in board.cells:
                    s += "#"
                else:
                    s += "."
            print(s, y) 
    
    def original_no_of_blocks(self, board):
        no_of_blocks = len(board.cells)
        return no_of_blocks

    def find_height_of_column(self, xpos, board):
        for y in range(24):
            if (xpos, y) in board.cells:
                return 24 - y
        if self.column_empty(xpos, board):
            return 0
    
    def column_empty(self, xpos, board):
        counter = 0
        for y in range(24):
            if (xpos, y) not in board.cells:
                counter = counter + 1
        if counter == 24:
            return True
        else:
            return False

    def aggregate_height(self, board):
        combination = 0
        for x in range(10):
            if self.find_height_of_column(x, board) == None:
                continue
            combination = combination + self.find_height_of_column(x, board)
        combination = combination ** 1.2
        return combination

    def find_holes(self, board):
        number_of_holes = 0
        for x in range(10):
            if self.find_height_of_column(x, board) == None:
                continue
            height = self.find_height_of_column(x, board)
            for y in range(24 - height, 24):
                if (x,y) not in board.cells:
                    number_of_holes = number_of_holes + 1
        return number_of_holes ** 2.3

    def no_of_blocks(self, board):
        no_of_blocks = len(board.cells)
        return no_of_blocks

    def original_blocks(self, board):
        blocks = 0
        for y in range(24):
            for x in range(10):
                if (x,y) in board.cells:
                    blocks += 1
        return blocks

    def bumpiness(self, board):
        combination = 0
        for x in range(9):
            height1 = self.find_height_of_column(x, board)
            height2 = self.find_height_of_column(x + 1, board)
            if height1 is None:
                height1 = 0
            if height2 is None:
                height2 = 0
            diff = abs(height1 - height2)
            combination = combination + diff
        return combination ** 1.15

    def calculate_lines_cleared(self, old_blocks, blocks):
        change = blocks - old_blocks
        if change == -6:
            return -3000
        elif change == -16:
            return -2500
        elif change == -26:
            return -2000
        elif change == -36:
            return 1000000
        else:
            return -2500

    def fuck_right_columns(self, board):
        height = self.find_height_of_column(9, board)
        return height ** 1.5

    def suck_off_left_column(self, board):
        height = self.find_height_of_column(0, board)
        return height * 30

    def no_twin_towers(self, board):
        tot_height = 0
        total = 0
        for i in range(10):
            temp = self.find_height_of_column(i, board)
            tot_height = tot_height + temp
        tot_height = tot_height / 10
        for j in range (10):
            if self.find_height_of_column(j, board) < tot_height - 3 or self.find_height_of_column(j, board) > tot_height + 3:
                total = total + 800
        return total ** 1.2

    def calculate_score(self, board, blocks):
        aggheight = self.aggregate_height(board)
        holes = self.find_holes(board)
        bumpiness = self.bumpiness(board)
        new_blocks = self.original_blocks(board)
        lines_cleared = self.calculate_lines_cleared(blocks, new_blocks)
        lol_screw_right = self.fuck_right_columns(board)
        lol_suck_off_left = self.suck_off_left_column(board)
        no_twin_towers = self.no_twin_towers(board)


        score = -60.160109115761685 * aggheight + -8000.072143055251 * holes + -100.96378946717479 * bumpiness + 234.13883042578186 * lines_cleared + -4982.598624172437 * lol_screw_right + 151.4688922575059 * lol_suck_off_left + -28.05134077309356 * no_twin_towers


        return score

    def set_xpos(self, xpos, board):
        if xpos == 0:
            for _ in range(5):
                if board.falling is None:
                    return
                board.move(Direction.Left)
        elif xpos == 1:
            for _ in range(4):
                if board.falling is None:
                    return
                board.move(Direction.Left)
        elif xpos == 2:
            for _ in range(3):
                if board.falling is None:
                    return
                board.move(Direction.Left)
        elif xpos == 3:
            for _ in range(2):
                if board.falling is None:
                    return
                board.move(Direction.Left)
        elif xpos == 4:
            for _ in range(1):
                if board.falling is None:
                    return
                board.move(Direction.Left)
        elif xpos == 5:
            if board.falling is None:
                return
            board.skip()
        elif xpos == 6:
            for _ in range(1):
                if board.falling is None:
                    return
                board.move(Direction.Right)
        elif xpos == 7:
            for _ in range(2):
                if board.falling is None:
                    return
                board.move(Direction.Right)
        elif xpos == 8:
            for _ in range(3):
                if board.falling is None:
                    return
                board.move(Direction.Right)
        elif xpos == 9:
            for _ in range(4):
                if board.falling is None:
                    return
                board.move(Direction.Right)
        else:
            print("no")
        
    def set_rot(self, rots, board):
        if board.falling.shape is Shape.O:
            board.skip()
        elif board.falling.shape is Shape.S or board.falling.shape is Shape.Z or board.falling.shape is Shape.I:
            if rots == 0 or rots == 2:
                if board.falling is None:
                    return
                board.skip()
            elif rots == 1 or rots == 3:
                if board.falling is None:
                    return
                board.rotate(Rotation.Clockwise)
        else:
            if rots == 0:
                if board.falling is None:
                    return
                board.skip()
            elif rots == 1:
                if board.falling is None:
                    return
                board.rotate(Rotation.Clockwise)
            elif rots == 2:
                if board.falling is None:
                    return
                board.rotate(Rotation.Clockwise)
                if board.falling is None:
                    return
                board.rotate(Rotation.Clockwise)
            elif rots == 3:
                if board.falling is None:
                    return
                board.rotate(Rotation.Anticlockwise)
            else:
                print("no")

    def move_to_target_pri_rots(self, xpos, rots, board):
        self.set_rot(rots, board)
        self.set_xpos(xpos, board)
        if board.falling is None:
            return
        board.move(Direction.Drop)

    def move_lister(self, board):
        solutions_and_score_final = []

        if board.falling is not None and (board.falling.shape is Shape.O):
            for xpos in range(10):
                for rots in range(1):
                    solutions_and_score_first = []
                    solutions_and_score_second = []
                    blocks = self.original_blocks(board)
                    sandbox = board.clone()
                    self.move_to_target_pri_rots(xpos, rots, sandbox)
                    temp_score = self.calculate_score(sandbox, blocks)
                    solutions_and_score_first.append( (temp_score, (xpos, rots)) )

                    if sandbox.falling is not None and (sandbox.falling.shape is Shape.O):
                        # print(sandbox.falling.shape)
                        for xpos_2 in range(10):
                                for rots_2 in range(1):
                                    blocks_in_clone = self.original_blocks(sandbox)
                                    sandbox_2 = sandbox.clone()
                                    self.move_to_target_pri_rots(xpos_2, rots_2, sandbox_2)
                                    # time.sleep(1)
                                    # self.print_board(sandbox_2)
                                    temp_score_2 = self.calculate_score(sandbox_2, blocks_in_clone)
                                    solutions_and_score_second.append( (temp_score_2, (xpos_2, rots_2)) )

                    elif sandbox.falling is not None and (sandbox.falling.shape is Shape.I or sandbox.falling.shape is Shape.S or sandbox.falling.shape is Shape.Z):
                        # print(sandbox.falling)
                        for xpos_2 in range(10):
                            for rots_2 in range(2):
                                blocks_in_clone = self.original_blocks(sandbox)
                                sandbox_2 = sandbox.clone()
                                self.move_to_target_pri_rots(xpos_2, rots_2, sandbox_2)
                                # time.sleep(1)
                                # self.print_board(sandbox_2)
                                temp_score_2 = self.calculate_score(sandbox_2, blocks_in_clone)
                                solutions_and_score_second.append( (temp_score_2, (xpos_2, rots_2)) )

                    elif sandbox.falling is not None:
                        # print(sandbox.falling)
                        for xpos_2 in range(10):
                            for rots_2 in range(4):
                                blocks_in_clone = self.original_blocks(sandbox)
                                sandbox_2 = sandbox.clone()
                                self.move_to_target_pri_rots(xpos_2, rots_2, sandbox_2)
                                # time.sleep(1)
                                # self.print_board(sandbox_2)
                                temp_score_2 = self.calculate_score(sandbox_2, blocks_in_clone)
                                solutions_and_score_second.append( (temp_score_2, (xpos_2, rots_2)) )

                    for index in range(len(solutions_and_score_second)):
                        temp = solutions_and_score_first[0][0] + solutions_and_score_second[index][0]
                        solutions_and_score_final.append((temp, solutions_and_score_first[0][1]))

        elif board.falling is not None and (board.falling.shape is Shape.S or board.falling.shape is Shape.I or board.falling.shape is Shape.Z):
            for xpos in range(10):
                for rots in range(2):
                    solutions_and_score_first = []
                    solutions_and_score_second = []
                    blocks = self.original_blocks(board)
                    sandbox = board.clone()
                    self.move_to_target_pri_rots(xpos, rots, sandbox)
                    temp_score = self.calculate_score(sandbox, blocks)
                    solutions_and_score_first.append( (temp_score, (xpos, rots)) )

                    if sandbox.falling is not None and (sandbox.falling.shape is Shape.O):
                        # print(sandbox.falling)
                        for xpos_2 in range(10):
                                for rots_2 in range(1):
                                    blocks_in_clone = self.original_blocks(sandbox)
                                    sandbox_2 = sandbox.clone()
                                    self.move_to_target_pri_rots(xpos_2, rots_2, sandbox_2)
                                    # time.sleep(1)
                                    # self.print_board(sandbox_2)
                                    temp_score_2 = self.calculate_score(sandbox_2, blocks_in_clone)
                                    solutions_and_score_second.append( (temp_score_2, (xpos_2, rots_2)) )

                    elif sandbox.falling is not None and (sandbox.falling.shape is Shape.I or sandbox.falling.shape is Shape.S or sandbox.falling.shape is Shape.Z):
                        # print(sandbox.falling)
                        for xpos_2 in range(10):
                            for rots_2 in range(2):
                                blocks_in_clone = self.original_blocks(sandbox)
                                sandbox_2 = sandbox.clone()
                                self.move_to_target_pri_rots(xpos_2, rots_2, sandbox_2)
                                # time.sleep(1)
                                # self.print_board(sandbox_2)
                                temp_score_2 = self.calculate_score(sandbox_2, blocks_in_clone)
                                solutions_and_score_second.append( (temp_score_2, (xpos_2, rots_2)) )

                    elif sandbox.falling is not None:
                        for xpos_2 in range(10):
                            for rots_2 in range(4):
                                blocks_in_clone = self.original_blocks(sandbox)
                                sandbox_2 = sandbox.clone()
                                self.move_to_target_pri_rots(xpos_2, rots_2, sandbox_2)
                                # time.sleep(1)
                                # self.print_board(sandbox_2)
                                temp_score_2 = self.calculate_score(sandbox_2, blocks_in_clone)
                                solutions_and_score_second.append( (temp_score_2, (xpos_2, rots_2)) )

                    for index in range(len(solutions_and_score_second)):
                        temp = solutions_and_score_first[0][0] + solutions_and_score_second[index][0]
                        solutions_and_score_final.append((temp, solutions_and_score_first[0][1]))

        elif board.falling is not None:
            for xpos in range(10):
                for rots in range(4):
                    solutions_and_score_first = []
                    solutions_and_score_second = []
                    blocks = self.original_blocks(board)
                    sandbox = board.clone()
                    self.move_to_target_pri_rots(xpos, rots, sandbox)
                    temp_score = self.calculate_score(sandbox, blocks)
                    solutions_and_score_first.append( (temp_score, (xpos, rots)) )

                    if sandbox.falling is not None and (sandbox.falling.shape is Shape.O):
                        for xpos_2 in range(10):
                                for rots_2 in range(1):
                                    blocks_in_clone = self.original_blocks(sandbox)
                                    sandbox_2 = sandbox.clone()
                                    self.move_to_target_pri_rots(xpos_2, rots_2, sandbox_2)
                                    # time.sleep(1)
                                    # self.print_board(sandbox_2)
                                    temp_score_2 = self.calculate_score(sandbox_2, blocks_in_clone)
                                    solutions_and_score_second.append( (temp_score_2, (xpos_2, rots_2)) )

                    elif sandbox.falling is not None and (sandbox.falling.shape is Shape.I or sandbox.falling.shape is Shape.S or sandbox.falling.shape is Shape.Z):
                        for xpos_2 in range(10):
                            for rots_2 in range(2):
                                blocks_in_clone = self.original_blocks(sandbox)
                                sandbox_2 = sandbox.clone()
                                self.move_to_target_pri_rots(xpos_2, rots_2, sandbox_2)
                                # time.sleep(1)
                                # self.print_board(sandbox_2)
                                temp_score_2 = self.calculate_score(sandbox_2, blocks_in_clone)
                                solutions_and_score_second.append( (temp_score_2, (xpos_2, rots_2)) )

                    elif sandbox.falling is not None:
                        for xpos_2 in range(10):
                            for rots_2 in range(4):
                                blocks_in_clone = self.original_blocks(sandbox)
                                sandbox_2 = sandbox.clone()
                                self.move_to_target_pri_rots(xpos_2, rots_2, sandbox_2)
                                # time.sleep(1)
                                # self.print_board(sandbox_2)
                                temp_score_2 = self.calculate_score(sandbox_2, blocks_in_clone)
                                solutions_and_score_second.append( (temp_score_2, (xpos_2, rots_2)) )

                    for index in range(len(solutions_and_score_second)):
                        temp = solutions_and_score_first[0][0] + solutions_and_score_second[index][0]
                        solutions_and_score_final.append((temp, solutions_and_score_first[0][1]))

        # print(solutions_and_score_final)
        if not solutions_and_score_final:
            solutions_and_score_final.append( (0,(0,0)) )
        return solutions_and_score_final

    def find_best_move(self, board):
        solutions = self.move_lister(board)
        solutions.sort()
        solutions.reverse()

        # print(solutions[0][0])

        best_move = solutions[0][1]
        if solutions[0][0] < -2800000 and board.discards_remaining > 0:
            best_move = (-1, -1)
        elif solutions[0][0] < -2800000 and board.discards_remaining == 0 and board.bombs_remaining > 0:
            best_move = (-2, -2)
        return best_move

    def move_real_player(self, xpos, rots, board):
        move = []

        if rots == 0:
            pass
        elif rots == 1:
            move.append(Rotation.Clockwise)
        elif rots == 2:
            move.append(Rotation.Clockwise)
            move.append(Rotation.Clockwise)
        elif rots == 3:
            move.append(Rotation.Anticlockwise)
        else:
            pass

        if xpos == 0:
            move.append(Direction.Left)
            move.append(Direction.Left)
            move.append(Direction.Left)
            move.append(Direction.Left)
            move.append(Direction.Left)

        elif xpos == 1:
            move.append(Direction.Left)
            move.append(Direction.Left)
            move.append(Direction.Left)
            move.append(Direction.Left)

        elif xpos == 2:
            move.append(Direction.Left)
            move.append(Direction.Left)
            move.append(Direction.Left)

        elif xpos == 3:
            move.append(Direction.Left)
            move.append(Direction.Left)

        elif xpos == 4:
            move.append(Direction.Left)

        elif xpos == 5:
            pass
            
        elif xpos == 6:
            move.append(Direction.Right)

        elif xpos == 7:
            move.append(Direction.Right)
            move.append(Direction.Right)

        elif xpos == 8:
            move.append(Direction.Right)
            move.append(Direction.Right)
            move.append(Direction.Right)

        elif xpos == 9:
            move.append(Direction.Right)
            move.append(Direction.Right)
            move.append(Direction.Right)
            move.append(Direction.Right)

        elif xpos == -1:
            move.append(Action.Discard)
        elif xpos == -2:
            move.append(Action.Bomb)
        else:
            pass
        
        return move

    def choose_action(self, board):
        # time.sleep(1)
        best_move = self.find_best_move(board)
        final_move = self.move_real_player(best_move[0], best_move[1], board)
        final_move.append(Direction.Drop)
        return final_move

SelectedPlayer = Player

