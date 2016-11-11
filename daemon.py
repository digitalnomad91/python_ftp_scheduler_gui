#########################################################################################
#								  Andrew Corbin										    #
#									10/31/2016											#
#	  If one takes care of the means, the end will take care of itself. - Gandhi		#
#########################################################################################

from datetime import datetime
from threading import Timer
import json
import subprocess
import os
import win32api
import sys
import time
import calendar
from ftplib import FTP_TLS



def Log(txt):
	print txt
	f = open('activity.log','w')
	f.write('hi there\n') # python will convert \n to os.linesep
	f.close() # you can omit in most cases as the destructor will call it
	
  # determine current epoch and scheduled input epoch
now = datetime.now()
now = datetime(now.year, now.month, now.day, now.hour, now.minute);
epoch = time.mktime(now.timetuple())

scheduledHr = int(sys.argv[2]) if (sys.argv[2]) != "0" else 0
scheduledMin = int(sys.argv[3]) if (sys.argv[3]) != "0" else 0

scheduled = datetime(now.year, now.month, int(sys.argv[1]), scheduledHr, scheduledMin)
scheduled = time.mktime(scheduled.timetuple())

# if current epoch is passed scheduled input, then add a day to time (run tomorrow)
if epoch > scheduled:
	day = datetime.now().day
	hr = datetime.now().hour
	min = datetime.now().minute
	
	if datetime.now().second+15 < 60:
		sec = datetime.now().second+15
	else:
		min = min + 1
		sec = 0
# otherwise run on input time today
else:
	day = datetime.now().day
	hr = int(sys.argv[2])
	min = int(sys.argv[3])
	sec = int(sys.argv[4])
	

hr = 0 if hr == "0" else hr
min = 0 if min == "0" else min
sec = 0 if sec == "0" else sec

# debug output
Log("Next: %d %d %d %d " % (day, hr, min, sec))
Log("Next Scheduled for: %d > %d" % (epoch, scheduled))



def getConfig():
	with open('config.db') as json_data:
		d = json.load(json_data)
	return d


def TimerCallback():
	data = getConfig()
	
  # loop processes list and kill each one
	processes = data["processes"]
	for line in processes.splitlines():
		Log("Killing Process %s " % line[line.rindex('\\')+1:])
		os.system('taskkill /f /im %s' % line[line.rindex('\\')+1:])
	
	
	# Connect to  SFTP 
	ftps = FTP_TLS('fuge.it')
	ftps.login('testuser', 'testpass')           # login anonymously before securing control channel
	ftps.prot_p()          # switch to secure data connection.. IMPORTANT! Otherwise, only the user and password is encrypted and not all the file data.
	ftps.retrlines('LIST')

		
		
  # Loop directories/files and sftp each one
	directories = data["directories"]
	for line in directories.splitlines():
		# If nothing after last slash then this is a directory we need to loop for files
		if line[line.rindex('\\')+1:] == "": 
			for fn in os.listdir(line):
				 if os.path.isfile(fn):
					# upload file to public/ on remote
					myfile = open(fn, 'r')
					ftps.storlines('STOR ' + fn, myfile)
					myfile.close()

		else: # otherwise it's a single file
			if os.path.isfile(line):
				# upload file to public/ on remote
				localpath = line
				myfile = open(line, 'r')
				ftps.storlines('STOR ' + filename, myfile)
				myfile.close()

				
	ftps.close()
	
	# reset daemon for tomorrow's run
	try: win32api.WinExec('daemon.exe %d %d %d %d' % (day, hr, min, sec)) # Works seamlessly
	except: pass
	
	# loop processes list and kill each one
	processes = data["processes"]
	for line in processes.splitlines():
		Log("Restarting Process %s " % line)
		try: win32api.WinExec(line) # Works seamlessly
		except: pass
	

# timer config
x=datetime.today()
y=x.replace(day=day, hour=hr, minute=min, second=sec, microsecond=0)
delta_t=y-x
secs=delta_t.seconds+1

# Start Timer
t = Timer(secs, TimerCallback)
t.start()


