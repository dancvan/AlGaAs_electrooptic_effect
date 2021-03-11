import numpy as np
import time
import h5py

## Setting Boundary conditions for each split electrode with unique central hole sizes

delta = .0001 ## 100 micrometer precision

lenX = .120 # range we are looking at (120 mm)
range_x = np.arange(0, lenX, delta)
lenZ = .0508/2.0 ## the distance between your plates
range_z = np.arange(-lenZ/2, lenZ/2, delta)

hole_radii = 1.5e-3

small_plate_rad = 12e-3

largest_plate_rad = 56e-3

rad_plate = np.arange(small_plate_rad,largest_plate_rad,2e-3)

fopt = 2 - (2*np.pi)/float(len(range_z))

#BCs
#Ttop = 50  ## insert gaussian beam profile for IFO beam heating (right now it is just a delta function BC)
V_o = 25.0 ## Voltage applied to plates
Utop = V_o
Ubottom = -1.0*V_o
Uleft = 0
Uright = 0

# Initial guess of what the temperature of inside will be
Uguess = 0

#Set meshgrid
X, Z = np.meshgrid(range_x, range_z)

U = np.empty((len(range_z), len(range_x), len(rad_plate)))
U_before = np.empty((len(range_z), len(range_x), len(rad_plate)))
U.fill(Uguess)

#Set BC
## Plates are finite, establish size

U[:, (len(range_x)-1):, :] = Uright
U[:, :1,:] = Uleft

for k in np.arange(0,len(rad_plate)):

    near_side = int(round((1.0/2.0*len(range_x)- rad_plate[k]/delta)))
    far_side = int(round((1.0/2.0*len(range_x)+ rad_plate[k]/delta)))

    U[(len(range_z)-1):,near_side:far_side,k] = Utop
    U[:1, near_side:far_side,k] = Ubottom

##Making holes in plates
first_half = int(round((1.0/2.0*len(range_x)- hole_radii/delta)))
second_half = int(round((1.0/2.0*len(range_x)+ hole_radii/delta)))

U[(len(range_z)-1):,first_half:second_half,:] = 0
U[:1, first_half:second_half,:] = 0

start = time.time()

for k in np.arange(0,len(rad_plate)):
    # Iteration
    print("Please wait for a moment")
    conv = 3
    count = 0
    while conv > 2:
        conv = np.sum(np.abs(U[:,:,k]-U_before[:,:,k]))
        print(conv)
        U_before[:,:, k] = U[:,:, k]
        for j in range(1, len(range_x)-1):
            for i in range(1, len(range_z)-1):
                U[i, j, k] = (1-fopt) * U[i, j, k] + fopt*.25*(U[i+1][j][k] + U[i-1][j][k] + U[i][j+1][k]+ U[i][j-1][k])

        for j in range(1, len(range_x)-1)[::-1]:
            for i in range(1, len(range_z)-1)[::-1]:
                U[i, j, k] = (1-fopt) * U[i, j, k] + fopt*.25*(U[i+1][j][k] + U[i-1][j][k] + U[i][j+1][k]+ U[i][j-1][k])
                #T[i,j] = .25*(T[i+1][j] + T[i-1][j] + T[i][j+1]+ T[i][j-1])
        count += 1

elapsed = time.time() - start

print("Iteration finished after {} iterations and took {} seconds".format(count, elapsed))


file = h5py.File('data/split_electrode/numerical_split_electrode_test_vary_disk_radii.h5'.format(count), 'w')
file.create_dataset('X', data=X)
file.create_dataset('Z', data=Z)
file.create_dataset('V_o', data=V_o)
file.create_dataset('lenX', data= lenX)
file.create_dataset('lenZ', data=lenZ)
file.create_dataset('potential', data=U)
file.create_dataset('delta', data=delta)
file.create_dataset('disk_radii',data=rad_plate )
file.create_dataset('hole_radii', data=hole_radii)
file.create_dataset('time_elapsed', data=elapsed)
file.create_dataset('disk_separation',data=lenZ)
file.close()
