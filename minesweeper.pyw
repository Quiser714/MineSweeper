# 这个小jio本参考了以下博文：
# https://blog.csdn.net/qq_45414559/article/details/105889784 解答了pyinstaller素材打包的问题
# https://blog.csdn.net/zuliang001/article/details/80762574 让我发现了pyinstaller素材打包的问题
# https://blog.csdn.net/h18208975507/article/details/103051804 告诉我exe的ico怎么换
#
import os
import random
import sys

import pygame

gameMap = [[0 for i in range(16)] for i in range(16)]  # 游戏数据地图，int型
GameOver = False  # 游戏结束标记


def loadImage():  # 载入游戏所需素材，返回库imageDict，字典类型
    # 为配合pyinstaller，写了一个我也搞不懂什么意思的if else
    if getattr(sys, 'frozen', False):
        cur_path = sys._MEIPASS
    else:
        cur_path = os.path.dirname(__file__)

    # 创建一个空字典，准备存入图片的rect类型数据
    imageDict = {}

    # 数字方块1-8
    for i in range(1, 9):
        imageDict['block{}'.format(i)] = pygame.image.load(
            os.path.join(cur_path, r'res/{}.gif'.format(i))).convert()

    # 炸弹方块，白色
    imageDict['bomb'] = pygame.image.load(
        os.path.join(cur_path, r'res/bomb.gif')).convert()

    # 还未点开时的蓝色方块
    imageDict['unknown'] = pygame.image.load(
        os.path.join(cur_path, r'res/unknown.gif')).convert()

    # 周围没有雷的空方块
    imageDict['empty'] = pygame.image.load(
        os.path.join(cur_path, r'res/empty.gif')).convert()

    # 大背景
    imageDict['background'] = pygame.image.load(
        os.path.join(cur_path, r'res/background.jpg')).convert()

    # 左键点击到地雷时显示的红色地雷方块
    imageDict['redbomb'] = pygame.image.load(
        os.path.join(cur_path, r'res/redbomb.gif')).convert()

    # 双击右键的问号？方块
    imageDict['Qmark'] = pygame.image.load(
        os.path.join(cur_path, r'res/Qmark.gif')).convert()

    # 单击右键插小红旗的红旗方块
    imageDict['flag'] = pygame.image.load(
        os.path.join(cur_path, r'res/flag.gif')).convert()

    # 左键按下还未松开时的颜色，不想写进去，我是懒狗
    imageDict['click'] = pygame.image.load(
        os.path.join(cur_path, r'res/click.gif')).convert()

    # 游戏胜利的墨镜emoji
    imageDict['win'] = pygame.image.load(
        os.path.join(cur_path, r'res/win.png')).convert()

    # 游戏未结束时的微笑emoji
    imageDict['smile'] = pygame.image.load(
        os.path.join(cur_path, r'res/smile.png')).convert()

    # 游戏失败时的难过emoji
    imageDict['lose'] = pygame.image.load(
        os.path.join(cur_path, r'res/lose.png')).convert()

    # 时间栏，需要用font填入时间
    imageDict['time'] = pygame.image.load(
        os.path.join(cur_path, r'res/time.png')).convert()

    # 剩余地雷数，需要用font填入时间
    imageDict['num'] = pygame.image.load(
        os.path.join(cur_path, r'res/num.png')).convert()

    # 游戏左上角图标
    ico = pygame.image.load(
        os.path.join(cur_path, r'res/win.png')).convert_alpha()
    pygame.display.set_icon(ico)

    return imageDict


