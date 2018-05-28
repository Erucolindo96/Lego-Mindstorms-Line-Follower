#!/usr/bin/env python3
from ev3dev.ev3 import *
import pid 
from math import *
from time import sleep

MAX_SPEED = 1000
MIN_SPEED = -200
REGULATION_FACTOR = 2


'''

Podstawowe zalozenia:
    1. Sterowanie obliczane przez PID, jest proporcjonalne do zmiany RÓŻNICY prędkości silników - sterowanie zwiększa/zmniejsza wartość ich prędkości, aby odpowiednio zmodyfikować różnicę prędkości silników.
    
    2. Silniki mają domyślną prędkość - sterowanie polega na zwiększaniu/zmniejszaniu ich prędkości tak, aby uzyskać wymaganą przez obliczone sterowanie różnicę prędkości

    3. Algorytm oblicza, który silnik jest silnikiem wewnętrznym, i rozdziela sterowanie na a) spowolnienie silnika wewnętrznego tyle, ile się da (jest pewna minimalna prędkość, którą wewnętrzny silnik może uzyskać) b) zwiększenie prędkości silnika zewnętrznego (jeśli już więcej nie możemy zwalniać wewnetrznego, a pozostało nam jeszcze sterowanie do rozdzielenia)

'''
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

        '''
        Wykonuje pomiar i  zapisuje wartość jasności koloru pod czujnikami
        '''
	def read_colors(self):
		self.color_l = self.color_sensor_l.value()
		self.color_r = self.color_sensor_r.value()
		return (self.color_l, self.color_r)
	'''
        Oblicza wartość sterowania na podstawie wskazań czujników
        Zwraca wartość sterowania.
        '''
	def count_regulation(self):
		'''
		actual_regulation > 0 => lewy bardziej na bialym => lewy mocniej, prawy slabiej		
		'''
		self.actual_regulation = self.pid_.get_regulation(self.color_l - self.color_r) * REGULATION_FACTOR
		return self.actual_regulation 
	'''
        Podowuje, na podstawie wskazań PIDa, odpowiednie wysterowanie silników
        '''
	def drive_motors(self):
		regulation = self.actual_regulation
		silniki = self.get_engines_interpretation(regulation)
		wew_silnik = silniki['wew_silnik']
		zew_silnik = silniki['zew_silnik']

		regulation_abs = abs(regulation)
		ile_dla_zewnetrznego = 	self.get_regulation_after_slow_inner(regulation_abs )
		self.slow_inner_eng_to_min_velocity(wew_silnik, regulation_abs)
		zew_silnik.run_forever(speed_sp=self.speed_corection(self.def_speed+ile_dla_zewnetrznego))

		#left_motor.run_forever(speed_sp=left_speed)
		#right_motor.run_forever(speed_sp=right_speed)
	'''
        Funkcja zabezpieczająca przez zwiększeniem prędkości ponad maksymalną możliwą dla API silnika(1000)
        , oraz minimalną(osiągalną dla silnika wewnętrznego)
        '''
	@staticmethod
	def speed_corection(speed):
		if speed > MAX_SPEED:
			return MAX_SPEED
		elif speed < MIN_SPEED:
			return MIN_SPEED
		else:
			return speed
        '''
        Metoda zwraca słownik - referencje do wewnętrznego silnika, oraz zewnętrznego. 
        Dzięki temu słownikowi wiemy, który silnik jest wewnętrzny, a który zewnętrzny w danej chwili
        '''
	def get_engines_interpretation(self, regulation):
		if regulation < 0:
			return {'wew_silnik' : self.motor_r, 'zew_silnik': self.motor_l}
		else:
			return {'wew_silnik' : self.motor_l, 'zew_silnik': self.motor_r}
	'''
        Metoda zwraca, ile sterowania pozostanie do rozdzielenia po wysterowaniu wewnetrznego
        Jeżeli zwróci zero, to znaczy, że całe sterowanie zużyte zostanie na wysterowanie silnikiem wewnętrznym
        '''
	def get_regulation_after_slow_inner(self, reg_abs):
		if reg_abs > (self.def_speed - MIN_SPEED):
			return reg_abs - (self.def_speed - MIN_SPEED)
		return 0
        ''' 
        Metoda spowalnia wewnętrzny silnik o tyle, ile może. 
        Ogranicza ją z jednej strony wartość sterowania(spowalnia silnik co najwyżej o tyle),
        a z drugiej strony prędkość minimalna silnika wewnętrznego (nie może zejść poniżej tej wartości)
        #tego chyba nie ma
        Zwraca o ile należy przyspieszyć silnik zewnętrzny, aby "wykorzystać" całe dostępne sterowanie
        '''			
	def slow_inner_eng_to_min_velocity(self, wew_silnik, reg_abs):
		rest_of_regulation = self.get_regulation_after_slow_inner(reg_abs)
		#print('zostalo sterowania {}'.format(rest_of_regulation))
		if rest_of_regulation == 0: #sterujemy tylko wew silnik
			wew_silnik.run_forever(speed_sp=self.speed_corection(self.def_speed - reg_abs))
		else: #troche sterowania zostanie - musimy wysterowac tez zewnetrzny silnik
			wew_silnik.run_forever(speed_sp=self.speed_corection(MIN_SPEED))
		#return rest_of_regulation
        '''
        Metoda sprawdzająca wartość koloru pod czujnikiem - nieużywana w line followerze 
        '''
	def check_the_color(color_sensor):
		colors=('unknown','black','blue','green','yellow','red','white','brown')
		self.color_sensor_l.mode = 'COL-COLOR'
		self.color_sensor_r.mode = 'COL-COLOR'
		color_sensor.mode='COL-REFLECT'
	

