from .persistent.Branch import Branch
from .persistent.Bus import Bus
from .persistent.Generator import Generator
from .persistent.Network import Network
import nevergrad as ng
from .nevergradBased.Optimizer import Optimizer
import numpy as np
import cmath
#from typing import List
try :
    from oct2py import octave as oct
except :
    pass

class PGSimulator:
    """
        Initiate a network simulator based on a dataset
    """
    
    def __init__(self, network : Network = None) -> None :
        self._network = network
        self._raw_data = 0
        self._optimizer =  Optimizer()

    ### DATA ###

    def set_data_matlab(self, bind : str = None) -> None :
        
        try :
            oct.eval("cd .")
            self._raw_data = oct.feval(bind)
        except :
            print("Please install oct2py and its dependencies if you want to use set_data_matlab()")
            raise
        
        self._network = Network()
        ### Adding buses
        buses = []
        for i in range(0, self._raw_data["bus"].shape[0]):
            buses.append(Bus(data = self._raw_data["bus"][i]))

        ### merge "gen" and "gencost" matrix 
        self._raw_data["all_gen"] = np.concatenate((self._raw_data["gen"],self._raw_data["gencost"]),axis=1)

        ### Adding generators
        for i in range(0, self._raw_data["gen"].shape[0]):
            buses[int(self._raw_data["gen"][i][0] - 1)].add_generator(data = self._raw_data["all_gen"][i])
        self._network.add_buses(buses)

        ### Adding branches
        for i in range(0,self._raw_data["branch"].shape[0]):
            self._network.add_branch(Branch(self._raw_data["branch"][i]))

    def get_network(self) -> Network :
        return self._network

    def get_network_data(self) -> dict :
        return self._network.get_network_data()

    ### DEFINITION OF ALL GRID FUNCTIONS

    def S(self, bus: Bus = None, gen: Generator = None) -> complex :
        """
            AC Power : 
            indicate the generator’s power injection or the constant power demand.
        """
        
        if bus is not None :
            return complex(bus.get_Pd(),bus.get_Qd())
        elif gen is not None : 
            """return Power injection and power injection range (min & max)"""
            return complex(gen.get_Pg(),gen.get_Qg()), complex(gen.get_Pmax(),gen.get_Qmax()), complex(gen.get_Pmin(),gen.get_Qmin())
        else :
            print("Bus/Generator object not found")
            raise
            
    def loss_function(self, candidate, loss_type : str = "line_loss") -> float :
        """
            Objective functions are line loss minimization 
            and generator fuel cost minimization
        """
        
        if loss_type == "line_loss":
            line_loss = 0 
            for g in range(0,len(self._network.get_generators())):
                line_loss += candidate[g]
            return abs(line_loss)

        elif loss_type == "fuel_cost":
            cost = 0
            for g in range(0,len(self._network.get_generators())):
                cost += (self._network().get_buses().get_generators()[g].get_cn_1()*(candidate[g]*candidate[g])) 
                + (self._network().get_buses().get_generators()[g].get_3p()*candidate[g]) + self._network().get_buses().get_generators()[g].get_c0()
            return abs(cost)

        else :
            print("Please choose between : line_loss, fuel cost")
            raise KeyError

    


    ### OPTiMiZATION ###

    def _opt_params(self, len_generators) -> None :
        self._optimizer.set_parametrization(self.get_opt_params(len_generators))

    def get_opt_params(self, len_generators) -> ng.p.Array :
        return ng.p.Array(shape=(len_generators,1)).set_bounds(0,)

    def optimizePG(self, optimizer: Optimizer = None, step : int = 1,
                    plot : str = "default"):

        # init params                
        self.step = step
        self.plot = plot

        # optimizer parametrization 
        self._opt_params(len(self._network.get_generators()))
        
        # init constraints
        constraints = {}
        constraints.update({"Bus Voltage Limits":None})
        
        #let's optimize
        results = self._optimizer.optimize(grid = self , func_to_optimize = self.loss_function, constraints=constraints, step = self.step)

        #self.plotResults(results, mode = self.plot , time_interval = self.time_interval, average_wide = self.average_wide)
        
        return results

