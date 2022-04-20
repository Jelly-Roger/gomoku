import pygame
import time
import sys
from pygame.locals import *

key_black = 1
key_white = 2
key_block = 0
white = (255, 255, 255)
black = (0, 0, 0)
color_restart = (230, 67, 64)  # restart按钮颜色
color_regret = (26, 173, 25)  # regret按钮颜色
grey = (200, 200, 200)  # 点击后按钮的颜色


class Element:
    def __init__(self, pointX, pointY, value):
        self.x = pointX
        self.y = pointY
        self.value = value


class Map:
    def __init__(self):
        self.len = 15
        self.ChessBoard = []
        self.start_x = 27
        self.start_y = 27
        self.winner = 0
        self.Laststep = []

    def init_board(self):
        for i in range(self.len):
            rowlist = []
            for j in range(self.len):
                pointX = self.start_x + 40 * j
                pointY = self.start_y + 40 * i
                rowlist.append(Element(pointX, pointY, key_block))
            self.ChessBoard.append(rowlist)

    def judge(self, row, col, key):
        for x in range(col - 4, col + 5):  # 目标点的左4个右4个
            if x >= 0 and x + 4 < 15:
                if self.ChessBoard[row][x].value == key and \
                        self.ChessBoard[row][x + 1].value == key and \
                        self.ChessBoard[row][x + 2].value == key and \
                        self.ChessBoard[row][x + 3].value == key and \
                        self.ChessBoard[row][x + 4].value == key:
                    self.winner = key
                    return True

        for y in range(row - 4, row + 5):
            if y >= 0 and y + 4 < 15:
                if self.ChessBoard[y][col].value == key and \
                        self.ChessBoard[y + 1][col].value == key and \
                        self.ChessBoard[y + 2][col].value == key and \
                        self.ChessBoard[y + 3][col].value == key and \
                        self.ChessBoard[y + 4][col].value == key:
                    self.winner = key
                    return True

        for x in range(row - 4, row + 5):
            for y in range(col - 4, col + 5):
                if x - y == row - col:
                    if x >= 0 and x + 4 < 15 and y >= 0 and y + 4 < 15:
                        if self.ChessBoard[x][y].value == key and \
                                self.ChessBoard[x + 1][y + 1].value == key and \
                                self.ChessBoard[x + 2][y + 2].value == key and \
                                self.ChessBoard[x + 3][y + 3].value == key and \
                                self.ChessBoard[x + 4][y + 4].value == key:
                            self.winner = key
                            return True

                if x + y == row + col:
                    if x >= 0 and x + 4 < 15 and y < 15 and y - 4 >= 0:
                        if self.ChessBoard[x][y].value == key and \
                                self.ChessBoard[x + 1][y - 1].value == key and \
                                self.ChessBoard[x + 2][y - 2].value == key and \
                                self.ChessBoard[x + 3][y - 3].value == key and \
                                self.ChessBoard[x + 4][y - 4].value == key:
                            self.winner = key
                            return True
        return False

    def regret(self, steps, Role):
        cnt = 0
        while True:
            if len(self.Laststep) == 0:
                break
            else:
                temp = self.Laststep.pop()
                self.ChessBoard[temp.x][temp.y].value = key_block
                Role = temp.value
                cnt = cnt + 1
                if cnt >= steps:
                    break

    def clear(self):
        self.ChessBoard.clear()
        self.winner = 0


class Graph:
    def __init__(self, screen_width, screen_height, console_x, console_y, title):
        self.title = title
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.console_x = console_x
        self.console_y = console_y

        self.button_width = 0
        self.button_height = 0
        self.button_x = 0
        self.button_y = 0

    def calc(self):
        self.button_width = (self.screen_width - self.console_x) - 50  # 按钮宽度
        self.button_height = 50  # 按钮长度
        self.button_x = (self.screen_width + self.console_x) / 2 - self.button_width / 2  # 按钮位置
        self.button_y = self.screen_height / 3 - self.button_height / 2

    def init_screen(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption(self.title)

    def load_pic(self):
        self.background = pygame.image.load("images/background.png")
        self.white = pygame.image.load("images/white.png")
        self.black = pygame.image.load("images/black.png")
        self.result = pygame.image.load("images/result.jpg")

    def load_text(self):
        font = pygame.font.Font(None, 30)
        self.text1 = font.render('restart', True, white)
        tw1, th1 = self.text1.get_size()
        self.posx_1 = self.button_x + self.button_width / 2 - tw1 / 2
        self.posy_1 = self.button_y + self.button_height / 2 - th1 / 2
        self.text2 = font.render('regret', True, white)
        tw2, th2 = self.text2.get_size()
        self.posx_2 = self.button_x + self.button_width / 2 - tw2 / 2
        self.posy_2 = 2 * self.button_y + self.button_height / 2 - th2 / 2

    def draw_button(self, clicked):
        pygame.draw.rect(self.screen, white,
                         (self.console_x, self.console_y, self.screen_width - self.console_x, self.screen_height - 5))
        if clicked == 0:
            color1 = color_restart
            color2 = color_regret
        elif clicked == 1:
            color1 = grey
            color2 = color_regret
        else:
            color1 = color_restart
            color2 = grey
        pygame.draw.rect(self.screen, color1, (self.button_x, self.button_y, self.button_width, self.button_height))
        pygame.draw.rect(self.screen, color2, (self.button_x, 2 * self.button_y, self.button_width, self.button_height))
        pygame.display.update()

    def draw_text(self):
        self.screen.blit(self.text1, (self.posx_1, self.posy_1))
        self.screen.blit(self.text2, (self.posx_2, self.posy_2))
        pygame.display.update()

    def draw_board(self, map):
        self.screen.blit(self.background, (0, 0))
        for temp in map.ChessBoard:
            for point in temp:
                if point.value == 1:
                    self.screen.blit(self.black, (point.x - 18, point.y - 18))
                if point.value == 2:
                    self.screen.blit(self.white, (point.x - 18, point.y - 18))
        pygame.display.update()

    def print_winner(self, delay):
        self.screen.blit(self.result, (200, 200))
        pygame.display.update()
        time.sleep(delay)

    def click_restart(self, x, y):
        if x >= self.button_x and x <= self.button_x + self.button_width and \
                y >= self.button_y and y <= self.button_y + self.button_height:
            return True
        else:
            return False

    def click_regret(self, x, y):
        if x >= self.button_x and x <= self.button_x + self.button_width and \
                y >= 2 * self.button_y and y <= 2 * self.button_y + self.button_height:
            return True
        else:
            return False
