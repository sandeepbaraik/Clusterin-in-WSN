import random
import math
import sys
import plot

n=4000  #No of bits to be transferred
initial_energy=1            #In joule
Eelec= 50 * (10 ** (-9))    #Electronic energy for node activity: 50nJ/bit
Efs= 10 * (10 ** (-12))     #Energy dissipation in free space: 10 pJ/nit
Emp=0.0013 * (10 ** (-12))  #Energy dissipation during multipath propagation: 0.0013 pJ/bit
Eda=5 * (10 ** (-9))        # Data aggregation energy: 5nJ/bit
d0=87                       #Threshold distance to determine the transmission model: 87 m
threshold_energy=0.001
bs_xloc=50
bs_yloc=50
w1=0.5
w2=0.3
w3=0.1
w4=0.1
w5=0.1

Etotal=float()
sd=float()
CHdisp=float()
total_Eda=0

node={}
node_collection={}
chromosome=[]
cluster_energy={}
nch=0
first=0
disp=None



def distance(xloc1,yloc1,xloc2,yloc2):
	return math.sqrt( ((xloc1-xloc2)**2)+((yloc1-yloc2)**2) )

def find_cluster_head(index):
	global chromosome
	global node_collection
	min_dist=9999
	flag=0
	for i in range (len(chromosome)):
		if chromosome[i]==1 and i != index:
			dist=distance(node_collection[index]['xloc'],node_collection[index]['yloc'],node_collection[i]['xloc'],node_collection[i]['yloc'])
			if dist<min_dist:
				min_dist=dist
				pos=i
				flag=1
	if flag==1:
		node_collection[index].update({'ch':pos})
	else:
		chromosome[index]=1
			
def find_cluster_member(index):
	global chromosome
	global node_collection
	cluster_member=[]
	for i in range(len(chromosome)):
		if chromosome[i]==0 and node_collection[i]['ch']==index:
			cluster_member.append(i)
	if len(cluster_member)!=0:
		node_collection[index].update({'cm':cluster_member})


def transmission_energy(d):
	if d<d0:
		return n*Eelec + Efs *d**2
	else:
		return n*Eelec + Emp * math.pow(d,4)
	
def reception_energy():
	#print(n* Eelec)
	return n* Eelec

def cal_fitness(Etotal,sd,CHdisp,ETotalCH, Total_dist):
	if CHdisp!=0:
		fitness=w1*Etotal + w2*sd + w3*(1/CHdisp) + w4*ETotalCH + w5*Total_dist
	else:
		fitness=w1*Etotal + w2*sd + w4*ETotalCH + w5 *Total_dist
	return fitness
	
def rem_trans_energy(i,dist):
	global chromosome
	global node_collection
	rem_energy=node_collection[i]['energy']
	energy=transmission_energy(dist)
	rem_energy-=energy
	if rem_energy<=threshold_energy:
		chromosome[i]=-1
	node_collection[i].update({'energy':rem_energy})
	return energy

def rem_recp_energy(i):
	global chromosome
	global node_collection
	rem_energy=node_collection[i]['energy']
	energy=reception_energy()
	rem_energy-=energy
	if rem_energy<=threshold_energy:
		chromosome[i]=-1
	node_collection[i].update({'energy':rem_energy})
	return energy
	
def find_cluster_energy(energy,i):
	global cluster_energy
	global node_collection
	c=node_collection[i]['cluster']
	energy+=cluster_energy[c]
	cluster_energy.update({c:energy})

def initialize(chrom):
	global node 
	global nch
	global cluster_energy
	for i in range(chrom):
		node.update({i:{'xloc':random.randint(0,100),'yloc':random.randint(0,100)}})
	
		
def update_cm(i):
	global chromosome
	global node_collection
	c=node_collection[i]['ch']
	new_cm=[]
	new_cm=node_collection[c]['cm']
	new_cm.append(i)
	node_collection[c].update({'cm':new_cm})
			
def update_network():
	global chromosome
	for i in range(len(chromosome)):
		if chromosome[i]==1 and 'cm' not in node_collection[i]:
			chromosome[i]=0
			#print("create_cluster",i)
	for i in range(len(chromosome)):
		if chromosome[i]==0 and 'ch' not in node_collection[i]:
			find_cluster_head(i)
			update_cm(i)
			
		
def create_cluster(chrom):
	#global x,y
	global chromosome
	chromosome=chrom
	
	#initialize cluster energy
	nch=chromosome.count(1)
	for i in range(nch):
		cluster_energy.update({i:0})
	
	if chromosome.count(1)==0:
		sys.exit
	for i in range(len(chromosome)):
		node_collection.update({i:{'xloc':node[i]['xloc'],'yloc':node[i]['yloc'],'energy':initial_energy}})
	
	#Find CH for each node
	for i in range(len(chromosome)):
		if(chromosome[i]==0):
			find_cluster_head(i)
	
	#CM for each CH
	for i in range(len(chromosome)):
		if(chromosome[i]==1):
			find_cluster_member(i)

	#If a cluster head has no cluster member
	update_network()
	
	#if no of CH is more than 10
