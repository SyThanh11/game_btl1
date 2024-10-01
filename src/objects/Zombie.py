from enum import Enum

from src.objects.Image import Image
from src.const.const import ZOMBIE_STANDING_INTERVAL


class ZombieState(Enum):
    APPEARING = 0
    STANDING = 1
    SLAMED = 2
    DISAPPEARING = 3
    HIDDEN = 4


class Zombie (Image):
    def __init__(self, scene):
        super().__init__(scene, scene.manager.image.get("zombie"))
        self.state = ZombieState.HIDDEN
        self.appearing_interval = 200
        self.standing_interval = ZOMBIE_STANDING_INTERVAL
        self.slamed_interval = 1000
        self.disappearing_interval = 200
        self.time_ratio = 1.0
        self.standing_pos = (0, 0)

    def set_state(self, state):
        if state == ZombieState.APPEARING:
            self.set_active(True)
            self.set_texture(self.scene.manager.image.get("zombie"))
            self.set_alpha(255)
            self.set_viewport(0, 0, 1, 0)
            self.standing_pos = self.get_pos()
            self.set_pos(self.standing_pos[0], self.standing_pos[1] + 50)
        elif state == ZombieState.STANDING:
            pass
        elif state == ZombieState.SLAMED:
            self.set_texture(self.scene.manager.image.get("slamed"))
        elif state == ZombieState.DISAPPEARING:
            pass
        elif state == ZombieState.HIDDEN:
            self.set_active(False)
        self.time_ratio = 1.0
        self.state = state

    def proceed_time(self, time_interval, total_time):
        if self.time_ratio < (time_interval / total_time):
            self.time_ratio = 1.0
            return False
        else:
            self.time_ratio -= time_interval / total_time
            return True

    def update(self, time_interval):
        if self.state == ZombieState.APPEARING:
            if self.proceed_time(time_interval, self.appearing_interval):
                self.set_viewport(0, 0, 1, 1 - self.time_ratio)
                self.set_pos(self.standing_pos[0], self.standing_pos[1] + 50 * self.time_ratio)
            else:
                self.set_viewport(0, 0, 1, 1)
                self.set_pos(self.standing_pos[0], self.standing_pos[1])
                self.set_state(ZombieState.STANDING)

        elif self.state == ZombieState.STANDING:
            if self.proceed_time(time_interval, self.standing_interval):
                pass
            else:
                self.set_state(ZombieState.DISAPPEARING)
        elif self.state == ZombieState.SLAMED:
            if self.proceed_time(time_interval, self.slamed_interval):
                self.set_alpha(255 * self.time_ratio)
            else:
                self.set_state(ZombieState.HIDDEN)
        elif self.state == ZombieState.DISAPPEARING:
            if self.proceed_time(time_interval, self.slamed_interval):
                self.set_viewport(0, 0, 1, self.time_ratio)
                self.set_pos(self.standing_pos[0], self.standing_pos[1] + 50 * (1 - self.time_ratio))
            else:
                self.set_viewport(0, 0, 1, 0)
                self.set_pos(self.standing_pos[0], self.standing_pos[1])
                missed_num = self.scene.manager.get_variable("missed")
                self.scene.manager.set_variable("missed", missed_num + 1)
                self.set_state(ZombieState.HIDDEN)
