#!/usr/bin/env python3
import pid
import robot

from time import sleep

TESTING = True
TESTING_STATE = "FIND_TAKING_LINE"

def main():
	try:
		robot_ = robot.Robot('outD', 'outA', 'outC','in4', 'in1')
		if TESTING:
			robot_.state = robot.stat_map[TESTING_STATE]()
		while 1:
			robot_.handle(testing=TESTING)
			sleep(0.2)
	except KeyboardInterrupt:
		robot_.motor_l.stop(stop_action="hold")
		robot_.motor_r.stop(stop_action="hold")
	except OSError as e:
		print(e)
		robot_.motor_l.stop(stop_action="hold")
		robot_.motor_r.stop(stop_action="hold")
	except robot.EndOfTestException as e:
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
