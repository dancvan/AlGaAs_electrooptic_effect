import numpy as np
import matplotlib.pyplot as plt

delta = .001
## Set x and y range
lenX = .120 # range we are looking at (120 mm)
R = .08 ## mm (2/3 the size of the range you are looking at)
range_x = np.arange(0, lenX, delta)
lenY = R/8.0 ## the distance between your plates
range_y = np.arange(-lenY/2, lenY/2, delta)

#Set meshgrid
X, Y = np.meshgrid(range_x, range_y)
V_o = 25.0 ## Voltage applied to plates

def griff_anal(X,Y,V_o, diam,d,n):
    term_1 = (4.0*V_o)/np.pi
    term_2 = 0
    for i in range(1,n*2,2):
        term_2 += (np.cosh((float(i)*np.pi*Y)/diam)*np.sin((float(i)*np.pi*X)/diam))/(float(i)*np.cosh((float(i)*np.pi*d)/(2*diam)))

    return term_1*term_2

U_anal = griff_anal(X,Y,V_o,lenX, lenY,1000)

colorinterp = 1000
colormap = plt.cm.coolwarm
figure = plt.figure(figsize=(30,10))
plt.contourf(X,Y, U_anal, colorinterp, cmap=colormap)
plt.ylim((-.004,.004))
plt.title("Contour of Electric Potential", fontsize=20)
#Set Colorbar
plt.colorbar()


E_U = np.empty((len(range_y),len(range_x)))
E_V = np.empty((len(range_y),len(range_x)))

#grad_span = 1
skip = 10
E_U, E_V = np.gradient(U_anal, delta)

X_new = X
#Y_new = Y[grad_span:-grad_span,grad_span:-grad_span]
Y_new = Y
fig, ax = plt.subplots(figsize=(30, 10))
q = ax.quiver(X[::skip,::skip], Y[::skip,::skip], E_V[::skip,::skip], E_U[::skip,::skip], units='xy', pivot='mid', cmap='magma')
ax.set_aspect('equal')
plt.xlabel('x-coordinate [1mm dot separation]')
plt.ylabel('y-coordinate [1mm dot separation]')
plt.show()
