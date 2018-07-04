from pylsl import StreamInfo, StreamInlet, StreamOutlet, LostError, resolve_byprop
import muselsl
import datetime
import time
import simpleaudio as sa
import winsound
import csv
from subprocess import *

#wave_obj = sa.WaveObject.from_wave_file("100Hz_44100Hz_16bit_30sec.wav")

events = [[time.time(), 'start']]

print('Turn on your Muse and hook up your computer audio jack to the Muse USB port. Ensure system sound is set to full and outputting to the correct port.')
address = input('Enter the address of your Muse: ')
backend = input("Enter the muselsl backend you want to use: Type bgapi, or bluemuse: ")

Popen('muselsl stream --address {0} --backend {1}'.format(address, backend), creationflags=CREATE_NEW_CONSOLE)
print('Stream will begin, wait for viewer to show data...')
Popen('muselsl view', creationflags=CREATE_NEW_CONSOLE)

start = input("-- When data is stable on all channels press enter to begin test (takes 30 seconds). --")

Popen('muselsl record', stdin=PIPE, creationflags=CREATE_NEW_CONSOLE)
time.sleep(5)
for i in range(5):
    events.append([time.time(), 'high voltage'])
    winsound.Beep(1000, 2500)
    events.append([time.time(), 'low voltage'])
    time.sleep(2.50)


fileTime = datetime.datetime.now().strftime('%Y-%m-%d-%H.%M.%S')
with open('events_' + fileTime + '.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',',
                                quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(['timestamp', 'event'])
        for data in events:
            writer.writerow(data)
print('Done.')

