import random
import sys

import pygame
import time
from pygame.constants import *


# 玩家飞机类
class PlayerPlane(pygame.sprite.Sprite):
    # 存放所有飞机子弹的组
    bullets = pygame.sprite.Group()

    def __init__(self, screen):
        # 继承父类精灵类 初始方法要调用后才能使用
        pygame.sprite.Sprite.__init__(self)
        # 创建玩家飞机
        self.image = pygame.image.load("./images/me1.png")
        self.life_image = pygame.image.load("./images/life.png")

        # 根据图片image获取矩形对象
        self.rect = self.image.get_rect()
        self.life_rect = self.life_image.get_rect()
        self.rect.topleft = [Manager.bg_size[0] / 2 - 102, 700 - 126]

        # 玩家的移动输出
        self.speed = 10

        self.plane_fire = 10
        self.plane_fire_time = 0

        self.screen = screen

        # 装子弹的列表
        self.bullets = pygame.sprite.Group()

    def key_control(self):
        # 监听键盘事件
        key_pressed = pygame.key.get_pressed()

        if key_pressed[K_w] or key_pressed[K_UP]:
            if self.rect.top <= 4:
                pass
            else:
                self.rect.top -= self.speed
        if key_pressed[K_s] or key_pressed[K_DOWN]:
            if self.rect.bottom >= Manager.bg_size[1]:
                pass
            else:
                self.rect.bottom += self.speed
        if key_pressed[K_a] or key_pressed[K_LEFT]:
            if self.rect.left <= 0:
                pass
            else:
                self.rect.left -= self.speed
        if key_pressed[K_d] or key_pressed[K_RIGHT]:
            if self.rect.right >= Manager.bg_size[0]:
                pass
            else:
                self.rect.right += self.speed
        # if key_pressed[K_SPACE]:
        #     # 按下空格发射子弹
        #     bullet = Bullet(self.screen, self.rect.left, self.rect.top)
        #     # 把子弹放到列表里
        #     self.bullets.add(bullet)
        #     # 存放所有飞机子弹的组
        #     PlayerPlane.bullets.add(bullet)

    def auto_fire(self):
        bullet = Bullet(self.screen, self.rect.left, self.rect.top)
        # 把子弹放到列表里
        self.bullets.add(bullet)
        # 存放所有飞机子弹的组
        PlayerPlane.bullets.add(bullet)

    def update(self):
        self.key_control()
        self.display()
        self.plane_fire_time += 1
        if self.plane_fire_time == self.plane_fire:
            self.auto_fire()
            self.plane_fire_time = 0

    def display(self):
        # 导入飞机
        self.screen.blit(self.image, self.rect)
        # 更新子弹坐标
        self.bullets.update()
        # 更新生命值
        for i in range(1, Manager.player_plane_life+1):
            self.life_rect.topleft = [Manager.bg_size[0] - 46 * i, 700 - 57]
            # 导入飞机生命值
            self.screen.blit(self.life_image, self.life_rect)

        # 把所有子弹全部添加到屏幕
        self.bullets.draw(self.screen)

    @classmethod
    def clear_bullets(cls):
        # 清空子弹
        cls.bullets.empty()


# 敌方飞机类
class EnemyPlane(pygame.sprite.Sprite):

    def __init__(self, screen):
        # 继承父类精灵类 初始方法要调用后才能使用
        pygame.sprite.Sprite.__init__(self)
        # 创建飞机
        self.image = pygame.image.load("./images/enemy1.png")

        # 根据图片image获取矩形对象
        self.rect = self.image.get_rect()

        x = random.randrange(1, Manager.bg_size[0], 50)
        self.rect.topleft = [x, 0]

        self.speed = 5

        self.screen = screen

        # 装子弹的列表
        self.bullets = pygame.sprite.Group()

        # 敌机移动方向
        self.direction = 'right'

    def display(self):
        # 导入飞机
        self.screen.blit(self.image, self.rect)
        # 遍历所有子弹
        self.bullets.update()

        # 把所有子弹添加到屏幕
        self.bullets.draw(self.screen)

    def auto_move(self):
        if self.direction == 'right':
            self.rect.right += self.speed
        elif self.direction == 'left':
            self.rect.right -= self.speed

        if self.rect.right >= Manager.bg_size[0]:
            self.direction = 'left'
        elif self.rect.right <= 0 + 57:
            self.direction = 'right'

        self.rect.bottom += self.speed / 2

    def update(self):
        self.auto_move()
        self.display()


# 子弹类
class Bullet(pygame.sprite.Sprite):
    def __init__(self, screen, x, y):
        # 精灵类初始化
        pygame.sprite.Sprite.__init__(self)

        # 图片
        self.image = pygame.image.load("./images/bullet1.png")

        # 获取矩形对象
        self.rect = self.image.get_rect()
        self.rect.topleft = [x + 102 / 2 - 1, y - 10]

        # 窗口
        self.screen = screen
        # 速度
        self.speed = 10

    def update(self):
        # 修改子弹坐标
        self.rect.top -= self.speed
        # 如果子弹移出屏幕上方则销毁子弹对象
        if self.rect.top <= -11:
            self.kill()


