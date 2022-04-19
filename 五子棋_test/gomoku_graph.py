import pygame
import time
import sys
from pygame.locals import *

initChessList = []  # 保存棋盘坐标
initRole = 1  # 1表示黑棋 2表示白棋
ResultFlag = False  # 结果标志
winvalue = 1  # 获胜方
Laststep = []  # 记录已经下过的棋的信息
white = (255, 255, 255)  # 白色
black = (0, 0, 0)  # 黑色
screen_width = 800  # 画布宽度
screen_height = 620  # 画布长度
console_x = 615  # 控制区域位置x
console_y = 0  # 控制区域位置y
button_width = (screen_width - console_x) - 50  # 按钮宽度
button_height = 50  # 按钮长度
button_x = (screen_width + console_x) / 2 - button_width / 2  # 按钮位置
button_y = screen_height / 3 - button_height / 2
color_restart = (230, 67, 64)  # restart按钮颜色
color_regret = (26, 173, 25)  # regret按钮颜色
grey = (200, 200, 200)  # 点击后按钮的颜色


class StornPoint():  # 每一个点的基本元素
    def __init__(self, x, y, value):
        self.x = x  # 初始化变量
        self.y = y
        self.value = value


def initChessSquare(x, y):  # 初始化棋盘
    for i in range(15):
        rowlist = []
        for j in range(15):
            pointX = x + 40 * j  # 行列与实际画布坐标的换算
            pointY = y + 40 * i
            sp = StornPoint(pointX, pointY, 0)
            rowlist.append(sp)
        initChessList.append(rowlist)


def EventHander(screen, text1, text2, posx_1, posy_1, posx_2, posy_2):  # 监听
    for event in pygame.event.get():
        global initRole
        global initChessList
        global Laststep
        if event.type == QUIT:  # 退出
            pygame.quit()
            sys.exit()
        if event.type == MOUSEBUTTONDOWN:  # 按下鼠标
            x, y = pygame.mouse.get_pos()
            # 点击了restart的按钮
            if x >= button_x and x <= button_x + button_width and \
                    y >= button_y and y <= button_y + button_height:
                pygame.draw.rect(screen, grey, (button_x, button_y, button_width, button_height))
                screen.blit(text1, (posx_1, posy_1))
                initChessList = []  # 重置
                Laststep = []
                initRole = 1
                initChessSquare(27, 27)
                return
            # 点击了悔棋的按钮
            if x >= button_x and x <= button_x + button_width and \
                    y >= 2 * button_y and y <= 2 * button_y + button_height:
                pygame.draw.rect(screen, grey, (button_x, 2 * button_y, button_width, button_height))
                screen.blit(text2, (posx_2, posy_2))
                if len(Laststep) != 0:  # 恢复上一步的盘面
                    temp = Laststep.pop()
                    initChessList[temp.x][temp.y].value = 0
                    initRole = temp.value
                    return
            i = 0
            j = 0
            for temp in initChessList:
                for point in temp:
                    if x >= point.x - 10 and x <= point.x + 10 and y >= point.y - 10 and y <= point.y + 10:
                        if point.value == 0 and initRole == 1:
                            point.value = 1  # 黑棋的值
                            Laststep.append(StornPoint(i, j, point.value))
                            judgeResult(i, j, point.value)
                            initRole = 2
                        elif point.value == 0 and initRole == 2:
                            point.value = 2  # 白棋的值
                            Laststep.append(StornPoint(i, j, point.value))
                            judgeResult(i, j, point.value)
                            initRole = 1
                        break
                    j += 1
                i += 1
                j = 0
        if event.type == MOUSEBUTTONUP:  # 如果松开鼠标
            pygame.draw.rect(screen, color_restart, (button_x, button_y, button_width, button_height))
            screen.blit(text1, (posx_1, posy_1))
            pygame.draw.rect(screen, color_regret, (button_x, 2 * button_y, button_width, button_height))
            screen.blit(text2, (posx_2, posy_2))
            pygame.display.update()


