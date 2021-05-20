#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#This is a module to retrieve the vulnerabilities from other scripts and send emails.
#

from urlparse import urlparse
import httplib, sys
import smtplib
import ssl
import socket
from datetime import date
import time
import argparse
import sys
import requests
import csv
import os
import subprocess

today = date.today()
today_day = date.today().strftime("%#d")
today_month = date.today().strftime("%m")
today_year = date.today().strftime("%Y")


sender_email = 'FIXME'
receiver_email = ['FIXME'] #debug only
password = 'FIXME' #google account - Security - App Passwords - generate New for mail and computer
#password = input("Input password")

#Definicoes Email
port = 587  # For starttls
# Create a secure SSL context
context = ssl.create_default_context()
smtp_server = 'FIXME'

LENGHT=10

months = {
  "01": "Janeiro",
  "02": "Fevereiro",
  "03": "Março",
  "04": "Abril",
  "05": "Maio",
  "06": "Junho",
  "07": "Julho",
  "08": "Agosto",
  "09": "Setembro",
  "10": "Outubro",
  "11": "Novembro",
  "12": "Dezembro"
}

def main():
    try:
        send_cisco()
        send_checkpoint()
    except Exception as e:
        sendErrorMail(str(e))
        message+='\n'+'Script came with an error: ' +str(e)
        print e
    print "\nScript ended successfully"
    sys.stdout.flush()


###Email Code###
def send_cisco():
    message=""
    message=subprocess.check_output("python cisco_feed.py", shell=True)
    if len(message)>LENGHT:
    	sendFeedMail("Cisco", message)
    	print "send Cisco"
    	return True
    return False

def send_checkpoint():
    message=""
    message=subprocess.check_output("python checkpoint_feed.py", shell=True)
    if len(message)>LENGHT:
    	sendFeedMail("Checkpoint", message.replace('\n',''))
    	print "send Checkpoint"
    	return True
    return False

	
def sendFeedMail(product, message):
    try:
        server = smtplib.SMTP(smtp_server,port)
        server.ehlo() # Can be omitted
        server.starttls() # Secure the connection
        server.ehlo() # Can be omitted
        server.login(sender_email, password)
        preline="Bom dia,\nNo dia "+today_day+" de "+ months[str(today_month)]+ " de "+ today_year +" detetou as seguintes vulnerabilidades nos produtos "+product+":\n\n"
        message = '''\
Subject: [Vulnerabilities] - Security Advisories - '''+product+'''

'''+preline+message+'''\n\n'''
		
        print "message is printing:"
        print message
        server.sendmail(sender_email, receiver_email, message)
    except Exception as e:
        print(e)
    finally:
        server.quit()
		
		
def sendErrorMail(error):
    try:
        server = smtplib.SMTP(smtp_server,port)
        server.ehlo() # Can be omitted
        server.starttls() # Secure the connection
        server.ehlo() # Can be omitted
        server.login(sender_email, password)
        message = '''\
Subject: [Vulnerabilities] - ERRO NO SCRIPT

'''+error+'''\n\nCumprimentos,\n'''

        print message
        server.sendmail(sender_email, receiver_email, message)
        message=''
    except Exception as e:
        print(e)
    finally:
        server.quit()

main()
