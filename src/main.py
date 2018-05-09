#!/usr/bin/env python3
import pid
import robot

from time import sleep

def main():
	try:
		robot_ = robot.Robot('outD', 'outA','in4', 'in1', 250)
		while 1:
			robot_.read_colors()
			print(robot_.count_regulation())
			robot_.drive_motors()
			sleep(0.2)
	except KeyboardInterrupt:
		robot_.motor_l.stop(stop_action="hold")
		robot_.motor_r.stop(stop_action="hold")
	except OSError as e:
		print(e)
		robot_.motor_l.stop(stop_action="hold")
		robot_.motor_r.stop(stop_action="hold")


main()




'''
Predkosc | K_crit | T_crit | REGULATION_FACTOR
100|15|0.7| 1
300|7|0.9 | 1
300|8|0.9|1.5 # 0,7 mnoznik przy Kd
250|7|0.9|1.5 #Kd mnoznik 0,5
250|6.5|1|1.5| #Kd mnoznik 0,5
250|5.5|1.7| Ki mnoznik 0.05, Kd mnoznik 0.6
250|5.5|1.7| Ki mnoznik 0.2, Kd mnoznik 0.7, pamietane bledy 70

'''
