from Model.Role import Monster, Player
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

    def round_attack_sequence(self):
        """
        获取本回合玩家和怪物的攻击先后顺序
        :return:
        """
        player = self.player
        monster = self.monster
        order_list = [] + player + monster
        sorted(order_list, key=lambda role: role.speed)
        return order_list

    def round_rest(self):
        """
        回合结束，在体力都大于0的前提下，玩家和怪物同时回复魔法值
        :return:
        """
        self.player.recover()
        self.monster.recover()

    def round_end_check(self, role):
        if not role.alive:
            if type(role) == Player:
                return {
                    "battle_state": Battle_state.lose,
                    "round_info": self.round_info()
                }
            # 暂时一对一，一个怪死了就算胜利
            else:
                return {
                    "battle_state": Battle_state.win,
                    "round_info": self.round_info()
                }
        else:
            return None

    def round_exec(self):
        player = self.player
        monster = self.monster
        order_list = self.round_attack_sequence()
        for role in order_list:
            if_round_check = self.round_end_check(role)
            if if_round_check:
                return if_round_check
            else:
                if type(role) == Player:
                    skill_id = input("请输入使用的技能id")
                    player.attack(monster, skill_id)
                else:
                    monster.attack(player)

        self.round_rest()
        return {
            "battle_state": Battle_state.be_in_progress,
            "round_info": self.round_info()
        }


class Battle_state:
    lose = -1
    be_in_progress = 0
    win = 1


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
