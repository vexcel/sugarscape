# -*- coding: utf-8 -*-
"""
Created on Fri Dec 30 19:22:06 2016

@author: Josef
"""
import numpy as np

class Simulation(object):
    def __init__(self):
        """
        Initializes the simulation object.
        """
        self.agents = []
        self.agentrules = []
        self.environmentrules = []
        self.simtime = 0
        self.Nagents = 0
        self.deaths_by_starvation = 0 # per one time-step
        self.deaths_by_age = 0 # per one time-step
        self.cellspace = None
        self.visions = None
        self.visionweights = None
        self.metabolisms = None
        self.metabolismweights = None
        self.agerange = None
        self.fertility_agerange = None
        self.initial_sugarrange = None
        
        
    def step_in_time(self):
        """
        Increments the simulation time by one.
        """
        self.simtime += 1
        
    def get_sugarlist(self):
        """
        Returns a list containing the sugar quantities each agent has.
        """
        return [agent.sugar for agent in self.agents]
    
    def get_agelist(self):
        """
        Returns a list containing the age value of each agent.
        """
        return [agent.age for agent in self.agents]
    
    def get_visionlist(self):
        """
        Returns a list containing the vision values each agent has.
        """
        return [agent.vision for agent in self.agents]
    
    def get_metabolismlist(self):
        """
        Returns a list containing the metabolism values each agent has.
        """
        return [agent.metabolism for agent in self.agents]
        
    def get_number_of_genders(self):
        """
        Returns the number of males and females in the simulation.
        """
        Nmales = 0
        Nfemales = 0
        for agent in self.agents:
            if agent.sex == 'male':
                Nmales += 1
            else:
                Nfemales += 1
                
        return [Nmales, Nfemales]
    
        
    def create_cellspace(self,dimensions=(80,80),sugar_regenerationrate=1,peaks=[[60,20],[20,60]],radius=20,maxcapacity=4):
        """
        Creates the cellspace and initializes it with the typical Sugarscape 
        sugar distribution.
        """
        self.cellspace = Cellspace(dimensions,sugar_regenerationrate)
        self.cellspace.initialize_sugardistribution(peaks,radius,maxcapacity)
        
    def set_agentrules(self,agentrules=['M']):
        """
        Set the rules which the agents obey.
        """
        self.agentrules = agentrules
        
    def set_environmentrules(self,envrules=['G']):
        """
        Set the rules which the environment obeys.
        """
        self.environmentrules = envrules
        
    def set_visions(self,visions=[1,2],visweights=[0.5,0.5]):
        """
        Set the vision values which the agents are initially given.
        """
        self.visions = visions
        self.visionweights = visweights   
        
    def set_metabolisms(self,metabolisms=[2,3],metweights=[0.5,0.5]):
        """
        Set the metabolism values which the agents are initially given.
        """
        self.metabolisms = metabolisms
        self.metabolismweights = metweights
        
    def set_agerange(self,agerange=[60,100]):
        """
        Sets the age range for the maximum age after which
        agents die.
        """
        self.agerange = agerange
        
    def set_fertility_agerange(self,fertility_agerange=[15,40]):
        """
        Sets the fertility age range.
        """
        self.fertility_agerange = fertility_agerange
        
    def set_initial_sugarrange(self,initial_sugarrange=[10,30]):
        """
        Sets the initial sugar range.
        """
        self.initial_sugarrange = initial_sugarrange
        
    def populate(self,Nagents_init=100):
        """
        Adds Nagents_init amount of agents to the simulation in the beginning.
        The parameters of the agents are selected randomly from the given
        parameter ranges.
        """
        Nsites = self.cellspace.Lx*self.cellspace.Ly
        flatcoords = np.random.choice(Nsites,Nagents_init,replace=False)
        xcoords = np.mod(flatcoords, self.cellspace.Lx)
        ycoords = np.floor_divide(flatcoords, self.cellspace.Ly)
        
        for i in xrange(Nagents_init):
            location = (xcoords[i],ycoords[i])
            sex = ('female' if np.random.rand()<0.5 else 'male')
            metabolism = np.random.choice(self.metabolisms,p=self.metabolismweights)
            vision = np.random.choice(self.visions,p=self.visionweights)
            maxage = np.random.randint(self.agerange[0],self.agerange[1]+1)
            initial_sugar = np.random.randint(self.initial_sugarrange[0],self.initial_sugarrange[1]+1)
            new_agent = Agent(metabolism,vision,maxage,location,sex,initial_sugar,self)
            self.agents.append(new_agent)
            self.cellspace.gridoccupation[location] = new_agent
            
        self.Nagents = len(self.agents)
        
    def remove_starved(self):
        """
        Removes the agents who have zero sugar left from the simulation.
        """
        # loop over all agents
        # build a local list of the agents who do not have anymore sugar
        # remove the starved from agents list
        # remove the starved from gridoccupation
        # increment the death by starving
        # update Nagents
        to_be_removed = []
        cp = self.cellspace
        for agent in self.agents:
            if agent.sugar <= 0:
                to_be_removed.append(agent)
        for agent in to_be_removed:
            loc = agent.location
            cp.gridoccupation[loc] = None
            self.agents.remove(agent)
            
        self.deaths_by_starvation = len(to_be_removed)
        self.Nagents = len(self.agents)
    
    def remove_old(self):
        """
        Removes the agents who have lived up to their maximum age 
        from the simulation.
        """
        # loop over all agents
        # build a local list of the agents who are older than their maxage
        # remove the old from the agents list
        # remove the old from grid occupation
        # increment death by age
        # update Nagents
        cp = self.cellspace
        to_be_removed = []
        for agent in self.agents:
            if agent.age > agent.maxage:
                to_be_removed.append(agent)
        for agent in to_be_removed:
            loc = agent.location
            cp.gridoccupation[loc] = None
            self.agents.remove(agent)
            
        self.deaths_by_age = len(to_be_removed)
        self.Nagents = len(self.agents)
            
    def add_child(self,parent1,parent2,location):
        """
        Adds an agent to the simulation.
        The initial parameters are inherited from the two parents.
        """
        # Define the initialization parameters
        # according to the inheritance rules
        # update agents list
        # update gridoccupation
        # update Nagents
        
        sex = ('female' if np.random.rand()<0.5 else 'male')
        
        suginheritance1 = parent1.init_sugar/2.0
        suginheritance2 = parent2.init_sugar/2.0
        parent1.sugar -= suginheritance1
        parent2.sugar -= suginheritance2
        initial_sugar = suginheritance1 + suginheritance2
        maxage = np.random.randint(self.agerange[0],self.agerange[1]+1)
        metabolism = np.random.choice([parent1.metabolism,parent2.metabolism])
        vision = np.random.choice([parent1.vision,parent2.vision])
        
        new_agent = Agent(metabolism,vision,maxage,location,sex,initial_sugar,self)
        self.agents.append(new_agent)
        self.cellspace.gridoccupation[location] = new_agent
        self.Nagents = len(self.agents)
                
        
        
    def update_simulation(self):
        """
        Updates the whole simulation by running one time-step.
        All agents are updated in random order each once.
        The ruleset of the simulation determines the actions taken at each agent
        update.
        The environment rules are carried out.
        The agents which are too old or are starving are removed from the simulation.
        """
        indices = np.random.choice(self.Nagents,self.Nagents,replace=False)
        for i in indices:
            agent = self.agents[i]
            agent.step_in_age()
            for rule in self.agentrules:
                self.execute_agentrule(rule,agent)
            
        for rule in self.environmentrules:
            self.execute_environmentrule(rule)
            
        self.remove_starved()
        self.remove_old()
        self.step_in_time()
            
    def execute_agentrule(self,rule,agent):
        """
        Calls the agent methods for a given rule.
        """
        if rule=='M':
            agent.move()
        if rule=='S':
            agent.mate()
            
    
    def execute_environmentrule(self,rule):
        """
        Calls the environment methods for a given rule.
        """
        if rule=='G':
            self.cellspace.grow_sugar_back()
    
    
        
