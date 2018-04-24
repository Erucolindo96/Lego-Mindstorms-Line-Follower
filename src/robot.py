#!/usr/bin/env python3
from ev3dev.ev3 import *
import pid 
from time import sleep




class Robot:

	motor_l, motor_r,
	color_sensor_l, color_sensor_r,
	def_speed, 
	color_l, color_r 
	pid, MAX_SPEED = 1000
	def __init__(self, left_motor_port ,right_motor_port, left_color_port, right_color_port, def_speed):
		self.motor_l = LargeMotor(left_motor_port)
		self.motor_r = LargeMotor(right_motor_port)

		self.color_sensor_l = ColorSensor(left_color_port)
		self.color_sensor_l.mode = 'COL-REFLECT'
		assert color_sensor_l.connected, "Connect a color sensor to any sensor port"

		self.color_sensor_r = ColorSensor(right_color_port)
		self.color_sensor_r.mode = 'COL-REFLECT'
		assert color_sensor_r.connected, "Connect a color sensor to any sensor port"

		self.def_speed = def_speed
		assert def_speeed <= MAX_SPEED, "Speed too much" 

		color_l = 0
		color_r = 0
		pid = PID(10, 0, 0, 0.1 )

	def readColor(self):
		color_l = color_sensor_l.value()
		color_r = color_sensor_r.value()
		return (color_l, color_r)

# to bedzie sluzyc do ustalenia predkosci silnikow i wysterowania ich
	def driveMotors(self): 
		
	
	














"""
class PID:
    iteration_time = 1
    desired_value = 0 # Wartosc zadana
    Kp = 90
    Ki = 0
    Kd = 0
    integral=0
    error_prior = 0

    def pid_regulation(self, color_left, color_right):
        actual_value = color_left - color_right
        error = actual_value - self.desired_value
        self.integral = self.integral + (error*self.iteration_time)
        derivative = (error-self.error_prior)/self.iteration_time
        output = self.Kp*error + self.Ki*self.integral + self.Kd*derivative
        self.error_prior = error
        if self.integral > 100 or self.integral < 100:
            self.integral = 0
        return output


def main():
    try:
        left_motor = LargeMotor('outD')
        right_motor = LargeMotor('outA')


        '''
        ir = InfraredSensor()
        assert ir.connected, "Connect a single infrared sensor to any sensor port"

        ts = TouchSensor();
        assert ts.connected, "Connect a touch sensor to any port"
        '''

        color_sensor_left = ColorSensor('in4')
        color_sensor_left.mode='COL-REFLECT'
        assert color_sensor_left.connected, "Connect a color sensor to any sensor port"

        color_sensor_right = ColorSensor('in1')
        color_sensor_right.mode='COL-REFLECT'
        assert color_sensor_right.connected, "Connect a color sensor to any sensor port"

        speed = 200

        pid = PID()
        while 1:
            color_left = color_sensor_left.value() #Max 80 dla bialego 0 - czarny
            color_right = color_sensor_right.value() #Max 80 dla bialego 0 - czarny
            print((color_left, color_right))
            wartosc_sterowania = pid.pid_regulation(color_left, color_right)
            wartosc_sterowania = wartosc_sterowania/20

            left_speed = speed
            right_speed = speed
            if wartosc_sterowania < 0 :
                #przyspiesz lewy silnik
                left_speed = speed_corection(speed - wartosc_sterowania)
                right_speed = speed_corection(speed + wartosc_sterowania)

            else :
                right_speed = speed_corection(speed + wartosc_sterowania)
                left_speed = speed_corection(speed - wartosc_sterowania)
            print(left_speed, right_speed)
            left_motor.run_forever(speed_sp=left_speed)
            right_motor.run_forever(speed_sp=right_speed)
            sleep(0.2)
    except KeyboardInterrupt:
        left_motor.stop(stop_action="hold")
        right_motor.stop(stop_action="hold")
    except OSError as e:
        print(e)
        left_motor.stop(stop_action="hold")
        right_motor.stop(stop_action="hold")



def speed_corection(speed):
    if speed > 1000:
        return 1000
    else:
        return speed



def  check_the_color(color_sensor):
    colors=('unknown','black','blue','green','yellow','red','white','brown')
    color_sensor.mode = 'COL-COLOR'
    print(colors[color_sensor.value()])
    color_sensor.mode='COL-REFLECT'



main()

"""
