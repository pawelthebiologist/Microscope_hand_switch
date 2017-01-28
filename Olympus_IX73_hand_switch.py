import time
import serial
from msvcrt import getch

# ser - serial port to communicate with scope

def send_command (ser, command):
    """ Send a text command to the microscope controller"""
	ser.write (command+'\r\n')
    time.sleep(0.2)
    message = ser.read(ser.inWaiting())
    if message == 'x\r\n':
        print ('Error!\r\n')
    else: 
        print ('OK\r\n')

def log_on ():
    """ Connect to microscope controller and return a serial port handle"""
	ser = serial.Serial(
        port='COM1',
        baudrate=19200,
        parity=serial.PARITY_EVEN,
        stopbits=serial.STOPBITS_TWO,
        bytesize=serial.EIGHTBITS
    )
    send_command (ser, '1L 1')
    return (ser)

def log_off (ser):
    """ Close the shutter, turn off remote control of microscope, close the port"""
	manipulate_shutter(ser,1)
    send_command (ser, '1L 0')
    ser.close()

    
def manipulate_shutter (ser, close): 
    """ If close == 1, then close shutter, if 0, then open shutter """
	send_command (ser, '1ESH1 '+str(close))
    
def switch_reflector_turret (ser, position):
    send_command (ser, '1MU1 '+str(position))


ser = log_on()

shutter_closed = 1      

while True:
    key = ord(getch())
    if key == 27 or key == 13: # ESC or Enter close the connection and exit
        break
    elif key == 55: 
        switch_reflector_turret(ser,1)
    elif key == 56: 
        switch_reflector_turret(ser,2)  
    elif key == 57: 
        switch_reflector_turret(ser,3)
    elif key == 52: 
        switch_reflector_turret(ser,4)
    elif key == 53: 
        switch_reflector_turret(ser,8)
    elif key == 48: # Toggle shutter on '0'
        shutter_closed = abs(shutter_closed-1)
        manipulate_shutter(ser, shutter_closed)

log_off(ser)

