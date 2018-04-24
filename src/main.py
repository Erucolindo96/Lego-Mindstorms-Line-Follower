#!/usr/bin/env python3


import pid
import robot


def main():
    try:

"""
trzeba wymyslec jakis sposob, aby obliczac okres probkowania PIDa - tzn czas pomiędzy kolejnymi pomiarami uchybu
"""


       # left_motor = LargeMotor('outD')
       # right_motor = LargeMotor('outA')

		robot = Robot('outD', 'outA','in4', 'in1', 100 )


"""		color_sensor_left = ColorSensor('in4')
		color_sensor_left.mode='COL-REFLECT'
		assert color_sensor_left.connected, "Connect a color sensor to any sensor port"

		color_sensor_right = ColorSensor('in1')
		color_sensor_right.mode='COL-REFLECT'
		assert color_sensor_right.connected, "Connect a color sensor to any sensor port"

		speed = 200
"""

#### jeszcze to nie jest gotowe 
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





