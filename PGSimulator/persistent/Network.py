import numpy as np
from .Branch import Branch
from .Generator import Generator
from .Bus import Bus
from typing import List, Any, Type, Dict


class Network:

    def __init__(self) -> None :
        self._branches = []
        self._buses = []
    
    def add_branches(self, branches_: List[Branch])-> None :
        for branch in branches_:
            self._branches.append(branch)

    def add_branch(self, branch: Branch)-> None :
        self._branches.append(branch)

    def remove_branch(self, branches_: List[Branch])-> None :
        for branch in branches_:
            self._branches.remove(branch)

    def remove_branch(self, branch: Branch)-> None :
        self._branches.remove(branch)

    def get_branches(self) -> List[Branch]:
        return self._branches

    def add_buses(self, buses_: List[Bus])-> None :
        for bus in buses_:
            self._buses.append(bus)

    def add_bus(self, bus : Bus)-> None :
        self._buses.append(bus)

    def remove_bus(self, buses_: List[Bus])-> None :
        for bus in buses_:
            self._buses.remove(bus)

    def remove_bus(self, bus : Bus)-> None :
        self._buses.remove(bus)

    def get_buses(self) -> List[Bus]:
        return self._buses

    def get_generators(self) -> List[Generator]:
        all_gen = []
        for bus in self.get_buses():
            all_gen.append(gen for gen in bus.get_generators())
        return all_gen

    def get_network_data(self) -> dict :
        """ get all data from network as numpy.ndarray """
        return {"Buses":np.array([bus_.get_bus_data() for bus_ in self._buses], dtype="object"), "Branches":np.array([br_.get_branch_data() for br_ in self._branches], dtype="object")}




