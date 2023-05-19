from board import Direction, Rotation, Action, Board
from adversary import RandomAdversary
from constants import BOARD_HEIGHT, BOARD_WIDTH, BLOCK_LIMIT
import random
from random import Random
import time

from adversary import RandomAdversary
from arguments import parser
from board import Board, Direction, Rotation, Action, Shape
from constants import BOARD_WIDTH, BOARD_HEIGHT, DEFAULT_SEED, INTERVAL, \
    BLOCK_LIMIT
from exceptions import BlockLimitException
import random
import pygame

txt = []

# INITIALISE THIS PIECE OF SHIT FIRST
# solutions = []

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
        # penalise excessive amounts of blocks

        # find initial number of cells

        # future number of cells
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

        score = -glob_solutions[s_counts][0] * aggheight + -glob_solutions[s_counts][1] * holes + -glob_solutions[s_counts][2] * bumpiness + glob_solutions[s_counts][3] * lines_cleared + -glob_solutions[s_counts][4] * no_twin_towers + -glob_solutions[s_counts][5] * lol_screw_right + glob_solutions[s_counts][6] * lol_suck_off_left

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
        # print(solutions)
        # print("--------------------------------------------------------------------")
        best_move = solutions[0][1]
        # if solutions[0][0] < -7000 and board.discards_remaining > 0:
        #     best_move = (-1, -1)
        # elif solutions[0][0] < -5570 and board.discards_remaining == 0 and board.bombs_remaining > 0:
        #     best_move = (-2, -2)

        # should_i_die = self.fuck_holes(board)
        # if should_i_die:
        #     best_move = (-2,-2)

        # print(best_move)
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

######################################################################################################################################

SelectedPlayer = Player

######################################################################################################################################