class Agent(object):
    numOfinstances = 0
    
    def __init__(self,metabolism,vision,maxage,location,sex,initial_sugar,simulation):
        """
        Initializes an Agent object.
        """
        self.id = self.getid()
        self.age = 0
        self.metabolism = metabolism
        self.vision = vision
        self.maxage = maxage
        self.location = location
        self.sex = sex
        self.sugar = initial_sugar
        self.init_sugar = initial_sugar
        self.sim = simulation
        
        
    def getid(cls):
        """
        A class method which keeps track of the identities of the agents.
        """
        idnum = cls.numOfinstances
        cls.numOfinstances += 1
        return idnum
    getid = classmethod(getid)
    
    def able_to_mate(self):
        """
        Returns True if the agent is in the fertile age-range and
        has enough sugar to mate.
        Return False if the agent is not able to mate.
        """
        return (self.sim.fertility_agerange[0] <= self.age <= self.sim.fertility_agerange[1]) and (self.sugar >= self.init_sugar)
    
    def info(self):
        """
        Prints out the agent information.
        """
        print 'id:',self.id
        print 'location:',self.location
        print 'age:',self.age
        print 'sugar:',self.sugar
        print 'metabolism:',self.metabolism
        print 'vision:',self.vision
        print 'sex:',self.sex
        print 'maxage:',self.maxage
        print 'initial sugar:',self.init_sugar
        
    def step_in_age(self):
        """
        Increments the age of the agent by one.
        """
        self.age += 1
        
    def move(self):
        """
        Updates the agents location according to the movement rule.
        """
        # look around as far as vision permits
        # find the free site with most sugar
        # move there
        # eat the sugar you need to survive
        # gather the sugar in excess
        # update agent location
        # update gridoccupation
        (x,y) = self.location
        cp = self.sim.cellspace
        (Lx,Ly) = cp.dimensions
        vis = self.vision
        xfield = np.arange(x-vis,x+vis+1)
        yfield = np.arange(y-vis,y+vis+1)
        # Take into account the periodicity
        xfield[xfield<0] = xfield[xfield<0]+Lx
        yfield[yfield<0] = yfield[yfield<0]+Ly
        xfield = np.mod(xfield,Lx)
        yfield = np.mod(yfield,Ly)
       
        field = [(xidx,y) for xidx in xfield]
        field += [(x,yidx) for yidx in yfield]
        np.random.shuffle(field)
        # Set the values of the current cell to the decision making variables 
        bestslevel = cp.sugarlevels[x,y]
        bestcoords = (x,y)
        disttobest = 0

        for loc in field:
            if not cp.gridoccupation[loc]:
                suglevel = cp.sugarlevels[loc]
                dist = np.absolute(loc[0]-x+loc[1]-y)
                if suglevel > bestslevel:
                    bestslevel = suglevel
                    bestcoords = loc
                    disttobest = dist
                elif (suglevel==bestslevel) and (dist<disttobest):
                    bestcoords = loc
                    disttobest = dist
        
        # Update the location            
        self.location = bestcoords
        cp.gridoccupation[bestcoords] = self
        cp.gridoccupation[(x,y)] = None
        # Collect all the sugar at the new position and eat the needed amount of it
        self.sugar += bestslevel-self.metabolism
        cp.sugarlevels[bestcoords] = 0
        
    def get_neighbours(self):
        """
        Returns a list of the neighbours of the agent.
        !!! Von Neumann neighbourhood!!!
        """
        (x,y) = self.location
        cp = self.sim.cellspace
        (Lx,Ly) = cp.dimensions
        xfield = np.arange(x-1,x+2)
        yfield = np.arange(y-1,y+2)
        # Take into account the periodicity
        xfield[xfield<0] = xfield[xfield<0]+Lx
        yfield[yfield<0] = yfield[yfield<0]+Ly
        xfield = np.mod(xfield,Lx)
        yfield = np.mod(yfield,Ly)
        
        locations = [(xidx,y) for xidx in xfield if xidx != x]
        locations += [(x,yidx) for yidx in yfield if yidx != y]
        
        neighbours = [cp.gridoccupation[loc] for loc in locations if cp.gridoccupation[loc]]
        return neighbours
    
    def get_freesites(self):
        """
        Returns a list of agents neighboring locations which are free.
        !!! Von Neumann neighbourhood!!!
        """
        (x,y) = self.location
        cp = self.sim.cellspace
        (Lx,Ly) = cp.dimensions
        xfield = np.arange(x-1,x+2)
        yfield = np.arange(y-1,y+2)
        # Take into account the periodicity
        xfield[xfield<0] = xfield[xfield<0]+Lx
        yfield[yfield<0] = yfield[yfield<0]+Ly
        xfield = np.mod(xfield,Lx)
        yfield = np.mod(yfield,Ly)
        
        locations = [(xidx,y) for xidx in xfield if xidx != x]
        locations += [(x,yidx) for yidx in yfield if yidx != y]
        
        freesites = [loc for loc in locations if not cp.gridoccupation[loc]]
        return freesites
        
    
    def mate(self):
        """
        Carries out the mating rule for the agent.
        """
        # Find the list of agents nearby
        # randomly loop through the list and test:
        # if the partner is of opposite sex, if both are fertile,
        # if both have the necessary amount of sugar for reproduction
        # and if there is a free site next to one of the two agents.
        
        # pre-condition to reduce computation
        if not self.able_to_mate():
            return
        neighbours = self.get_neighbours()
        np.random.shuffle(neighbours)
        for neigh in neighbours:
            if self.able_to_mate() and neigh.able_to_mate() and (self.sex != neigh.sex):
                freesites = self.get_freesites()
                if not freesites:
                    freesites = neigh.get_freesites()
                if freesites:
                    loc = freesites[np.random.choice(len(freesites))]
                    self.sim.add_child(self,neigh,loc)
        
    
    def combat(self):
        pass
    
    
