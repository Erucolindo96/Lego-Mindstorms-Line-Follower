from src.states.base_state import RobotState
from src.states.exceptions import ChangingStateExcaption


class StateLeavingBox(RobotState):
    def __init__(self, robot):
        super().__init__(robot)

    def handle(self):
        self.robot.drive_forward(1000, 100)
        #opuszczamy łychę
        self.robot.move_medium_motor_for_time(1200, -150)
        #i odjezdzamy do tylu - wiencząc zwycięstwo
        self.robot.drive_forward(2000, -100)
        self.robot.move_medium_motor_for_time(2000, 100)
        raise ChangingStateExcaption("END")