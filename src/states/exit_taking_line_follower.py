from src.states.exceptions import ChangingStateExcaption
from src.states.line_follower import StateLineFollower


class StateExitTakingLineFollower(StateLineFollower):
    def __init__(self, robot):
        super().__init__(robot)
        self.def_speed = 100 #bylo 250
        self.color_l = 0
        self.color_r = 0
        self.actual_regulation = 0
        T_crit = 1.7
        K_crit = 5.5
        self.pid_ = pid.PID(0.6 * K_crit, 0.2 * T_crit, 0.7 * T_crit)

    def check_changing_state(self):
        BLACK_EPSILON = 20
        colors = ('unknown', 'black', 'blue', 'green', 'yellow', 'red', 'white', 'brown')
        self.robot.color_sensor_l.mode = 'COL-REFLECT'
        self.robot.color_sensor_r.mode = 'COL-REFLECT'
        color1, color2 = self.read_colors()
        print ((color1, color2))
        if color1 < BLACK_EPSILON and color2 < BLACK_EPSILON:
            raise ChangingStateExcaption("FIND_EXIT_TAKING_LINE")