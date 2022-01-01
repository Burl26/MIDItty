# MIDItty
## MIDI Serial Bridge (for Linux)

This creates a virtual ALSA MIDI device connected to a hardware serial port.

Why?  This eliminates the need for USB/serial devices and allows you directly connect USB serial devices
like FTDI interfaces, Arduino, Raspberry PI, etc. directly to your Linux system.

The program also allows you to make a jack connection to a target MIDI input device (eg. synthesizer).
If you do not specify a target, it will leave the device open and you can manually connect
using other jack connection methods.

Requirements:
* Linux - tested on Ubuntu and Mint
* jack or jack2
* rtmidi - see https://pypi.org/project/python-rtmidi/ for installation details

Notes:
1. I recommend you use the maximum baud rate (do not specify BAUD).
2. You can connect two PCs together using two FTDI with crossed RX/TX lines.  For best results,
   use optocouplers as directly connecting may cause noise issues in the serial signals.  Direct connection to
   USB-powered devices will not not optocouplers.
3. The target does not have to be the full jack name.  You can use a fragment of the description.
   In the example below, the fragment 'setB' is all that is needed to connect 'setBfree DSP Tonewheel Organ'.

Example Command:
python3 miditty.py -s /dev/ttyUSB0 -t setB

usage: miditty.py \[\-h\] \[\-s SERIAL] \[\-t TARGET\] \[\-b BAUD\]

optional arguments:

\-h, \-\-help                  show this help message and exit.

\-s SERIAL, \-\-serial SERIAL  serial device.

\-t TARGET, \-\-target TARGET  create jack MIDI connection to this target (optional).

\-b BAUD, \-\-baud BAUD        baudrate (default = 115200). Valid options are 9600, 19200.
  
