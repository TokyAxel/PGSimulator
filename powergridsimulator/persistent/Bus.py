class Bus:
    """
        Bus classe : representation of nodes in network with some parameters

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


    """ : float

    def __init__(self, id : int = None, btype : int = None ) -> None:
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

    def set_id(self, value : int) -> None :
        self._id = value
    
    def set_type(self, value : int ) -> None :
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

    def set_baseKV(self, value : float)-> None :
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

    def get_baseKV(self) -> float :
        return self._baseKV

    def get_zone(self) -> int :
        return self._zone

    def get_Vmax(self) -> float :
        return self._Vmax

    def get_Vmin(self) -> float :
        return self._Vmin



    
        