# Statics
import numpy as np
import click
'''
#########################################
TO DO LIST

- add all encompassing features to resolve_force()
	- this stream lines all other processes
- add the simplify system method to 
- add systems of eq solver

'''
@click.group()
def cli():
	pass

class Resultant_System():
	def __init__(self, dim, origin=(0,0,0)):
		self.dim = dim
		self.forces = np.zeros(int(dim))
		self.moments = 0
		self.moment_origin = origin
	def add_force(self, F_vector, F_start=False):

		self.forces += F_vector

		# automatically add the force to the moments
		if F_start and self.dim == 3:
			# self.add_moment(d3_moment(F_vector=F_vector, F_start=F_start , position_start=self.moment_origin))
			self.moments += d3_moment(F_vector=F_vector, F_start=F_start, position_start=self.moment_origin)
		elif F_start and self.dim == 2:
			self.moments += d2_moment(about_point=self.moment_origin, F_vector=F_vector)

	def add_moment(self, F_vector=False, F_start=False, F_end=False, F_mag=False, F_unit=False, position_start=False, position_end=False, r_vector=False):
		#this add moment assumes that ccw is the positive direciton
		if position_start and not position_end and F_start:
			position_end = F_start
		if self.dim == 3:
			moment = d3_moment(F_vector, F_start, F_end, F_mag, F_unit, self.moment_origin, position_end, r_vector)
		if self.dim == 2:
			moment = d2_moment(about_point = self.moment_origin, F_start = F_start, F_end = F_end, F_vector = F_vector, F_mag = F_mag, dir = 'ccw')


		self.moments += moment

	def resultant_force(self):
		print ('the resultant force of the system is: %s with a magnitude of %s' % (self.forces, vector_magnitude(self.forces)))
        # more calculatios must be added
	def resultant_moment(self):
		print ('the resultant ccw moment of the system is %s about the point %s' % (self.moments, self.moment_origin))
        # more calculations must be added
	def simplify_system(self):
		pass

def type_changer(input, desired):
	t = type(input)
	#print('in type changer:\nInput is ==%s==\nType of input:%s\nDesired Output: %s\n\n' % (input, t, desired))

	if t == bool:
		return input

	if t != desired:
		if t == str and desired == list:
			output = [int(i) for i in input.split(',')]
		elif t == str and desired == int:
			return int(input)
		elif t == list and desired == np.ndarray:
			 return np.array(input)

		elif t == str and desired == np.ndarray:
			output = np.array([int(i) for i in input.split(',')])
		elif t == tuple and desired == np.ndarray:
			return np.array(input)
		return output
	else:
		return input


@cli.command()
@click.option('--t', help='The angle that would make the x component of force related to cosine')
@click.option('--mag', help='the magnitude of the vector')
@click.argument('xsign',default= 1)
@click.argument('ysign', default=1)
@click.argument('dim', default=2)
def resolve(t, mag, xsign=1, ysign=1, dim=2):
	click.echo(resolve_force(t, mag, xsign, ysign, dim))

def resolve_force(interior_angle, magnitude, xsign=1, ysign=1, dim=2):
	print ('int angle')
	interior_angle = type_changer(interior_angle, int)
	print('magnitude')
	magnitude = type_changer(magnitude, int)
	xsign = type_changer(xsign, int)
	ysign = type_changer(ysign, int)
	dim = type_changer(dim, int)

	from math import sin,cos
	if dim == 2:
		x = cos(interior_angle) * magnitude * xsign
		y = sin(interior_angle) * magnitude * ysign

		return np.array([x,y])
	else:
		print ('resolve force: 3d has not yet been configured')


@cli.command()
@click.argument('r1')
@click.argument('r2')
@click.argument('r3', default=False)
def cross(r1, r2, r3):
	click.echo(cross_product(r1,r2,r3))

def cross_product(row_1, row_2, row_3=False):
	row_1 = type_changer(row_1, np.ndarray).transpose()
	row_2 = type_changer(row_2, np.ndarray).transpose()


	if row_3:
		row_3 = type_changer(row_3, np.ndarray).transpose()

		product = np.cross(row_2, row_3)
		product = np.dot(row_1, product)

	else:
		product = np.cross(row_1, row_2)
	# returns numpy array
	return product


@cli.command()
@click.argument('i')#, help = 'the starting point for teh position vector')
@click.argument('t')#, help = 'the end point for the position vector')
def rvec(i, t):
	click.echo(position_vector(i,t))

def position_vector(initial, terminal):
	# change any potential input into a numpy array (string / list possible)
	i = type_changer(initial, np.ndarray)
	t = type_changer(terminal, np.ndarray)

	r = t - i

	#print('in posiiton vector: the initial term is %s (%s) and the final term is %s (%s), the result vecto is %s'% (initial, i, terminal, t, r))
	# returns a numpy array
	return r


@cli.command()
@click.argument('r1')
@click.argument('r2')
def dot(r1, r2):
	click.echo(dot_product(r1, r2))

