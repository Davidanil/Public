#!/bin/bash
##For COSI, to check IOC's from external sources..
##Made by: p-dcardoso
##Improved by: you, maybe

##You will need mapfile, cat, grep, curl, echo, date, sed. Butt I am guessing you have that by default
##Insert hashes in the hashes.txt
##Insert more API keys in api_keys.txt. Seriously, create an account and add your API key, it will go much faster ;D
##run command './hash2MD5_virustotal.sh' after previous steps being completed.
##Output file by default is vtscore.txt but change it if you want. (But why would you?)


##Constants that can be changed##
VIRUSTOTALPERMITEDREQUESTSperMIN=4 #GOT A PREMIUM KEY? change to 903182389120398102, insert key to hashes.txt(1st and only row) and share the key man, Teamwork OP.
OUTPUTFILE="vtscore.txt"

#Count number of lines, since = to number of keys/hashes
#insert them in an array
NUMBERKEYS=$(wc -l api_keys.txt | cut -f1 -d' ')
mapfile -t keys < api_keys.txt
NUMBERHASHES=$(wc -l hashes.txt | cut -f1 -d' ')
mapfile -t hashes < hashes.txt

#For kicks, and because virusTotal has a limit/requests/key/minute
echo Start time: "$(date)"
starttime="$(date -u +%s)"
STARTTIME="$(date)"

#counters
currentHash=0
currentKey=0

##Function to check if we reached EOF in the hash file
check() {
	if [ $currentHash -ge $NUMBERHASHES ] #making sure we won't pass number of hashes
	then
		trim_noise_end
		exit 1
	fi
}

##Function to beautify
trim_noise_end () {
	#Honestly one of the hardest parts, regex in bash? wtf...
	grep -o '"md5": "\w*"' noise >> tmp0
	grep -o '"malicious": \d*,' noise >> tmp0

	#Probably you can put these 4 sed commands in a row, I just couldn't be bothered.
	sed 's/md5//g' tmp0 > tmp1
	sed 's/malicious//g' tmp1 > tmp0
	sed 's/ //g' tmp0 > tmp1
	sed 's/"//g' tmp1 > tmp0
	sed 's/://g' tmp0 > tmp1
	sed 's/,//g' tmp1 > $OUTPUTFILE

	#Remove files that were basically variables
	rm tmp*
	rm noise
	echo Start time: "$STARTTIME" #For kicks, remember?
	echo End time: "$(date)" 
	echo Done, open "$OUTPUTFILE" to check them
}


while [ 1 ] #We have to do all the hashes, until EOF, but check() will check that
do
	check
		starttime="$(date -u +%s)"
		currentKey=0
		while [ $currentKey -le $NUMBERKEYS ] #This loop goes through all the keys
		do	
			n=0
			while [ $n -lt $VIRUSTOTALPERMITEDREQUESTSperMIN ] #This loop only uses each key VIRUSTOTALPERMITEDREQUESTSperMIN number of times
			do
				check
				hash="${hashes[${currentHash}]}"
				key="${keys[${currentKey}]}"
				url=$(echo "https://www.virustotal.com/api/v3/files/${hash}"|tr -d '\r') #create the url without \r
				key_string="x-apikey: $key"
				curl -s --request GET --url "$url" --header "$key_string">> noise #Get the goods, silently
				echo -e "$currentHash of $NUMBERHASHES hashes completed" #So you know where you are
				n=$(( $n + 1 ))
				currentHash=$(( $currentHash + 1 ))
			done
		currentKey=$(($currentKey + 1))
		done
	endtime="$(date -u +%s)"
	while [ $(($endtime-$starttime)) -lt 60 ] #After using all the keys, we need to wait a minute(60s)... 
	do 
		sleep 1 #No need to constantly be hammering the CPU
		endtime="$(date -u +%s)"
	done
done