class Block:  # 方块类，游戏地图上下的每个小格
    # 构造函数，参数为自身的值(-1代表雷)value，x,y代表在地图上的坐标，以及素材库imageDict
    def __init__(self, value, x, y, imageDict):
        super().__init__()
        self.situation = 'unknown'              # unknown, flag, pic, Qmark 四种状态
        self.value = value                      # 自身实际值，数字0-8或地雷-1
        self.x = x                              # 自身所在地图x坐标
        self.y = y                              # 自身所在地图y坐标
        self.notClicked = imageDict['unknown']  # 为被点击时的图片
        self.flag = imageDict['flag']           # 被右键插旗时的图片
        self.marked = imageDict['Qmark']        # 标上问号时的图片

        # self.pic为被点开来时的图片
        if value != 0 and value != -1:  # 方格被点开时有数字
            self.pic = imageDict['block{}'.format(value)]
        elif value == -1:               # 地雷
            self.pic = imageDict['redbomb']
        else:                           # 空的
            self.pic = imageDict['empty']

        # 对外显示的图片，初始化为未被点击时的样子
        self.showPic = self.notClicked

    def mouseClick(self, keynum):  # 被点击时的响应函数
        if keynum == 1:  # 代表鼠标左键点击
            if self.situation == 'unknown':     # 此时状态为未被点击
                self.showPic = self.pic     # 对外显示为自身实际的样子
                self.situation = 'pic'      # 将自身状态改为已开苞
                if self.value == -1:        # 如果这是个雷，返回GameOver
                    return 'GameOver'
                else:                       # 否则返回自身的值
                    return self.value
            elif self.situation == 'pic':  # 此时状态为已被点开
                return 'QuickSweep'  # 返回快速清扫，懒人常用
            else:
                pass
        elif keynum == 3:  # 代表右键点击，此时旗，问号，复原三种状态轮换，若已被左键点开则无响应
            if self.situation == 'unknown':
                self.showPic = self.flag
                self.situation = 'flag'
            elif self.situation == 'flag':
                self.showPic = self.marked
                self.situation = 'Qmark'
            elif self.situation == 'Qmark':
                self.showPic = self.notClicked
                self.situation = 'unknown'
            else:
                pass


class MapOfBlock:  # 大地图类

    def __init__(self, gameMap, imageDict):  # 构造函数，参数为int型二维数组gameMap和素材库imageDict
        super().__init__()
        self.background = imageDict['background']  # 游戏背景
        self.Map = [[0 for i in range(16)]
                    for i in range(16)]  # 生成一个16*16的二维数组，用0填充
        for i in range(len(gameMap)):
            for j in range(len(gameMap[0])):
                # 根据参数gameMap生成相应的Block实例储存在Map中
                self.Map[i][j] = Block(
                    gameMap[i][j], 20+35*j, 20+35*i, imageDict)

    def blitMap(self, screen):  # 填充屏幕，不update更新
        screen.blit(self.background, (0, 0))  # 填充背景
        for i in range(len(self.Map)):
            for j in range(len(self.Map[0])):
                # 填充每一个方块
                screen.blit(self.Map[i][j].showPic,
                            (self.Map[i][j].x, self.Map[i][j].y))

    def clickBlock(self, x, y, keynum):  # 点击屏幕相应时间，参数为屏幕的x,y和左键(keynum==1)或右键(keynum==3)
        x = (x-20)//35                          # 将屏幕坐标转换为数组下标，x列
        y = (y-20)//35                          # 将屏幕坐标转换为数组下标，y行
        mc = self.Map[y][x].mouseClick(keynum)  # 屏幕对应方块被点击时的反馈信息
        if mc == 0:                             # 左键点击空方块，递归点开周围8格方块
            for i in (y-1, y, y+1):
                for j in (x-1, x, x+1):
                    if (i >= 0 and i <= 15 and j >= 0 and j <= 15) and not (i == y and j == x):
                        self.clickBlock(j*35+20, i*35+20, keynum)
        elif mc == 'QuickSweep':                # 左键点击数字方块，快速打开周围未开启方块
            # 清点周围存在小红旗个数
            flagCounter = 0
            for i in (y-1, y, y+1):
                for j in (x-1, x, x+1):
                    if (i >= 0 and i <= 15 and j >= 0 and j <= 15) and not (i == y and j == x):
                        if self.Map[i][j].situation == 'flag':
                            flagCounter += 1

            # 小红旗个数与自身数值相同时，玩家认为剩余未开全不是雷
            if flagCounter == self.Map[y][x].value:
                for i in (y-1, y, y+1):
                    for j in (x-1, x, x+1):
                        if (i >= 0 and i <= 15 and j >= 0 and j <= 15) and not (i == y and j == x):  # 防止边缘方块发生越界情况
                            if self.Map[i][j].situation == 'unknown':  # 只操作违背点击过的方块
                                self.clickBlock(j*35+20, i*35+20, keynum)
        elif mc == 'GameOver':                  # 游戏结束
            global GameOver
            GameOver = True


