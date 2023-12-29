import random
import time
import pygame
from pygame.locals import *
from collections import namedtuple

chess_pieces = namedtuple("chess_pieces", "name value color")
black_chess = chess_pieces("黑棋", 2, (0, 0, 0))
white_chess = chess_pieces("白棋", 1, (255, 255, 255))
point = namedtuple('point', "x,y")

pygame.init()
# 定义格子大小
cell_size = 30
# 定义棋盘大小
chessboard_width = (18 * cell_size) + 300
chessboard_height = (18 * cell_size) + 100
# 棋子半径
chess_r = 30 // 2 - 3
# 定义边框大小
cheek_w_h = chessboard_width - 270 + 5
# 创建窗口
wind = pygame.display.set_mode((chessboard_width, chessboard_height - 40))
# 设置窗口标题
pygame.display.set_caption("五子棋")
# 定义颜色
black = (0, 0, 0)  # 线条颜色  黑色
white = (255, 255, 255)  # 白色
bp_color = (136, 95, 63)  # 棋盘颜色
red = (235, 28, 39)  # 红色

# 设置字体文件
try:
    font = pygame.font.Font(r'STXINGKA.TTF', 36)
    font_1 = pygame.font.Font(r'STXINGKA.TTF', 80)
except:
    try:
        print("找不到当前文件下华文行楷字体，已切换系统华文行楷字体")
        font = pygame.font.Font(r'C:\Windows\Fonts\STXINGKA.TTF', 36)
        font_1 = pygame.font.Font(r'C:\Windows\Fonts\STXINGKA.TTF', 80)
        # 设置 字体大小
    except:
        print("找不到系统华文行楷字体，已切换系统默认")
        font = pygame.font.Font(r'C:\Windows\Fonts\simsun.ttc', 36)
        font_1 = pygame.font.Font(r'C:\Windows\Fonts\simsun.ttc', 80)
# 游戏是否结束的标志变量
game_over = False
# 白子胜利次数
white_win = 0
# 黑子胜利次数
black_win = 0
# 电脑胜利次数
Ai_win = 0
# 和电脑对战胜利次数
Ai_white_win = 0


class Chessboard:

    def __init__(self):
        self.board = [[0] * 19 for _ in range(19)]

    whywin = 0

    # 判断是否可以落子
    def cat_seat(self, x, y):
        return True if self.board[x][y] == 0 else False

    # 判断是否获胜
    def win(self, x, y, z, game_type):
        # 判断 横排
        self.horizontal(x, y, z, game_type)
        # 判断 竖排
        self.vertical(x, y, z, game_type)
        # 判断 左斜
        self.left_oblique(x, y, z, game_type)
        # 判断 右斜
        self.right_oblique(x, y, z, game_type)
        if self.whywin == 1:
            self.whywin = 0
            return 1
        elif self.whywin == 2:
            self.whywin = 0
            return 2

    # 判断 竖排
    def vertical(self, x, y, z, game_type):
        count = 0
        y1 = max(0, y - 4)
        y2 = min(19, y + 5)
        for i in range(y1, y2):
            if self.board[x][i] == z:
                count += 1
            else:
                count = 0
                continue
            self.why_win(count, z, game_type)

    # 判断 左斜
    def left_oblique(self, x, y, z, game_type):
        count = 0
        x1 = max(0, x - 4)
        x2 = min(19, x + 5)
        for i in range(x1, x2):
            y1 = i + y - x
            if y1 < 19 and y1 >= 0:
                if self.board[i][y1] == z:
                    count += 1
                else:
                    count = 0
                    continue
                self.why_win(count, z, game_type)

    # 判断 右斜
    def right_oblique(self, x, y, z, game_type):
        count = 0
        y1 = max(0, y - 4)
        y2 = min(19, y + 5)
        for i in range(y1, y2):
            x1 = x + y - i
            if x1 < 19 and x1 >= 0:
                if self.board[x1][i] == z:
                    count += 1
                else:
                    count = 0
                    continue
                self.why_win(count, z, game_type)

    # 判断 横排
    def horizontal(self, x, y, z, game_type):
        count = 0
        x1 = max(0, x - 4)
        x2 = min(19, x + 5)
        for i in range(x1, x2):
            if self.board[i][y] == z:
                count += 1
            else:
                count = 0
                continue
            self.why_win(count, z, game_type)

    def why_win(self, count, z, game_type):
        global white_win, black_win, Ai_win, Ai_white_win
        if game_type:
            if count == 5:
                if z == 1:
                    print("白棋获胜！")
                    white_win += 1
                    self.whywin = 1
                else:
                    print("黑棋获胜！")
                    black_win += 1
                    self.whywin = 2
        else:
            if count == 5:
                if z == 1:
                    print("白棋获胜！")
                    Ai_white_win += 1
                    self.whywin = 1
                else:
                    print("黑棋获胜！")
                    Ai_win += 1
                    self.whywin = 2

    def reset_game(self, info, bo):
        # 重置棋盘数组
        self.board = [[0] * 19 for _ in range(19)]
        get_Chessboard()
        info.info_text(bo)
        # 更新显示
        pygame.display.update()

    def win_reset(self, color):
        global game_over
        text = font_1.render(f"{color}胜利！", True, red)
        text_2 = font.render("“按 ‘回车’ 开始新游戏！”", True, white)
        wind.blit(text, (200, 220))
        wind.blit(text_2, (160, 300))
        game_over = True


