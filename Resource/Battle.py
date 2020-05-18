from Model.Role import Monster
from Model.Skill import Skill


class Battle:
    def __init__(self, player, monster):
        self.player = player
        self.monster = monster

    def if_battle_end(self):
        player = self.player
        monster = self.monster
        if not player.check_if_hp_enough():
            return {
                "batter_state": 0,
                "message": "战斗失败"
            }
        if not monster.check_if_hp_enough():
            return {
                "batter_state": 1,
                "message": "战斗胜利"
            }
        return None

    def round_rest(self):
        """
        双方回蓝
        :return:
        """
        self.player.recover()
        self.monster.recover()

    def start(self):
        player = self.player
        monster = self.monster
        if player.speed >= monster.speed:
            while 1:
                player.attack(monster)
                monster.attack(player)
                if self.if_battle_end():
                    return self.if_battle_end()
                self.round_rest()

        else:
            while 1:
                monster.attack(player)
                player.attack(monster)
                if self.if_battle_end():
                    return self.if_battle_end()
                self.round_rest()


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
    return battle.start()