#	if chromosome.count(1)>10:
#		ch=[]
#		ll=[]
#		prob=random.randrange(5,10)
#		#print("Prob",prob)
#		for i in range(len(chromosome)):
#			if chromosome[i]==1:
#				ch.append(i)
#		ll.extend(random.sample(ch,prob))
#		for i in range(len(chromosome)):
#			if chromosome[i]==1 and i not in ll:
#				chromosome[i]=0
#		
#		#Find CH
#		for i in range(len(chromosome)):
#			if(chromosome[i]==0):
#				find_cluster_head(i)
#		for i in range(len(chromosome)):
#			if chromosome[i]==0 and 'ch' not in node_collection[i]:
#				find_cluster_head(i)
#				update_cm(i)
#		
	
	
	#Cluster for CH nodes
	clus=0
	for i in range(len(chromosome)):
		if chromosome[i]==1:
			node_collection[i].update({'cluster':clus})
			clus+=1
			
	#Cluster of non CH nodes 
	for i in range(len(chromosome)):
		if chromosome[i]==0:
			ch=node_collection[i]['ch']
			node_collection[i].update({'cluster':node_collection[ch]['cluster']})

	#print("Chromosome in wsn",chromosome)
	return chromosome
	
	
		
def tdma_schedule():
	global chromosome
	global node_collection
	#global EiCH
	for i in range(len(chromosome)):
		if chromosome[i]==1 and 'cm' in node_collection[i] and len(node_collection[i]['cm'])!=0:
			for j in (node_collection[i]['cm']):
				if chromosome[j]!=-1:
					dist=distance(node_collection[i]['xloc'],node_collection[i]['yloc'],node_collection[j]['xloc'],node_collection[j]['yloc'])
					energy=rem_trans_energy(i,dist)
					#EiCH+=energy
					find_cluster_energy(energy,i)
				
					#Energy consumption of CMs for receiving the TDMA schedule
					energy=rem_recp_energy(chromosome[j])
#					EiCH+=energy
					find_cluster_energy(energy,chromosome[j])

		
def reclustering(clus):
	global chromosome
	global node_collection
	
	#Find the node with max energy in that particular cluster to be apponinted as new CH
	max_energy=-999
	new_ch=int()
	for i in range(len(node_collection)):
		if node_collection[i]['cluster']==clus and chromosome[i]!=-1:
			energy=node_collection[i]['energy']
			if energy > max_energy:
				max_energy=energy
				new_ch=i

	chromosome[new_ch]=1
	#Update CH of all nodes belonging to that particular cluster
	for i in range(len(node_collection)):
		if node_collection[i]['cluster']==clus and chromosome[i]==0:
			node_collection[i].update({'ch':new_ch})
			
	#update CM of newly elected CH
	cluster_member=[]
	for i in range(len(node_collection)):
		if chromosome[i]==0 and node_collection[i]['ch']==new_ch:
			cluster_member.append(i)
	if len(cluster_member)!=0:
		node_collection[new_ch].update({'cm':cluster_member})
	else:
		chromosome[new_ch]=0
		find_cluster_head(new_ch)
		update_cm(new_ch)
	
		
	return chromosome

def network_run(chrom):
	
	global node_collection
	global total_Eda
	global chromosome
	chromosome=chrom
	
	#If cluster head is dead
	for i in range(len(node_collection)):
		if chromosome[i]==0:
			ch=node_collection[i]['ch']
			if chromosome[ch]==-1:
				clus=node_collection[i]['cluster']
				chromosome=reclustering(clus)
				#EiCH,Erx=tdma_schedule(chromosome)
	
			
	
	
	#Message sent from base_station to all Nodes
