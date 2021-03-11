import numpy as np
import time
import h5py
import matplotlib.pyplot as plt

## Setting Boundary conditions for each split electrode with unique central hole sizes

delta = 100e-6 ## 100 micrometer precision
large_sep = 50.4e-3
small_sep = 12.4e-3
lenX = 120e-3 # range we are looking at (120 mm)
range_x = np.arange(0, lenX, delta)
sep = np.arange(small_sep, large_sep, delta*10)
range_z_largest = np.arange(-sep[-1]/2, sep[-1]/2, delta)
U = np.empty((len(range_z_largest), len(range_x), len(sep)))


start = time.time()


for k in np.arange(0,len(sep)):

    lenZ = sep[k]  ## the distance between your plates

    range_z = np.arange(-lenZ/2, lenZ/2, delta)

    hole_radii = 1.5e-3

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

    ## Hole size is a fraction of the range you are looking at.. what is that fraction and what is that relative to the plate size?
    U_temp = np.empty((len(range_z), len(range_x)))
    U_before = np.empty((len(range_z), len(range_x)))
    U_temp.fill(Uguess)

    #Set BC
    ## Plates are finite, establish size
    rad_plate = 50.8e-3

    near_side = int(round((1.0/2.0*len(range_x)- rad_plate/delta)))
    far_side = int(round((1.0/2.0*len(range_x)+ rad_plate/delta)))

    U_temp[(len(range_z)-1):,near_side:far_side] = Utop
    U_temp[:1, near_side:far_side] = Ubottom
    U_temp[:, (len(range_x)-1):] = Uright
    U_temp[:, :1] = Uleft

    ##Making holes in plates
    first_half = int(round((1.0/2.0*len(range_x)- hole_radii/delta)))
    second_half = int(round((1.0/2.0*len(range_x)+ hole_radii/delta)))

    U_temp[(len(range_z)-1):,first_half:second_half] = 0
    U_temp[:1, first_half:second_half] = 0

    # Iteration
    print("Please wait for a moment")
    conv = 3
    count = 0
    while conv > 2:
        conv = np.sum(np.abs(U_temp[:,:]-U_before[:,:]))
        print(conv)
        U_before[:,:] = U_temp[:,:]
        for j in range(1, len(range_x)-1):
            for i in range(1, len(range_z)-1):
                U_temp[i, j] = (1-fopt) * U_temp[i, j] + fopt*.25*(U_temp[i+1][j] + U_temp[i-1][j] + U_temp[i][j+1]+ U_temp[i][j-1])

        for j in range(1, len(range_x)-1)[::-1]:
            for i in range(1, len(range_z)-1)[::-1]:
                U_temp[i, j] = (1-fopt) * U_temp[i, j] + fopt*.25*(U_temp[i+1][j] + U_temp[i-1][j] + U_temp[i][j+1] + U_temp[i][j-1])
                #T[i,j] = .25*(T[i+1][j] + T[i-1][j] + T[i][j+1]+ T[i][j-1])
        count += 1

    #Storing potential array in larger array
    U[(len(range_z_largest)-len(range_z))/2:(len(range_z_largest)+len(range_z))/2,:,k] = U_temp[:,:]

elapsed = time.time() - start



print("Iteration finished after {} iterations and took {} seconds".format(count, elapsed))




file = h5py.File('data/split_electrode/numerical_split_electrode_test_vary_sep_test.h5'.format(count), 'w')
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
file.create_dataset('disk_separation',data=sep)
file.close()
