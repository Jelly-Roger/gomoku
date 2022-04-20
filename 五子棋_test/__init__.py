import gomoku_ai
import gomoku_graph


def output(l):
    for i in l:
        print("%d %d" % (i[0], i[1]))


# debug
if __name__ == '__main__':
    gomoku_graph.initChessSquare(0, 0)
    gomoku_graph.initChessList[0][0].value = gomoku_ai.key_black
    gomoku_graph.initChessList[0][1].value = gomoku_ai.key_black
    gomoku_graph.initChessList[0][2].value = gomoku_ai.key_black
    gomoku_graph.initChessList[0][3].value = gomoku_ai.key_black
    gomoku_graph.initChessList[1][0].value = gomoku_ai.key_black
    gomoku_graph.initChessList[2][0].value = gomoku_ai.key_black
    gomoku_graph.initChessList[3][0].value = gomoku_ai.key_black
    gomoku_graph.initChessList[4][0].value = gomoku_ai.key_black
    gomoku_graph.initChessList[1][1].value = gomoku_ai.key_black
    gomoku_graph.initChessList[2][2].value = gomoku_ai.key_black
    gomoku_graph.initChessList[3][3].value = gomoku_ai.key_black

    chess_ai = gomoku_ai.AI(gomoku_graph.initChessList)

    print("white live_three:%d  live_four:%d  rush_four:%d" % (
        chess_ai.cal_live_three(chess_ai.pos_white, gomoku_ai.key_white),
        chess_ai.cal_live_four(chess_ai.pos_white, gomoku_ai.key_white),
        chess_ai.cal_rush_four(chess_ai.pos_white, gomoku_ai.key_white)))
    print("black live_three:%d  live_four:%d  rush_four:%d" % (
    chess_ai.cal_live_three(chess_ai.pos_black, gomoku_ai.key_black),
    chess_ai.cal_live_four(chess_ai.pos_black, gomoku_ai.key_black),
    chess_ai.cal_rush_four(chess_ai.pos_black, gomoku_ai.key_black)))

    # acts = chess_ai.action()
    # output(acts)
    """
    for i in range(chess_ai.size):
        for j in range(chess_ai.size):
            print(chess_ai.state_board[i][j].value,end=" ")
        print('\n')
    """
    # print(chess_ai.ab_search())