def dot_product(row1,row2):
	row1 = type_changer(row1, np.ndarray)
	row2 = type_changer(row2, np.ndarray)

	dot = np.dot(row1, row2)
	return dot


@cli.command()
@click.argument('vec')
def mag(vec):
	click.echo(vector_magnitude(vec))

def vector_magnitude(vector):
	import math
	vector = type_changer(vector, np.ndarray)
	total = 0

	for index in vector:
		total += index ** 2

	# returns a constant
	result = math.sqrt(total)
	#print('in vector magnitude: the result is %s while the input was %s' % (result, vector))
	return result

@cli.command()
@click.argument('vec')
def unit(vec):
	click.echo(unit_vector(vec))

def unit_vector(input_vector):
	input_vector = type_changer(input_vector, np.ndarray)

	u = input_vector / vector_magnitude(input_vector)

	# returns a numpy array
	return u


@cli.command()
@click.option('--fvec', default=False, help='this is the force vector')
@click.option('--fs', default=False, help='starting point of the force vector')
@click.option('--fe', default=False, help='ending point of the force vector')
@click.option('--fmag', default=False, help='the magnitud of the vector')
@click.option('--funit', default=False, help='the magnitud of the vector')
@click.option('--rs', default=False, help='the starting point of the position vector from the point to the force')
@click.option('--re', default=False, help='the ending point ofthe position vector to  the point on the force')
@click.option('--rvec', default=False, help='the full position vector from the point to the force')
def d3tor(fvec, fs, fe, fmag, funit, rs, re, rvec):
	click.echo(d3_moment(fvec, fs, fe, fmag, funit, rs, re, rvec))

def d3_moment(F_vector=False, F_start=False, F_end=False, F_mag=False, F_unit=False, position_start=False, position_end=False, r_vector=False):
	#print('r vec is %s\n Force vector is %s' % (r_vector, F_vector))
	if F_start and not position_end:
		position_end = F_start
	elif position_end and not F_start:
		F_start = position_end

	r_vector = type_changer(r_vector, np.ndarray)
	F_vector = type_changer(F_vector, np.ndarray)

	#print('outside in d3 momet position start %s and position end is %s' % (position_start,position_end))

	if position_start and position_end:
		#print('||||| going to calculate the position vector, pos start %s pos_End %s' % (position_start,position_end))
		r_vector = position_vector(position_start, position_end)
		#print('result of opteration for position vector: ', r_vector)
	if F_start and F_end and F_mag:
		#print('|||||| calculating the force vector: F_start %s F_end %s adn F_mag %s' % (F_start, F_end, F_mag))
		# this should probably be a numpy array i think uuuuhhhh im not too sure though figure that shit out
		F_vector = F_mag * unit_vector(position_vector(F_start, F_end))
		#print(F_vector)
	if F_mag and F_unit:
		if type(F_unit) == list:
			F_unit = np.array(F_unit)
			F_vector = F_unit * F_mag

	if type(r_vector) != np.ndarray or type(F_vector) != np.ndarray:
		#print('moment arrays:\nvec:%s %s\nForce Vector:%s %s' % (r_vector, type(r_vector),F_vector, type(F_vector)))
		print('There was not enough information to calculate torque\n')
		return False


	moment = np.cross(r_vector.transpose(), F_vector.transpose())
	
	return moment


@cli.command()
@click.option('--point', default=[0,0,0], help='the point that the moment is being calculated around ')
@click.option('--fs', default=False, help='the start of the force vector')
@click.option('--fe', default=False, help='ending point of the force vector')
@click.option('--fvec', default=False, help='this is the force vector')
@click.option('--fmag', default=False, help='this is the force vector magnitude')
@click.option('--dir', default=False, help='the direction that the moment is being calculated in, default ccw')
def d2tor(point, fs, fe, fvec,fmag, dir):
	click.echo(d2_moment(point, fs, fe, fvec,fmag, dir))

def d2_moment(about_point=False, F_start=False, F_end=False, F_vector=False,F_mag=False, dir=False):
	about_point = type_changer(about_point,list)
	F_start = type_changer(F_start, list)
	F_end = type_changer(F_end, int)
	F_vector = type_changer(F_vector, list)
	F_mag = type_changer(F_mag, int)

	if not F_vector:
		if F_start and F_end and F_mag:
			F_vector = unit_vector(position_vector(F_start,F_end)) * F_mag
		else:
			print('These is not enough infomation for a 2d moment calculation (F_Vector)')
			return False
	if type(F_vector) != np.array:
		F_vector = np.array(F_vector)
	if not about_point:
		print('These is not enough infomation for a 2d moment calculation (about point)')
		return False
	x_offset = F_start[0] - about_point[0]
	y_offset = F_start[1] - about_point[1]

	moment = (F_vector[0]*y_offset - F_vector[1]*x_offset) * -1

	if dir == 'ccw' or dir == False:
		pass
	elif dir =='cw':
		moment *= -1
	else:
		print('unknown value of dir. It should either be ccw or cw. It is assumed to be ccw')
	return moment

