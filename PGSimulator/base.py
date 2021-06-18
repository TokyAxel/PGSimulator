from .persistent.Branch import Branch
from .persistent.Bus import Bus
from .persistent.Network import Network
import nevergrad as ng
from .nevergradBased.Optimizer import Optimizer
import numpy as np
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
        ### delete column "2"
        self._raw_data["all_gen"] = np.delete(self._raw_data["all_gen"],[10],axis=1)

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

    ### OPTiMiZATION ###

    def __opt_params(self):
        self.__optimizer.set_parametrization(self.get_opt_params())

    def get_opt_params(self):
        ### May contains constraints
        return None

    def optimizePG(self, optimizer: Optimizer = None, step : int = 1,
                    plot : str = "default"):

        # init params                
        self.step = step
        self.plot = plot

        # optimizer parametrization 
        self.__opt_params()
        
        # init constraints
        constraints = {}
        constraints.update({"Bus Voltage Limits":None})
        
        #let's optimize
        results = self.__optimizer.optimize(grid = self , func_to_optimize = self.loss_function, constraints=constraints, step = self.step)

        #self.plotResults(results, mode = self.plot , time_interval = self.time_interval, average_wide = self.average_wide)
        
        return results

