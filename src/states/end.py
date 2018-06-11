from time import sleep

from src.states.base_state import RobotState


class StateEnd(RobotState):
    def __init__(self, robot):
        super().__init__(robot)

    def handle(self):
        print("the end!")
        sleep(1)