import numpy as np
from scipy.special import sph_harm
import math
import argparse

import argparse
parser = argparse.ArgumentParser(description='Render a Gaussian random Bergman metric of degree N on the round sphere.')
parser.add_argument('N', action="store", type=int, help="degree")
parser.add_argument('-e', action="store_true", default=False, help="use eigenfunctions of degree exactly N")
parser.add_argument('-o', action="store_true", default=False, help="use an orthonormal basis")
parser.add_argument('-c', action="store_true", default=False, help="calculate only, do not render")
# TODO: mesh resolution paramater
args = parser.parse_args()

N = args.N
if (args.e):
	M=N
else:
	M=1

d = (N+M+1)*(N-M+1) #N*N+2*N #total dimension d_N
# create spherical coordinate mesh
pi = np.pi
cos = np.cos
sin = np.sin
res = 201j # mesh resolution
phi, theta = np.mgrid[0:pi:res*1j, 0:2*pi:res*1j]

print "Calculating harmonics..."
# calculate the standard (real) spherical harmonics
Y = []
for l in range(M,N+1):
	print (l, 0)
	Y.append(sph_harm(0,l,theta,phi).real)
	for m in range(1,l+1):
		print (l, m)
		a = sph_harm(m,l,theta,phi)
		Y.append(math.sqrt(2)*a.real)
		Y.append(math.sqrt(2)*a.imag)

# if rendering
if not args.c:
	# take Z be a gaussian random combination
	print 'Sampling...'
	if args.o:
		x = [Y[i] for i in range(3) ]
	else:
		x = [ sum([ np.random.normal()*Y[j] for j in range(d) ]) for i in range(3) ]
	

	print "Rendering..."
	from mayavi import mlab
	s = mlab.mesh(x[0],x[1],x[2])
	mlab.show()






