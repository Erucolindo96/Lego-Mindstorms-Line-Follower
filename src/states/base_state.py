class RobotState:
    def __init__(self, robot):
        self.robot = robot

    def handle(self):
        raise NotImplementedError