class SwitchBlock:
    def __init__(self, imageDict):
        super().__init__()
        self.smile = imageDict['smile']
        self.win = imageDict['win']
        self.lose = imageDict['lose']
        self.showPic = self.smile
        #self.w = pygame.display.Info()


def startGame(screen, imageDict):  # 开始游戏及数据初始化
    # 屏幕填充背景、未知方块，刷新屏幕
    screen.blit(imageDict['background'], (0, 0))
    for i in range(16):
        for j in range(16):
            screen.blit(imageDict['unknown'], (35*j+20, 35*i+20))
            pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                x, y = pygame.mouse.get_pos()
                if x < 20 or x > 35*16+20 or y < 20 or y > 35*16+20:  # 点击无关空余区域时无响应
                    continue

                # 位置坐标转换为数组下标
                col = (x-20)//35
                row = (y-20)//35

                # 先将点击的方块置为雷，最后再换成数字，以保证随机生成的雷不会生成在这一点，进而保证点击的第一个区域必不为雷
                gameMap[row][col] = -1

                # 随机生成40个雷，并生成其他数字方块
                numOfMines = 0
                while numOfMines < 40:
                    x = random.randint(0, 15)
                    y = random.randint(0, 15)
                    if gameMap[x][y] == -1:
                        continue
                    else:
                        gameMap[x][y] = -1
                        numOfMines += 1
                        for i in (x - 1, x, x + 1):
                            for j in (y - 1, y, y + 1):
                                if i < 0 or i > 15 or j < 0 or j > 15 or gameMap[i][j] == -1:
                                    pass
                                else:
                                    gameMap[i][j] += 1
                # 将点击的方块换回0，并计算周围雷的数量
                gameMap[row][col] = 0
                for i in (row-1, row, row+1):
                    for j in (col-1, col, col+1):
                        if not (i < 0 or i > 15 or j < 0 or j > 15) and gameMap[i][j] == -1:
                            gameMap[row][col] += 1

                # 返回点击方块的行和列
                return row, col


def main():

    pygame.init()                                   # 各种初始化
    screen = pygame.display.set_mode((600, 660))    # 设置屏幕为600*660
    imageDict = loadImage()                         # 导入素材库
    pygame.display.set_caption('QS的扫雷模拟器')     # 设置标题

    # 点击方块后再生成数据地图，获取点击的第一个方块的下标
    y, x = startGame(screen, imageDict)
    BlockMap = MapOfBlock(gameMap, imageDict)       # 生成方块地图
    BlockMap.clickBlock(35*x+20, 35*y+20, 1)        # 再次点击第一个方块，游戏正式开始
    BlockMap.blitMap(screen)                        # 填充屏幕
    pygame.display.update()                         # 刷新屏幕

    while True:  # 游戏主循环
        for event in pygame.event.get():
            if event.type == pygame.QUIT:                               # 右上角叉，退出游戏
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:                        # 按下ESC键，退出游戏
                    sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:                  # 点击鼠标时
                x, y = pygame.mouse.get_pos()                           # 获取鼠标位置
                if x < 20 or x >= 35*16+20 or y < 20 or y >= 35*16+20:  # 点击无用区域时无响应
                    continue
                BlockMap.clickBlock(x, y, event.button)                 # 获取相关相应
        BlockMap.blitMap(screen)    # 填充屏幕
        pygame.display.update()     # 刷新屏幕
        if GameOver:
            sys.exit()


if __name__ == '__main__':
    main()

'''
初级9*9，10个雷
中级16*16，40个雷
高级16*30，99个雷


event.button可以等于几个整数值：
1 - 左键点击
2 - 中点击
3 - 点击右键
4 - 滚动
5 - 向下滚动
'''
