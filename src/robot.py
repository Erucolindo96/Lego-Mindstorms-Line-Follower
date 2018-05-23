#!/usr/bin/env python3
from ev3dev.ev3 import *
import pid 
from math import *
from time import sleep
from enum import Enum

MAX_SPEED = 1000
MIN_SPEED = -200
REGULATION_FACTOR = 2

RobotState__ = Enum( 'RobotState',
 'LINE_FOLLOWER FIND_TAKING_LINE TAKING_LINE_FOLLOWER INSIDE_TAKING_FIELD TAKING_BOX EXITING_FIELD FIND_LEAVING_LINE LEAVING_BOX'
)


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
		self.pid_ = pid.PID(0.6*K_crit, 0.2*T_crit, 0.7*T_crit)
	
	def handle(self):
		self.read_colors()
		#print(self.robot.count_regulation())
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
		ile_dla_zewnetrznego = 	self.ile_zostanie_sterowania_po_wysterowaniu_wewnetrznego(regulation_abs )
		self.zwolnij_wew_silnik_jak_sie_da(wew_silnik, regulation_abs)
		zew_silnik.run_forever(speed_sp=self.speed_corection(self.def_speed+ile_dla_zewnetrznego))

		#left_motor.run_forever(speed_sp=left_speed)
		#right_motor.run_forever(speed_sp=right_speed)
	
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
			return {'wew_silnik' : self.robot.motor_r, 'zew_silnik': self.robot.motor_l}
		else:
			return {'wew_silnik' : self.robot.motor_l, 'zew_silnik': self.robot.motor_r}
			
	def ile_zostanie_sterowania_po_wysterowaniu_wewnetrznego(self, reg_abs):
		if reg_abs > (self.def_speed - MIN_SPEED):
			return reg_abs - (self.def_speed - MIN_SPEED)
		return 0
			
	def zwolnij_wew_silnik_jak_sie_da(self, wew_silnik, reg_abs):
		ile_zostanie_sterowania = self.ile_zostanie_sterowania_po_wysterowaniu_wewnetrznego(reg_abs)
		#print('zostalo sterowania {}'.format(ile_zostanie_sterowania))
		if ile_zostanie_sterowania == 0: #sterujemy tylko wew silnik
			wew_silnik.run_forever(speed_sp=self.speed_corection(self.def_speed - reg_abs))
		else: #troche sterowania zostanie - musimy wysterowac tez zewnetrzny silnik
			wew_silnik.run_forever(speed_sp=self.speed_corection(MIN_SPEED))
		#return ile_zostanie_sterowania


	def check_changing_state(self):
		colors=('unknown','black','blue','green','yellow','red','white','brown')
		self.robot.color_sensor_l.mode = 'COL-COLOR'
		if colors[self.robot.color_sensor_l.value()] == 'red':
			raise Exception("FIND_TAKING_LINE")
		if colors[self.robot.color_sensor_l.value()] == 'green':
			raise Exception("FIND_LEAVING_LINE")
		self.robot.color_sensor_l.mode='COL-REFLECT'



class StateFindTakingLine(RobotState):
		def __init__(self, robot):
			super().__init__(robot)
			self.licznik = 100
			self.licznik2 = 200
		
		def handle(self):
			"""
			obrot w lewo o 90 stopni i podjechać trochę do przodu
			"""
			for i in range(self.licznik):
				self.robot.motor_l.run_forever(speed_sp=300)
				self.robot.motor_r.run_forever(speed_sp=-300)
			for i in range(self.licznik2):
				self.robot.motor_l.run_forever(speed_sp=300)
				self.robot.motor_r.run_forever(speed_sp=300)
			raise Exception("TAKING_LINE_FOLLOWER")


class StateFindTakingLineFollower(StateLineFollower):
	def __init__(self, robot):
		super().__init__(robot)
		self.def_speed = 250
		self.color_l = 0
		self.color_r = 0
		self.actual_regulation = 0
		T_crit = 1.7
		K_crit = 5.5
		self.pid_ = pid.PID(0.6*K_crit, 0.2*T_crit, 0.7*T_crit)


	def check_changing_state(self):
		colors=('unknown','black','blue','green','yellow','red','white','brown')
		self.robot.color_sensor_l.mode = 'COL-COLOR'
		self.robot.color_sensor_r.mode = 'COL-COLOR'
		if colors[self.robot.color_sensor_l.value()] == 'red' and colors[self.robot.color_sensor_l.value()] == 'red':
			raise Exception("INSIDE_TAKING_FIELD")
		self.robot.color_sensor_l.mode= 'COL-REFLECT'
		self.robot.color_sensor_r.mode = 'COL-REFLECT'
	

class StateInsideTakingField(RobotState):
	def __init__(self, robot):
		super().__init__(robot)
		self.licznik = 100
	
	def handle(self):
		""" Podjedz pod klocek podnieś lopatke obroc sie 180 i pojedz do lini """
		while self.robot.infrared_sensor.value() < 5:
			self.robot.motor_l.run_forever(speed_sp=100)
			self.robot.motor_r.run_forever(speed_sp=100)
		self.robot.medium_motor.run_timed(time_sp=2000, speed_sp=-750)
		sleep(0.5)
		for i in range(self.licznik):
			self.robot.motor_l.run_forever(speed_sp=300)
			self.robot.motor_r.run_forever(speed_sp=-300)

		pass
	


state_map = {
	"LINE_FOLLOWER": StateLineFollower,
	"TAKING_LINE_FOLLOWER": StateFindTakingLineFollower,
	"INSIDE_TAKING_FIELD": StateInsideTakingField,
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
	
	def handle(self):
		try:
			self.state.handle()
		except Exception as e:
			for i in range(10):
				print(e)
			self.state = state_map[e](self)

	def obrot_polpelny(self):
		pass






