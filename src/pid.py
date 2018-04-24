#!/usr/bin/env python3


class PID:
	MAX_INTEGRAL = 100
    iteration_time
    desired_value# Wartosc zadana
    Kp
    Ki
    Kd
    integral
    error_prior


	def __init__(self, Kp, Ki, Kd, it_time):
		self.Kp = Kp
		self.Ki = Ki
		self.Kd = Kd
		self.integral = 0
		self.error_prior = 0
		self.desired_value = 0
		self.iteration_time = it_time

	def getRegulation(self, act_val):
		error = act_val - self.desired_value
		self.integral = self.integral + error*self.iteration_time
		if self.integral > MAX_INTEGRAL
			self.integral = 0;		
		derivative = (error-self.error_prior)/self.iteration_time
		regulation = self.Kp*error + self.Ki*self.integral + self.Kd*derivative
		self.error_prior = error
		return regulation







