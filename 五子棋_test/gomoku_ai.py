import sys
import numpy as np

value_lf = 1000
value_lt = 100
value_rf = 100
key_white = 2
key_black = 1
key_block = 0
depth = 2


class AI:
    def __init__(self, state_board):
        self.state_board = state_board
        self.pos_white = []  # 记录白棋的位置
        self.pos_black = []  # 记录黑棋的位置
        self.size = len(state_board)
        for i in range(self.size):
            for j in range(self.size):
                if state_board[i][j].value == key_black:
                    self.pos_black.append((i, j))
                elif state_board[i][j].value == key_white:
                    self.pos_white.append((i, j))

    def ab_search(self):  # 返回下一步的坐标
        _, x, y = self.max_value(-sys.maxsize - 1, sys.maxsize, depth)
        return x, y

    def max_value(self, a, b, dep):
        if dep == 0:
            return self.eval(), 0, 0
        val = -sys.maxsize - 1
        best_act = ()
        acts = self.action()

        for act in acts:
            self.push(dep, act)
            val = max(val, self.min_value(a, b, dep - 1)[0])
            self.pop(dep, act)
            # 剪枝
            if val >= b:
                return val, act[0], act[1]
            if val > a:
                a = val
                best_act = act
        return val, best_act[0], best_act[1]

    def min_value(self, a, b, dep):
        if dep == 0:
            return self.eval(), 0, 0
        val = sys.maxsize
        best_act = ()
        acts = self.action()

        for act in acts:
            self.push(dep, act)
            val = min(val, self.max_value(a, b, dep - 1)[0])
            self.pop(dep, act)
            if val <= a:
                return val, act[0], act[1]
            if val < b:
                b = val
                best_act = act
        return val, best_act[0], best_act[1]

    # 由于根节点为下白棋，故可以根据dep来判断该步下黑棋还是白棋
    def push(self, flag, act):
        if flag & 1:
            self.pos_black.append(act)
            self.state_board[act[0]][act[1]].value = key_black
        else:
            self.pos_white.append(act)
            self.state_board[act[0]][act[1]].value = key_white

    def pop(self, flag, act):
        if flag & 1:
            self.pos_black.pop()
        else:
            self.pos_white.pop()
        self.state_board[act[0]][act[1]].value = key_block

    def action(self):
        mx_r, mx_c, mn_r, mn_c = 0, 0, 0, 0
        pos = self.pos_white + self.pos_black
        if len(pos) != 0:
            mx_r, mx_c = np.max(pos, axis=0)
            mn_r, mn_c = np.min(pos, axis=0)

        # 构造可下子的方形区域
        r_begin = max(0, mn_r - 2)
        r_end = min(self.size - 1, mx_r + 2)
        c_begin = max(0, mn_c - 2)
        c_end = min(self.size - 1, mx_c + 2)

        act = []
        r = r_begin
        while r <= r_end:
            c = c_begin
            while c <= c_end:
                if self.state_board[r][c].value == 0:
                    act.append((r, c))
                c = c + 1
            r = r + 1
        return act

    def eval(self):
        num_lf = self.live_four()
        num_lt = self.live_three()
        num_rf = self.rush_four()
        return num_lf * value_lf + num_lt * value_lt + num_rf*value_rf

    def in_board(self, row, col):
        if row < 0 or row > self.size - 1 or col < 0 or col > self.size - 1:
            return False
        return True

    # 活四
    def live_four(self):
        # 计算白棋活四数量
        num_w = self.cal_live_four(self.pos_white, key_white)
        # 计算黑棋活四数量
        num_b = self.cal_live_four(self.pos_black, key_black)
        return num_w - num_b

    def cal_live_four(self, pos, key):
        num = 0
        for r, c in pos:
            if self.same(r + 1, c, key_block) and self.same(r - 4, c, key_block) \
                    and self.same(r - 1, c, key) and self.same(r - 2, c, key) and self.same(r - 3, c, key):
                num = num + 1

            if self.same(r + 1, c - 1, key_block) and self.same(r - 4, c + 4, key_block) \
                    and self.same(r - 1, c + 1, key) and self.same(r - 2, c + 2, key) and self.same(r - 3, c + 3, key):
                num = num + 1

            if self.same(r, c - 1, key_block) and self.same(r, c + 4, key_block) \
                    and self.same(r, c + 1, key) and self.same(r, c + 2, key) and self.same(r, c + 3, key):
                num = num + 1

            if self.same(r - 1, c - 1, key_block) and self.same(r + 4, c + 4, key_block) \
                    and self.same(r + 1, c + 1, key) and self.same(r + 2, c + 2, key) and self.same(r + 3, c + 3, key):
                num = num + 1
        return num

    def same(self, row, col, key):
        if not self.in_board(row, col):
            return False
        return self.state_board[row][col].value == key

    # 活三
    def live_three(self):
        num_w = self.cal_live_three(self.pos_white, key_white)
        num_b = self.cal_live_three(self.pos_black, key_black)
        return num_w - num_b

    def cal_live_three(self, pos, key):
        num = 0
        for r, c in pos:
            # 朝上两种
            if self.same(r + 1, c, key_block) and self.same(r - 1, c, key) \
                    and ((self.same(r - 3, c, key_block) and self.same(r - 2, c, key) and (
                    self.same(r + 2, c, key_block) or self.same(r - 4, c, key_block)))
                         or (self.same(r - 2, c, key_block) and self.same(r - 3, c, key) and self.same(r - 4, c,
                                                                                                       key_block))):
                num = num + 1
            # 斜上两种
            if self.same(r + 1, c - 1, key_block) and self.same(r - 1, c + 1, key) \
                    and ((self.same(r - 3, c + 3, key_block) and self.same(r - 2, c + 2, key) and
                          (self.same(r + 2, c - 2, key_block) or self.same(r - 4, c + 4, key_block)))
                         or (self.same(r - 2, c + 2, key_block) and self.same(r - 3, c + 3, key) and self.same(r - 4,
                                                                                                               c + 4,
                                                                                                               key_block))):
                num = num + 1
            # 横向两种
            if self.same(r, c - 1, key_block) and self.same(r, c + 1, key) \
                    and ((self.same(r, c + 3, key_block) and self.same(r, c + 2, key)
                          and (self.same(r, c - 2, key_block) or self.same(r, c + 4, key_block)))
                         or (self.same(r, c + 2, key_block) and self.same(r, c + 3, key) and self.same(r, c + 4,
                                                                                                       key_block))):
                num = num + 1
            # 斜下两种
            if self.same(r - 1, c - 1, key_block) and self.same(r + 1, c + 1, key) \
                    and ((self.same(r + 3, c + 3, key_block) and self.same(r + 2, c + 2, key)
                          and (self.same(r - 2, c - 2, key_block) or self.same(r + 4, c + 4, key_block)))
                         or (self.same(r + 2, c + 2, key_block) and self.same(r + 3, c + 3, key) and self.same(r + 4,
                                                                                                               c + 4,
                                                                                                               key_block))):
                num = num + 1
        return num

    def rush_four(self):
        num_w = self.cal_rush_four(self.pos_white, key_white)
        num_b = self.cal_rush_four(self.pos_black, key_black)
        return num_w - num_b

    def cal_rush_four(self, pos, key):
        num = 0
        dx = [-1, -1, 0, 1]
        dy = [0, 1, 1, 1]
        s = len(dx)

        for r, c in pos:
            for i in range(s):
                if (self.same(r - dx[i], c - dy[i], key_block) ^ self.same(r + dx[i] * 4, c + 4 * dy[i], key_block)) \
                        and self.same(r + dx[i], c + dy[i], key) and self.same(r + 2 * dx[i], c + 2 * dy[i], key) and \
                        self.same(r + 3 * dx[i], c + 3 * dy[i], key):
                    num = num + 1
                elif self.same(r + dx[i], c + dy[i], key) and self.same(r + 2 * dx[i], c + 2 * dy[i], key_block) and \
                        self.same(r + 3 * dx[i], c + 3 * dy[i], key) and self.same(r + 4 * dx[i], c + 4 * dy[i], key):
                    num = num + 1
                elif self.same(r + dx[i], c + dy[i], key_block) and self.same(r + 2 * dx[i], c + 2 * dy[i], key) and \
                        self.same(r + 3 * dx[i], c + 3 * dy[i], key) and self.same(r + 4 * dx[i], c + 4 * dy[i], key):
                    num = num + 1
                elif self.same(r + dx[i], c + dy[i], key) and self.same(r + 2 * dx[i], c + 2 * dy[i], key) and \
                        self.same(r + 3 * dx[i], c + 3 * dy[i], key_block) and self.same(r + 4 * dx[i], c + 4 * dy[i],
                                                                                         key):
                    num = num + 1
        return num

