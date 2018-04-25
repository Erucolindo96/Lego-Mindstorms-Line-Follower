#!/usr/bin/env python3
import pid
import robot

from time import sleep

def main():
	try:
		robot_ = robot.Robot('outD', 'outA','in4', 'in1', 300)
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
Predkosc | K_crit | T_crit
100|15|0.7
300|7|0.9

'''
