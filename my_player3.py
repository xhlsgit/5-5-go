from MyGo import MyGO
from Board import Board
from Qlearnplayer3 import QLearnplayer
from MinMaxplayer3 import MinMaxPlayer
from Specialplayer3 import Specialplayer
from time import time


PLAYER_X = 1
PLAYER_O = 2

def play(mygo, player1, player2, learn):
    """ Player 1 -> X, X goes first
        player 2 -> O
    """
    player1.set_side(PLAYER_X)
    player2.set_side(PLAYER_O)

    while not mygo.game_over():
        player1.move(mygo)
        player2.move(mygo)
        # print('mygo move %d steps' % mygo.step)

    if learn == True:
        player1.learn(mygo)
        player2.learn(mygo)

    return mygo.game_result

def battle(mygo, player1, player2, iter, learn=False, show_result=True):
    p1_stats = [0, 0, 0] # draw, win, lose
    for i in range(0, iter):
        # if i % 100 == 0:
        print("play %d" % i)
        # mygo.print()
        tmp_go = copy(mygo)
        result = play(tmp_go, player1, player2, learn)
        p1_stats[result] += 1
        # if i % 1000 == 0:
        # print("finish play, start reset")

    p1_stats = [round(x / iter * 100.0, 1) for x in p1_stats]
    if show_result:
        print('_' * 60)
        print('{:>15}(X) | Wins:{}% Draws:{}% Losses:{}%'.format(player1.__class__.__name__, p1_stats[1], p1_stats[0], p1_stats[2]).center(50))
        print('{:>15}(O) | Wins:{}% Draws:{}% Losses:{}%'.format(player2.__class__.__name__, p1_stats[2], p1_stats[0], p1_stats[1]).center(50))
        print('_' * 60)
        print()

    return p1_stats


def train(player, mygo, NUM, count = 0):
    minmaxplayer = MinMaxPlayer()
    # train: play NUM games against players who only make random moves

    # battle(mygo, randomplayer, qlearner, NUM, learn=True, show_result=False)
    # qlearner.count = 0
    player.count = count
    # if mygo.type == 1:
    #     print('Training QLearner against RandomPlayer for {} times......'.format(NUM))
    #     battle(mygo, qlearner, randomplayer, NUM, learn=True, show_result=False)
    # else:
    #     print('Training RandomPlayer against QLearner for {} times......'.format(NUM))
    #     battle(mygo, randomplayer, qlearner, NUM, learn=True, show_result=False)

    print('Training Specialplayer against MinMaxPlayer for {} times......'.format(NUM))
    battle(mygo, player, minmaxplayer, NUM, learn=True, show_result=False)
    player.count = count
    print('Training MinMaxPlayer against Specialplayer for {} times......'.format(NUM))
    battle(mygo, minmaxplayer, player, NUM, learn=True, show_result=False)





### offline

def copy(mygo):
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

def print_result(player1, player2, p1_stats):
    p1_stats = [round(x / 10 * 100.0, 1) for x in p1_stats]
    print('_' * 60)
    print('{:>15}(X) | Wins:{}% Draws:{}% Losses:{}%'.format(player1.__class__.__name__, p1_stats[1], p1_stats[0],
                                                             p1_stats[2]).center(50))
    print('{:>15}(O) | Wins:{}% Draws:{}% Losses:{}%'.format(player2.__class__.__name__, p1_stats[2], p1_stats[0],
                                                             p1_stats[1]).center(50))
    print('_' * 60)
    print()

def test(player, mygo):
    minmaxplayer = MinMaxPlayer()
    # test: play 10 games against each opponent
    print('Playing Specialplayer against MinMaxplayer for 20 times......')
    p1_stats = [0, 0, 0]  # draw, win, lose
    for test_i in range(10):
        print("test special_minmax case %d:" % test_i)
        player.set_side(PLAYER_X)
        # randomplayer.set_side(PLAYER_O)
        minmaxplayer.set_side(PLAYER_O)

        while not mygo.game_over():
            player.move(mygo)
            minmaxplayer.move(mygo)

        result = mygo.game_result
        p1_stats[result] += 1
        print("winner: ", result)
        print("finish test %d, start reset" % test_i)
        mygo.reset()
    print_result(player, minmaxplayer, p1_stats)
    q_rand = p1_stats

    p2_stats = [0, 0, 0]  # draw, win, lose
    for test_i in range(10):
        print("test minmax_special case %d:" % test_i)
        minmaxplayer.set_side(PLAYER_X)
        player.set_side(PLAYER_O)

        while not mygo.game_over():
            minmaxplayer.move(mygo)
            player.move(mygo)

        result = mygo.game_result
        p2_stats[result] += 1
        print("winner: ", result)
        print("finish test %d, start reset" % test_i)
        mygo.reset()

    print_result(minmaxplayer, player, p2_stats)
    rand_q = p2_stats
    print(rand_q)
    print(q_rand)
    # summarize game results
    winning_rate_w_random_player = round(100 - (q_rand[2] + rand_q[1]) * 10 / 2, 2)

    print("Summary:")
    print("_" * 60)
    print("QLearner VS  MinMaxPlayer |  Win/Draw Rate = {}%".format(winning_rate_w_random_player))
    print("_" * 60)


def offline_train():
    specialplayer = Specialplayer()
    board = Board()
    p_board = Board()
    mygo = MyGO(board, p_board)
    start_time = time()
    test(specialplayer, mygo)
    end_time = time()
    print("The program used %f time" % (end_time - start_time))


### online
def load_step(state, side):
    with open('step.txt', 'r') as f:
        step1 = f.readline()
        step1 = int(step1)
        step2 = f.readline()
        step2 = int(step2)

    cnt = 0
    for i in range(5):
        for j in range(5):
            if not state[i][j] == 0:
                cnt += 1
    if cnt == 0:
        step1 = 0
    elif cnt == 1:
        step2 = 1


    if side == 1:
        ansstep = step1
        step1 = (step1 + 2) % 24
    else:
        ansstep = step2
        step2 = (step2 + 2) % 24

    with open('step.txt', 'w') as f:
        f.write(str(step1) + '\n')
        f.write(str(step2) + '\n')
    return ansstep


def input_init():
    with open('input.txt', 'r') as f:
        side = f.readline()
        side = int(side)

        states = f.readlines()
        for i in range(0,10):
            states[i] = states[i].strip('\n')
        op_states = states[0:5]
        my_states = states[5:10]

        m_states = []
        o_states = []
        for i in range(5):
            my_state = []
            op_state = []
            for j in range(5):
                my_state.append(int(my_states[i][j]))
                op_state.append(int(op_states[i][j]))
            m_states.append(my_state)
            o_states.append(op_state)
    step = load_step(m_states, side)

    return side, m_states, o_states, step

def make_move(mygo):
    # minmaxplayer = MinMaxPlayer()
    # ans = minmaxplayer.make_move(mygo)
    specialplayer = Specialplayer()
    ans = specialplayer.make_move(mygo)
    # print(ans)
    with open('output.txt', 'w') as f:
        f.write(ans)

def online_compete():
    side, my_state, op_state, step = input_init()
    board = Board()
    board.set_state(my_state)
    # print(board.state)
    p_board = Board()
    p_board.set_state(op_state)
    mygo = MyGO(board, p_board, side, step)
    # mygo.print()
    # qlearner.load()
    # make_move(qlearner, mygo)
    make_move(mygo)



if __name__ == "__main__":
    # offline_train()
    # start_time = time()
    online_compete()
    # end_time = time()
    # print("The program used %f time" % (end_time - start_time))




