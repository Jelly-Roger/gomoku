import gomoku_ai
import gomoku_graph


def output(l):
    for i in l:
        print("%d %d" % (i[0], i[1]))


# debug
if __name__ == '__main__':
    gomoku_graph.initChessSquare(0, 0)

    #gomoku_graph.initChessList[5][5].value = gomoku_ai.key_black
    #gomoku_graph.initChessList[6][5].value = gomoku_ai.key_black
    #gomoku_graph.initChessList[7][5].value = gomoku_ai.key_black
    #gomoku_graph.initChessList[6][5].value = gomoku_ai.key_black
    #gomoku_graph.initChessList[9][5].value = gomoku_ai.key_black

    chess_ai = gomoku_ai.AI(gomoku_graph.initChessList)

    print("white live_three:%d  live_four:%d  rush_four:%d  sleep_three:%d" % (
        chess_ai.cal_live_three(chess_ai.pos_white, gomoku_ai.key_white),
        chess_ai.cal_live_four(chess_ai.pos_white, gomoku_ai.key_white),
        chess_ai.cal_rush_four(chess_ai.pos_white, gomoku_ai.key_white),
        chess_ai.cal_sleep_three(chess_ai.pos_white, gomoku_ai.key_white)))

    print("black live_three:%d  live_four:%d  rush_four:%d  sleep_three:%d" % (
        chess_ai.cal_live_three(chess_ai.pos_black, gomoku_ai.key_black),
        chess_ai.cal_live_four(chess_ai.pos_black, gomoku_ai.key_black),
        chess_ai.cal_rush_four(chess_ai.pos_black, gomoku_ai.key_black),
        chess_ai.cal_sleep_three(chess_ai.pos_black, gomoku_ai.key_black)))

    # acts = chess_ai.action()
    # output(acts)
    """
    for i in range(chess_ai.size):
        for j in range(chess_ai.size):
            print(chess_ai.state_board[i][j].value,end=" ")
        print('\n')
    """
    # print(chess_ai.ab_search())
