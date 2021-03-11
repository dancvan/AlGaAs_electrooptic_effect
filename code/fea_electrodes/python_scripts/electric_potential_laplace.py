import numpy as np
import matplotlib.pyplot as plt
#Set iteration number
maxIter = 2000

lenX = 100
range_x = np.arange(0, lenX)
lenY = 100
range_y = np.arange(-lenY, 0)
delta = 1


#BCs
#Ttop = 50  ## insert gaussian beam profile for IFO beam heating (right now it is just a delta function BC)
V = 10.0 ## Voltage applied to plates
Ttop = 10.0
Tbottom = -10.0
Tleft = 0
Tright = 0

# Initial guess of what the temperature of inside will be
Tguess = 0

#Set interpolation and colormap
colorinterp = 50
colormap = plt.cm.coolwarm

#Set meshgrid
X, Y = np.meshgrid(range_x, range_y)

T = np.empty((lenY, lenX))
T.fill(Tguess)

#Set BC
## Plates are finite, establish size
T[(lenY/4-1):,:] = Ttop
T[:1, :] = Tbottom
T[:, (lenX-1):] = Tright
T[:, :1] = Tleft


# Iteration
print("Please wait for a moment")
for iteration in range(0, maxIter):
	for i in range(1, lenY-1, delta):
		for j in range(1, lenX-1, delta):
			T[i,j] = 0.25 * (T[i+1][j] + T[i-1][j] + T[i][j+1]+ T[i][j-1])

print("Iteration finished")

#Set contour
figure = plt.figure(figsize=(17,10))
plt.contourf(X,Y,T, colorinterp, cmap=colormap)
plt.title("Contour of Electric Potential", fontsize=20)
#Set Colorbar
plt.colorbar()

#Show the result in the plot winow
plt.show()
print("")

## Electric field calculation via finite differences
E_U = np.empty((lenY,lenX))
E_V = np.empty((lenY,lenX))
for i in range(1, lenY-1, delta):
	for j in range(1, lenX-1, delta):
		E_U[i,j] = abs(T[i][j+1]-T[i][j]) - abs(T[i][j-1]-T[i][j])
        E_V[i,j] = abs(T[i+1][j]-T[i][j]) - abs(T[i-1][j]-T[i][j])

figure_quiv = plt.figure(figsize=(17,10))
plt.quiver(T, E_U, E_V, units='xy')
## additional code for V1
T_sum = np.sum(T, axis=0)
fig = plt.figure(figsize =(17,10))
plt.plot(range_x, T_sum, label='Temperature after numerical laplace (using Jacpbi method)')
plt.title('Temperature integration after Laplace')
plt.plot(range_x, Ttop, label = 'Temperature on the surface of the fused silica substrate')
plt.legend()
plt.show()
