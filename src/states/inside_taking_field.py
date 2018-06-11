from datetime import datetime

from src.states.base_state import RobotState
from src.states.exceptions import ChangingStateExcaption


class StateInsideTakingField(RobotState):
    def __init__(self, robot):
        super().__init__(robot)

    def handle(self):
        """ Podjedz pod klocek podnieś lopatke obroc sie 180 i pojedz do lini """
        riding_speed = 100
        #jedziemy do tylu kawalek
        self.robot.move_motors_for_time(1200, -riding_speed, -riding_speed)
        #opuszczamuy łyche
        self.robot.move_medium_motor_for_time(1150, -150)
        start_time = datetime.now()
        while self.robot.infrared_sensor.value() >= 1:
            self.robot.motor_l.run_forever(speed_sp=riding_speed)
            self.robot.motor_r.run_forever(speed_sp=riding_speed)
        self.robot.stop_motors()
        end_time = datetime.now()
        time_of_riding = end_time-start_time
        #podnosimy łyche
        self.robot.move_medium_motor_for_time(1700, 200)
        self.robot.rotate_semi_full_angle()
        self.robot.drive_forward(time_of_riding.total_seconds()*1000, riding_speed)
        raise ChangingStateExcaption("EXIT_TAKING_LINE_FOLLOWER")
        #raise ChangingStateExcaption("LINE_FOLLOWER")