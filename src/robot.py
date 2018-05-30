#!/usr/bin/env python3
from ev3dev.ev3 import *
import pid 
from math import *
from time import sleep
from enum import Enum
from src.state import *
from datetime import datetime

class EndOfTestException(Exception):
	pass

state_map = {
	"LINE_FOLLOWER": StateLineFollower,
	"FIND_TAKING_LINE": StateFindTakingLine,
	"ENTER_TAKING_LINE_FOLLOWER": StateEnterTakingLineFollower,
	"INSIDE_TAKING_FIELD": StateInsideTakingField,
	"EXIT_TAKING_LINE_FOLLOWER": StateExitTakingLineFollower,
	"FIND_EXIT_TAKING_LINE": StateFindExitTakingLine,
	"FIND_LEAVING_LINE": StateFindLeavingLine,
	"ENTER_LEAVING_LINE_FOLLOWER": StateEnterLeavingLineFollower,
	"LEAVING_BOX": StateLeavingBox,
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
			except ChangingStateExcaption as e:
				self.state = state_map[e](self)
		else:
			try:
				self.state.handle()
			except ChangingStateExcaption as e:
				raise EndOfTestException(e)

	def move_motors_for_time(self, miliseconds, speed_left, speed_right):
		start_time = datetime.now()
		while (datetime.now() - start_time).total_seconds() * 1000 < miliseconds:
			self.motor_l.run_forever(speed_sp=speed_left)
			self.motor_r.run_forever(speed_sp=speed_right)

	def drive_forward(self, miliseconds, speed):
		self.move_motors_for_time(miliseconds, speed, speed)

	def rotate_semi_full_angle(self):
		self.move_motors_for_time(1, -100, 100)

	def rotate_right_angle_left(self):
		self.move_motors_for_time(1, -100, 100)

	def rotate_right_angle_right(self):
		self.move_motors_for_time(1, 100, -100)






