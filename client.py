#! /usr/python
import socket
import sys
import os
positions=[]
map=[[0 for col in range(6)] for row in range(4)]
host='192.168.2.2'
#host=''
port=8888
positions=[]
data_recieved=[]
recieved=[]
user_id=2
def update_data(position):	#sends data to server, currently sending id and x,y position e.g 2233:(1,3)
	global user_id
	global recieved
	sc=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	try:
		sc.connect((host,port))
	except socket.error:
		sc.connect((host,port+1))
	
	message=str(user_id)+':'+position
	#print message
	try:	
		sc.sendall(message)
	except socket.error:
		return 1
	reply= sc.recv(4096)
	#print reply	
	recieved=reply.split(':')
	#print recieved
	#pull_other_users(recieved)
	return 0

def get_others():
	global recieved
	sc=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	try:
		sc.connect((host,port))
	except socket.error:
		sc.connect((host,port+1))
	
	message='g'
	#print message
	try:	
		sc.sendall(message)
	except socket.error:
		return 1
	reply= sc.recv(4096)
	print reply
	recieved=reply.split(':')
	print recieved
	return 0

def place_others():
	print recieved
	counter=0
	for place in recieved:
		if place != '[\'\']':
			if counter != user_id:
				comma=place.find(',')
				leng = len(place)
				x=place[0:comma]
				y=place[comma+1:leng]
				map[int(x)][int(y)]='D'
		counter+=1



def create_map():		#general base map, may not be needed
	x=0
	for row in map:
		y=0
		for y in range(0,6):
			map[x][y]="#"
			
		x+=1

def draw_map():			# Outputs map to screen
	#os.system('clear')
	for row in map:
		print row

def update_map(x,y,x1,y1):			#Updates user position, and clears old one
	map[x1][y1]="#"
	counter_x=0
	for row in map:
		counter_y=0
		if(counter_x==x):
			for z in range(0,6):
				if(counter_y==y):
					map[counter_x][z]="@"
				counter_y+=1
		counter_x+=1

def new_update_map(x,y):
	create_map()
	map[x][y]="@"
	#get_others()
	place_others()
	draw_map()

def main_loop():
	x=2		#staring x and y for mr @
	y=3
	while True:
		x1=x
		y1=y
		user_input=raw_input()
		if 'a' in user_input:
			if y>0:
				y-=1
		elif 's' in user_input:
			if x>0:
				x-=1
		elif 'd' in user_input:
			if y<6:
				y+=1
		elif 'w' in user_input:
			if x<4:
				x+=1
		#new_update_map(x,y)
		#update_data(str(x)+","+str(y))
		#The following force update only on change
		if x != x1:
			update_data(str(x)+","+str(y))
			new_update_map(x,y)
		if y != y1:
			update_data(str(x)+","+str(y))
			new_update_map(x,y)
			
create_map()
draw_map()
#print update_data("(1,3)") 
print data_recieved

while 1:
	main_loop()
