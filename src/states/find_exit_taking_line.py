from src.states.base_state import RobotState
from src.states.exceptions import ChangingStateExcaption


class StateFindExitTakingLine(RobotState):
    def __init__(self, robot):
        super().__init__(robot)

    def handle(self):
        """
         Podjechać do przodu obrocic sie w lewo o 90 stopnu
        """
        self.robot.drive_forward(500, 250)
        self.robot.rotate_right_angle_left()
        raise ChangingStateExcaption("LINE_FOLLOWER")