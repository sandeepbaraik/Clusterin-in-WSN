# -*- coding: utf-8 -*-
"""
Created on Fri Feb 28 06:32:19 2020

@author: Sandeep
"""

import random
import wsn

POPULATION_SIZE=100
GENES=[0,1]
chromosome_size=100
max_diff=10
max_gen=20


class Individual(object):
	def __init__(self,chromosome):
		self.chromosome=chromosome
		self.fitness=self.calc_fitness()
	
	@classmethod
	def mutated_genes(self):
		return random.choice(GENES)
	
	def random_num():
		
		ones=random.randrange(5,10)
		zeros=100-ones
		Input = [zeros,ones] 
		Output = [] 

		# Number initialisation 
		no = 0

		# using iteration 
		for rep in Input: 
			for elem in range(rep): 
				Output.append(no) 
			no += 1

		# printing output 
		random.shuffle(Output)
		return Output
	
	@classmethod
	def create_gnome(self):
		#####NEW CODE
		chromosome=[]
		for _ in range(chromosome_size):
			chromosome.append(self.mutated_genes())
	
		return chromosome
			
	
	def mate (self,par2):

		child_chromosome=[]
		for gp1,gp2 in zip(self.chromosome,par2.chromosome):
			prob=random.random()


			if prob < 0.45:
				child_chromosome.append(gp1)
				
			elif prob < 0.9:
				child_chromosome.append(gp2)
			
			else:
				child_chromosome.append(self.mutated_genes())
				
		return Individual(child_chromosome)
	

	def calc_fitness(self):
		chrom=wsn.create_cluster(self.chromosome)
		self.chromosome=chrom
		
		fitness,chromosome=wsn.network_run(self.chromosome)
		return fitness
		

def main():
	
	generation=1
	found=False
	population=[]
	wsn.initialize(chromosome_size)
	
	for _ in range(POPULATION_SIZE):
		gnome=Individual.create_gnome()
		population.append(Individual(gnome))
		
	best=population[0].chromosome
	
	
	while not found:
		global diff
		
		population=sorted(population,key=lambda x: x.fitness)
		
		if generation>max_gen and diff>=max_diff:
			found=True
			break
		
		new_generation=[]
		#Perform elitism
		s=int((10*POPULATION_SIZE)/100)
		new_generation.extend(population[:s])
		
		
		s=int((90*POPULATION_SIZE)/100)
		for _ in range(s):
			parent1= random.choice(population[:50])
			parent2=random.choice(population[:50])
			child=parent1.mate(parent2)
			new_generation.append(child)
		
		population=new_generation
		
		print("Generation: {} \tFitness:{}".format(generation,population[0].fitness))
		print("No of CH",(population[0].chromosome).count(1))
		generation+=1
		
		if generation>max_gen:
			if population[0].chromosome==best:
				diff+=1
			else:
				best=population[0].chromosome
				diff=0
		
	print("Generation: {} \tFitness:{}".format(generation,population[0].fitness))
	print("No of CH",(population[0].chromosome).count(1))
	wsn.run(population[0].chromosome,(population[0].chromosome).count(1))
	
if __name__ == '__main__':
	main()