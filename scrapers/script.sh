#!/bin/bash

#Not yet tested in large scale, nor will I, untill i determine the "legalness" of webscrapping in Portugal-
#Allows to create Portugal's Database of phone numbers, names, addresses.
#With anonimity(through TOR, or proxychains [change: torify->proxychains]).
#Range is the number of phones you can scrape until the change of ip.
#You should update range accordingly. Test with a few hundred first to see when the website starts blocking requests from same ip. Don't go full speed!
#A good choice of range gives you efficiency, a bad one gives you blocked requests (miss numbers) or very slow computing.

#VARIABLES CHANGE HERE 214405300 (McDonalds to test)
phonebase=210000000 #first phone to be tested
phonefinal=220000000 #last phone to be tested
range=200 #most important variable
currentip=$(curl ifconfig.me/ip) #check the current ip before begining

function main {
	echo "Starting..."
	echo " "
	echo Your IP is: $currentip, but don't worry, I'll change it every $range numbers ';)' 
 	echo " "
	start
	dostuff
} 

#Starts deamons of the great TOR
function start {
	sudo service tor stop
	sudo service tor start
	sudo service tor status|grep Active
	ip
}

#Checks ip
function ip {
	echo ""
	newip=$(torify curl ifconfig.me/ip)
	echo $newip
}

#Executes the scraper within range
function dostuff {
	python3.5 pai.py $phonebase $range
	check
}

#Checks if scraper is still alive so it finishes or updates the ip and continues
function check { 
	ps=$(ps --no-headers -C python3.5|wc -l)
	if [ $phonebase -eq $phonefinal ]
	then
		finish
	elif [ $ps -eq 0 ]
	then #updates ip and continues
		reload
		phonebase=$((range + phonebase))
		dostuff
	else
		check
	fi
}

#forces update on TOR circuit
function reload {
	newip=$currentip
	while [ "$newip" == "$currentip" ]
	do
		sudo service tor force-reload
		ip
	done
}

function finish {
	echo "Finished"
	exit 0
}

main 
