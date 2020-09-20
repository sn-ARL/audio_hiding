import soundfile as sf
import numpy as np
from appraisal import *
import matplotlib.pyplot as plt


def string_to_bits(string):
    res = ''
    for sym in string:
        bits = str(bin(ord(sym))[2:])
        res += '0'*(14-len(bits))+bits
    return res

def bits_to_string(bits):
    string =''
    for i in range(len(bits)//14):
        sym = bits[i*14:(i+1)*14]
        string += chr(int(sym,2))
    return string

def graph(msg, psp):
    msg = list(msg)
    pspAll = list()
    l = len(psp)
    for i in range(len(msg)):
	    pspAll[i*l: (i+1)*l] = psp

    psp_msg = pspAll.copy()
    psp_msg = np.array(psp_msg)
    for i in range(len(msg)):
	    if msg[i] == '0':
		    psp_msg[i*l:(i+1)*l] = psp_msg[i*l:(i+1)*l]*-1
    
    plt.subplot (3, 1, 1)
    plt.plot(abs(np.fft.fft(msg)))  #???
    plt.xlabel("Частота, Гц")
    plt.ylabel("Энергия сигнала \n отн. ед.")
    plt.subplot (3, 1, 2)
    plt.plot(abs(np.fft.fftfreq(len(pspAll), 1/44100)), abs(np.fft.fft(pspAll)))
    plt.xlabel("Частота, Гц")
    plt.ylabel("Энергия сигнала \n отн. ед.")
    plt.subplot (3, 1, 3)
    plt.plot(abs(np.fft.fftfreq(len(pspAll), 1/44100)), abs(np.fft.fft(psp_msg)))
    plt.xlabel("Частота, Гц")
    plt.ylabel("Энергия сигнала \n отн. ед.")
    plt.show()
    return None

def stegAudio(wav_path, text_path):
    stg_path = wav_path + '_stg.wav'
    data, samplerate = sf.read(wav_path)    #прочитали аудиофайл
    file = open(text_path, 'r', encoding='utf-8')             #прочитали текст
    text = file.read()

    a = len(data)                           #число отсчётов
    #print(a)
    bits = string_to_bits(text)             #получаю битовую последовательность текста
    #print(bits)
    n = int(a/len(bits))                    #число отсчетов на 1 бит информации
    
    if n == 0:                              #проверяем хватает ли места в аудиофайле
        print('маловато будет...')
        return None
    
    np.random.seed(seed)
    psp = np.random.choice([-0.0005,0.0005], n)  #ПСП
    #print(len(psp))
    graph(bits, psp)

    temp_data = data.copy()
    for i,b in enumerate(bits):
        if b == '0':
            temp = psp * (-1)
        else:
            temp = psp
        data_N = np.array(data[i*n:(i+1)*n])
        temp_data[i*n:(i+1)*n] = data_N + (temp*(data_N+2))

    sf.write(stg_path, temp_data, samplerate)      #записали файл с сообщением

    data_stg, useless = sf.read(stg_path)   #прочитали аудиофайл
    
    #print('Информационная последовательность: ',text[:60])
    #print('Битовая последовательность: ',bits[:60*14])
    #print(data[:60])
    #print(psp)

    msg_bits = ''
    for i in range(len(bits)):
        temp1 = np.array(data[i*n:(i+1)*n])
        temp2 = np.array(data_stg[i*n:(i+1)*n])
        res = (temp1-temp2)/(temp1+2)
        if (res[0] > 0 and psp[0]>0) or (res[0] <0 and psp[0] < 0):
            msg_bits+='0'
        else:
            msg_bits+='1'

    plt.subplot (4, 1, 1)
    plt.plot(data[:n*5])
    plt.ylabel("Сигнал \n переносчик")
    plt.subplot (4, 1, 2)
    psp1 = list()
    type(psp)
    for k in range(5):
        if bits[k] == '0':
            psp1[k*n: (1+k)*n] = psp
        else:
            psp1[k*n: (1+k)*n] = psp*-1
    plt.plot(psp1[:5*n])
    plt.ylabel("ПСП")
    plt.subplot (4, 1, 3)
    plt.plot(list(bits)[:5])
    plt.ylabel("Код")
    plt.subplot (4, 1, 4)
    plt.plot(data_stg[:5*n])
    plt.ylabel("Закодированный \n сигнал")
    plt.show()

    #print('Сигнал переносчик:\n',data[:40])
    #print('ПСП:\n',psp)
    #print('Код:\n',bits[:80])
    #print('Закодированный сигнал:\n',data_stg[:40])
    return bits_to_string(msg_bits)



wav_path = 'mono_mus.wav'
text_path ='msg.txt'
#wav_path = 'test.wav'
seed = 151
stg_path = wav_path + '_stg.wav'

print(stegAudio(wav_path, text_path))
print('MSE: ', round(MSE(wav_path, stg_path)*100,5), '%')
print('NMSE: ', round(NMSE(wav_path, stg_path)*100,5), '%')
#print('PSNR: ', round(PSNR(wav_path, stg_path),2), 'dB')
