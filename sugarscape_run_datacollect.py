# -*- coding: utf-8 -*-
"""
Created on Sun Jan 08 16:49:22 2017

@author: Josef
"""

from sugarscape import Simulation,Agent,Cellspace
import numpy as np

        

if __name__=="__main__":
    #-----------Define parameters----------------------------------------#
    # Define the metabolisms which agents can initially get
    metabolisms = [1,2,3,4]
    metweights = [1.0/len(metabolisms) for i in xrange(len(metabolisms))] # uniform weights
    # Define the visions which agents can initially get
    visions = [1,2,3,4,5,6]
    visweights = [1.0/len(visions) for i in xrange(len(visions))] # uniform weights
    # Define the maximum age range for the agents
    max_agerange = [60,100]
    # Define the age range for fertility
    fertility_agerange = [15,40]
    # Define the dimensions of the cellspace
    cellspace_dimension = (80,80)
    # Define the sugar regeneration rate
    sugar_regenerationrate = 1
    # Define the range of sugar the agents can initially get
    initial_sugarrange = [10,30]
    # Define the amount of agents in the simulation initially
    Nagents_initial = 200
    # Define the rules of the simulation
    environment_rules = ['G'] # G = Grow sugar at sugar_regenerationrate
    agent_rules = ['M','S'] # M = movement rule, S = mating rule
    # Define the location of sugarpeaks in the lattice
    peaks = [[60,20],[20,60]]
    # Define the radius of the sugarpeaks
    radius = 35
    # Define the maximum amount of sugar at the sugarpeaks
    maxcapacity = 6
    # Define the number of iterations
    Ncycles = 4000
    #--------------------------------------------------------------------#
    
    # Create simulation object and initialize the simulation
    sim = Simulation()
    sim.set_agentrules(agent_rules)
    sim.set_environmentrules(environment_rules)
    sim.create_cellspace(cellspace_dimension,sugar_regenerationrate,peaks,radius,maxcapacity)
    sim.set_metabolisms(metabolisms,metweights)
    sim.set_visions(visions,visweights)
    sim.set_agerange(max_agerange)
    sim.set_fertility_agerange(fertility_agerange)
    sim.set_initial_sugarrange(initial_sugarrange)
    sim.populate(Nagents_initial)
    
    print 'Simulation initialized'
    
    #----------Run the simulation---------------#
    populationvec = []
    gendermat = []
    deathstarv = []
    deathage = []
    visionmat = []
    metabmat = []
    agemat = []
    sugarmat = []
    timevec = []
    
    while sim.simtime<=Ncycles and sim.Nagents>0:
        print 'Agents:',sim.Nagents,'simtime:',sim.simtime
        # Yield the values we are interested in
        timevec.append(sim.simtime)
        populationvec.append(sim.Nagents)
        deathstarv.append(sim.deaths_by_starvation)
        deathage.append(sim.deaths_by_age)
        gendermat.append(sim.get_number_of_genders())
        # To avoid too large file-size, compute the statistics right away
        agestemp = sim.get_agelist()
        agemat.append([np.mean(agestemp),np.std(agestemp)])
        
        metabstemp = sim.get_metabolismlist()
        metabmat.append([np.mean(metabstemp),np.std(metabstemp)])
        
        visionstemp = sim.get_visionlist()
        visionmat.append([np.mean(visionstemp),np.std(visionstemp)])
        
        sugarstemp = sim.get_sugarlist()
        sugarmat.append([np.mean(sugarstemp),np.std(sugarstemp)])
        # Update the simulation
        sim.update_simulation()
        
        
    # Transform the arrays into numpy format
    populationvec = np.array(populationvec)
    deathstarv = np.array(deathstarv)
    deathage = np.array(deathage)
    visionmat = np.array(visionmat)
    metabmat = np.array(metabmat)
    gendermat = np.array(gendermat)
    agemat = np.array(agemat)
    sugarmat = np.array(sugarmat)
    timevec = np.array(timevec)
    
    # Save the results
    np.savez('ss_data.npz',
             populationvec=populationvec,
             deathstarv=deathstarv,
             deathage=deathage,
             gendermat=gendermat,
             visionmat=visionmat,
             metabmat=metabmat,
             agemat=agemat,
             sugarmat=sugarmat,
             timevec=timevec)
    
    print 'Data saved succesfully'
        
    
    
    

        