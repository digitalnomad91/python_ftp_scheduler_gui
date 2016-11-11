#########################################################################################
#									Andrew Corbin										#
#									10/31/2016											#
#	  If one takes care of the means, the end will take care of itself. - Gandhi		#
#########################################################################################

from Tkinter import *
import tkMessageBox
from ScrolledText import *
from datetime import datetime
from threading import Timer
import json
import win32api 
import os
import time


class scrollTxtArea:
	def __init__(self,root):
		frame=Frame(root)
		frame.pack()
		self.textPad(frame)
		return

	def textPad(self,frame):
		#add a frame and put a text area into it
		textPad=Frame(frame)
		self.text=Text(textPad,height=50,width=90)
		
		# add a vertical scroll bar to the text area
		scroll=Scrollbar(textPad)
		self.text.configure(yscrollcommand=scroll.set)
		
		#pack everything
		self.text.pack(side=LEFT)
		scroll.pack(side=RIGHT,fill=Y)
		textPad.pack(side=TOP)
		return
		
		
def main():
	master = Tk()
	#master.wm_state('iconic')
	#master.iconify()
	##load config file data for presets
	d = getConfig()

	z = Label(master, text="Local Backup Directories: (one per line)", justify="right")
	z.pack()
	directories = ScrolledText(master, width=36, height=5)
	directories.pack()
	defaultDirs = d["directories"]
	directories.insert('insert', defaultDirs)
	

	z = Label(master, text="Processes to kill: (one per line)", justify="right")
	z.pack()
	
	processes = ScrolledText(master, width=36, height=5)
	processes.pack()
	defaultProcesses = d["processes"]
	processes.insert('insert', defaultProcesses)

	
	z = Label(master, text="FTP Host:", justify="right")
	z.pack()
	ftpHost = Entry(master, width=50)
	ftpHost.pack()
	defaultFTP = d["ftpHost"]
	ftpHost.insert(END, defaultFTP)
	
	
	z = Label(master, text="FTP Directory:", justify="right")
	z.pack()
	ftpDir = Entry(master, width=50)
	ftpDir.pack()
	defaultFTPDir = d["ftpDir"]
	ftpDir.insert(END, defaultFTPDir)
	
	
	z = Label(master, text="FTP Port:", justify="right")
	z.pack()
	ftpPort = Entry(master, width=50)
	ftpPort.pack()
	defaultFTPPort = d["ftpPort"]
	ftpPort.insert(END, defaultFTPPort)

	
	z = Label(master, text="Time of day: (e.g. 0130 for 1:30 AM)", justify="right")
	z.pack()
	timeOfDay = Entry(master, width=50)
	timeOfDay.pack()
	defaulttimeOfDay = d["timeOfDay"]
	timeOfDay.insert(END, defaulttimeOfDay)


	
	w = Label(master, text="This program will kill the specified processes, scan a\n local directory, and SFTP the contents to a remote machine \n at the specified time (daily).", width=50)
	w.pack()	
	
	def callback():
		print "Writing config file"
		data = {'directories': directories.get("1.0",'end-1c'),
			'processes': processes.get("1.0",'end-1c'),
			'ftpHost': ftpHost.get(),
			'ftpDir': ftpDir.get(),
			'ftpPort': ftpPort.get(),
			'timeOfDay': timeOfDay.get()
			}
	
		try:
			with open('config.db', 'w') as outfile:
					json.dump(data, outfile)
					tkMessageBox.showwarning(
						"Success!",
						"Your changes have been saved.\n(%s)" 
					)
		except:
			tkMessageBox.showwarning(
				"Error",
				"Cannot write to file.\n(%s)" 
			)
			return
			
		now = datetime.now()
		print now.day
		
		print "Killing Running Daemons"
		os.system('taskkill /f /im daemon.exe')
		
		time.sleep(1)
			
		print "Running Daemon"
		print 'daemon.exe %d %d %d %d' % (now.day, int(timeOfDay.get()[:2]), int(timeOfDay.get()[2:]), now.second)
		try: win32api.WinExec('daemon.exe %d %d %d %d' % (now.day, int(timeOfDay.get()[:2]), int(timeOfDay.get()[2:]), now.second)) # Works seamlessly
		except: 
			print "Error"
		
		
		
	b = Button(master, text="Save Config & Run Daemon", width=25, command=callback)
	b.pack()

	mainloop()

	Label(master, text="test").pack(side=LEFT)
	e = Entry(master, width=50)
	e.pack(side=LEFT)

	text = e.get()

	text = content.get()
	content.set(text)
	
def getConfig():
	with open('config.db') as json_data:
		d = json.load(json_data)
	return d

main()




