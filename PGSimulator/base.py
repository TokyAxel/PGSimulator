from persistent.Network import Network
from persistent.Branch import Branch
from persistent.Bus import Bus
from oct2py import octave as oct

class Powergridsimulator:
    """
        Initiate a network simulator based on a dataset
    """
    
    def __init__(self, network : Network = None) -> None :
        self._network = network
        self._raw_data = 0

    def set_data_matlab(self, bind : str = None) -> None :
        
        self._raw_data = oct.feval(bind)
        
        buses = []
        for i in range(0,raw_data["bus"].shape[0]):
            buses.append(Bus(data = self._raw_data["bus"][i]))

        ### merge "gen" and "gencost" matrix 
        self._raw_data["all_gen"] = np.concatenate((self._raw_data["gen"],self._raw_data["gencost"]),axis=1)
        ### delete column "2"
        self._raw_data["all_gen"] = np.delete(self._raw_data["all_gen"],[10:11],axis=1)

        for i in range(0,raw_data["gen"].shape[0]):
            buses[self._raw_data["gen"][i][0]].add_generator(data = self._raw_data["all_gen"][i])
        self._network.add_bus(buses)

        for i in range(0,raw_data["branch"].shape[0]):
            self._network.add_branch(Branch(self._raw_data["branch"][i]))

    def get_network(self) -> Network :
        return self._network
        

