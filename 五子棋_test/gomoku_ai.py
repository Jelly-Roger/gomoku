class AI:
    def __init__(self, state_board):
        self.state_board = state_board
        self.pos_white = []  # 记录白棋的位置
        self.pos_black = []  # 记录黑棋的位置
        self.key_white = 2
        self.key_black = 1
        self.size = len(state_board)
        for i in range(self.size):
            for j in range(self.size):
                if state_board[i][j].value == 1:
                    self.pos_black.append((i, j))
                elif state_board[i][j].value == 2:
                    self.pos_white.append((i, j))

    def ab_search(self):  # 返回下一步的坐标
        pass

    def max_value(self, a, b):
        pass

    def min_value(self, a, b):
        pass

    def eval(self):
        pass

    def in_board(self, row, col):
        if row < 0 or row > self.size - 1 or col < 0 or col > self.size - 1:
            return False
        return True

    # 活四
    def live_four(self):
        # 计算白棋活四数量
        num_w = self.cal_live_four(self.pos_white, self.key_white)
        # 计算黑棋活四数量
        num_b = self.cal_live_four(self.pos_black, self.key_black)
        return num_w - num_b

    def cal_live_four(self, pos, key):
        num = 0
        for r, c in pos:
            if self.same(r + 1, c, 0) and self.same(r - 4, c, 0) \
                    and self.same(r - 1, c, key) and self.same(r - 2, c, key) and self.same(r - 3, c, key):
                num = num + 1

            if self.same(r + 1, c - 1, 0) and self.same(r - 4, c + 4, 0) \
                    and self.same(r - 1, c + 1, key) and self.same(r - 2, c + 2, key) and self.same(r - 3, c + 3, key):
                num = num + 1

            if self.same(r, c - 1, 0) and self.same(r, c + 4, 0) \
                    and self.same(r, c + 1, key) and self.same(r, c + 2, key) and self.same(r, c + 3, key):
                num = num + 1

            if self.same(r - 1, c - 1, 0) and self.same(r + 4, c + 4, 0) \
                    and self.same(r + 1, c + 1, key) and self.same(r + 2, c + 2, key) and self.same(r + 3, c + 3, key):
                num = num + 1
        return num

    def same(self, row, col, key):
        if not self.in_board(row, col):
            return False
        return self.state_board[row][col].value == key

    # 活三
    def live_three(self):
        num_w = self.cal_live_three(self.pos_white, self.key_white)
        num_b = self.cal_live_three(self.pos_black, self.key_black)
        return num_w - num_b

    def cal_live_three(self, pos, key):
        num = 0
        for r, c in pos:
            # 朝上两种
            if self.same(r + 1, c, 0) and self.same(r - 1, c, key) \
                    and ((self.same(r - 3, c, 0) and self.same(r - 2, c, key) and (
                    self.same(r + 2, c, 0) or self.same(r - 4, c, 0)))
                         or (self.same(r - 2, c, 0) and self.same(r - 3, c, key) and self.same(r - 4, c, 0))):
                num = num + 1
            # 斜上两种
            if self.same(r + 1, c - 1, 0) and self.same(r - 1, c + 1, key) \
                    and ((self.same(r - 3, c + 3, 0) and self.same(r - 2, c + 2, key) and
                          (self.same(r + 2, c - 2, 0) or self.same(r - 4, c + 4, 0)))
                         or (self.same(r - 2, c + 2, 0) and self.same(r - 3, c + 3, key) and self.same(r - 4, c + 4,
                                                                                                       0))):
                num = num + 1
            # 横向两种
            if self.same(r, c - 1, 0) and self.same(r, c + 1, key) \
                    and ((self.same(r, c + 3, 0) and self.same(r, c + 2, key)
                          and (self.same(r, c - 2, 0) or self.same(r, c + 4, 0)))
                         or (self.same(r, c + 2, 0) and self.same(r, c + 3, key) and self.same(r, c + 4, 0))):
                num = num + 1
            # 斜下两种
            if self.same(r - 1, c - 1, 0) and self.same(r + 1, c + 1, key) \
                    and ((self.same(r + 3, c + 3, 0) and self.same(r + 2, c + 2, key)
                          and (self.same(r - 2, c - 2, 0) or self.same(r + 4, c + 4, 0)))
                         or (self.same(r + 2, c + 2, 0) and self.same(r + 3, c + 3, key) and self.same(r + 4, c + 4,
                                                                                                       0))):
                num = num + 1
        return num


