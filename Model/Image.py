import os


class Image:
    def __init__(self,
                 game,
                 screen,
                 monster_image,
                 player_image,
                 data_dir=os.path.dirname(os.path.dirname(__file__)) + '/Data',
                 bg_image="/Image/Background/background.png",
                 role_size=(300, 300),
                 monster_x=0,
                 player_x=500,
                 role_y=160
                 ):
        self.game = game
        self.screen = screen

        self.data_dir = data_dir
        self.bg_image = data_dir + bg_image
        self.monster_image = data_dir + monster_image
        self.player_image = data_dir + player_image

        self.role_size = role_size
        self.monster_x = monster_x
        self.player_x = player_x
        self.role_y = role_y

    def load_image(self):
        game = self.game
        screen = self.screen

        bg_source = game.image.load(self.bg_image)
        bg = game.transform.scale(bg_source, (800, 600))

        monster_source = game.image.load(self.monster_image)
        monster = game.transform.scale(monster_source, self.role_size)

        player_source = game.image.load(self.player_image)
        player_scale = game.transform.scale(player_source, self.role_size)
        player = game.transform.flip(player_scale, True, False)

        screen.blit(bg, (0, 0))
        screen.blit(monster, (self.monster_x, self.role_y))
        screen.blit(player, (self.player_x, self.role_y))