# 画棋盘
def get_Chessboard():
    # 填充背景颜色
    wind.fill(bp_color)
    # 设置棋盘
    for i in range(1, 20):
        pygame.draw.line(wind, black, (30, i * cell_size), (chessboard_width - 270, i * cell_size))
        pygame.draw.line(wind, black, (i * cell_size, 30), (i * cell_size, chessboard_height - 70))
    # 设置 棋盘边框
    pygame.draw.line(wind, black, (25, 25), (25, cheek_w_h), 5)
    pygame.draw.line(wind, black, (23, 25), (cheek_w_h, 25), 5)
    pygame.draw.line(wind, black, (23, cheek_w_h), (cheek_w_h, cheek_w_h), 5)
    pygame.draw.line(wind, black, (cheek_w_h, 23), (cheek_w_h, cheek_w_h + 2), 5)

    # 设置天元
    pygame.draw.circle(wind, black, (120, 120), 5, 5)
    pygame.draw.circle(wind, black, (480, 120), 5, 5)
    pygame.draw.circle(wind, black, (300, 120), 5, 4)

    pygame.draw.circle(wind, black, (120, 300), 5, 4)
    pygame.draw.circle(wind, black, (300, 300), 5, 4)
    pygame.draw.circle(wind, black, (480, 300), 5, 4)

    pygame.draw.circle(wind, black, (120, 480), 5, 4)
    pygame.draw.circle(wind, black, (300, 480), 5, 4)
    pygame.draw.circle(wind, black, (480, 480), 5, 4)
    # 更新屏幕显示
    pygame.display.flip()


