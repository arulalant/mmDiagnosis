#!/usr/bin/python
# ref : http://kutuma.blogspot.com/2007/08/sending-emails-via-gmail-with-python.html
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email import Encoders
import os

gmail_user = "auto.mail.ncmrwf.in@gmail.com"
gmail_pwd = "Monsoon@Ncmrwf"

def gmail(to, subject, text, attach=None, port=587):
   msg = MIMEMultipart()

   msg['From'] = "no-reply auto.mail.ncmrwf<"+gmail_user+">"
   msg['To'] = to
   msg['Subject'] = subject

   msg.attach(MIMEText(text))
   
   if attach: 
       part = MIMEBase('application', 'octet-stream')
       part.set_payload(open(attach, 'rb').read())
       Encoders.encode_base64(part)
       part.add_header('Content-Disposition',
           'attachment; filename="%s"' % os.path.basename(attach))
       msg.attach(part)

   mailServer = smtplib.SMTP("smtp.gmail.com", port)
   mailServer.ehlo()
   mailServer.starttls()
   mailServer.ehlo()
   mailServer.login(gmail_user, gmail_pwd)
   mailServer.sendmail(gmail_user, to, msg.as_string())
   # Should be mailServer.quit(), but that crashes...
   mailServer.close()



