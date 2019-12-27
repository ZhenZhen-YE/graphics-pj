import numpy as np
from scipy.fftpack import fft
import scipy
import pygame
from scipy.io import wavfile as wav
import scipy.signal
import time


while(True):
    try:
        filename = input("Enter a file name: ")
        pygame.mixer.init()
        pygame.mixer.music.load(filename)
        rate, data = wav.read(filename)
        break
    except:
        print("Invalid Name, please try again or press ctrl+Z to exit.")

percentage_displayed_f = 0.7                              
max_height_percentile = 99.8
fftlength = 2048
entertainment = False

music = scipy.mean(data, axis=1)

f, t, Sxx = scipy.signal.spectrogram(music, rate,nperseg=fftlength)                                          
no_of_displayed_f = int(len(f)*percentage_displayed_f+0.5)
Sxx = Sxx[:no_of_displayed_f-2].transpose()
f = f[:no_of_displayed_f-2]


pygame.init()
screen = pygame.display.set_mode((1000, 500))
rect_scale_factor = 1000/scipy.percentile(Sxx, max_height_percentile)
done = False
dt= t[1] - t[0]


pygame.font.init()
myfont = pygame.font.SysFont('Arial', 15)
title = myfont.render(filename, False, (100, 200, 220))



colours = []
colour_f = 0.05     
for i in range(no_of_displayed_f):
    green   = scipy.sin(colour_f*i*2 + 0) * 63 + 64
    blue = scipy.sin(colour_f*i*2 + 20) * 127 + 128
    red  = scipy.sin(colour_f*i*2 + 40) * 127 + 128
    colours.append((red, green, blue))
 
start_time = time.time()


Sxx_len = len(Sxx)
rect_width = 1000/no_of_displayed_f
done = False

pygame.mixer.music.play()


while not done:
    try:
        cur_time = time.time() - start_time

        timer = myfont.render(str(int(cur_time)) + "s", False, (100, 200, 220))
        screen.blit(timer, (10, 500 - 60))
        screen.blit(title, (10, 500 - 30))

        main_time_index = int(cur_time // dt)

        for index, frequency in enumerate(Sxx[(main_time_index)]):
            proportion_of_tleft = main_time_index - (main_time_index)
            height = max(proportion_of_tleft*frequency + (1-proportion_of_tleft) * Sxx[(main_time_index) + 1][index],2 / rect_scale_factor)/2-80
            k = (index + 1) * rect_width
            pygame.draw.polygon(screen, colours[index],[(k, height-10), (k + 3, height), (k + 4, height+15), (k + 1, height+4),(k - 1, height-3)])

        pygame.display.flip()
        screen.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                pygame.mixer.music.stop()
                break

    except:
        pygame.display.quit()
        pygame.mixer.music.stop()
        break

