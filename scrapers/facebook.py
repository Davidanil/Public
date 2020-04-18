import requests
import urllib, urllib2, cookielib
import re
from bs4 import BeautifulSoup

#Phone start and range
phone=910000000
range=260;
i=0

while i < range:
	#Settings - Change here!
	url="https://www.facebook.com/search/top/?init=quick&q=" + str(phone) + "&tas=0.6508492445573211"
	regex = '<div class="_5d-5">(.+?)</div>'
	regex2 = '<a href="https://www.facebook.com/(.+?)?ref=br_rs">'
	
	#Transformation
	patern= re.compile(regex)
	patern2= re.compile(regex2)
	
	#Open url and find
	htmlfile=urllib.urlopen(url)
	htmltext=htmlfile.read()
	name=re.findall(patern, htmltext)
	username=re.findall(patern2, htmltext)
	
	#Print
	if len(name)==1:
		print name, username, phone
	i+=1
	phone+=1


