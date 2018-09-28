# Statics

def cross_product(row_1, row_2, row_3=False):
	import numpy as np

	row_1 = np.array(row_1).transpose()
	row_2 = np.array(row_2).transpose()
	if row_3:
		row_3 = np.array(row_3).transpose()

		product = np.cross(row_2,row_3)
		product = np.dot(row_1, product)

	else:
		product= np.cross(row_1,row_2)

	return product

def position_vector(initial, terminal):
	import numpy as np
	i = np.array(initial)
	t = np.array(terminal)

	r = t - i
	return r

def vector_magnitude(vector):
	import math
	total = 0
		for index in vector:
			total += index**2
	return math.sqrt(total)

def unit_vector(input_vector):
	import numpy as np
	import math
	print(type(input_vector))
	if type(input_vector) == list:
		print('unit vector: chaning to numpy')
		input_vector = np.array(input_vector)

	u = input_vector / vector_magnitude(input_vector)

	return u

def axis_moment(axis_start=False, axis_end=False, force_vector=False, axis_unit_vector=False, F_start=False, F_end=False, F_mag=False, F_unit):
	import numpy as np
	if axis_start and axis_end:
		axis_unit_vector = unit_vector(position_vector(axis_start,axis_end))
	if F_start and F_end and F_mag:
		# this should probably be a numpy array i think
		force_vector = F_mag * unit_vector(position_vector(F_start, F_end))
	if F_mag and F_unit:
		if type(F_unit) == list:
			F_unit = np.array(F_unit)
		force_vector = F_unit * F_mag

	