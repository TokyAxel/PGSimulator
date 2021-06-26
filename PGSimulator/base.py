from .persistent.Branch import Branch
from .persistent.Bus import Bus
from .persistent.Generator import Generator
from .persistent.Network import Network
import nevergrad as ng
from .nevergradBased.Optimizer import Optimizer
import numpy as np
import cmath
import math
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
        buses = []
        for i in range(0, self._raw_data["bus"].shape[0]):
            buses.append(Bus(data = self._raw_data["bus"][i]))

        ### merge "gen" and "gencost" matrix 
        self._raw_data["all_gen"] = np.concatenate((self._raw_data["gen"],self._raw_data["gencost"]),axis=1)

        ### Adding generators
        for i in range(0, self._raw_data["gen"].shape[0]):
            buses[int(self._raw_data["gen"][i][0] - 1)].add_generator(data = self._raw_data["all_gen"][i])
        
        ### Adding buses
        self._network.add_buses(buses)

        ### Adding branches
        for i in range(0,self._raw_data["branch"].shape[0]):
            self._network.add_branch(Branch(self._raw_data["branch"][i]))

    def get_network(self) -> Network :
        return self._network

    def get_network_data(self) -> dict :
        return self._network.get_network_data()

    ### DEFINITION OF ALL GRID FUNCTIONS

    def AC_power(self, bus: Bus = None, gen: Generator = None, Pg = None) -> complex :
        """ 
            indicate the generator’s power injection (S^g) or the constant power demand (S^d).
        """
        
        if bus is not None :
            return complex(bus.get_Pd(),bus.get_Qd())
        elif gen is not None : 
            """return Power injection and power injection range (min & max)"""
            if Pg is None :
                return [complex(gen.get_Pg(),gen.get_Qg()), complex(gen.get_Pmax(),gen.get_Qmax()), complex(gen.get_Pmin(),gen.get_Qmin())]
            else :
                return [complex(Pg,gen.get_Qg()), complex(gen.get_Pmax(),gen.get_Qmax()), complex(gen.get_Pmin(),gen.get_Qmin())]
        else :
            raise KeyError("Bus/Generator object not found")

    def br_admittance(self, r ,x ):
        return complex(r/((r*r)+(x*x)), (-1. * x ) / ((r*r)+(x*x))) 

    def transformer(sef, angle, t):
        value = complex(t*math.cos(pow(angle,t)), t*math.sin(pow(angle,t))) 
        if abs(value) == 0:
            return complex(1,0)
        else :
            return value 
            
    def loss_function(self, candidate, loss_type : str = "fuel_cost") -> float :
        """
            Objective functions are line loss minimization 
            and generator fuel cost minimization
        """
        
        if loss_type == "line_loss": # INCOMPLETE
            line_loss = 0 
            for g in range(0,len(self._network.get_all_generators())):
                line_loss += candidate[i][0]
            return abs(line_loss)

        elif loss_type == "fuel_cost":
            cost = 0
            

            """ fuel cost objective function """
            for i in range(0,len(self._network.get_buses())):
                power = 0
                flow = 0
                for g in range(0,len(self._network.get_buses()[i].get_generators())):
                    try :
                        cost += (self._network.get_buses()[i].get_generators()[g].get_cn_1()*(candidate[i][0]*candidate[i][0])) 
                        + (self._network.get_buses()[i].get_generators()[g].get_3p()*candidate[i][0]) + self._network.get_buses()[i].get_generators()[g].get_c0()
                    except :
                        print("pass cause bus doesn't have gen")
                        pass

                """ + Ohm's law and Kirchhoff's current law as penalization """
                ### power generated on each bus
                for g in range(0,len(self._network.get_buses()[i].get_generators())):
                    try:
                        power += complex(candidate[i][0],candidate[i][1])
                    except:
                        print("pass cause bus doesn't have gen")
                        pass

                ### fixed demand on each bus
                power -= complex(self._network.get_buses()[i].get_Pd(),self._network.get_buses()[i].get_Qd())
                
                ### Bus shunt 
                power -= ( (complex(self._network.get_buses()[i].get_Gs(),self._network.get_buses()[i].get_Bs()))
                * (candidate[i][2] * candidate[i][2]) )

                ### AC power flow
                for br in range(0,len(self._network.get_branches())):
                    if self._network.get_branches()[br].get_fbus() == i+1 :
                        ### S_lij
                        flow += ( 
                        (( complex(self.br_admittance(self._network.get_branches()[br].get_r(),self._network.get_branches()[br].get_x()).conjugate(), -1. *  self._network.get_branches()[br].get_b()/2) )
                        * ( (candidate[i][2] * candidate[i][2])
                        / (abs(self.transformer(self._network.get_branches()[br].get_angle(), self._network.get_branches()[br].get_ratio())) * abs(self.transformer(self._network.get_branches()[br].get_angle(), self._network.get_branches()[br].get_ratio()))) ))
                        - ((self.br_admittance(self._network.get_branches()[br].get_r(),self._network.get_branches()[br].get_x()).conjugate()) 
                        * ( complex(candidate[i][2] * self._network.get_buses()[(self._network.get_branches()[br].get_tbus())-1].get_Vm() * math.cos(candidate[i][3] - self._network.get_buses()[(self._network.get_branches()[br].get_tbus())-1].get_Va()), candidate[i][2] * self._network.get_buses()[(self._network.get_branches()[br].get_tbus())-1].get_Vm() * math.sin(candidate[i][3] - self._network.get_buses()[(self._network.get_branches()[br].get_tbus())-1].get_Va()))
                        / self.transformer(self._network.get_branches()[br].get_angle(), self._network.get_branches()[br].get_ratio()) ) ) 
                        )
                        ### S_lji
                        #flow += () * ( ) 
                        #- () * ( / )

                cost += abs( power - flow )
            return cost

        else :
            print("Please choose between : line_loss, fuel_cost")
            raise KeyError

    def voltage_bounds(self, candidate) -> bool:
        """
            Bus Voltage Limits: Voltages in AC power systems shouldnot  vary  too  far  (typically ̆10%) 
        """
        checker = 1
        for i in range(0,len(self._network.get_buses())): 
            if self._network.get_buses()[i].get_Vmin() < candidate[i][2] and self._network.get_buses()[i].get_Vmax() > candidate[i][2]:
                continue
            else :
                checker = 0
                break

        if checker == 1: return True
        else : return False
     

    def generator_bounds(self,candidate) -> bool:
        """
            characterization of a generation capability curve
        """
        ### This version use apparent power comparison
        for g in range(0,len(self._network.get_all_generators())):
            if abs(self.AC_power(gen = self._network.get_all_generators()[g])[2]) > abs(complex(candidate[i][0], candidate[i][1])) or abs(self.AC_power(gen = self._network.get_all_generators()[g])[1]) < abs(complex(candidate[i][0], candidate[i][1])):
                return False
        return True

    ### OPTiMiZATION ###

    def _opt_params(self, len_buses, len_var, bounds : bool = False) -> None :
        """
            len_var is the number of variable to find : Pg, Qg, Vm and angle
        """
        self._optimizer.set_parametrization(self.get_opt_params(len_buses, len_var, bounds))

    def get_opt_params(self, len_buses, len_var, bounds : bool = False) -> ng.p.Array :
        if bounds is False :
            return ng.p.Array(shape=(len_buses, len_var))
        else :
            #variable_parametrization = []
            #for b in range(0,len(self._network.get_buses())):
                #try : 
                    ### HERE WE STILL SUPPOSE ONE BUSE == ONE GENERATOR
                    #for g in range(0,len(self._network.get_buses()[b].get_generators())):
                        #variable_parametrization += [self._network.get_buses()[b].get_generators()[g].get_P_bounds()]
                        #variable_parametrization += [self._network.get_buses()[b].get_generators()[g].get_P_bounds()]
                #except :
                    #variable_parametrization += [ng.p.Choice([0.,0.])]

                #variable_parametrization += [ng.p.Scalar(lower=self._network.get_buses()[b].get_Vmin() ,upper=self._network.get_buses()[b].get_Vmax())]
            #print(ng.p.Tuple(*variable_parametrization))
            #return ng.p.Tuple(*variable_parametrization)

            lower_bounds = []
            upper_bounds = []
            for b in range(0,len(self._network.get_buses())):
                low = []
                up = []
                try : 
                    ### HERE WE STILL SUPPOSE ONE BUSE == ONE GENERATOR
                    for g in range(0,len(self._network.get_buses()[b].get_generators())):
                        low.append(self._network.get_buses()[b].get_generators()[g].get_Pmin())
                        low.append(self._network.get_buses()[b].get_generators()[g].get_Qmin())
                        up.append(self._network.get_buses()[b].get_generators()[g].get_Pmax())
                        up.append(self._network.get_buses()[b].get_generators()[g].get_Qmax())
                        if low[0] == up[0] :
                            up[0] = up[0]+1.e-10

                except :
                    low.append(0.)
                    low.append(0.)
                    upper.append(1.e-10)
                    upper.append(1.e-10)
                
                low.append(self._network.get_buses()[b].get_Vmin())
                low.append(-180)
                up.append(self._network.get_buses()[b].get_Vmax())
                up.append(180)

                lower_bounds.append(low)
                upper_bounds.append(up)

            return ng.p.Array(shape=(len_buses, len_var), lower = np.array(lower_bounds), upper = np.array(upper_bounds))
            


    def optimizePG(self, optimizer: Optimizer = None, loss_type : str = "fuel_cost", step : int = 1,
                    plot : str = "default"):

        # init params                
        self.step = step
        self.plot = plot

        # optimizer parametrization 
        self._opt_params(len(self._network.get_buses()), 4, bounds = True)
        
        # init constraints
        constraints = None
        #constraints.update({"voltage bounds":self.voltage_bounds})
        #constraints.update({"generator_bounds":self.voltage_bounds})
        
        #let's optimize
        results = self._optimizer.optimize(grid = self , func_to_optimize = self.loss_function, constraints=constraints, step = self.step)

        #self.plotResults(results, mode = self.plot , time_interval = self.time_interval, average_wide = self.average_wide)
        
        return results