# 敌机子弹类
class EnemyBullet(pygame.sprite.Sprite):
    def __init__(self, screen, x, y):
        # 精灵类初始化
        pygame.sprite.Sprite.__init__(self)

        # 图片
        self.image = pygame.image.load("./images/bullet1.png")
        # 获取矩形对象
        self.rect = self.image.get_rect()
        self.rect.topleft = [x - 58 / 2, y + 43]

        # 窗口
        self.screen = screen
        # 速度
        self.speed = 5

    def update(self):
        # 修改子弹坐标
        self.rect.top += self.speed
        # 如果子弹移出屏幕下方则销毁子弹对象
        if self.rect.top >= Manager.bg_size[1]:
            self.kill()


# 音效类
class GameSound(object):
    def __init__(self):
        pygame.mixer.init()  # 音乐模块初始化
        pygame.mixer.music.load("./sound/game_music.ogg")
        pygame.mixer.music.set_volume(0.5)  # 声音大小

        self.player__bomb = pygame.mixer.Sound("./sound/me_down.wav")
        self.player__bomb.set_volume(0.5)
        self.enemy__bomb = pygame.mixer.Sound("./sound/enemy1_down.wav")
        self.enemy__bomb.set_volume(0.5)

    @staticmethod
    def playBackgroundMusic():
        pygame.mixer.music.play(-1)  # 开始播放音乐

    def playBombSound(self):
        pygame.mixer.Sound.play(self.player__bomb)

    def enemyBombSound(self):
        pygame.mixer.Sound.play(self.enemy__bomb)


# 碰撞类
class Bomb(object):
    # 初始化碰撞
    def __init__(self, screen, bomb_type):
        self.screen = screen
        if bomb_type == "enemy":
            # 加载爆炸资源
            self.mImages = [pygame.image.load
                            ("./images/me_destroy_" + str(v) + ".png") for v in range(1, 4)]
        else:
            self.mImages = [pygame.image.load
                            ("./images/enemy1_down" + str(v) + ".png") for v in range(1, 4)]
        # 设置当前爆炸播放索引
        self.mIndex = 0
        # 爆炸设置
        self.mPos = [0, 0]
        # 是否可见
        self.mVisible = False

    def action(self, rect):
        # 触发爆炸方法draw
        # 爆炸的坐标
        self.mPos[0] = rect.left
        self.mPos[1] = rect.top
        # 打开爆炸的开关
        self.mVisible = True

    def draw(self):
        if not self.mVisible:
            return
        self.screen.blit(self.mImages[self.mIndex], (self.mPos[0], self.mPos[1]))
        self.mIndex += 1
        if self.mIndex >= len(self.mImages):
            # 如果播放到最后 则重制
            self.mIndex = 0
            self.mVisible = False


# 地图
class GameBackground(object):
    # 初始化地图
    def __init__(self, screen):
        self.mImage1 = pygame.image.load("./images/background.png")
        self.mImage2 = pygame.image.load("./images/background.png")
        # 窗口
        self.screen = screen
        # 辅助移动地图
        self.y1 = 0
        self.y2 = -Manager.bg_size[1]

    # 移动地图
    def move(self):
        self.y1 += 2
        self.y2 += 2
        if self.y1 >= Manager.bg_size[1]:
            self.y1 = 0
        if self.y2 >= 0:
            self.y2 = -Manager.bg_size[1]

    # 绘制地图
    def draw(self):
        self.screen.blit(self.mImage1, (0, self.y1))
        self.screen.blit(self.mImage2, (0, self.y2))


