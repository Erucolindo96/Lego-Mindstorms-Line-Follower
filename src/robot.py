#!/usr/bin/env python3
from ev3dev.ev3 import *
import pid 
from math import *
from time import sleep

MAX_SPEED = 1000
MIN_SPEED = -200
REGULATION_FACTOR = 2

class Robot:
	def __init__(self, left_motor_port ,right_motor_port, left_color_port, right_color_port, def_speed):
		self.motor_l = LargeMotor(left_motor_port)
		self.motor_r = LargeMotor(right_motor_port)

		self.color_sensor_l = ColorSensor(left_color_port)
		self.color_sensor_l.mode = 'COL-REFLECT'
		assert self.color_sensor_l.connected, "Connect a color sensor to any sensor port"

		self.color_sensor_r = ColorSensor(right_color_port)
		self.color_sensor_r.mode = 'COL-REFLECT'
		assert self.color_sensor_r.connected, "Connect a color sensor to any sensor port"

		self.def_speed = def_speed
		assert self.def_speed <= MAX_SPEED, "Speed too much" 

		self.color_l = 0
		self.color_r = 0
		self.actual_regulation = 0
		T_crit = 1.7
		K_crit = 5.5
		self.pid_ = pid.PID(0.6*K_crit, 0.2*T_crit, 0.7*T_crit)
		#self.pid_ = pid.PID(K_crit, 0, 0)

	def read_colors(self):
		self.color_l = self.color_sensor_l.value()
		self.color_r = self.color_sensor_r.value()
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
			return {'wew_silnik' : self.motor_r, 'zew_silnik': self.motor_l}
		else:
			return {'wew_silnik' : self.motor_l, 'zew_silnik': self.motor_r}
			
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

	def check_the_color(color_sensor):
		colors=('unknown','black','blue','green','yellow','red','white','brown')
		self.color_sensor_l.mode = 'COL-COLOR'
		self.color_sensor_r.mode = 'COL-COLOR'
		color_sensor.mode='COL-REFLECT'
	

