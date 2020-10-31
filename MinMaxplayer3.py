from MyGo import MyGO, go_copy
from Board import Board, board_copy
import random
class Node:
    def __init__(self, mygo):
        self.go = mygo
        self.son = []

    def value(self):
        go = self.go
        X = 0
        O = 0
        for i in range(5):
            for j in range(5):
                if go.board[i][j] == 1:
                    X += 1
                elif go.board[i][j] == 2:
                    O += 1
        return X-O

    def set_son(self):
        son = self.son
        son = []
        go = self.go
        for i in range(5):
            for j in range(5):
                if go.valid_position(i, j):
                    son.append((i, j))



class Minmax_Tree:

    Min_Value = (-30, 30)
    Max_Value = (30, -1)

    def self_value(self, go): # value = {X - O, min(Oliberty)}
        X = 0
        O = 0
        min_Oliber = 30
        board = go.board
        state = board.state
        vis = [[0 for _ in range(5)] for _ in range(5)]
        for i in range(5):
            for j in range(5):
                if go.board.state[i][j] == 1:
                    X += 1
                elif go.board.state[i][j] == 2:
                    O += 1
                if vis[i][j] == 1 or (not state[i][j] == 2):
                    continue
                allies = board.find_ally(i, j)
                for ally in allies:
                    vis[ally[0]][ally[1]] = 1
                min_Oliber = min(min_Oliber, len(board.find_liberty(i, j)))
        ans = (X - O, min_Oliber)
        return ans

    def rand_pick(self, nodes):
        length = len(nodes)
        if length == 0:
            # print("XXX")
            node = (-1, -1)
            return node
        elif length == 1:
            return nodes[0]
        else:
            randomNumber = random.randint(0, length - 1)
            return nodes[randomNumber]

    def get_height(self, mygo):
        height = 0
        game_sum = 200000
        empty_block = 0
        for i in range(5):
            for j in range(5):
                if mygo.board.state[i][j] == 0:
                    empty_block += 1
        while (not height > 24 - mygo.step) and game_sum > 0:
            game_sum = int(game_sum / empty_block)
            height += 1
        height -= 1
        return height

    def larger(self, value, limit):
        if value[0] > limit[0]:
            return True
        if value[0] == limit[0] and value[1] < limit[1]:
            return True
        return False

    def equal(self, value, limit):
        if value[0] == limit[0] and value[1] == limit[1]:
            return True
        return False

    def less(self, value, limit):
        if value[0] < limit[0]:
            return True
        if value[0] == limit[0] and value[1] > limit[1]:
            return True
        return False

    def max(self, value, limit):
        if value[0] > limit[0]:
            return value
        if value[0] == limit[0] and value[1] < limit[1]:
            return value
        return limit

    def min(self, value, limit):
        if value[0] < limit[0]:
            return value
        if value[0] == limit[0] and value[1] > limit[1]:
            return value
        return limit

    def find_max(self, go, height, alpha, beta):
        # print("find max:")
        if height == 0:
            # print(self.self_value(go))
            return -1, -1, self.self_value(go)
        sons = []
        bestvalue = self.Min_Value
        bestx = -1
        besty = -1
        for i in range(5):
            for j in range(5):
                if go.valid_position(i, j):
                    sons.append((i, j))
        random.shuffle(sons)
        for son in sons:
            x = son[0]
            y = son[1]
            new_go = go_copy(go)
            new_go.move(x, y)
            tx, ty, tv = self.find_min(new_go, height - 1, alpha, beta)
            if self.larger(tv, bestvalue):
                bestx, besty = x, y
                bestvalue = tv

            if self.larger(bestvalue, beta) or self.equal(bestvalue, beta):
                return bestx, besty, bestvalue
            alpha = self.max(alpha, bestvalue)

        return bestx, besty, bestvalue




    def find_min(self, go, height, alpha, beta):
        # print("find min:")
        if height == 0:
            # print("XXX")
            return -1, -1, self.self_value(go)
        sons = []
        bestvalue = self.Max_Value
        bestx = -1
        besty = -1
        for i in range(5):
            for j in range(5):
                if go.valid_position(i, j):
                    sons.append((i, j))
        random.shuffle(sons)
        for son in sons:
            x = son[0]
            y = son[1]
            new_go = go_copy(go)
            new_go.move(x, y)
            tx, ty, tv = self.find_max(new_go, height - 1, alpha, beta)
            if self.less(tv, bestvalue):
                bestx, besty = x, y
                bestvalue = tv

            if self.less(bestvalue, alpha) or self.equal(bestvalue, alpha):
                return bestx, besty, bestvalue
            beta = self.min(beta, bestvalue)

        return bestx, besty, bestvalue


    def find_ans(self, mygo, height = -1):
        son = []
        for i in range(5):
            for j in range(5):
                if mygo.valid_position(i, j):
                    son.append((i, j))
        if len(son) == 0:
            return -1, -1

        if height == -1:
            height = self.get_height(mygo)
        # print(height)
        alpha = self.Min_Value
        beta = self.Max_Value
        if mygo.type == 1:
            posx, posy, value = self.find_max(mygo, height, alpha, beta)
        else:
            posx, posy, value = self.find_min(mygo, height, alpha, beta)
        return posx, posy




class MinMaxPlayer:

    def set_side(self, side):
        self.side = side

    def move(self, mygo):
        tree = Minmax_Tree()
        x, y = tree.find_ans(mygo)
        return mygo.move(x, y)

    def make_move(self, mygo):
        tree = Minmax_Tree()
        x, y = tree.find_ans(mygo)
        if x == -1:
            ans = "PASS"
        else:
            ans = "%d,%d" % (x, y)
        return ans

    def learn(self, mygo):
        return



