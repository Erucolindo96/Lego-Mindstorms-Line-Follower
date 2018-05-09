#!/usr/bin/env python3
from datetime import datetime

MAX_INTEGRAL = 70

'''
class PID:
	def __init__(self, Kp, Ki, Kd):
		self.Kp = Kp
		self.Ki = Ki
		self.Kd = Kd
		self.integral = 0
		self.error_prior = 0
		self.desired_value = 0
		self.last_time = datetime.now().timestamp()

	def get_regulation(self, act_val):
		actual_time = datetime.now().timestamp()
		iteration_time = actual_time - self.last_time
		self.last_time = actual_time
		error = act_val - self.desired_value
		self.integral = self.integral + error*iteration_time
		if self.integral > MAX_INTEGRAL:
			self.integral = self.integral/2
		#if self.integral > MAX_INTEGRAL:
		#	self.integral = 0;		
		derivative = (error-self.error_prior)/iteration_time
		regulation = self.Kp*error + self.Ki*self.integral + self.Kd*derivative
		self.error_prior = error
		return regulation

'''


class PID:
	def __init__(self, Kp, Ki, Kd):
		self.Kp = Kp
		self.Ki = Ki
		self.Kd = Kd
		self.integral = 0
		self.error_prior = []
		self.error_cnt = 0
		self.desired_value = 0
		self.last_time = datetime.now().timestamp()

	def get_regulation(self, act_val):
		actual_time = datetime.now().timestamp()
		iteration_time = actual_time - self.last_time
		self.last_time = actual_time
		error = act_val - self.desired_value

		if self.error_cnt >= MAX_INTEGRAL:
			#odejmij od calki najstarszy blad w tablicy, bo bedziemy go wywalac pozniej
			self.integral -= self.error_prior[0]*iteration_time
  					
		self.integral+=error*iteration_time
		print("Integral:{} ".format(self.integral))
		#zapis aktualnego bledu do pamietanych bledow		
		if self.error_cnt >= MAX_INTEGRAL:
			#wywalamy zerowy element i na koniec wstawiamy nowy
			self.error_prior = self.error_prior[1:]
			self.error_prior.append(error)
		else:
			#po prostu dodaj na koniec nowy element i zwieksz ilosc elementow
			self.error_prior.append(error)
			++self.error_cnt

		derivative = (error-self.error_prior[self.error_cnt-1] )/iteration_time
		regulation = self.Kp*error + self.Ki*self.integral + self.Kd*derivative
		#self.error_prior = error
		return regulation

