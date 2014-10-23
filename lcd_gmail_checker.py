#!/usr/bin/python
#
# JA_16202 HD44780 LCD Test Script for
# Raspberry Pi
# lcd_gmail_checker.py
#
# Author : Eric Yoo
# Github   : https://github.com/ssegma/RaspberryLCDNotifier
#
# Date   : 11/07/2014
#
# Usage 
# 1. install RPi GPIO; https://pypi.python.org/pypi/RPi.GPIO
# 2. Update   USERNAME and PASSWORD in line 205


# The wiring for the LCD is as follows:
# 1 : GND
# 2 : 5V
# 3 : Contrast (0-5V)*    -> GND
# 4 : RS (Register Select)
# 5 : R/W (Read Write)       - GROUND THIS PIN
# 6 : Enable or Strobe
# 7 : Data Bit 0             - NOT USED
# 8 : Data Bit 1             - NOT USED
# 9 : Data Bit 2             - NOT USED
# 10: Data Bit 3             - NOT USED
# 11: Data Bit 4
# 12: Data Bit 5
# 13: Data Bit 6
# 14: Data Bit 7
# 15: LCD Backlight +5V**    - Not used
# 16: LCD Backlight GND      - not used

#import
import RPi.GPIO as GPIO
import time
import os
import datetime
import socket
import fcntl
import struct
import smtplib
from email.mime.text import MIMEText
import feedparser

# Define GPIO to LCD mapping
LCD_RS = 7
LCD_E  = 8
LCD_D4 = 25
LCD_D5 = 24
LCD_D6 = 23
LCD_D7 = 18

# Define some device constants
LCD_WIDTH = 16    # Maximum characters per line
LCD_CHR = True
LCD_CMD = False

LCD_LINE_1 = 0x80 # LCD RAM address for the 1st line
LCD_LINE_2 = 0xC0 # LCD RAM address for the 2nd line

# Timing constants
E_PULSE = 0.001
E_DELAY = 0.001

def main():
  # Main program block
  GPIO.setwarnings(False)
  GPIO.setmode(GPIO.BCM)       # Use BCM GPIO numbers
  GPIO.setup(LCD_E, GPIO.OUT)  # E
  GPIO.setup(LCD_RS, GPIO.OUT) # RS
  GPIO.setup(LCD_D4, GPIO.OUT) # DB4
  GPIO.setup(LCD_D5, GPIO.OUT) # DB5
  GPIO.setup(LCD_D6, GPIO.OUT) # DB6
  GPIO.setup(LCD_D7, GPIO.OUT) # DB7

  # Initialise display
  lcd_init()

  # Send some test
  lcd_byte(LCD_LINE_1, LCD_CMD)
  lcd_string("Welcome to Rpi!!")
  lcd_byte(LCD_LINE_2, LCD_CMD)
  lcd_string("Eric Yoo")

  time.sleep(3) # 3 second delay

  #menu()
  gmail_notifier()


def lcd_init():
  # Initialise display
  lcd_byte(0x33,LCD_CMD)
  lcd_byte(0x32,LCD_CMD)
  lcd_byte(0x28,LCD_CMD)
  lcd_byte(0x0C,LCD_CMD)
  lcd_byte(0x06,LCD_CMD)
  lcd_byte(0x01,LCD_CMD)

def lcd_string(message):
  # Send string to display

  message = message.ljust(LCD_WIDTH," ")

  for i in range(LCD_WIDTH):
    lcd_byte(ord(message[i]),LCD_CHR)


