import gomoku_ai
import gomoku_graph


def output(l):
    for i in l:
        print("%d %d" % (i[0], i[1]))


# debug
if __name__ == '__main__':
    gomoku_graph.initChessSquare(0, 0)
    gomoku_graph.initChessList[5][6].value = gomoku_ai.key_black
    gomoku_graph.initChessList[5][7].value = gomoku_ai.key_black
    gomoku_graph.initChessList[6][5].value = gomoku_ai.key_black
    gomoku_graph.initChessList[7][5].value = gomoku_ai.key_black
    gomoku_graph.initChessList[5][4].value = gomoku_ai.key_black
    gomoku_graph.initChessList[4][5].value = gomoku_ai.key_black

    chess_ai = gomoku_ai.AI(gomoku_graph.initChessList)
    print(chess_ai.ab_search())
    #acts = chess_ai.action()
    #output(acts)
    """
    for i in range(chess_ai.size):
        for j in range(chess_ai.size):
            print(chess_ai.state_board[i][j].value,end=" ")
        print('\n')
    """
    # print(chess_ai.ab_search())
