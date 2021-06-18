import numpy as np
from typing import List
from .Generator import Generator

class Bus:
    """
        Node object in network with some parameters

        Parameters
        ----------
        id : int
            unique identity
        btype : int
            type of the bus (TODO -> checkout all types)
        Pd : float
            Pd is ... TODO
        Qd : float

        Gs : float

        Bs : float

        area : int

        Vm : float

        Va : float

        baseKV : float

        zone : int

        Vmax : float

        Vmin : float

    """

    def __init__(self, id : int = None, btype : int = None, data : np.ndarray = None ) -> None:
        if data is None :
            self._id = id
            self._btype = btype
            self._Pd = None
            self._Qd = None
            self._Gs = None
            self._Bs = None
            self._area = None
            self._Vm = None
            self._Va = None
            self._BaseKV = None
            self._zone = None
            self._Vmax = None
            self._Vmin = None
            self._generators = []
        else :
            try :
                self.load_bus(data)
            except :
                raise
    
    def load_bus(self, data : np.ndarray ) -> None :
        self.set_id(int(data[0]))
        self.set_btype(int(data[1]))
        self.set_Pd(data[2])
        self.set_Qd(data[3])
        self.set_Gs(data[4])
        self.set_Bs(data[5])
        self.set_area(int(data[6]))
        self.set_Vm(data[7])
        self.set_Va(data[8])
        self.set_BaseKV(data[9])
        self.set_zone(int(data[10]))
        self.set_Vmax(data[11])
        self.set_Vmin(data[12])
        self._generators = []
        
    def add_generator(self, data : np.ndarray ) -> None :
        #if self._generators == [] :
        self._generators.append(Generator(data=data))
        #else :
            #self._generators[int(data[0])].load_generator(data)

    def get_params(self) -> dict :
        return {"id": self._id, 
                "type": self._btype, 
                "Pd": self._Pd, 
                "Qd": self._Qd, 
                "Gs": self._Gs, 
                "Bs": self._Bs, 
                "area": self._area, 
                "Vm": self._Vm, 
                "Va": self._Va, 
                "BaseKV": self._BaseKV, 
                "zone": self._zone, 
                "Vmax": self._Vmax,
                "Vmin": self._Vmin
                }

    def set_id(self, value : int) -> None :
        self._id = value
    
    def set_btype(self, value : int ) -> None :
        self._btype = value

    def set_Pd(self, value : float ) -> None :
        self._Pd = value

    def set_Qd(self, value : float)-> None :
        self._Qd = value

    def set_Gs(self, value : float)-> None :
        self._Gs = value

    def set_Bs(self, value : float)-> None :
        self._Bs = value

    def set_area(self, value : int)-> None :
        self._area = value

    def set_Vm(self, value : float)-> None :
        self._Vm = value

    def set_Va(self, value : float)-> None :
        self._Va = value

    def set_BaseKV(self, value : float)-> None :
        self._baseKV = value

    def set_zone(self, value : int)-> None :
        self._zone = value

    def set_Vmax(self, value : float)-> None :
        self._Vmax = value

    def set_Vmin(self, value : float)-> None :
        self._Vmin = value
    
    def get_id(self) -> int :
        return self._id
        
    def get_btype(self) -> int :
        return self._btype

    def get_Pd(self) -> float :
        return self._Pd

    def get_Qd(self) -> float :
        return self._Qd

    def get_Gs(self) -> float :
        return self._Gs

    def get_Bs(self) -> float :
        return self._Bs

    def get_area(self) -> int :
        return self._area

    def get_Vm(self) -> float :
        return self._Vm

    def get_Va(self) -> float :
        return self._Va

    def get_BaseKV(self) -> float :
        return self._baseKV

    def get_zone(self) -> int :
        return self._zone

    def get_Vmax(self) -> float :
        return self._Vmax

    def get_Vmin(self) -> float :
        return self._Vmin

    def get_generators(self) -> List[Generator] :
        return self._generators 

    def get_generators_data(self) -> np.array :
        for i in range(0,len(self._generators)):
            yield self._generators[i].get_generator_data()

    def get_bus_data(self) -> dict :
        """ Notes : spec. = specifications """
        return { "Bus spec." : 
                        np.array([self.get_id(),
                        self.get_btype(),
                        self.get_Pd(),
                        self.get_Qd(),
                        self.get_Gs(),
                        self.get_Bs(),
                        self.get_area(),
                        self.get_Vm(),
                        self.get_Va(),
                        self.get_BaseKV(),
                        self.get_zone(),
                        self.get_Vmax(),
                        self.get_Vmin()]),
                "Generator(s) spec.":
                        np.array([output for output in self.get_generators_data()], dtype="object")
            }



    
        