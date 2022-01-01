#!/usr/bin/env python3

# MIDI Serial Bridge
# Receive MIDI via tty(serial), typically from USB serial adapter (FTDI, 
# microcontroller, etc.)
# For best results, use this at high baud rates.
#

import time
import serial
import argparse
import rtmidi
import jack

PORTNAME = 'MIDItty Serial to MIDI'

# get arguments
parser = argparse.ArgumentParser(description='MIDItty Serial to MIDI virtual ALSA device')
padd = parser.add_argument
padd('-s', '--serial', help='Serial device')
padd('-t', '--target', help='Create jack MIDI connection to this target (optional).')
padd('-b', '--baud', help='Baudrate (default = 115200). Valid options are 9600, 19200')
args = parser.parse_args()

# check if this is already running and exit if it is
client = jack.Client(name='MIDItty')  # use default
tp = client.get_ports(is_output=True)
for i in tp:
    if i.name.find(PORTNAME) >= 0:
        print('MIDItty is already configured in jack\nExiting\n')
        client.close()
        exit()

# check for serial port by opening it
baud = 115200
if args.baud is not None:
    if args.baud == '9600':
        baud = 9600
    elif args.baud == '19200':
        baud = 19200

try:
    # maybe for huge sysx transfers, you might want to select hardware handshaking
    ser = serial.Serial(args.serial, baud, xonxoff=False, rtscts=False, dsrdtr=False)
except:
    print('Could not open serial device: '.join(args.serial).join('\n'))
    client.close()
    exit()
ser.flushInput()
ser.flushOutput()

# if a jack target client is identified, then try to connect it.
argname = args.target
connclient = None
if not argname == '' and argname is not None:
    tp = client.get_ports(is_input=True)
    for i in tp:
        if i.name.find(argname) >= 0:
            connclient = i
            print('Found target: '.join(i.name).join('\n'))
            break
    if connclient is None:
        print('Could not find target: '.join(argname).join('\n'))
        client.close()
        ser.close()
        exit()

# open the midi output device
midiout = rtmidi.MidiOut()
midiout.open_virtual_port(PORTNAME)
time.sleep(0.5)

# get the jack client of this
tp = client.get_ports(is_output=True)
thisclient = None
for i in tp:
    if i.name.find(PORTNAME) >= 0:
        thisclient = i
        break
if thisclient is None:
    print('Could not locate self in jack\n')
    client.close()
    midiout.close_port()
    midiout.delete()
    ser.close()
    exit()

# try to connect this to the output
if connclient is not None and thisclient is not None:
    try:
        client.connect(thisclient, connclient)
        print('Connected')
    except:
        print('Error in connecting '.join(thisclient.name).join(' to ').join(connclient.name).join('\n'))

with midiout:
    print('Running...')
    # main loop runs forever
    while (True):
        if (ser.inWaiting() > 0):
            d = ser.read(ser.in_waiting)
            midiout.send_message(d)
    # test        
    #note_on = [0x90, 60, 112] # channel 1, middle C, velocity 112
    #note_off = [0x80, 60, 0]
    #midiout.send_message(note_on)
    #time.sleep(0.5)
    #midiout.send_message(note_off)
    #time.sleep(0.1)
    
# if we are running, this code never executes. 
# clean up and close
midiout.close_port()
midiout.delete()
ser.close()
del midiout