@cli.command()
@click.option('--a_s', default=False, help = 'the starting point of the axis of rotation')
@click.option('--a_e', default=False, help = 'the ending point of the axis of rotation')
@click.option('--aunit', default=False, help = 'the unit vecotr for the axis of rotaiton')
@click.option('--fvec', default=False, help = 'the force vector that is being used for the calculation')
@click.option('--fs', default=False, help = 'the starting point of the force vector being used')
@click.option('--fe', default=False, help = 'the ending point of the force vector being used')
@click.option('--fmag', default=False, help = 'the magnitude of the force vector')
@click.option('--funit', default=False, help = 'the unit vector of the force')
@click.option('--rs', default=False, help = 'the starting point of the position vector(on the axis)')
@click.option('--re', default=False, help = 'the ending point ofhte position vector(on the force)')
@click.option('--rvec', default=False, help = 'the position vector (from the axis to the force)')
def axis(a_s, a_e, aunit ,fvec, fs, fe, fmag, funit, rs, re, rvec):
	click.echo(axis_moment(a_s, a_e, aunit ,fvec, fs, fe, fmag, funit, rs, re, rvec))

def axis_moment(axis_start=False, axis_end=False, axis_unit_vector=False,F_vector=False, F_start=False, F_end=False, F_mag=False, F_unit=False, position_start=False, position_end=False, r_vector=False):
	axis_start = type_changer(axis_start, list)
	axis_end = type_changer(axis_end, list)
	axis_unit_vector = type_changer(axis_unit_vector, list)
	F_vector = type_changer(F_vector, list)
	F_start = type_changer(F_start, list)
	F_end = type_changer(F_end, list)
	F_mag = type_changer(F_mag, int)
	F_unit = type_changer(F_unit, list)
	position_start = type_changer(position_start, list)
	position_end = type_changer(position_end, list)
	r_vector = type_changer(r_vector, list)

	if not axis_unit_vector:
		if axis_start and axis_end:
			#print('about to find the axis unit vector in axis moment: axis_start: %s axis_end %s' % (axis_start, axis_end))
			axis_unit_vector = unit_vector(position_vector(axis_start, axis_end))
		else:
			#print('there is not enough information for this axis moment problem')
			return False
	# this code block ensures that we extrapolate the input data enough to calculate a position vector 
	if not position_start:
		if axis_start:
			position_start = axis_start
		elif axis_end:
			position_start = axis_end
	if not position_end:
		if F_start:
			position_end = F_start
		elif F_end:
			position_end = F_end
	#print('about to start the moment calculation, position start %s position end %s' % (position_start, position_end))

	moment = d3_moment(F_vector, F_start, F_end, F_mag, F_unit, position_start, position_end, r_vector)

	result_axis_moment = np.dot(axis_unit_vector, moment)

	return result_axis_moment
@cli.command()
@click.option('--fvec', default=False, help ='the force vector being used')
@click.option('--fs', default=False, help =' the starting point of the force vector')
@click.option('--fe', default=False, help ='the ending point of the force vector')
@click.option('--negfs', default=False, help ='the starting point of the negative force vector')
@click.option('--fmag', default=False, help ='the magnitude of the force vector')
@click.option('--rvec', default=False, help ='the position vector (from -F to +F)')
@click.option('--funit', default=False, help ='the unit vector of the force being used')
def d3couple(fvec, fs, fe, negfs,fmag, rvec, funit):
	click.echo(d3_couple_moment(fvec, fs, fe, negfs,fmag, rvec, funit))

def d3_couple_moment(F_vector=False, F_start=False, F_end=False, neg_F_start=False,F_mag=False, r_vector=False, F_unit=False):
	if type(r_vector) == list:
		r_vector = np.array(r_vector)
	if type(F_vector) == list:
		F_vector = np.array(F_vector)
	if F_start and neg_F_start:
		r_vector = position_vector(neg_F_start, F_start)
	if F_unit and F_mag:
		F_vector = F_mag * np.array(F_unit)
	if F_start and F_end:
		F_vector = F_mag * unit_vector(position_vector(F_start,F_end))
	if not r_vector.any() or not F_vector.any():
		print('type of array \nr vec:%s\nForce Vector:%s' % (r_vector, F_vector))
		print('there was an error in d3 couple moment, not enough info')
		return False
	moment = np.cross(r_vector, F_vector)
	return moment


@cli.command()
@click.argument('d')
@click.argument('fmag')
def d2couple(d,fmag):
	click.echo(d2_couple_moment(d,fmag))

def d2_couple_moment(d=False, F_mag=False):
	if not d and not F_mag:
		print('there is not enough intomation to slove the 2d couple moment')
		return False
	moment = d*F_mag
	return moment

if __name__ =='__main__':
	cli()
