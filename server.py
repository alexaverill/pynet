#! /usr/python
import socket
import sys
import string
from thread import *

so = socket.socket(socket.AF_INET,socket.SOCK_STREAM)


#Globals
host=''
port=8888
positions=[['' for col in range(1)] for row in range(5)] #hold client positions
#positions=[25]
connections=0 #number of places to send things

map = [[0 for col in range(6)] for row in range(4)] #map for placeholding and viewing on the server

try:
	so.bind((host,port))
	print port
except socket.error, msg:
	so.bind((host, port+1))
	print port+1
print "Ready"
so.listen(10)
def show_positions():		#Debug function to show user positions array
	for row in positions:
		print row


def update_data(passed_data):
	length=len(passed_data)
	#print length
	if length>0:
		colon=passed_data.find(':')
		comma=passed_data.find(',')

		#print colon
		#print comma
		c_id = passed_data[0:colon]
		#print c_id
		x=passed_data[colon+1:comma]
		y=passed_data[comma+1:length]
		#print x
		#print y
		positions[int(c_id)]=x+','+y
		#show_positions()

def main_handler(conn):

	while True:
		data=conn.recv(1024)
		passing=data 		#temp variable to pass to run through update fun.
		if len(passing)>0:
			update_data(passing)
			reply =':'.join(str(x) for x in positions)	
			#print reply
			#reply='a'
			conn.sendall(reply)
		if not data:
			break	
	conn.close()
	#show_positions()
	#print data

while 1:
	
	conn, addr = so.accept()
	start_new_thread(main_handler,(conn,))
so.close()
