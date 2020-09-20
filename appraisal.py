import soundfile as sf
import math
import numpy as np
import matplotlib.pyplot as plt

def MSE(container_path, stego_path):
    data_con, useless = sf.read(container_path) 
    data_stg, useless = sf.read(stego_path) 

    mse = 0
    for i in range(len(data_con)):
        mse += (data_con[i] - data_stg[i])**2

    #print('MSE: ', round(mse/len(data_con)*100,5), '%')
    return mse/len(data_con)

def NMSE(container_path, stego_path):
    data_con,useless = sf.read(container_path) 
    data_stg, useless = sf.read(stego_path) 

    nmse_o = 0
    nmse_z = 0
    for i in range(len(data_con)):
        nmse_o += (data_con[i] - data_stg[i])**2
        nmse_z += data_con[i]**2

    #print('NMSE: ', round(nmse_o/nmse_z*100,5), '%')
    return nmse_o/nmse_z


def PSNR(container_path, stego_path):
    mse = MSE(container_path, stego_path)
    data_con = sf.read(container_path) 

    max = 0
    for i in range(len(data_con)):
        if max < data_con[0][i]**2:
            max = data_con[0][i]**2
    
    #print(10* math.log10(max/mse))
    return 10*math.log10(max/mse)

def psp_check(seed):
    np.random.seed(seed)
    psp = np.random.choice([0,1], 1000)
    zero = 0
    for elem in psp:
        if elem == 0:
            zero +=1
    one = 1000 - zero
    
    fig, ax = plt.subplots()
    ax.bar(['"0" '+str(zero),'"1" '+ str(one)], [zero, one])
    fig.set_figwidth(5)    
    fig.set_figheight(6)
    plt.show()

    return None

psp_check(151)

