from queue import Queue
from copy import copy, deepcopy
from Board import Board, board_copy
class MyGO:

    def __init__(self, board, p_board, type=1, step=0):
        self.board = board
        self.p_board = p_board
        self.step = step
        self.type = type
        self.game_result = 0
        self.reward = 0

    def print(self):
        print("Board:")
        for i in range(5):
            print(self.board.state[i])
        print("Step:")
        print(self.step)
        print("Type:")
        print(self.type)
        print("Game_result:")
        print(self.game_result)

    def encode_state(self):
        state = self.board.state
        type = self.type
        ret = ''.join([str(state[i][j]) for i in range(5) for j in range(5)])
        # ret = ret + str(type)
        return ret

    def game_over(self):
        if self.step == 24:
            cnt = [0, 0, 2.5]
            for i in range(5):
                for j in range(5):
                    cnt[self.board.state[i][j]] += 1

            if cnt[1] > cnt[2]:
                self.game_result = 1
            else:
                self.game_result = 2
            self.reward = abs(cnt[1] - cnt[2])
            return True
        return False

    def optype(self):
        if self.type == 1:
            return 2
        else:
            return 1

    def valid_position(self, x, y):
        board = board_copy(self.board)
        state = board.state
        type = self.type
        opt = self.optype()

        # the position is occupied
        if not state[x][y] == 0:
            return False


        # the position is dead
        board.add_certain_pieces([(x, y)], type)
        dead_pieces = board.find_dead_pieces(opt)
        board.remove_certain_pieces(dead_pieces)
        liberties = board.find_liberty(x, y)
        if len(liberties) == 0:
            return False

        # the position is komi
        if board.state == self.p_board.state:
            return False

        return True

    def move(self, i, j):
        board = self.board
        type = self.type
        optype = self.optype()
        self.step += 1
        self.p_board = deepcopy(self.board)
        board.add_certain_pieces([(i, j)], type)
        dead_pieces = board.find_dead_pieces(optype)
        board.remove_certain_pieces(dead_pieces)
        self.type = self.optype()

    def reset(self):
        self.board = Board()
        self.p_board = Board()
        self.step = 0
        self.type = 1
        self.game_result = 0
        self.game_reward = 0

def go_copy(mygo):
    board = Board()
    p_board = Board()
    for i in range(5):
        for j in range(5):
            board.state[i][j] = mygo.board.state[i][j]
            p_board.state[i][j] = mygo.p_board.state[i][j]
    side = mygo.type
    step = mygo.step
    ans_go = MyGO(board, p_board, side, step)
    return ans_go