def run_script():
    BLACK = (0, 0, 0)
    GREY = (30, 30, 30)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)

    CELL_WIDTH = 20
    CELL_HEIGHT = 20

    EVENT_FORCE_DOWN = pygame.USEREVENT + 1
    FRAMES_PER_SECOND = 60


    class Block(pygame.sprite.Sprite):
        def __init__(self, color, x, y, shape):
            super().__init__()

            self.image = pygame.Surface([CELL_WIDTH, CELL_HEIGHT])
            if shape is Shape.B:
                pygame.draw.circle(self.image, WHITE, [CELL_WIDTH//2, CELL_HEIGHT//2],
                                CELL_WIDTH/2)
            else:
                self.image.fill(color)
                pygame.draw.rect(self.image, WHITE, [0, 0, CELL_WIDTH, CELL_HEIGHT], width=1)

            self.rect = self.image.get_rect()
            self.rect.x = x * CELL_WIDTH
            self.rect.y = y * CELL_HEIGHT

    class Discard(pygame.sprite.Sprite):
        def __init__(self, x, y):
            super().__init__()

            self.image = pygame.Surface([CELL_WIDTH, CELL_HEIGHT])
            pygame.draw.line(self.image, RED, (0, 0), (CELL_WIDTH, CELL_HEIGHT), width=3)
            pygame.draw.line(self.image, RED, (0, CELL_HEIGHT), (CELL_WIDTH, 0), width=3)

            self.rect = self.image.get_rect()
            self.rect.x = x * CELL_WIDTH
            self.rect.y = y * CELL_HEIGHT

    def init_text(screen):
        global txt, scorefont
        font = pygame.font.SysFont(None, 24)
        img = font.render('SCORE', True, WHITE)
        txt.append((img, ((BOARD_WIDTH + 3)*CELL_WIDTH - img.get_rect().width//2, 0)))
        img = font.render('NEXT', True, WHITE)
        txt.append((img, ((BOARD_WIDTH + 3)*CELL_WIDTH - img.get_rect().width//2, CELL_HEIGHT*3)))
        img = font.render('BOMBS', True, WHITE)
        txt.append((img, ((BOARD_WIDTH + 3)*CELL_WIDTH - img.get_rect().width//2, CELL_HEIGHT*9)))
        img = font.render('DISCARDS', True, WHITE)
        txt.append((img, ((BOARD_WIDTH + 3)*CELL_WIDTH - img.get_rect().width//2, CELL_HEIGHT*12)))

        scorefont = pygame.font.Font("Segment7-4Gml.otf", 40)

    def render(screen, board):
        global scorefont, txt
        screen.fill(BLACK)
        for t,pos in txt:
            screen.blit(t, pos)    

        for i in range(0,10,2):
            pygame.draw.rect(screen, GREY,
                            [i * CELL_WIDTH, 0,
                            CELL_WIDTH, board.height * CELL_HEIGHT])

        img = scorefont.render(str(board.score), True, WHITE)
        screen.blit(img, ((BOARD_WIDTH + 3)*CELL_WIDTH - img.get_rect().width//2, CELL_HEIGHT))

        sprites = pygame.sprite.Group()

        # Add the cells already on the board for drawing.
        for (x, y) in board:
            sprites.add(Block(pygame.Color(board.cellcolor[x, y]), x, y, Shape.O))

        if board.falling is not None:
            # Add the cells of the falling block for drawing.
            for (x, y) in board.falling:
                sprites.add(Block(pygame.Color(board.falling.color), x, y, board.falling.shape))

        if board.next is not None:
            # Add the cells of the next block for drawing.
            width = board.next.right - board.next.left
            for (x, y) in board.next:
                sprites.add(
                    Block(pygame.Color(board.next.color),
                        x + board.width + 2.5 - width/2, y+4,
                        board.next.shape))

        for i in range(board.bombs_remaining):
            sprites.add(Block(pygame.Color(WHITE),board.width + 0.4 + i*1.1,10, Shape.B))

        for i in range(board.discards_remaining):
            sprites.add(Discard(board.width + 0.4 + (i%5)*1.1,13+(i//5)*1.1))
            
        sprites.draw(screen)

        pygame.draw.line(
            screen,
            BLUE,
            (board.width * CELL_WIDTH + 2, 0),
            (board.width * CELL_WIDTH + 2, board.height * CELL_HEIGHT)
        )

        # Update window title with score.
        pygame.display.set_caption(f'Score: {board.score}')


    class UserPlayer(Player):
        """
        A simple user player that reads moves from the command line.
        """

        key_to_move = {
            pygame.K_RIGHT: Direction.Right,
            pygame.K_LEFT: Direction.Left,
            pygame.K_DOWN: Direction.Down,
            pygame.K_SPACE: Direction.Drop,
            pygame.K_UP: Rotation.Clockwise,
            pygame.K_z: Rotation.Anticlockwise,
            pygame.K_x: Rotation.Clockwise,
            pygame.K_b: Action.Bomb,
            pygame.K_d: Action.Discard
        }

        def choose_action(self, board):
            while True:
                event = pygame.event.wait()
                if event.type == pygame.QUIT:
                    raise SystemExit
                elif event.type == pygame.KEYUP:
                    if event.key in self.key_to_move:
                        return self.key_to_move[event.key]
                    elif event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                        raise SystemExit
                elif event.type == EVENT_FORCE_DOWN:
                    return None


    def check_stop():
        for event in pygame.event.get():
            if event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE:
                raise SystemExit
            elif event.type == pygame.QUIT:
                raise SystemExit


    def run():
        board = Board(BOARD_WIDTH, BOARD_HEIGHT)
        adversary = RandomAdversary(random.randint(0, 1000), BLOCK_LIMIT)

        args = parser.parse_args()
        if args.manual:
            player = UserPlayer()
        else:
            player = SelectedPlayer()

        pygame.init()

        screen = pygame.display.set_mode([
            (BOARD_WIDTH + 6) * CELL_WIDTH,
            BOARD_HEIGHT * CELL_HEIGHT
        ])

        clock = pygame.time.Clock()

        init_text(screen)

        # Set timer to force block down when no input is given.
        pygame.time.set_timer(EVENT_FORCE_DOWN, INTERVAL)

        try:
            for move in board.run(player, adversary):
                render(screen, board)
                pygame.display.flip()

                # If we are not playing manually, clear the events.
                if not args.manual:
                    check_stop()
                    clock.tick(FRAMES_PER_SECOND)

            # print("Score=", board.score)
            # print("Press ESC in game window to exit")
            # while True:
            #     check_stop()
        except BlockLimitException:
            print("Out of blocks")
            # print("Score=", board.score)
            # print("Press ESC in game window to exit")
        except KeyboardInterrupt:
            pass
        finally:
            return board.score


    if __name__ == '__main__':
        return run()

#################################################################################################################################

# def run_game
def run_game(aggheight_weight, holes_weight, bumpiness_weight, no_of_cells_weight, no_twin_towers_weight ,fuck_right_column, suck_off_left_column):
    rungamescore = run_script()
    print("Score:", rungamescore)
    return rungamescore

def generator():
# generate solutions
    iterations = 25
    global glob_solutions;
    global s_counts;
    s_counts = 0
    glob_solutions = []
    for _ in range(iterations):
        # glob_solutions.append( (random.uniform(0,1), random.uniform(0,1), random.uniform(0,1), random.uniform(0,1), random.uniform(0,300), random.uniform(0,1), random.uniform(0,1)) )
        glob_solutions.append( (60.639151643799586, 6500.0320934178402, 70.71581371947448, 230.710814769124598, 28.000, 5000.9118110065175, 150.597146283463623) )
        # score = -60.639151643799586 * aggheight + -6000.0320934178402 * holes + -70.71581371947448 * bumpiness + 230.710814769124598 * lines_cleared + -5000.9118110065175 * lol_screw_right + 150.597146283463623 * lol_suck_off_left + -28.000 * no_twin_towers
        # score = -15.413274865868066 * aggheight + -1000.46138654346066 * holes + -45.927867061653465 * bumpiness + 15.917725483349415 * lines_cleared + -300.43925661913318 * lol_screw_right + 30.45967112695778 * lol_suck_off_left
        # score = -15.010066 * aggheight + -230.7663 * holes + -45.884483 * bumpiness + 10.760666 * lines_cleared + -200.3 * lol_screw_right + 19.5 * lol_suck_off_left
        # score = -15.010464186051717 * aggheight + -230.76041846401776 * holes + -45.883168105396656 * bumpiness + 10.761032136968657 * lines_cleared + -200.30215527098824 * lol_screw_right + 19.499738963524617 * lol_suck_off_left



# for 10000 random agents, find score, upload score + agent info to list
    for i in range(iterations):
        rankedsolutions = []
        for s in glob_solutions:
            rankedsolutions.append( (run_game(s[0],s[1],s[2],s[3],s[4],s[5],s[6]), s) )
            # sort the solutions
            rankedsolutions.sort()
            rankedsolutions.reverse()

        average = 0
        for q in rankedsolutions:
            average = average + q[0]
        print(f"=== Gen {i} best solutions ===")
        print(rankedsolutions[0])
        print(f"total average: {average / iterations}")


        if rankedsolutions[0][0] > 20000:
            # break
            pass

        # take top 100 score
        bestsolutions = rankedsolutions[:8]

        # shove in parameters of all 100 best solutions
        elements0 = []
        elements1 = []
        elements2 = []
        elements3 = []
        elements4 = []
        elements5 = []
        elements6 = []


        for s in bestsolutions:
            elements0.append(s[1][0])
            elements1.append(s[1][1])
            elements2.append(s[1][2])
            elements3.append(s[1][3])
            elements4.append(s[1][4])
            elements5.append(s[1][5])
            elements6.append(s[1][6])

            # elements0.append(s[1][0])
            # elements0.append(s[1][1])
            # elements0.append(s[1][2])
            # elements0.append(s[1][3])
            # elements0.append(s[1][4])

        # choose 4 random elements from elements list and start mixing them up
        newGen = []
        for _ in range(iterations): # btw assign random 'noise'
            # e1 = random.choice(elements0) * random.uniform(0.99,1.01)
            # e2 = random.choice(elements0) * random.uniform(0.99,1.01)
            # e3 = random.choice(elements0) * random.uniform(0.99,1.01)
            # e4 = random.choice(elements0) * random.uniform(0.99,1.01)
            # e5 = random.choice(elements0) * random.uniform(0.99,1.01)

            # e0 = random.choice(elements0) * random.uniform(0.99,1.01)
            # e1 = random.choice(elements1) * random.uniform(0.99,1.01)
            # e2 = random.choice(elements2) * random.uniform(0.99,1.01)
            # e3 = random.choice(elements3) * random.uniform(0.99,1.01)
            # e4 = random.choice(elements4) * random.uniform(0.99,1.01)
            # e5 = random.choice(elements5) * random.uniform(0.99,1.01)
            # e6 = random.choice(elements6) * random.uniform(0.99,1.01)

            e0 = random.choice(elements0) * random.uniform(0.99,1.01)
            e1 = random.choice(elements1) * random.uniform(0.99,1.01)
            e2 = random.choice(elements2) * random.uniform(0.99,1.01)
            e3 = random.choice(elements3) * random.uniform(0.99,1.01)
            e4 = random.choice(elements4) * random.uniform(0.99,1.01)
            e5 = random.choice(elements5) * random.uniform(0.99,1.01)
            e6 = random.choice(elements6) * random.uniform(0.99,1.01)

            newGen.append( (e0,e1,e2,e3,e4,e5,e6) )

        # now repeat the whole thing with the newGen
        glob_solutions = newGen
        s_counts = s_counts + 1

generator()