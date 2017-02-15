# -*- coding: utf-8 -*-
"""
Created on Sun Jan 08 23:46:32 2017

@author: Josef
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc


if __name__=="__main__":
    plt.close('all')
    
    # Load the data
    data = np.load('ss_data.npz') # data.keys()
    
    # Unpack the data objects
    popvec = data['populationvec']
    
    sugarmean = data['sugarmat'][:,0]
    sugarstd = data['sugarmat'][:,1]
    
    Ndeathstarv = data['deathstarv']
    Ndeathsage = data['deathage']
    
    metabmean = data['metabmat'][:,0]
    metabstd = data['metabmat'][:,1]
    
    agemean = data['agemat'][:,0]
    agestd = data['agemat'][:,1]
    
    males = data['gendermat'][:,0]
    females = data['gendermat'][:,1]
    
    visionmean = data['visionmat'][:,0]
    visionstd = data['visionmat'][:,1]
    
    timevec = data['timevec']
    
   
    # Set the figure font
    rc('font',**{'family':'serif','serif':['Computer Modern Roman']})
    plt.rc('text', usetex=True)
    
    # Visualize the population as a function of time
    fig = plt.figure(figsize=(8,5), dpi=150)
    ax = fig.add_subplot(111)
    ax.plot(timevec,popvec)
    ax.set_title('Population as a function of simulation time', fontsize=14)
    ax.set_xlabel('Simulation time', fontsize=14)
    ax.set_ylabel('Population', fontsize=14)
    ax.grid(True, which='both',alpha=0.3)
    fig.savefig('poptime.pdf', format='pdf')
    plt.show()
    
    # Visualize the fraction of females and males in the population
    # as a function of time
    fracfemales = females/popvec.astype(float)
    fracmales = males/popvec.astype(float)
    fig = plt.figure(figsize=(8,5), dpi=150)
    ax = fig.add_subplot(111)
    ax.plot(timevec,fracfemales,c='r',label='Fraction of females')
    ax.plot(timevec,fracmales,c='b',label='Fraction of males')
    ax.set_title('Fraction of males and females as a function of time',fontsize=14)
    ax.set_xlabel('Simulation time',fontsize=14)
    ax.set_ylabel('Fraction of the population',fontsize=14)
    ax.set_ylim([0,1])
    ax.legend(loc='upper right')
    ax.grid(True,which='both',alpha=0.3)
    fig.savefig('fractime.pdf', format='pdf')
    plt.show()
    
    # Visualize the average age with standard deviation as a function of time
    fig = plt.figure(figsize=(8,5), dpi=150)
    ax = fig.add_subplot(111)
    ax.plot(timevec,agemean,label='Average age')
    ax.set_title('Average age as a function of simulation time', fontsize=14)
    ax.set_xlabel('Simulation time', fontsize=14)
    ax.set_ylabel('Average age', fontsize=14)
    ax.grid(True, which='both',alpha=0.3)
    fig.savefig('agetime.pdf', format='pdf')
    plt.show()
    
    # Visualize the average metabolism with standard deviation as a function of time
    fig = plt.figure(figsize=(8,5), dpi=150)
    ax = fig.add_subplot(111)
    ax.plot(timevec,metabmean,label='Average metabolism')
    ax.set_title('Average metabolism as a function of simulation time', fontsize=14)
    ax.set_xlabel('Simulation time', fontsize=14)
    ax.set_ylabel('Average metabolism', fontsize=14)
    ax.set_ylim([0,5])
    ax.grid(True, which='both',alpha=0.3)
    fig.savefig('mettime.pdf', format='pdf')
    plt.show()
    
    # Visualize the average vision with standard deviation as a function of time
    fig = plt.figure(figsize=(8,5), dpi=150)
    ax = fig.add_subplot(111)
    ax.plot(timevec,visionmean,label='Average vision')
    ax.set_title('Average vision as a function of simulation time', fontsize=14)
    ax.set_xlabel('Simulation time', fontsize=14)
    ax.set_ylabel('Average vision', fontsize=14)
    ax.set_ylim([0,7])
    ax.grid(True, which='both',alpha=0.3)
    fig.savefig('vistime.pdf', format='pdf')
    plt.show()
    
    # Visualize the number of deaths per cycle as a function of time (death to old age)
    fig = plt.figure(figsize=(8,5), dpi=150)
    ax = fig.add_subplot(111)
    ax.plot(timevec,Ndeathsage, linewidth=0.5, label='Number of deaths per cycle')
    ax.set_title('Number of deaths per cycle (old age) as a function of simulation time', fontsize=14)
    ax.set_xlabel('Simulation time', fontsize=14)
    ax.set_ylabel('Number of deaths', fontsize=14)
    ax.grid(True, which='both',alpha=0.3)
    fig.savefig('agedeath.pdf', format='pdf')
    plt.show()
    
    # Visualize the number of deaths per cycle as a function of time (death to starvation)
    fig = plt.figure(figsize=(8,5), dpi=150)
    ax = fig.add_subplot(111)
    ax.plot(timevec,Ndeathstarv, linewidth=0.5, label='Number of deaths per cycle')
    ax.set_title('Number of deaths per cycle (starvation) as a function of simulation time', fontsize=14)
    ax.set_xlabel('Simulation time', fontsize=14)
    ax.set_ylabel('Number of deaths', fontsize=14)
    ax.grid(True, which='both',alpha=0.3)
    fig.savefig('starvdeath.pdf', format='pdf')
    plt.show()
    
    # Visualize the average amount of sugar with standard deviation as a function of time
    fig = plt.figure(figsize=(8,5), dpi=150)
    ax = fig.add_subplot(111)    
    ax.plot(timevec,sugarmean,label='Average sugar')
    ax.set_title('Average sugar as a function of simulation time', fontsize=14)
    ax.set_xlabel('Simulation time', fontsize=14)
    ax.set_ylabel('Average sugar', fontsize=14)
    ax.grid(True, which='both',alpha=0.3)
    fig.savefig('sugartime.pdf', format='pdf')
    plt.show()
    
    #ax.errorbar(timevec,agemean,linestyle='None',marker='.',markersize=4,yerr=agestd,label="Standard deviation")
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    