def judgeResult(i, j, value):  # 判断游戏是否结束
    global ResultFlag
    global winvalue
    flag = False
    for x in range(j - 4, j + 5):  # 目标点的左4个右4个
        if x >= 0 and x + 4 < 15:
            if initChessList[i][x].value == value and \
                    initChessList[i][x + 1].value == value and \
                    initChessList[i][x + 2].value == value and \
                    initChessList[i][x + 3].value == value and \
                    initChessList[i][x + 4].value == value:
                flag = True
                ResultFlag = flag
                winvalue = value
                return

    for y in range(i - 4, i + 5):
        if y >= 0 and y + 4 < 15:
            if initChessList[y][j].value == value and \
                    initChessList[y + 1][j].value == value and \
                    initChessList[y + 2][j].value == value and \
                    initChessList[y + 3][j].value == value and \
                    initChessList[y + 4][j].value == value:
                flag = True
                ResultFlag = flag
                winvalue = value
                return

    for x in range(i - 4, i + 5):
        for y in range(j - 4, j + 5):
            if x - y == i - j:
                if x >= 0 and x + 4 < 15 and y >= 0 and y + 4 < 15:
                    if initChessList[x][y].value == value and \
                            initChessList[x + 1][y + 1].value == value and \
                            initChessList[x + 2][y + 2].value == value and \
                            initChessList[x + 3][y + 3].value == value and \
                            initChessList[x + 4][y + 4].value == value:
                        flag = True
                        ResultFlag = flag
                        winvalue = value
                        return
            if x + y == i + j:
                if x >= 0 and x + 4 < 15 and y < 15 and y - 4 >= 0:
                    if initChessList[x][y].value == value and \
                            initChessList[x + 1][y - 1].value == value and \
                            initChessList[x + 2][y - 2].value == value and \
                            initChessList[x + 3][y - 3].value == value and \
                            initChessList[x + 4][y - 4].value == value:
                        flag = True
                        ResultFlag = flag
                        winvalue = value
                        return


def main():
    global initChessList, ResultFlag, winvalue, Laststep
    initChessSquare(27, 27)
    # pygame的实现
    pygame.init()
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("五子棋")
    background = pygame.image.load("images/bg.png")
    whiteStorn = pygame.image.load("images/storn_white.png")
    blackStorn = pygame.image.load("images/storn_black.png")
    resultStorn = pygame.image.load("images/resultStorn.jpg")
    # 设置字体 计算字体位置
    font = pygame.font.Font(None, 30)
    text1 = font.render('restart', True, white)
    tw1, th1 = text1.get_size()
    posx_1 = button_x + button_width / 2 - tw1 / 2
    posy_1 = button_y + button_height / 2 - th1 / 2
    text2 = font.render('regret', True, white)
    tw2, th2 = text2.get_size()
    posx_2 = button_x + button_width / 2 - tw2 / 2
    posy_2 = 2 * button_y + button_height / 2 - th2 / 2
    # 绘画按钮
    pygame.draw.rect(screen, white, (console_x, console_y, screen_width - console_x, screen_height - 5))
    pygame.draw.rect(screen, color_restart, (button_x, button_y, button_width, button_height))
    pygame.draw.rect(screen, color_regret, (button_x, 2 * button_y, button_width, button_height))
    screen.blit(text1, (posx_1, posy_1))
    screen.blit(text2, (posx_2, posy_2))

    while True:
        # 绘画盘面
        screen.blit(background, (0, 0))
        for temp in initChessList:
            for point in temp:
                if point.value == 1:
                    screen.blit(blackStorn, (point.x - 18, point.y - 18))
                if point.value == 2:
                    screen.blit(whiteStorn, (point.x - 18, point.y - 18))
        # 如果游戏结束
        if ResultFlag == True:
            if winvalue == 1:
                print("黑方获胜！")
            elif winvalue == 2:
                print("白方获胜！")
            # 重置盘面
            initChessList = []
            Laststep = []
            initChessSquare(27, 27)
            screen.blit(resultStorn, (200, 200))
        pygame.display.update()

        if ResultFlag == True:
            time.sleep(3)
            ResultFlag = False
            winvalue = 1

        EventHander(screen, text1, text2, posx_1, posy_1, posx_2, posy_2)


if __name__ == '__main__':
    main()
