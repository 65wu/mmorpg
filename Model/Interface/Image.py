import os


class Image:
    def __init__(self,
                 game,
                 screen,
                 monster_image,
                 player_image,
                 data_dir=os.path.dirname(
                     os.path.dirname(os.path.dirname(__file__))) + '/Data',
                 bg_image="/Image/Background/background.png",
                 role_size=(300, 300),
                 monster_x=0,
                 player_x=500,
                 role_y=160
                 ):
        """
        图片类初始化
        :param game: pygame
        :param screen: 屏幕
        :param monster_image: 怪物图片地址
        :param player_image: 玩家图片地址
        :param data_dir: 数据文件夹根目录， 按需求可自己更改
        :param bg_image: 背景图片地址
        :param role_size: 角色大小，这个数值会同时影响到玩家和怪物图片
        :param monster_x: 怪物图片的横坐标
        :param player_x: 玩家图片的横坐标
        :param role_y: 角色的y坐标，玩家和怪物图片统一高度
        """
        self.game = game
        self.screen = screen

        self.data_dir = data_dir
        self.bg_image = data_dir + bg_image
        # 注意玩家和怪物图片是利用data根目录推导而成
        self.monster_image = data_dir + monster_image
        self.player_image = data_dir + player_image

        self.role_size = role_size
        self.monster_x = monster_x
        self.player_x = player_x
        self.role_y = role_y

    def load_image(self):
        """
        加载图片
        :return:
        """
        game = self.game
        screen = self.screen

        # 这里对背景图片进行伸缩
        bg_source = game.image.load(self.bg_image)
        bg = game.transform.scale(bg_source, (800, 600))

        monster_source = game.image.load(self.monster_image)
        monster = game.transform.scale(monster_source, self.role_size)

        player_source = game.image.load(self.player_image)
        player_scale = game.transform.scale(player_source, self.role_size)
        # 这里对玩家图像做了镜像处理
        player = game.transform.flip(player_scale, True, False)

        screen.blit(bg, (0, 0))
        screen.blit(monster, (self.monster_x, self.role_y))
        screen.blit(player, (self.player_x, self.role_y))
