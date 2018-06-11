import pid
from time import sleep
from datetime import datetime

MAX_SPEED = 1000
MIN_SPEED = -200
REGULATION_FACTOR = 2


class ChangingStateExcaption(Exception):
    pass


class RobotState:
    def __init__(self, robot):
        self.robot = robot

    def handle(self):
        raise NotImplementedError


class StateLineFollower(RobotState):
    def __init__(self, robot):
        super().__init__(robot)
        self.def_speed = 250
        self.color_l = 0
        self.color_r = 0
        self.actual_regulation = 0
        T_crit = 1.7
        K_crit = 5.5
        self.pid_ = pid.PID( 0.6 *K_crit, 0.2* T_crit, 0.7 * T_crit)

    def handle(self):
        self.read_colors()
        self.count_regulation()
        self.drive_motors()
        self.check_changing_state()

    def read_colors(self):
        self.color_l = self.robot.color_sensor_l.value()
        self.color_r = self.robot.color_sensor_r.value()
        return (self.color_l, self.color_r)

    def count_regulation(self):
        '''
        actual_regulation > 0 => lewy bardziej na bialym => lewy mocniej, prawy slabiej
        '''
        self.actual_regulation = self.pid_.get_regulation(self.color_l - self.color_r) * REGULATION_FACTOR
        return self.actual_regulation

    def drive_motors(self):
        regulation = self.actual_regulation
        silniki = self.get_silniki(regulation)
        wew_silnik = silniki['wew_silnik']
        zew_silnik = silniki['zew_silnik']

        regulation_abs = abs(regulation)
        ile_dla_zewnetrznego = self.ile_zostanie_sterowania_po_wysterowaniu_wewnetrznego(regulation_abs)
        self.zwolnij_wew_silnik_jak_sie_da(wew_silnik, regulation_abs)
        zew_silnik.run_forever(speed_sp=self.speed_corection(self.def_speed + ile_dla_zewnetrznego))

    @staticmethod
    def speed_corection(speed):
        if speed > MAX_SPEED:
            return MAX_SPEED
        elif speed < MIN_SPEED:
            return MIN_SPEED
        else:
            return speed

    def get_silniki(self, regulation):
        if regulation < 0:
            return {'wew_silnik': self.robot.motor_r, 'zew_silnik': self.robot.motor_l}
        else:
            return {'wew_silnik': self.robot.motor_l, 'zew_silnik': self.robot.motor_r}

    def ile_zostanie_sterowania_po_wysterowaniu_wewnetrznego(self, reg_abs):
        if reg_abs > (self.def_speed - MIN_SPEED):
            return reg_abs - (self.def_speed - MIN_SPEED)
        return 0

    def zwolnij_wew_silnik_jak_sie_da(self, wew_silnik, reg_abs):
        ile_zostanie_sterowania = self.ile_zostanie_sterowania_po_wysterowaniu_wewnetrznego(reg_abs)
        if ile_zostanie_sterowania == 0:  # sterujemy tylko wew silnik
            wew_silnik.run_forever(speed_sp=self.speed_corection(self.def_speed - reg_abs))
        else:  # troche sterowania zostanie - musimy wysterowac tez zewnetrzny silnik
            wew_silnik.run_forever(speed_sp=self.speed_corection(MIN_SPEED))
            # return ile_zostanie_sterowania

    def check_changing_state(self):
        colors = ('unknown', 'black', 'blue', 'green', 'yellow', 'red', 'white', 'brown')
        self.robot.color_sensor_l.mode = 'COL-COLOR'
        if colors[self.robot.color_sensor_l.value()] == 'red':
            raise ChangingStateExcaption("FIND_TAKING_LINE")
        if colors[self.robot.color_sensor_l.value()] == 'green':
            raise ChangingStateExcaption("FIND_LEAVING_LINE")
        self.robot.color_sensor_l.mode = 'COL-REFLECT'


class StateFindTakingLine(RobotState):
    def __init__(self, robot):
        super().__init__(robot)

    def handle(self):
        """obrot w lewo o 90 stopni i podjechać trochę do przodu"""
        self.robot.drive_forward(500, 250)
        self.robot.rotate_right_angle_left()
        self.robot.drive_forward(750, 250)
        raise ChangingStateExcaption("ENTER_TAKING_LINE_FOLLOWER")


class StateEnterTakingLineFollower(StateLineFollower):
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
        if colors[self.robot.color_sensor_l.value()] == 'red' and colors[self.robot.color_sensor_l.value()] == 'red':
            self.robot.color_sensor_l.mode = 'COL-REFLECT'
            self.robot.color_sensor_r.mode = 'COL-REFLECT'
            raise ChangingStateExcaption("INSIDE_TAKING_FIELD")
        self.robot.color_sensor_l.mode = 'COL-REFLECT'
        self.robot.color_sensor_r.mode = 'COL-REFLECT'        


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

class StateFindLeavingLine(RobotState):
    def __init__(self, robot):
        super().__init__(robot)

    def handle(self):
        """
            obrot w lewo o 90 stopni i podjechać trochę do przodu
        """
        self.robot.drive_forward(500, 250)
        self.robot.rotate_right_angle_left()
        self.robot.drive_forward(750, 250)
        raise ChangingStateExcaption("ENTER_LEAVING_LINE_FOLLOWER")



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


class StateEnd(RobotState):
    def __init__(self, robot):
        super().__init__(robot)

    def handle(self):
        print("the end!")
        sleep(1)



