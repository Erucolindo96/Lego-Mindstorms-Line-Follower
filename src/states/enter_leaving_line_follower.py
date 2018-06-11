from src.states.exceptions import ChangingStateExcaption
from src.states.line_follower import StateLineFollower


class StateEnterLeavingLineFollower(StateLineFollower):
    def __init__(self, robot):
        super().__init__(robot)
        self.def_speed = 250
        self.color_l = 0
        self.color_r = 0
        self.actual_regulation = 0
        T_crit = 1.7
        K_crit = 5.5
        self.pid_ = pid.PID(0.6 * K_crit, 0.2 * T_crit, 0.7 * T_crit)

    def check_changing_state(self):
        colors = ('unknown', 'black', 'blue', 'green', 'yellow', 'red', 'white', 'brown')
        self.robot.color_sensor_l.mode = 'COL-COLOR'
        self.robot.color_sensor_r.mode = 'COL-COLOR'
        if colors[self.robot.color_sensor_l.value()] == 'green' and colors[self.robot.color_sensor_l.value()] == 'green':
            self.robot.color_sensor_l.mode = 'COL-REFLECT'
            self.robot.color_sensor_r.mode = 'COL-REFLECT'
            raise ChangingStateExcaption("LEAVING_BOX")
        self.robot.color_sensor_l.mode = 'COL-REFLECT'
        self.robot.color_sensor_r.mode = 'COL-REFLECT'