import pygame
import sys
from pygame.locals import *
from gomoku_ai import AI
import gomoku_ai
from gomoku_graph import Element, Map, Graph, key_black, key_block, key_white

Role = 1


def EventHander(chess_Map, chess_AI, chess_Graph):  # 监听
    for event in pygame.event.get():
        global Role
        if event.type == QUIT:  # 退出
            pygame.quit()
            sys.exit()
        if event.type == MOUSEBUTTONDOWN:  # 按下鼠标
            posx, posy = pygame.mouse.get_pos()
            # 点击了restart的按钮
            if chess_Graph.click_restart(posx, posy):
                chess_Graph.draw_button(1)
                chess_Graph.draw_text()
                chess_Map.clear()
                chess_Map.init_board()
                chess_AI.clear()
                Role = 1
                return
            # 点击了悔棋的按钮
            if chess_Graph.click_regret(posx, posy):
                chess_Graph.draw_button(2)
                chess_Graph.draw_text()
                chess_Map.regret(2, Role)
                chess_AI.pos_white.pop()
                chess_AI.pos_black.pop()
                return

            if Role == 1:
                for r, temp in enumerate(chess_Map.ChessBoard):
                    for c, point in enumerate(temp):
                        if posx >= point.x - 10 and posx <= point.x + 10 and \
                                posy >= point.y - 10 and posy <= point.y + 10:
                            if point.value == key_block:
                                point.value = key_black  # 黑棋的值
                                chess_Map.Laststep.append(Element(r, c, point.value))
                                chess_Map.judge(r, c, point.value)
                                # 更新黑棋位置
                                chess_AI.pos_black.append((r, c))
                                Role = 2
                                break

        if event.type == MOUSEBUTTONUP:  # 如果松开鼠标
            chess_Graph.draw_button(0)
            chess_Graph.draw_text()
            pygame.display.update()


def main():
    global Role
    chess_Map = Map()
    chess_Map.init_board()
    chess_AI = AI(chess_Map.ChessBoard)
    chess_Graph = Graph(800, 620, 615, 0, "五子棋")
    chess_Graph.init_screen()
    chess_Graph.calc()
    chess_Graph.load_pic()
    chess_Graph.load_text()
    chess_Graph.draw_button(0)
    chess_Graph.draw_text()
    while True:
        chess_Graph.draw_board(chess_Map)
        if chess_Map.winner != 0:
            if chess_Map.winner == key_black:
                print("黑方获胜！")
            else:
                print("白方获胜！")
            chess_Graph.print_winner(3)
            chess_Map.clear()
            pygame.quit()
            sys.exit()

        if Role == 1:
            EventHander(chess_Map, chess_AI, chess_Graph)
        elif Role == 2:
            r, c = chess_AI.ab_search()  # ai下棋
            if chess_Map.ChessBoard[r][c].value == key_block:
                chess_Map.ChessBoard[r][c].value = key_white  # 黑棋的值
                chess_Map.Laststep.append(Element(r, c, key_white))
                chess_Map.judge(r, c, key_white)
                chess_AI.pos_white.append((r, c))
                Role = 1
            #debug(chess_AI)


def debug(chess_AI):
    print("white live_three:%d  live_four:%d  rush_four:%d  sleep_three:%d  live_two:%d" % (
        chess_AI.cal_live_three(chess_AI.pos_white, gomoku_ai.key_white),
        chess_AI.cal_live_four(chess_AI.pos_white, gomoku_ai.key_white),
        chess_AI.cal_rush_four(chess_AI.pos_white, gomoku_ai.key_white),
        chess_AI.cal_sleep_three(chess_AI.pos_white, gomoku_ai.key_white),
        chess_AI.cal_live_two(chess_AI.pos_white, gomoku_ai.key_white)))

    print("black live_three:%d  live_four:%d  rush_four:%d  sleep_three:%d  live_two:%d" % (
        chess_AI.cal_live_three(chess_AI.pos_black, gomoku_ai.key_black),
        chess_AI.cal_live_four(chess_AI.pos_black, gomoku_ai.key_black),
        chess_AI.cal_rush_four(chess_AI.pos_black, gomoku_ai.key_black),
        chess_AI.cal_sleep_three(chess_AI.pos_black, gomoku_ai.key_black),
        chess_AI.cal_live_two(chess_AI.pos_black, gomoku_ai.key_black)))


if __name__ == '__main__':
    main()
    """
    chess_Map = Map()
    chess_Map.init_board()
    chess_Map.ChessBoard[7][7].value = key_black
    chess_Map.ChessBoard[5][5].value = key_white
    chess_Map.ChessBoard[7][8].value = key_black
    chess_AI = AI(chess_Map.ChessBoard)
    print(chess_AI.ab_search())
    
    chess_Map.ChessBoard[3][5].value = key_white
    chess_Map.ChessBoard[4][5].value = key_white
    chess_Map.ChessBoard[5][5].value = key_white
    chess_Map.ChessBoard[6][5].value = key_black
    chess_Map.ChessBoard[7][5].value = key_black

    chess_Map.ChessBoard[4][6].value = key_black
    chess_Map.ChessBoard[5][6].value = key_black
    chess_Map.ChessBoard[6][6].value = key_white

    chess_Map.ChessBoard[5][7].value = key_white
    chess_Map.ChessBoard[6][7].value = key_black
    chess_Map.ChessBoard[7][7].value = key_black

    debug(AI(chess_Map.ChessBoard))
    """