import numpy as np
import matplotlib.pyplot as plt
#Set iteration number
maxIter = 300

delta = .001 ## 100 micrometer precision

lenX = .120 # range we are looking at (120 mm)
R = .08 ## mm (2/3 the size of the range you are looking at)
range_x = np.arange(0, lenX, delta)
lenY = R/8.0 ## the distance between your plates
range_y = np.arange(-lenY, 0, delta)

#fopt = 2 - (2*np.pi)/float(len(range_x))

#BCs
#Ttop = 50  ## insert gaussian beam profile for IFO beam heating (right now it is just a delta function BC)
V = 25.0 ## Voltage applied to plates
Ttop = V
Tbottom = -1.0*V
Tleft = 0
Tright = 0

# Initial guess of what the temperature of inside will be
Tguess = 0

#Set interpolation and colormap
colorinterp = 100
colormap = plt.cm.coolwarm

#Set meshgrid
X, Y = np.meshgrid(range_x, range_y)


T = np.empty((len(range_y), len(range_x)))
T.fill(Tguess)

T.shape
#Set BC
## Plates are finite, establish size
rad_plate = len(range_x)

T[(len(range_y)-1):,int(round((len(range_x)*(1.0/6.0)))):int(round((len(range_x)*(5.0/6.0))))+1] = Ttop
T[:1, int(round((len(range_x)*(1.0/6.0)))):int(round((len(range_x)*(5.0/6.0))))+1] = Tbottom
T[:, (len(range_x)-1):] = Tright
T[:, :1] = Tleft

##Making holes in plates
first_half = int(round((1.0/2.0-1.0/30.0)*len(range_x)))+1
second_half = int(round((1.0/2.0+1.0/30.0)*len(range_x)))

first_half
second_half

T[(len(range_y)-1):,first_half:second_half] = 0
T[:1, first_half:second_half] = 0

# Iteration
print("Please wait for a moment")
for iter in range(0, maxIter):
	for i in range(1, len(range_y)-1):
		for j in range(1, len(range_x)-1):
			#T[i,j] = (1-fopt) * T[i,j] + fopt*.25*(T[i+1][j] + T[i-1][j] + T[i][j+1]+ T[i][j-1])
			T[i,j] = .25*(T[i+1][j] + T[i-1][j] + T[i][j+1]+ T[i][j-1])

print("Iteration finished")
np.size(T[0])
T.shape
X.shape
Y.shape
#Set contour
figure = plt.figure(figsize=(30,10))
plt.contourf(X,Y,T, colorinterp, cmap=colormap)
plt.title("Contour of Electric Potential", fontsize=20)
#Set Colorbar
plt.colorbar()
#Show the result in the plot winow
plt.show()
print("")

## Electric field calculation via finite differences
E_U = np.empty((len(range_y),len(range_x)))
E_V = np.empty((len(range_y),len(range_x)))

E_U, E_V = np.gradient(T, delta)

fig, ax = plt.subplots()
q = ax.quiver(range_x, range_y, E_V, E_U, units='xy', pivot='mid')
fig.set_size_inches(100,10)
plt.show()

E_U[len(range_y)/2,len(range_x)/2]
E_U[len(range_y)/2,len(range_x)/2+10]
E_U[len(range_y)/2,len(range_x)/2-1]

## Some comments:
## The plots never seem to come out the same consistently which makes me think there is some sort of humerical errors here.
## First thing is to catch this in my calculation of what I think is the electric field
