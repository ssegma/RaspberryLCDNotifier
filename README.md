RaspberryLCDNotifier
====================

Raspberry Pi LCD notifier in Python
Shows number of unread email on dot matrix LCD.
Email status updates every sec.


Hardware
---------
* Raspberry Pi
* 16x2 dot matrix LCD


Prerequisites
--------------
* This program runs on the top of Python and Rpi.GPIO library.
* Gmail parser comes from libgmail and feedparser.


How this works
-----------------
* Gmail provides ATOM feed service thru "https://{}:{}@mail.google.com/gmail/feed/atom".format(USERNAME, PASSWORD))"
* With feedparser, we break it down, and search for [fullcount] field.
* After parsing unread count, display it in format on the dot matrix LCD display.
  

Reference
------------
 http://www.rpiblog.com/2012/11/interfacing-16x2-lcd-with-raspberry-pi.html
