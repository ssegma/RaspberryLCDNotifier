RaspberryLCDNotifier
====================

Raspberry Pi LCD notifier in Python<br>
Shows number of unread email on dot matrix LCD.<br>
Email status updates every sec.<br>


Hardware
---------
* Raspberry Pi
* 16x2 dot matrix LCD

How to use it.
-----------------
1. install RPi GPIO; https://pypi.python.org/pypi/RPi.GPIO
2. Update   USERNAME and PASSWORD in line 205
3. Enjoy then..


Prerequisites/Library 
--------------
* This program runs on the top of Python and Rpi.GPIO library. https://pypi.python.org/pypi/RPi.GPIO
* Gmail parser comes from libgmail and feedparser.


How this works
-----------------
* Gmail provides ATOM feed service thru "https://{}:{}@mail.google.com/gmail/feed/atom".format(USERNAME, PASSWORD))"
* With feedparser, we break it down, and search for [fullcount] field.
* After parsing unread count, display it in format on the dot matrix LCD display.
  

Reference
------------
 http://www.rpiblog.com/2012/11/interfacing-16x2-lcd-with-raspberry-pi.html
 https://pypi.python.org/pypi/RPi.GPIO
 