class Cellspace(object):
    def __init__(self,dimensions,sugar_regenerationrate):
        """
        Initializes the Cellspace object.
        """
        self.dimensions = dimensions
        self.Lx = dimensions[0]
        self.Ly = dimensions[1]
        self.sugarcapacities = np.ones(shape=dimensions)
        self.sugarlevels = np.zeros(shape=dimensions)
        self.sugar_regenerationrate = sugar_regenerationrate
        self.gridoccupation = {(x,y):None for x in xrange(dimensions[0]) for y in xrange(dimensions[1])}
        
    def initialize_sugardistribution(self,peaks,radius,maxcapacity):
        """
        Sets the Sugarscape sugar-profile by initializing the sugar capacities
        and the sugar levels.
        """
        Lx = self.Lx
        Ly = self.Ly
        radius = float(radius)
        for peak in peaks:
            xindices = np.arange(peak[0]-radius,peak[0]+radius+1,1,dtype=np.int)
            yindices = np.arange(peak[1]-radius,peak[1]+radius+1,1,dtype=np.int)
            for y in yindices:
                for x in xindices:
                    if (0 <= x < Lx) and (0 <= y < Ly):
                        dist = np.linalg.norm([peak[0]-x,peak[1]-y])
                        if dist<radius:
                            sugarvalueraw = maxcapacity*(1-dist/radius)
                            sv = np.ceil(sugarvalueraw)
                            cc = self.sugarcapacities[x,y]
                            cl = self.sugarlevels[x,y]
                            self.sugarcapacities[x,y] = np.maximum(sv,cc)
                            self.sugarlevels[x,y] = np.maximum(sv,cl)
        
        # set the right maximum capacities to every cell, the maximum is a linear slope radially descending from the peak
        # set the sugarlevels to the maximum allowed
        
    def grow_sugar_back(self):
        """
        Increases the amount of sugar in each cell of the cellspace
        by the amount of sugar regeneration rate.
        """
        self.sugarlevels = np.minimum(self.sugarlevels+self.sugar_regenerationrate,self.sugarcapacities)
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
    