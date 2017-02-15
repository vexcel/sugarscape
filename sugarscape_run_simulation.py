# -*- coding: utf-8 -*-
"""
Created on Fri Dec 30 19:25:10 2016

@author: Josef
"""

from sugarscape import Simulation,Agent,Cellspace
import matplotlib.pyplot as plt
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
    Ncycles = 220
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
    
    #----------------------Simulation Visualisation-----------------------#
    capturetimes = [1,50,100,150,200]
    continuous_visualization = True
    
    plt.close('all')
    fig = plt.figure(figsize=(8,8), dpi=100)
    ax = fig.add_subplot(111)
    sugarfield = sim.cellspace.sugarlevels
    im = ax.imshow(sugarfield,cmap=plt.get_cmap('afmhot'))
    cb = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    i=0
    if continuous_visualization:
        while i<Ncycles and sim.Nagents>0:
            print 'Agents:',sim.Nagents
            plt.cla()
            ax.set_title('Sugarscape, time %s, agents %s'%(sim.simtime,sim.Nagents))
            sugarfield = sim.cellspace.sugarlevels
            im = ax.imshow(sugarfield,cmap=plt.get_cmap('afmhot'),vmin=0,vmax=maxcapacity)
            for agent in sim.agents:
                (y,x) = agent.location
                ax.scatter(x,y,c='r')
            plt.show()
            plt.pause(0.001)  
        
            sim.update_simulation()
            i += 1
    else:
        while i<Ncycles and sim.Nagents>0:
            print 'Agents:',sim.Nagents
            if sim.simtime in capturetimes:
                plt.cla()
                ax.set_title('Sugarscape, time %s, agents %s'%(sim.simtime,sim.Nagents))
                sugarfield = sim.cellspace.sugarlevels
                im = ax.imshow(sugarfield,cmap=plt.get_cmap('afmhot'),vmin=0,vmax=maxcapacity)
                for agent in sim.agents:
                    (y,x) = agent.location
                    ax.scatter(x,y,c='r')
                plotname = 'sugarscape_at_time_'+str(sim.simtime)+'.pdf'
                fig.tight_layout()
                fig.savefig(plotname, format='pdf')
                plt.show()
                plt.pause(0.001)  
        
            sim.update_simulation()
            i += 1

    
    
    

        