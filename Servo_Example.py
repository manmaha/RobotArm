#!/usr/bin/python

from Adafruit_PWM_Servo_Driver import PWM
import time
import signal

# ===========================================================================
# Example Code
# ===========================================================================

# Initialise the PWM device using the default address
pwm = PWM(0x40)
# Note if you'd like more debug output you can instead run:
#pwm = PWM(0x40, debug=True)

servoMin = 145  # Min pulse length out of 4096
servoMid = 440  # Mid pulse length
servoMax = 740  # Max pulse length out of 4096

def signal_handler(signum, frame):
        print('You pressed Ctrl+C!')
        sys.exit(0)  

def setServoPulse(channel, pulse):
  pulseLength = 1000000                   # 1,000,000 us per second
  pulseLength /= 60                       # 60 Hz
  print "%d us per period" % pulseLength
  pulseLength /= 4096                     # 12 bits of resolution
  print "%d us per bit" % pulseLength
  pulse *= 1000
  pulse /= pulseLength
  pwm.setPWM(channel, 0, pulse)

signal.signal(signal.SIGINT, signal_handler)
channels = range(0,8) 
pwm.setPWMFreq(60)                        # Set frequency to 60 Hz
#while (True):
# for channel in channels:
  # Change speed of continuous servo on channel O
#  pwm.setPWM(channel, 0, servoMin)
#  time.sleep(1)
#  pwm.setPWM(channel, 0, servoMax)
#  time.sleep(1)

for channel in channels:
	pwm.setPWM(channel, 0, servoMin)
	time.sleep(1)
	pwm.setPWM(channel, 0, servoMax)
	time.sleep(1)
	pwm.setPWM(channel, 0, servoMid)
	time.sleep(1)
  

  


