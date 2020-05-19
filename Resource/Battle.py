from Model.Role import Monster
from Model.Skill import Skill


class Round:
    def __init__(self, player, monster):
        self.count = 1
        self.player = player
        self.monster = monster

    def round_info(self):
        """
        返回玩家和怪物的基本信息
        :return:
        """
        player_info = self.player.basic_info()
        monster_info = self.monster.basic_info()
        return {
            "player_info": player_info,
            "monster_info": monster_info
        }

    def round_exec(self):
        player = self.player
        monster = self.monster
        if player.speed >= monster.speed:
            player.attack(monster)
            monster.attack(player)
        else:
            monster.attack(player)
            player.attack(monster)

    def round_rest(self):
        """
        回合结束，在体力都大于0的前提下，玩家和怪物同时回复魔法值
        :return:
        """
        self.player.recover()
        self.monster.recover()


class Battle:
    def __init__(self, player, monster):
        self.player = player
        self.monster = monster


def test():
    monster_a = Monster(
        name="哥布林",
        level=1,
        hp=100,
        mp=25,
        attack=10,
        defence=5,
        speed=2,
        skill_list=[
            Skill("重击", 15, 5),
            Skill("猛击", 25, 10)
        ]
    )

    monster_b = Monster(
        name="牛头人",
        level=1,
        hp=120,
        mp=15,
        attack=25,
        defence=3,
        speed=1,
        skill_list=[
            Skill("头锥", 30, 15)
        ]
    )
    battle = Battle(monster_a, monster_b)
