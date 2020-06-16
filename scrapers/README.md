# Scrapers

Usage:
	python phonebook_generator.py #use the generator, must edit first for the appropriate numbers

	python facebook.py #to use facebook scraper, must edit first for the appropriate numbers 
	
	sh script.sh #to use pai scraper, must edit first for the appropriate numbers and range


**phonebook_generator.py**
Wanted to generate vcards with A LOT of numbers to my phone in order to use sync.me(3rd party app) as a resolver of those numbers to give me names.
Couldn't do it back then, because the vcards were big and with the processing power of the phone, it became slow af.
Can I do it now? Maybe, must try one day TESTME

**facebook.py**
Was suposed to work by querying phone numbers on facebook to find the person.
Needs to be logged in for better results, but I couldn't find a way to do it. 
I have an idea how to, but for now it stays like this FIXME
Incorporate with script.sh  TODO

**pai.py**
Is suposed to query  phone numbers on PAI (Páginas Amarelas da Internet) to scrape all the information associated.
It works, as long as I continuously change IP with Script.sh
script.sh and pai.py are a duo!

**script.sh**
Is a watchdog that checks if the .py is done, and constantly changes ip
FIXME to be more global (add arguments)

**cert_checker.py**
Queries several url's certificates, verifies if they are expired or about to (acording to the number of days you want) and notifies you via email (gmail configured)
It works near-perfectly.

### Intro
  Not yet tested in large scale, nor will I, since it is illegal to own a database. Do it at your own risk!
  Scraper gets the page and transforms into beautifulSoup xD. 
  Gets the name, number and address outputs it to a file.txt in form of a INSERT query so you can insert it into a database [table1 - change it if you have another table]
  Ideally you only touch the script. Change the range phonebase and phonefinal as your will.
  With anonimity(through TOR, or proxychains [change: torify->proxychains]).
  There are 2 because I use system commands such as calling torify, and it's easier to compartimentalize. One works, the other tells it to work. 
  
### Motivation
  Allows to create \[Random Country's\] Database of phone numbers, names, addresses.
  Do you need another motivation?

### Tips:
  Range is the number of phones you can scrape until the change of ip.
  
  #You should update range accordingly. Test with a few hundred first to see when the website starts blocking requests from same ip. Don't go full speed!
  #A good choice of range gives you efficiency, a bad one gives you blocked requests (miss numbers) or very slow computing.
 
  
