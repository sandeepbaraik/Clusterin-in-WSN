# -*- coding: utf-8 -*-
"""
Created on Mon Apr  6 06:37:46 2020

@author: Sandeep
"""
import matplotlib.pyplot as plt 

def initialize(node_collection,bs_xloc,bs_yloc,comm_rounds):
	x=[]
	y=[]
	for i in range(len(node_collection)):
		x.append(node_collection[i]['xloc'])
		y.append(node_collection[i]['yloc'])
		
	
	
	plt.style.use('seaborn-dark')
	plt.scatter(x,y,color="blue",marker="D",s=30)
	plt.scatter(bs_xloc,bs_yloc,color="red",marker="s",s=40)
	
	plt.show()
	
	#No. of dead sensor nodes vs communication rounds
	dead_sensors=[0,10,20,30,40,50,60,70,80,90,100]
	
	plt.plot(dead_sensors,comm_rounds,marker="*",color="blue")
	plt.xlabel("Number of dead sensor nodes")
	plt.ylabel("Number of communication rounds")
	plt.show()
	
