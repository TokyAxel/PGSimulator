import numpy as np
from .Bus import Bus

class Branch:

    def __init__(self, data : np.ndarray = None) -> None:
        if data is None :
            self._fbus = None
            self._tbus = None
            self._r = None
            self._x = None
            self._b = None
            self._rateA = None
            self._rateB = None
            self._rateC = None
            self._ratio = None
            self._angle = None
            self._status = None
            self._angmin = None
            self._angmax = None

        else :
            try :
                self.load_branch(data)
            except :
                raise
    
    def load_branch(self, data : np.ndarray ) -> None :
        self.set_fbus(int(data[0])) #TODO check and add the "correspondant" bus
        self.set_tbus(int(data[1])) #TODO check and add the "correspondant" bus
        self.set_r(data[2])
        self.set_x(data[3])
        self.set_b(data[4])
        self.set_rateA(data[5])
        self.set_rateB(data[6])
        self.set_rateC(data[7])
        self.set_ratio(data[8])
        self.set_angle(data[9])
        self.set_status(data[10])
        self.set_angmin(data[11])
        self.set_angmax(data[12])


    def set_fbus(self, value: Bus) -> None:
        """ This allows us to say from witch bus this branch is from """
        self._fbus = value
        
    def set_tbus(self, value: Bus) -> None:
        """ This allows us to say to witch bus this branch goes to"""
        self._tbus = value

    def set_r(self, value: float) -> None:
        self._r = value

    def set_x(self, value: float) -> None:
        self._x = value

    def set_b(self, value: float) -> None:
        self._b = value

    def set_rateA(self, value: float) -> None:
        self._rateA = value

    def set_rateB(self, value: float) -> None:
        self._rateB = value

    def set_rateC(self, value: float) -> None:
        self._rateC = value

    def set_ratio(self, value: float) -> None:
        self._ratio = value

    def set_angle(self, value: float) -> None:
        self._angle = value

    def set_status(self, value: float) -> None:
        self._status = value

    def set_angmin(self, value: float) -> None:
        self._angmin = value

    def set_angmax(self, value: float) -> None:
        self._angmax = value

    def get_fbus(self)->Bus:
        return self._fbus
        
    def get_tbus(self)->Bus:
        return self._tbus
        
    def get_r(self)->float:
        return self._r
        
    def get_x(self)->float:
        return self._x
        
    def get_b(self)->float:
        return self._b
        
    def get_rateA(self)->float:
        return self._rateA
        
    def get_rateB(self)->float:
        return self._rateB
        
    def get_rateC(self)->float:
        return self._rateC
        
    def get_ratio(self)->float:
        return self._ratio
        
    def get_angle(self)->float:
        return self._angle
        
    def get_status(self)->float:
        return self._status
        
    def get_angmin(self)->float:
        return self._angmin
        
    def get_angmax(self)->float:
        return self._angmax

    def get_branch_data(self) -> np.array :
        return np.array([
            self.get_fbus(),
            self.get_tbus(),
            self.get_r(),
            self.get_x(),
            self.get_b(),
            self.get_rateA(),
            self.get_rateB(),
            self.get_rateC(),
            self.get_ratio(),
            self.get_angle(),
            self.get_status(),
            self.get_angmin(),
            self.get_angmax(),
        ])
    