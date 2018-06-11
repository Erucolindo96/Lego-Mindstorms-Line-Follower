#!/usr/bin/env python3
from ev3dev.ev3 import *
import pid 
from math import *
from time import sleep
from enum import Enum
from state import *
from datetime import datetime
from src.states import exceptions
from src.states import line_follower
from src.states import find_exit_taking_line
from src.states import enter_taking_line_follower
from src.states import inside_taking_field
from src.states import exit_taking_line_follower
from src.states import find_exit_taking_line
from src.states import find_leaving_line
from src.states import enter_leaving_line_follower
from src.states import leaving_box
from src.states import end

RIGTH_ANGLE_ROUND_T = 1650
ROUND_VEL = 100

class EndOfTestException(Exception):
	pass

state_map = {
	"LINE_FOLLOWER": line_follower.StateLineFollower,
	"FIND_TAKING_LINE": find_exit_taking_line.StateFindTakingLine,
	"ENTER_TAKING_LINE_FOLLOWER": enter_taking_line_follower.StateEnterTakingLineFollower,
	"INSIDE_TAKING_FIELD": inside_taking_field.StateInsideTakingField,
	"EXIT_TAKING_LINE_FOLLOWER": exit_taking_line_follower.StateExitTakingLineFollower,
	"FIND_EXIT_TAKING_LINE": find_exit_taking_line.StateFindExitTakingLine,
	"FIND_LEAVING_LINE": find_leaving_line.StateFindLeavingLine,
	"ENTER_LEAVING_LINE_FOLLOWER": enter_leaving_line_follower.StateEnterLeavingLineFollower,
	"LEAVING_BOX": leaving_box.StateLeavingBox,
	"END": end.StateEnd,
}

class Robot:
	def __init__(self, left_motor_port ,right_motor_port, medium_motor_port, left_color_port, right_color_port):
		self.motor_l = LargeMotor(left_motor_port)
		self.motor_r = LargeMotor(right_motor_port)
		self.medium_motor = MediumMotor(medium_motor_port)

		self.color_sensor_l = ColorSensor(left_color_port)
		self.color_sensor_l.mode = 'COL-REFLECT'
		assert self.color_sensor_l.connected, "Connect a color sensor to any sensor port"

		self.color_sensor_r = ColorSensor(right_color_port)
		self.color_sensor_r.mode = 'COL-REFLECT'
		assert self.color_sensor_r.connected, "Connect a color sensor to any sensor port"

		self.infrared_sensor = InfraredSensor()
		assert self.infrared_sensor.connected

		self.state = state_map["LINE_FOLLOWER"](self)
		#self.pid_ = pid.PID(K_crit, 0, 0)
	
	def handle(self, testing=False):
		if not testing:
			try:
				self.state.handle()
			except exceptions.ChangingStateExcaption as e:
				self.state = state_map[str(e)](self)
		else:
			try:
				self.state.handle()
			except exceptions.ChangingStateExcaption as e:
				raise EndOfTestException(e)

	def move_motors_for_time(self, miliseconds, speed_left, speed_right):
		start_time = datetime.now()
		while (datetime.now() - start_time).total_seconds() * 1000 < miliseconds:
			self.motor_l.run_forever(speed_sp=speed_left)
			self.motor_r.run_forever(speed_sp=speed_right)
		self.motor_l.stop(stop_action="hold")
		self.motor_r.stop(stop_action="hold")

	def move_medium_motor_for_time(self, miliseconds, speed):
		start_time = datetime.now()
		while (datetime.now() - start_time).total_seconds() * 1000 < miliseconds:
			self.medium_motor.run_forever(speed_sp=speed)
		self.medium_motor.stop(stop_action="hold")

	def drive_forward(self, miliseconds, speed):
		self.move_motors_for_time(miliseconds, speed, speed)

	def stop_motors(self):
		self.motor_l.stop(stop_action="hold")
		self.motor_r.stop(stop_action="hold")
		self.medium_motor.stop(stop_action="hold")
	'''
	180 stopni
	'''
	def rotate_semi_full_angle(self):
		self.move_motors_for_time(2*RIGTH_ANGLE_ROUND_T, ROUND_VEL, -ROUND_VEL)
	'''
	W prawo o 90
	'''
	def rotate_right_angle_left(self):
		self.move_motors_for_time(RIGTH_ANGLE_ROUND_T, ROUND_VEL, -ROUND_VEL)
	'''
	W lewo o 90
	'''
	def rotate_right_angle_right(self):
		self.move_motors_for_time(RIGTH_ANGLE_ROUND_T, -ROUND_VEL, ROUND_VEL)






