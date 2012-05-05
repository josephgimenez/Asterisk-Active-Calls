#!/usr/bin/python

import commands
import re
import shutil
import datetime
import csv
import smtplib
import sys

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.message import Message
from email import encoders
from email.utils import COMMASPACE
import mimetypes


#Find service level information
channels = commands.getoutput("/usr/sbin/asterisk -r -x 'sip show channels'").split('\n')

#Iterate through Asterisk response to 'sip show channels'
#Find line that contains regex expression below
#If line we're looking for it found, break from loop

for line in channels:
    activechannels = re.search("^(\d+)\sactive", line)

    if (activechannels is not None):
        break

#Convert regex result to integer
activechannels = int(activechannels.group(1))

#We only care about when active channels are greater than or equal to 23
if (activechannels < 23):
    sys.exit(0)

try:
  s = smtplib.SMTP('localhost', port=25)
except:
  print "Error connecting to smtp on localhost port 25"

mail_to = ['xxxxxxxxxxx@peoplematter.com', 'xxxxxxxx@peoplematter.com']
msg_report = MIMEMultipart('alternative')
msg_report['Subject'] = 'Active lines have reached ' + str(activechannels)
msg_report['From'] = 'lineusage@peoplematter.com'
msg_report['To'] = COMMASPACE.join(mail_to)

try:
  s.sendmail(msg_report['From'], mail_to, msg_report.as_string())
except:
  print "Error sending e-mail."

s.quit()

