#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#This is a code to verify certificates from several url's and notify yourself or others if any is expired or about to.
#
#
__author__ = "davidanil"
from urlparse import urlparse
import httplib, sys
import smtplib
import ssl
import socket
import OpenSSL
from datetime import datetime
import time
import argparse
import sys

urls = {'url.here.please.com'}

sender_email = 'senderEMAIL@DOMAIN.COM'
receiver_email = ['receiverMAIL@DOMAIN.COM']

password = 'PASSWORDHERE' #google account - Security - App Passwords - generate New for mail and computer
#password = input("Input password")

WARNING_DAYS = 30 #N dias para expirar o certificado
CRITICAL_DAYS = 15 #must be less than WARNING_DAYS
#Definicoes Email
port = 587  # For starttls
# Create a secure SSL context
context = ssl.create_default_context()
smtp_server = 'smtp.gmail.com'

def main():
    alive_message=''
    for url in urls:
        time.sleep(3)
        try:
            if is_https(url):
                result=check(url)
                if result <= WARNING_DAYS or False:
                    if result <= CRITICAL_DAYS or False:
                        #sendMail(url, 'CRITICAL',result)
                        alive_message+='\n'+url + ' is critical with '+str(result)+' days'
                        print url + ' is critical with '+str(result)+' days'
                    else:
                        #sendMail(url, 'WARNING',result)
                        alive_message+='\n'+url + ' is warning with '+str(result)+' days'
                        print url + ' is warning with '+str(result)+' days'
                else:
                    alive_message+='\n'+url + ' is good with '+str(result)+' days'
                    print url + ' is good with '+str(result)+' days'
            else:
                alive_message+='\n'+url + ' is not https'
                print url + ' is not identified as https, but should be'
                sendErrorMail(url, ' foi identificado com http em vez de https')
        except Exception as e:
            #sendErrorMail(url, str(e))
            alive_message+='\n'+url+ ' is error with: ' +str(e)
            print e
    sendAliveMail(alive_message)
    print "\nScript ended successfully"
    sys.stdout.flush()


def check(url):
    cert=ssl.get_server_certificate(addr=(url,443))
    x509 = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, cert)
    result = pyopenssl_check_expiration(x509.get_notAfter())
    return  result

def sendMail(url, type, days):
    try:
        server = smtplib.SMTP(smtp_server,port)
        server.ehlo() # Can be omitted
        server.starttls() # Secure the connection
        server.ehlo() # Can be omitted
        server.login(sender_email, password)
        message = '''\
Subject: [Certificate_Script] '''+type+''' - '''+url+'''

O certificado do url: '''+url+''' expira em menos de '''+str(days)+''' dias\n\nCumprimentos,\nO script'''

        server.sendmail(sender_email, receiver_email, message)
    except Exception as e:
        print(e)
    finally:
        server.quit()


def sendAliveMail(alive_message):
    try:
        server = smtplib.SMTP(smtp_server,port)
        server.ehlo() # Can be omitted
        server.starttls() # Secure the connection
        server.ehlo() # Can be omitted
        server.login(sender_email, password)
        message = '''\
Subject: [Certificate_Script] IAMALIVE

'''+alive_message+'''\n\nCumprimentos,\nO script'''

        server.sendmail(sender_email, receiver_email, message)
    except Exception as e:
        print(e)
    finally:
        server.quit()

def sendErrorMail(url, error):
    try:
        server = smtplib.SMTP(smtp_server,port)
        server.ehlo() # Can be omitted
        server.starttls() # Secure the connection
        server.ehlo() # Can be omitted
        server.login(sender_email, password)
        message = '''\
Subject: [Certificate_Script] ERROR - '''+url+'''

O script deparou-se com o seguinte erro: \n\n'''+error+''' \n\n\nVerificar se o script parou de funcionar\nCorrigir o erro e voltar a executar.\n\nCumprimentos,\nO script'''

        server.sendmail(sender_email, receiver_email, message)
    except Exception as e:
        print(e)
    finally:
        server.quit()

def pyopenssl_check_expiration(asn1): #https://gist.github.com/crashdump/5683952
    ''' Return the numbers of day before expiration. False if expired.'''
    try:
        expire_date = datetime.strptime(asn1, "%Y%m%d%H%M%SZ")
    except:
        print "error"

    expire_in = expire_date - datetime.now()
    if expire_in.days > 0:
        return expire_in.days
    else:
        return False

def is_https(url):
    url = urlparse('http://'+url)
    conn = httplib.HTTPConnection(url.netloc)
    conn.request("HEAD", url.path)
    if conn.getresponse():
        conn.close()
        return True
    else:
        conn.close()
        return False

main()
