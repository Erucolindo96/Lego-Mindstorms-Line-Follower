from src.states.base_state import RobotState
from src.states.exceptions import ChangingStateExcaption


class StateFindTakingLine(RobotState):
    def __init__(self, robot):
        super().__init__(robot)

    def handle(self):
        """obrot w lewo o 90 stopni i podjechać trochę do przodu"""
        self.robot.drive_forward(500, 250)
        self.robot.rotate_right_angle_left()
        self.robot.drive_forward(750, 250)
        raise ChangingStateExcaption("ENTER_TAKING_LINE_FOLLOWER")