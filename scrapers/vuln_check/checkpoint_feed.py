import requests
import urllib, urllib2, cookielib
import re
from datetime import date, timedelta
import os

today = date.today()
yesterday_date = today - timedelta(days = 1)
yesterday = yesterday_date.strftime("%#d %b %Y") 
if os.name != 'nt':
	yesterday = yesterday_date.strftime("%-d %b %Y") #for != Windows remove trailling zero from day
year=yesterday_date.strftime("%Y")

#unused code
to_severities = {
  "CRITICAL": "1",
  "HIGH": "2",
  "MEDIUM": "3",
  "LOW": "4"
}

to_severities_back = {
  "1": "CRITICAL",
  "2": "HIGH",
  "3": "MEDIUM",
  "4": "LOW"
}


#URl
url="https://www.checkpoint.com/advisories/"
severity_regex = '<td class="advisory-severity-(.+?)">\n<strong>'
date_regex = '</td>\n<td>(.+?)</td>'
cpai_regex = '<a href="/defense/advisories/public/'+year+'/(.+?).html">\nCPAI'
title_regex = 'html">\n(.+?)\n</a>\n'

description_regex = 'Description</td>\n<td>(.+?)</td>\n</tr>'
vulnerable_regex = '<tr><td>Who is Vulnerable\?</td><td> (.+?)</td></tr>'
 
#Transformation
severity= re.compile(severity_regex)
date=re.compile(date_regex)
cpai=re.compile(cpai_regex)
title=re.compile(title_regex)

#Open url and find
htmlfile=urllib.urlopen(url)
htmltext=htmlfile.read()

severity=re.findall(severity, htmltext)
date=re.findall(date, htmltext)
cpai=re.findall(cpai, htmltext)
title=re.findall(title, htmltext)

#Print
i=0
def convert_severity(string):
	return to_severities[string]


while (date[i]==yesterday):
	message=''
	url2='https://www.checkpoint.com/defense/advisories/public/'+year+'/'+cpai[i]+'.html'
	message=message+ 'Severity: '+severity[i].upper() +'\n'
	message=message+ 'Title: '+title[2*i+1] +'\n'
	message=message+ 'Reference: '+ url2+'\n'
	
	htmlfile2=urllib.urlopen(url2)
	htmltext2=htmlfile2.read()
	
	description=re.compile(description_regex)
	description=re.findall(description, htmltext2)
	message=message+ 'Description: '+ description[0]+'\n'
	
	vulnerable=re.compile(vulnerable_regex)
	vulnerable=re.findall(vulnerable, htmltext2)
	message=message+ 'Vulnerable Devices: '+vulnerable[0] +'\n'
	print message.replace("<br/>", ", ")
	i+=1



##Example OUTPUT:
# Severity:               HIGH
# Title:                  Google Chrome Use After Free (CVE-2020-6459)
# Checkpoint Reference:   CPAI-2020-1001
# Link                    https://www.checkpoint.com/defense/advisories/public/2020/cpai-2020-1001.html
# Description:            A use-after-free vulnerability exists in Google Chrome. Successful exploitation of this vulnerability could allow a remote attacker to execute arbitrary code on the affected system.
# Vulnerable Devices:     Google Chrome prior to 81.0.4044.12