class info_bar:
    # pygame.init()
    # chess = Chessboard()

    # 定义两个单选按钮的位置和大小
    radio1_rect = pygame.Rect(620, 200, 20, 20)
    radio2_rect = pygame.Rect(620, 250, 20, 20)

    # 定义两个单选按钮的状态
    radio1_state = True
    radio2_state = False

    # 显示文本
    def info_text(self, bools):
        pygame.draw.circle(wind, white, (630, 60), 20, 20)
        pygame.draw.circle(wind, black, (630, 120), 20, 20)

        pygame.draw.circle(wind, white, (630, 480), 20, 20)
        pygame.draw.circle(wind, black, (630, 540), 20, 20)

        text1 = font.render("双人对战", True, black)
        text2 = font.render("人机对战", True, black)
        text3 = font.render("玩家一", True, black)
        text3_1 = font.render("玩家", True, black)
        text4 = font.render("玩家二", True, black)
        text4_1 = font.render("电脑", True, black)
        text5 = font.render("战况:", True, black)
        text6 = font.render(f"{white_win}\t胜", True, red)
        text6_1 = font.render(f"{black_win}\t胜", True, red)
        text6_2 = font.render(f"{Ai_win}\t胜", True, red)
        text6_3 = font.render(f"{Ai_white_win}\t胜", True, red)

        wind.blit(text1, (650, 190))
        wind.blit(text2, (650, 242))
        wind.blit(text5, (610, 400))

        if bools:
            wind.blit(text4, (670, 100))
            wind.blit(text3, (670, 40))
            wind.blit(text6, (680, 460))
            wind.blit(text6_1, (680, 520))
        else:
            wind.blit(text4_1, (670, 100))
            wind.blit(text3_1, (670, 40))
            wind.blit(text6_3, (680, 460))
            wind.blit(text6_2, (680, 520))

        pygame.display.flip()

    # 定义检查鼠标是否点击了单选按钮的函数
    def check_radio_click(self, pos, chess, info, computer):
        if self.radio1_rect.collidepoint(pos):
            self.radio1_state = True
            self.radio2_state = False
            chess.reset_game(info, True)
            computer.clear_board()
            # self.info_text(True)
        elif self.radio2_rect.collidepoint(pos):
            self.radio1_state = False
            self.radio2_state = True
            chess.reset_game(info, False)
            computer.clear_board()

            # self.info_text(False)

    def draw_radio_click(self):
        # 绘制单选按钮
        # wind.fill((0, 0, 0))
        pygame.draw.circle(wind, white, (self.radio1_rect.centerx, self.radio1_rect.centery), self.radio1_rect.width // 2)
        pygame.draw.circle(wind, white, (self.radio2_rect.centerx, self.radio2_rect.centery), self.radio2_rect.width // 2)
        if self.radio1_state:
            pygame.draw.circle(wind, (0, 0, 0), (self.radio1_rect.centerx, self.radio1_rect.centery), self.radio1_rect.width // 4)
        if self.radio2_state:
            pygame.draw.circle(wind, (0, 0, 0), (self.radio2_rect.centerx, self.radio2_rect.centery), self.radio2_rect.width // 4)
        pygame.display.flip()


offset = [(1, 0), (0, 1), (1, 1), (1, -1)]

class AI:
    def __init__(self):
        self.line_points = 19  # 棋盘的行列数
        self.my = black_chess  # 电脑            2
        self.opponent = white_chess  # 玩家        1
        self.checkerboard = [[0] * self.line_points for _ in range(self.line_points)]

    # 清空数组
    def clear_board(self):
        self.checkerboard = [[0] * self.line_points for _ in range(self.line_points)]

    # 获取敌方（玩家）点位
    def get_opponent_drop(self, point):
        self.checkerboard[point.y][point.x] = self.opponent.value

    # 计算 AI 的点位：
    def AI_drop(self):
        point_1 = None
        score = 0  # 总得分
        for i in range(self.line_points):
            for j in range(self.line_points):
                if self.checkerboard[j][i] == 0:
                    # 获取当前 点位的 得分
                    score_new = self.get_score(point(i, j))
                    if score_new > score:
                        score = score_new
                        point_1 = point(i, j)
                    # 等分情况 相同时 随机觉得一个位置
                    elif score_new == score and score_new > 0:
                        if random.randint(0, 100) % 2 == 0:
                            point_1 = point(i, j)
        # 将 计算出的点位加入 数组 并返回 点位
        self.checkerboard[point_1.y][point_1.x] = self.my.value
        return point_1
        # return point(9,9)

    def get_score(self, point):
        score = 0
        # offset = [(1, 0), (0, 1), (1, 1), (1, -1)]
        for i in offset:
            # 将各个方向的得分加起来 并返回
            score += self.get_direction(point, i[0], i[1])
        return score

    # 用于 计算某个方向的得分
    def get_direction(self, point, x, y):
        count_my = 0  # 落子处我方连续子数
        count_op = 0  # 落子处对方连续子数
        space_my = None  # 我方连续子中有无空格
        space_op = None  # 对方连续子中有无空格
        both_my = 0  # 我方连续子两端有无阻挡
        both_op = 0  # 对方连续子两端有无阻挡

        # 计算四个方向
        flag = self.get_chess_color(point, x, y, True)
        if flag != 0:
            for i in range(1, 6):
                set_x = point.x + i * x
                set_y = point.y + i * y
                # 判断是否越界
                if 0 <= set_x < self.line_points and 0 <= set_y < self.line_points:
                    if flag == 2:
                        if self.checkerboard[set_y][set_x] == self.my.value:
                            count_my += 1
                            # 判断中间是否有空格隔开
                            if space_my is False:
                                space_my = True
                        elif self.checkerboard[set_y][set_x] == self.opponent.value:
                            count_op += 1
                            break
                        else:
                            if space_my is None:
                                space_my = False
                            else:
                                break  # 表示遇到了第二个空格

                    elif flag == 1:
                        if self.checkerboard[set_y][set_x] == self.my.value:
                            both_op += 1
                            break
                        elif self.checkerboard[set_y][set_x] == self.opponent.value:
                            count_op += 1
                            # 判断中间是否有空格隔开
                            if space_op is False:
                                space_op = True
                        else:
                            if space_op is None:
                                space_op = False
                            else:
                                break  # 表示遇到了第二个空格
                else:
                    # 走到棋盘外 为阻挡
                    if flag == 2:
                        both_my += 1
                    elif flag == 1:
                        both_op += 1

        # 初始化 空格
        if space_my is False:
            space_my = None
        if space_op is False:
            space_op = None

        # 计算另外四个方向
        flag_ = self.get_chess_color(point, -x, -y, True)
        if flag_ != 0:
            for i in range(1, 6):
                set_x = point.x - i * x
                set_y = point.y - i * y
                # 判断是否越界
                if 0 <= set_x < self.line_points and 0 <= set_y < self.line_points:
                    if flag_ == 2:
                        if self.checkerboard[set_y][set_x] == self.my.value:
                            count_my += 1
                            # 判断中间是否有空格隔开
                            if space_my is False:
                                space_my = True
                        elif self.checkerboard[set_y][set_x] == self.opponent.value:
                            count_op += 1
                            break
                        else:
                            if space_my is None:
                                space_my = False
                            else:
                                break  # 表示遇到了第二个空格

                    elif flag_ == 1:
                        if self.checkerboard[set_y][set_x] == self.my.value:
                            both_op += 1
                            break
                        elif self.checkerboard[set_y][set_x] == self.opponent.value:
                            count_op += 1
                            # 判断中间是否有空格隔开
                            if space_op is False:
                                space_op = True
                        else:
                            if space_op is None:
                                space_op = False
                            else:
                                break  # 表示遇到了第二个空格
                else:
                    # 走到棋盘外 为阻挡
                    if flag_ == 2:
                        both_my += 1
                    elif flag_ == 1:
                        both_op += 1
        # 计算得分
        if count_my == 4:
            score = 10000
        elif count_op == 4:
            score = 9000
        elif count_my == 3:
            if both_my == 0:
                score = 1000
            elif both_my == 1:
                score = 100
            else:
                score = 0
        elif count_op == 3:
            if both_op == 0:
                score = 900
            elif both_op == 1:
                score = 90
            else:
                score = 0
        elif count_my == 2:
            if both_my == 0:
                score = 100
            elif both_my == 1:
                score = 10
            else:
                score = 0
        elif count_op == 2:
            if both_op == 0:
                score = 90
            elif both_op == 1:
                score = 9
            else:
                score = 0
        elif count_my == 1:
            score = 10
        elif count_op == 1:
            score = 9
        else:
            score = 0
        # 如果有空格则得分 折半
        if space_op or space_my:
            score = score / 2

        return score

    def get_chess_color(self, points, x, y, next):
        # 查看在某一方向的棋子的颜色 玩家 返回1 电脑返回2 未找到或者出界 返回 0
        # 当第一次未找到是 会继续向下查找一层
        chess_x = points.x + x
        chess_y = points.y + y
        if 0 <= chess_x < self.line_points and 0 <= chess_y < self.line_points:
            # print(f"{chess_x}:{chess_y}")
            if self.checkerboard[chess_y][chess_x] == self.opponent.value:
                return 1
            elif self.checkerboard[chess_y][chess_x] == self.my.value:
                return 2
            else:
                if next:
                    return self.get_chess_color(point(chess_x, chess_y), x, y, False)
                else:
                    return 0
        else:
            return 0


# 获取 点击后的棋盘位置
def get_seat(xy):
    drop_x = xy[0] - cell_size
    drop_y = xy[1] - cell_size
    x = drop_x // cell_size
    y = drop_y // cell_size
    if drop_x % cell_size > 12:
        x += 1
    if drop_y % cell_size > 12:
        y += 1
    if x > 18 or x < 0 or y < 0 or y > 18:
        return None
    return point(x, y)


def playing_chess(chess, point, value, name, color, game_type):
    chess.board[point.x][point.y] = value
    pygame.draw.circle(wind, color, ((point.x + 1) * 30, (point.y + 1) * 30), 12, 12)
    if chess.win(point.x, point.y, value, game_type) == value:
        chess.win_reset(name)
    pygame.display.flip()


def main():
    global game_over
    # 游戏是否结束的标志变量
    game_type = True
    # 初始化 pygame库
    # pygame.init()
    get_Chessboard()
    count = 0
    chess = Chessboard()
    info = info_bar()
    info.info_text(True)
    computer = AI()
    # 保持窗口打开
    while True:
        info.draw_radio_click()  # 单选按钮
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                quit()            # 关闭cmd
            elif event.type == MOUSEBUTTONDOWN and event.button == 1:
                if not game_over:
                    info.check_radio_click(event.pos, chess, info, computer)
                    drop = pygame.mouse.get_pos()
                    point = get_seat(drop)
                    print(f"转换前：{drop}")
                    if point != None and chess.cat_seat(point.x, point.y):
                        if info.radio1_state:
                            # 双人对战
                            print(f"转换后：{'白棋' if count % 2 == 0 else '黑棋'}:({point.x},{point.y})")
                            if count % 2 == 0:
                                playing_chess(chess, point, white_chess.value, white_chess.name, white, game_type)
                            else:
                                playing_chess(chess, point, black_chess.value, black_chess.name, black, game_type)
                            count += 1
                            game_type = True
                        else:
                            # 人机对战
                            print(f"玩家：白棋:({point.x},{point.y})")
                            playing_chess(chess, point, white_chess.value, white_chess.name, white, game_type)
                            if game_over:
                                continue
                            computer.get_opponent_drop(point)
                            point_com = computer.AI_drop()
                            print(f"电脑：黑棋:({point_com.x},{point_com.y})")
                            time.sleep(0.3)
                            playing_chess(chess, point_com, black_chess.value, black_chess.name, black, game_type)
                            game_type = False

                    pygame.display.flip()
            elif game_over and event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                game_over = False
                count = 0
                chess.reset_game(info, game_type)
                computer.clear_board()


if __name__ == '__main__':
    main()
