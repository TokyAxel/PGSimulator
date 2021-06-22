import numpy as np

class Generator:
    """
        Generator implementation

        Parameters
        ----------
        
        bus	
        Pg	
        Qg	
        Qmax	
        Qmin	
        Vg	
        mBase	
        status	
        Pmax	
        Pmin
        cost_model 	 
        startup	
        shutdown	
        n	
        c(n-1) -> cn_1	
        ... -> 3p
        c0
    """

    def __init__(self, bus_id : int = None, data : np.ndarray = None ) -> None:
        if data is None :
            self._bus_id = bus_id
            self._Pg = None
            self._Qg = None
            self._Qmax = None
            self._Qmin = None
            self._Vg = None
            self._mBase = None
            self._status = None
            self._Pmax = None
            self._Pmin = None
            self._cost_model = None
            self._startup = None
            self._shutdown = None
            self._n = None
            self._cn_1 = None	
            self._3p = None	
            self._c0 = None
            
        else :
            try :
                self.load_generator(data)
            except :
                raise
    
    def load_generator(self, data : np.ndarray ) -> None :
        self.set_bus_id(int(data[0]))
        self.set_Pg(data[1])
        self.set_Qg(data[2])
        self.set_Qmax(data[3])
        self.set_Qmin(data[4])
        self.set_Vg(data[5])
        self.set_mBase(data[6])
        self.set_status(int(data[7]))
        self.set_Pmax(data[8])
        self.set_Pmin(data[9])
        self.set_cost_model(int(data[10]))
        self.set_startup(data[11])
        self.set_shutdown(data[12])
        self.set_n(int(data[13]))
        self.set_cn_1(data[14])	
        self.set_3p(data[15])	
        self.set_c0(data[16])

    def get_params(self) -> dict :
        return {"bus_id": self._bus_id, 
                "type": self._Pg, 
                "Pd": self._Qg, 
                "Qmax": self._Qmax, 
                "Qmin": self._Qmin, 
                "Vg": self._Vg, 
                "mBase": self._mBase, 
                "status": self._status, 
                "Pmax": self._Pmax, 
                "Pmin": self._Pmin, 
                "cost model (1 = piecewise linear, 2 = polynomial)": self.cost_model, 
                "startup": self._startup, 
                "shutdown": self._shutdown,
                "n": self._n,
                "c(n-1)": self.cn_1,
                "...": self._3p,
                "c0": self.set_c0,
                }

    def set_bus_id(self, value : int) -> None :
        self._bus_id = value
    
    def set_Pg(self, value : float ) -> None :
        self._Pg = value

    def set_Qg(self, value : float ) -> None :
        self._Qg = value

    def set_Qmax(self, value : float)-> None :
        self._Qmax = value

    def set_Qmin(self, value : float)-> None :
        self._Qmin = value

    def set_Vg(self, value : float)-> None :
        self._Vg = value

    def set_mBase(self, value : float)-> None :
        self._mBase = value

    def set_status(self, value : int)-> None :
        self._status = value

    def set_Pmax(self, value : float)-> None :
        self._Pmax = value

    def set_Pmin(self, value : float)-> None :
        self._Pmin = value

    def set_cost_model(self, value : int)-> None :
        self._cost_model = value

    def set_startup(self, value : float)-> None :
        self._startup = value

    def set_shutdown(self, value : float)-> None :
        self._shutdown = value

    def set_n(self, value : int)-> None :
        self._n = value

    def set_cn_1(self, value : float)-> None :
        self._cn_1 = value
    
    def set_3p(self, value : float)-> None :
        self._3p = value

    def set_c0(self, value : float)-> None :
        self._c0 = value


    def get_bus_id(self) -> int :
        return self._bus_id
        
    def get_Pg(self) -> float :
        return self._Pg

    def get_Qg(self) -> float :
        return self._Qg

    def get_Qmax(self) -> float :
        return self._Qmax

    def get_Qmin(self) -> float :
        return self._Qmin

    def get_Vg(self) -> float :
        return self._Vg

    def get_mBase(self) -> float :
        return self._mBase

    def get_status(self) -> int :
        return self._status

    def get_Pmax(self) -> float :
        return self._Pmax

    def get_Pmin(self) -> float :
        return self._Pmin

    def get_cost_model(self) -> int :
        return self._cost_model

    def get_startup(self) -> float :
        return self._startup

    def get_shutdown(self) -> float :
        return self._shutdown

    def get_n(self) -> int :
        return self._n

    def get_cn_1(self) -> float :
        return self._cn_1
    
    def get_3p(self) -> float :
        return self._3p

    def get_c0(self) -> float :
        return self._c0

    def get_generator_data(self) -> list:
        return [
            self.get_bus_id(),
            self.get_Pg(),
            self.get_Qg(),
            self.get_Qmax(),
            self.get_Qmin(),
            self.get_Vg(),
            self.get_mBase(),
            self.get_status(),
            self.get_Pmax(),
            self.get_Pmin(),
            self.get_cost_model(),
            self.get_startup(),
            self.get_shutdown(),
            self.get_n(),
            self.get_cn_1(),	
            self.get_3p(),	
            self.get_c0()
        ]



    
        