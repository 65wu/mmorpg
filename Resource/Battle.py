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
        """
        判断回合是否应该终止
        :param role: 即将执行攻击的角色
        :return: 如果角色死亡，判断玩家是胜利还是失败，如果未死亡则直接返回None值
        """
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

    def round_exec(self, skill_id):
        """
        单回合执行函数
        :param skill_id: 用户选择的技能
        :return: 返回本回合信息，如果回合继续，还会返回双方造成的伤害
        """
        player = self.player
        monster = self.monster
        player_attack_damage = monster_attack_damage = 0
        order_list = self.round_attack_sequence()

        # 依照速度排序，依次执行攻击
        for role in order_list:
            if_round_end = self.round_end_check(role)
            # 检查是否有角色死亡
            if if_round_end:
                return if_round_end
            else:
                # 如果是玩家，则使用玩家选择的技能
                if type(role) == Player:
                    player_attack_damage = player.attack(monster, skill_id)["damage"]
                else:
                    monster_attack_damage = monster.attack(player)["damage"]

        # 回合继续，双方回复mp
        self.round_rest()
        return {
            "battle_state": Battle_state.be_in_progress,
            "round_info": self.round_info(),
            "damage": {
                "by_player": player_attack_damage,
                "by_monster": monster_attack_damage
            }
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