def lcd_byte(bits, mode):
  # Send byte to data pins
  # bits = data
  # mode = True  for character
  #        False for command

  GPIO.output(LCD_RS, mode) # RS

  # High bits
  GPIO.output(LCD_D4, False)
  GPIO.output(LCD_D5, False)
  GPIO.output(LCD_D6, False)
  GPIO.output(LCD_D7, False)
  if bits&0x10==0x10:
    GPIO.output(LCD_D4, True)
  if bits&0x20==0x20:
    GPIO.output(LCD_D5, True)
  if bits&0x40==0x40:
    GPIO.output(LCD_D6, True)
  if bits&0x80==0x80:
    GPIO.output(LCD_D7, True)

  # Toggle 'Enable' pin
  time.sleep(E_DELAY)
  GPIO.output(LCD_E, True)
  time.sleep(E_PULSE)
  GPIO.output(LCD_E, False)
  time.sleep(E_DELAY)

  # Low bits
  GPIO.output(LCD_D4, False)
  GPIO.output(LCD_D5, False)
  GPIO.output(LCD_D6, False)
  GPIO.output(LCD_D7, False)
  if bits&0x01==0x01:
    GPIO.output(LCD_D4, True)
  if bits&0x02==0x02:
    GPIO.output(LCD_D5, True)
  if bits&0x04==0x04:
    GPIO.output(LCD_D6, True)
  if bits&0x08==0x08:
    GPIO.output(LCD_D7, True)

  # Toggle 'Enable' pin
  time.sleep(E_DELAY)
  GPIO.output(LCD_E, True)
  time.sleep(E_PULSE)
  GPIO.output(LCD_E, False)
  time.sleep(E_DELAY)

def menu():
  timelastchecked = 0
  time.sleep(0.5)
  while(1):
   if time.time() >= timelastchecked:
    timelastchecked = time.time()+3
    mystring = ""
    mytime = ""
    mytemp = ""
    pretemp = "NBX ["
    posttemp = "] "

    f=os.popen("date")
    for i in f.readlines():
     mytime += i
     mytime = mytime[11:-13]
     f=os.popen("/opt/vc/bin/vcgencmd measure_temp")
     for i in f.readlines():
      mytemp += i
      mytemp = mytemp[5:-3]
      mystring = pretemp + mytemp + posttemp + mytime
      preIP = "IP "
      address = get_ip_address('eth0')
      address = preIP + address
      lcd_byte(LCD_LINE_1, LCD_CMD)
      lcd_string(address)
      lcd_byte(LCD_LINE_2, LCD_CMD)
      lcd_string(mystring)

def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,
        struct.pack('256s', ifname[:15])
    )[20:24])


def gmail_notifier():
  import pprint
  temp1 = ""

  #Gmail account details
  USERNAME = "ericyooo1@gmail.com" #Your gmail email address
  PASSWORD = "xxxxxx"  # your gmail password

  timelastchecked = 0
  time.sleep(0.5)
  while(1):
   if time.time() >= timelastchecked:
    timelastchecked = time.time()+3
    mystring = ""
    mytime = ""
    mytemp = ""
    pretemp = "["
    posttemp = "] "
    unread = "Unread:"

    f=os.popen("date")
    for i in f.readlines():
     mytime += i
     mytime = mytime[11:-13]
     f=os.popen("/opt/vc/bin/vcgencmd measure_temp")
     for i in f.readlines():
      mytemp += i
      mytemp = mytemp[5:-3]
      #mystring = pretemp + mytemp + posttemp + mytime
      mystring = USERNAME


      #print ( pprint.pprint( feedparser.parse("https://" + USERNAME + ":" + PASSWORD + "@mail.google.com/gmail/feed/atom")['feed'] ) )

      feed = feedparser.parse("https://{}:{}@mail.google.com/gmail/feed/atom".format(USERNAME, PASSWORD))
      try:
        newmails = int(feed["feed"]["fullcount"])
      except KeyError:
        newmails = 0
        print ( pprint.pprint(feed["feed"]) )
        # handle the error
        continue  # you might want to sleep or put the following code in the else block

      unread = unread + str(newmails)

   #LCD Message
   time.sleep(0.5)
   lcd_byte(LCD_LINE_1, LCD_CMD)
   lcd_string(mystring)
   lcd_byte(LCD_LINE_2, LCD_CMD)
   lcd_string(unread)
   time.sleep(1)



if __name__ == '__main__':
  main()
