# Statics
import numpy as np
'''
#########################################
TO DO LIST

- add all encompassing features to resolve_force()
    - this stream lines all other processes
- add the simplify system method to 
- add systems of eq solver

'''



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
    def resultant_moment(self):
        print ('the resultant ccw moment of the system is %s about the point %s' % (self.moments, self.moment_origin))
    def simplify_system(self):
        pass



def resolve_force(interior_angle, magnitude, xsign=1, ysign=1, dim=2):
    from math import sin,cos
    if dim == 2:
        x = cos(interior_angle) * magnitude * xsign
        y = sin(interior_angle) * magnitude * ysign

        return np.array([x,y])
    else:
        print ('resolve force: 3d has not yet been configured')

def cross_product(row_1, row_2, row_3=False):
    row_1 = np.array(row_1).transpose()
    row_2 = np.array(row_2).transpose()
    if row_3:
        row_3 = np.array(row_3).transpose()

        product = np.cross(row_2, row_3)
        product = np.dot(row_1, product)

    else:
        product = np.cross(row_1, row_2)

    # returns numpy array
    return product


def position_vector(initial, terminal):
    i = np.array(initial)
    t = np.array(terminal)

    r = t - i
    
    # returns a numpy array
    return r
def dot_product(row1,row2):
    if type(row1) != np.ndarray:
        row1 = np.array(row1)
    if type(row2) != np.ndarray:
        row2 = np.array(row2)
    dot = np.dot(row1, row2)
    return dot

def vector_magnitude(vector):
    import math
    total = 0
    for index in vector:
        total += index ** 2

    # returns a constant
    return math.sqrt(total)


def unit_vector(input_vector):
    if type(input_vector) == list:
        print('unit vector: chaning to numpy')
        input_vector = np.array(input_vector)

    u = input_vector / vector_magnitude(input_vector)

    # returns a numpy array
    return u

def d3_moment(F_vector=False, F_start=False, F_end=False, F_mag=False, F_unit=False, position_start=False, position_end=False, r_vector=False):
    if F_start and not position_end:
        position_end = F_start
    elif position_end and not F_start:
        F_start = position_end


    if type(r_vector) == list:
        r_vector = np.array(r_vector)
    if type(F_vector) == list:
        F_vector = np.array(F_vector)


    if position_start and position_end:
        r_vector = position_vector(position_start, position_end)
    if F_start and F_end and F_mag:
        # this should probably be a numpy array i think
        F_vector = F_mag * unit_vector(position_vector(F_start, F_end))
    if F_mag and F_unit:
        if type(F_unit) == list:
            F_unit = np.array(F_unit)
            F_vector = F_unit * F_mag

    if type(r_vector) != np.ndarray or type(F_vector) != np.ndarray:
        print('moment arrays:\nvec:%s %s\nForce Vector:%s %s' % (r_vector, type(r_vector),F_vector, type(F_vector)))
        print('There was not enough information to calculate torque\n')
        return False


    moment = np.cross(r_vector.transpose(), F_vector.transpose())
    
    return moment

def d2_moment(about_point=False, F_start=False, F_end=False, F_vector=False,F_mag=False, dir=False):
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


def axis_moment(axis_start=False, axis_end=False, axis_unit_vector=False,F_vector=False, F_start=False, F_end=False, F_mag=False, F_unit=False, position_start=False, position_end=False, r_vector=False):
    if not axis_unit_vector:
        if axis_start and axis_end:
            axis_unit_vector = unit_vector(position_vector(axis_start, axis_end))
        else:
            print('there is not enough information for this axis moment problem')
            return False
    moment = d3_moment(F_vector, F_start, F_end, F_mag, F_unit, position_start, position_end, r_vector)

    result_axis_moment = np.dot(axis_unit_vector, moment)

    return result_axis_moment

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

def d2_couple_moment(d=False, F_mag=False):
    if not d and not F_mag:
        print('there is not enough intomation to slove the 2d couple moment')
        return False
    moment = d*F_mag
    return moment

if __name__ =='__main__':
    x = dot_product([1,2,2,],[3,3,1])
    print(x)
