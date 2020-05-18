import random
from Model.Skill import Skill


class Role:
    def __init__(
        self,
        name,
        level,
        hp,
        mp,
        attack,
        defence,
        speed,
        skill_list
    ):
        """
        :param name: 角色名
        :param level: 角色等级
        :param hp: 角色血量，分为最大血量和当前血量
        :param mp: 角色魔法量，同上
        :param attack: 攻击值
        :param defence: 防御值
        :param speed: 速度，决定先手前后顺序
        :param skill_list: 技能，列表类型，默认都拥有普通攻击
        """
        self.name = name
        self.level = level
        self.hp_current = self.hp_max = hp
        self.mp_current = self.mp_max = mp
        self.attack = attack
        self.defence = defence
        self.speed = speed
        self.skill_list = [Skill("普通攻击", 20, 0)] + skill_list

    def basic_info(self):
        """
        返回基本信息
        :return:
        """
        return {
            "name": self.name,
            "level": self.level,
            "hp_max": self.hp_max,
            "hp_current": self.hp_current,
            "mp_max": self.mp_max,
            "mp_current": self.mp_current
        }

    def detailed_info(self):
        """
        返回详细信息
        :return:
        """
        return {
            "name": self.name,
            "level": self.level,
            "hp_max": self.hp_max,
            "hp_current": self.hp_current,
            "mp_max": self.mp_max,
            "mp_current": self.mp_current,
            "attack": self.attack,
            "defence": self.defence,
            "speed": self.speed,
            "skill_list": self.skill_list
        }

    def check_if_hp_enough(self):
        """
        检查角色是否死亡
        :return: 布尔值
        """
        if self.hp_current < 0:
            return False
        else:
            return True

    def check_if_mp_enough(self, skill: Skill):
        """
        检查魔法值是否足够释放技能
        :param skill: 使用的技能
        :return:
        """
        if self.hp_current - skill.mp_cost < 0:
            return False
        else:
            return True

    def check_skill_index_legal(self, skill_id):
        """
        检查技能标签是否合法
        :param skill_id: 技能标签
        :return:
        """
        if skill_id < 0 & skill_id > len(self.skill_list):
            return False
        else:
            return True

    def use_skill(self, skill_id, target):
        if not self.check_skill_index_legal:
            return {
                "message": "技能不合法，违规操作",
                "code": -1
            }
        else:
            current_skill = self.skill_list[skill_id]

        if not self.check_if_mp_enough(current_skill):
            return {
                "message": "魔法值不足",
                "code": 0
            }
        else:
            target.hp_current -= (
                    self.attack +
                    current_skill.damage -
                    int(target.defence / 2)
            )
            return {
                "message": "使用技能成功",
                "code": 1
            }

    def attack(self, target):
        """
        攻击函数，调用技能
        :param target: 即将被攻击的目标
        :return:
        """
        pass

    def recover(self):
        """
        每回合固定回复魔法值
        :return:
        """
        self.mp_current = min(
            int(self.mp_max * 0.2) + self.mp_current,
            self.mp_max
        )


class Monster(Role):
    def attack(self, target):
        try_count = 0
        skill_int = random.randint(len(self.skill_list))

        while try_count < 3:
            code = self.use_skill(skill_int, target)["code"]
            if code == 1:
                return {
                    "message": "攻击成功",
                    "code": 1
                }
            else:
                try_count += 1

        # 蓝不够，直接普通攻击
        self.use_skill(0, target)
        return {
            "message": "攻击成功",
            "code": 1
        }