#	for i in range(len(chromosome)):
#		if chromosome[i]!=-1:
#			energy=rem_recp_energy(i)
#			find_cluster_energy(energy,i)

	#Message from cluster head to their respective cluster members regarding tdma schedule
	tdma_schedule()
			
	#Message sent from nodes to their respective cluster heads
	EiCH=0     #ENergy consumption from ith node to its corresponding CH node
	Erx=0      #Reception energy of CH
	
	for i in range (len(chromosome)):
		if chromosome[i]==0:
			ch=node_collection[i]['ch']
			dist=distance(node_collection[i]['xloc'],node_collection[i]['yloc'],node_collection[ch]['xloc'],node_collection[ch]['yloc'])
			energy=rem_trans_energy(i,dist)
			EiCH+=energy
			find_cluster_energy(energy,i)
			
			#Reception energy consumption in CH
			energy=rem_recp_energy(i)
			Erx+=energy
			find_cluster_energy(energy,i) 
			total_Eda+=Eda

	
	Eintra=EiCH+Erx+total_Eda
	
	
	#Data transferred from ch to bs
	EiBS=0        #Transmission energy from ith CH to BS
	for i in range (len(chromosome)):
		if chromosome[i]==1:
			dist=distance(node_collection[i]['xloc'],node_collection[i]['yloc'],bs_xloc,bs_yloc)
			energy=rem_trans_energy(i,dist)
			EiBS+=energy
			find_cluster_energy(energy,i)
	Einter=EiBS
	Etotal=Eintra+Einter
	
	#Standard deviation in energy consumption between CHs
	Eclusteri=0
	
	for i in range(len(cluster_energy)):
		Eclusteri+=cluster_energy[i]
	try:
		meu=Eclusteri/nch
	except:
		meu=0

	energy=0
	for i in range(len(cluster_energy)):
		energy+=(meu-cluster_energy[i])**2
	sd=math.sqrt(energy)
	
	#CH dispersion
	min_dist=99999
	flagdisp=0
	
	for i in range(len(chromosome)-1):
		if chromosome[i]==1:
			ch=i
			for j in range(i+1,len(chromosome)):
				if chromosome[j]==1:
					dist=distance(node_collection[j]['xloc'],node_collection[j]['yloc'],node_collection[ch]['xloc'],node_collection[ch]['yloc'])
					flagdisp=1
				if dist<min_dist:
					min_dist=dist
					
	if flagdisp==1:
		CHdisp=min_dist
		global first
		global disp
		if first==0:
			disp=CHdisp
			first=1
	else: 
		CHdisp=0

	ETotalCH=Erx+EiBS+total_Eda
	
	#Residual energy
	ce=0
	for i in range(len(cluster_energy)):
		ce+=cluster_energy[i]
	#print("chromosome",chromosome)
	#print("CH",chromosome.count(1))
#	for i in range(len(node_collection)):
#		#if chromosome[i]==1:
#			
#		print(node_collection[i],end='\n')
	
	#Distance of CH from BS
	Total_dist=0
	for i in range(len(chromosome)):
		
		if chromosome[i]==1:
			dist=distance(node_collection[i]['xloc'],node_collection[i]['yloc'],bs_xloc, bs_yloc)
			Total_dist+=dist
			
#		
	return cal_fitness(Etotal,sd,CHdisp,ETotalCH,Total_dist),chromosome


def run(chrom,no_of_ch):
	

	global chromosome
	chromosome=chrom
	
	comm_rounds=[]    #communication rounds
	round_count=0
	rounds=0
	flag1=0
	flag10=0
	dead = False
	initialize(len(chromosome))
	create_cluster(chromosome)
	dead_nodes_percent={}
	
	while not dead:
		
		if chromosome.count(-1)==len(chromosome):
			dead=True
			break
		
		fitness,chromosome=network_run(chromosome)
		#print("live cluster heads",chromosome.count(1))
		
		#print("chromosome",chromosome)
		dead_nodes=chromosome.count(-1)
		rounds+=1
		print("ROUND NO", rounds)
		print("No of dead sensor nodes",dead_nodes)
#		for i in range(len(node_collection)):
#			print("{:.2f}".format(node_collection[i]['energy']),",",end="")
		
		print()
		if dead_nodes>=1 and flag1==0:
			fnd=rounds
			flag1=1
		if dead_nodes>=10 and flag10==0:
			
			deadten=rounds
			
			flag10=1
		if dead_nodes not in dead_nodes_percent:
			dead_nodes_percent.update({dead_nodes:{'rounds':rounds}})
		
		#Number of dead sensor nodes vs communication rounds
		if round_count==0:
			if dead_nodes > round_count:
				comm_rounds.append(rounds-1)
				round_count+=10
		elif dead_nodes == round_count:
			comm_rounds.append(rounds)
			round_count+=10
		elif dead_nodes > round_count:
			comm_rounds.append(rounds-1)
			round_count+=10
		
		
			
		
		
#		if dead_nodes>=50:
#			for i in range(len(node_collection)):
#				print("Energy",node_collection[i]['energy'])
		
	print("First node died at round:",fnd)
	print("Tenth node died at round:",deadten)
	print("Percentage of dead nodes: ",dead_nodes_percent)
	print("No of CH",no_of_ch)
	

	last_elem=comm_rounds[-1]
	for i in range(len(comm_rounds)+1,12):
		comm_rounds.append(last_elem)
			
	print("Comm",comm_rounds)
#	global disp
#	print("chdisp",disp)
	plot.initialize(node_collection,bs_xloc,bs_yloc,comm_rounds)