# 管理类
class Manager(object):
    bg_size = (480, 700)
    # 创建敌机定时器的id
    create_enemy_id = USEREVENT + 1
    # 游戏结束 倒计时的id
    game_over_id = USEREVENT
    # 游戏是否结束
    is_game_over = False
    # 重开倒计时时间
    over_time = 3
    # 敌机出现的间隔
    enemy_time = 200

    # 飞机初始生命值
    player_plane_life = 3

    def __init__(self):
        pygame.init()
        # 创建窗口
        self.screen = pygame.display.set_mode(Manager.bg_size, 0, 24)  # 分辨率 显示模式 颜色位数
        # 创建背景图片
        self.map = GameBackground(self.screen)
        # 初始化一个装玩家精灵的group
        self.players = pygame.sprite.Group()
        # 初始化一个装敌精灵的group
        self.enemies = pygame.sprite.Group()
        # 初始化一个玩家爆照的对象
        self.player_bomb = Bomb(self.screen, 'enemy')
        # 初始化一个敌机爆炸的对象
        self.enemy_bomb = Bomb(self.screen, "player")
        # 初始化一个声音播放的对象
        self.sound = GameSound()

    @staticmethod
    def quit_game():
        pygame.quit()
        sys.exit()

    def show_over_text(self):
        # 游戏结束 倒计时后重新开始
        self.draw_text('game over %d' % Manager.over_time, 100, Manager.bg_size[1] / 2,
                       textHeight=50, fontColor=[200, 0, 0])

    def game_over(self):
        Manager.is_game_over = True  # 标志游戏结束
        pygame.time.set_timer(Manager.game_over_id, 1000)  # 开启游戏倒计时
        # 把玩家从精灵组移除
        self.players.remove(self.players.sprites()[0])
        # 重制生命值
        Manager.player_plane_life = 3

    def game_over_timer(self):
        self.show_over_text()
        # 倒计时-1
        Manager.over_time -= 1
        if Manager.over_time == 0:
            # 触发游戏结束
            pygame.time.set_timer(Manager.game_over_id, 0)
            # 重制
            Manager.over_time = 3
            Manager.is_game_over = False
            self.start_game()

    @staticmethod
    def start_game():
        # 重新开始游戏 有些类属性清空
        PlayerPlane.clear_bullets()
        manager2 = Manager()
        manager2.main()

    def new_player(self):
        # 创建玩家飞机对象 添加到对应组
        player = PlayerPlane(self.screen)
        self.players.add(player)

    def new_enemy(self):
        # 创建敌机对象 添加到对应组
        enemy = EnemyPlane(self.screen)
        self.enemies.add(enemy)

    def draw_text(self, text, x, y, textHeight=30, fontColor=(255, 0, 0), backgroundColor=None):
        # 通过字体文件获取字体对象
        font_obj = pygame.font.Font('./font/font.ttf', textHeight)
        # 配置要显示的文字
        text_obj = font_obj.render(text, True, fontColor, backgroundColor)
        # 显示的对象rect
        text_rect = text_obj.get_rect()
        # 设置显示对象的坐标
        text_rect.topleft = (x, y)
        # 绘制字到指定区域
        self.screen.blit(text_obj, text_rect)

    def main(self):
        # 设置程序标题
        pygame.display.set_caption('打飞机', '打飞机')
        # 设置图标
        surface = pygame.image.load('./images/life.png')
        pygame.display.set_icon(surface)
        # 播放背景音乐
        self.sound.playBackgroundMusic()
        # 创建一个玩家
        self.new_player()
        # 开启创建敌机的定时器
        pygame.time.set_timer(Manager.create_enemy_id, Manager.enemy_time)

        while True:
            # 把背景图片贴到窗口
            # 移动地图
            self.map.move()
            self.map.draw()

            # 绘制文字
            # self.draw_text('sss:100', 0, 0)
            if Manager.is_game_over:
                # 判断游戏结束才显示文本
                self.show_over_text()

            # 获取事件
            for event in pygame.event.get():
                # 判断事件类型
                if event.type == QUIT:
                    self.quit_game()
                elif event.type == Manager.create_enemy_id:
                    # 创建一个敌机
                    self.new_enemy()
                elif event.type == Manager.game_over_id:
                    # 定时器触发事件
                    self.game_over_timer()

            # 调用爆炸的对象
            self.player_bomb.draw()
            self.enemy_bomb.draw()

            # 判断碰撞
            is_collide = pygame.sprite.groupcollide(self.players, self.enemies, False, True)  # 如果发生碰撞 True移除

            if is_collide:
                items = list(is_collide.items())[0]
                x = items[0]
                y = items[1][0]
                # 玩家爆炸图片
                self.player_bomb.action(x.rect)
                # 敌机爆炸图片
                self.enemy_bomb.action(y.rect)
                # 玩家爆炸的声音
                self.sound.playBombSound()
                # 敌机爆炸的声音
                self.sound.enemyBombSound()
                Manager.player_plane_life -= 1
                if Manager.player_plane_life == 0:
                    self.game_over()

            # 判断玩家子弹和敌机碰撞
            is_collide_player_bullets = pygame.sprite.groupcollide(PlayerPlane.bullets, self.enemies, True, True)
            if is_collide_player_bullets:
                items = list(is_collide_player_bullets.items())[0]
                y = items[1][0]
                # 敌机爆炸图片
                self.enemy_bomb.action(y.rect)
                # 敌机爆炸的声音
                self.sound.enemyBombSound()

            # 玩家飞机和子弹的显示
            self.players.update()
            # 敌机和子弹的显示
            self.enemies.update()

            # 刷新窗口内容
            pygame.display.update()
            time.sleep(0.01)


if __name__ == '__main__':
    manager = Manager()
    manager.main()