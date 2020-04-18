import time
import sys

#Encoding stuff
reload(sys)
sys.setdefaultencoding('UTF8')

#Change print outputs
class Tee(object):
    def __init__(self, *files):
        self.files = files
    def write(self, obj):
        for f in self.files:
            f.write(obj)
            f.flush()
    def flush(self) :
        for f in self.files:
            f.flush()
original = sys.stdout

#Start timer
start=time.time()

STR1 = "BEGIN:VCARD\nVERSION:2.1\nN:"
STR2 = ";;;\nTEL;HOME;VOICE:"
STR3 = "\nEND:VCARD"
phone=910000000

while phone != 920000000:
	sys.stdout = original
	print ("Current: ", phone)
	stringer = "BEGIN:VCARD\nVERSION:2.1\nN:" + str(phone) + ";;;\nTEL;HOME;VOICE:" + str(phone) + "\nEND:VCARD"
	#File Output
	f = open('gen.vcf', 'a')
	sys.stdout = Tee(sys.stdout, f)
	print (stringer)
	f.close()
	phone+=1


#Console Output
sys.stdout = original
finish=time.time()
elapsed=finish-start
horas=elapsed//3600
minutos=elapsed//60
print ("\n\nHoras:", horas,"\nMinutos:",minutos, "\nSegundos:", elapsed)

