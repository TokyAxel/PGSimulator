import oct2py
from .persistent.Branch import Branch
from .persistent.Bus import Bus
from .persistent.Generator import Generator
from .persistent.Network import Network
import nevergrad as ng
from .nevergradBased.Optimizer import Optimizer
import matplotlib.pyplot as plt
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
        self._marker = [',', '+', '.','<','>','p','h','H','*','x','v','^','s','1','2','3','4','8']

    ### DATA ###

    def set_data_matlab(self, bind : str = None) -> None :
        """
            Get data from matlab file format
        """
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

    def set_optimizer(self, optimizer: Optimizer):
        self._optimizer = optimizer

    ### DEFINITION OF ALL GRID FUNCTIONS

    def AC_power(self, bus: Bus = None, gen: Generator = None, Pg = None) -> complex :
        """ 
            Indicate the generator’s power injection (S^g) or the constant power demand (S^d).
        """
        
        if bus is not None :
            return complex(bus.get_Pd(),bus.get_Qd())
        elif gen is not None : 
            """
                return Power injection and power injection range (min & max)
            """
            if Pg is None :
                return [complex(gen.get_Pg(),gen.get_Qg()), complex(gen.get_Pmax(),gen.get_Qmax()), complex(gen.get_Pmin(),gen.get_Qmin())]
            else :
                return [complex(Pg,gen.get_Qg()), complex(gen.get_Pmax(),gen.get_Qmax()), complex(gen.get_Pmin(),gen.get_Qmin())]
        else :
            raise KeyError("Bus/Generator object not found")

    def transformer(sef, angle, tap):
        """
            Transformer parameters
        """
        value = complex(tap*math.cos(pow(angle,tap)), tap*math.sin(pow(angle,tap))) 
        if abs(value) == 0:
            return complex(1,0)
        else :
            return value 
            
    def loss_function(self, candidate, loss_type : str = "fuel_cost") -> float :
        """
            Objective functions are line loss minimization 
            and generator fuel cost minimization
        """
        
        if loss_type == "line_loss": # INCOMPLETE TODO
            line_loss = 0 
            for g in range(0,len(self._network.get_all_generators())):
                line_loss += candidate[g][0]
            return abs(line_loss)

        elif loss_type == "fuel_cost":
            cost = 0
            power_flow = 0
            count = 0

            """ 
                fuel cost objective function 
            """
            for i in range(0,len(self._network.get_buses())):
                power = 0
                flow = 0
                for g in range(0,len(self._network.get_buses()[i].get_generators())):
                    cost += (self._network.get_buses()[i].get_generators()[g].get_cn_1())*(candidate[0][count][0]**2) 
                    cost += (self._network.get_buses()[i].get_generators()[g].get_3p()*candidate[0][count][0]) + self._network.get_buses()[i].get_generators()[g].get_c0()

                    """ 
                        + Ohm's law and Kirchhoff's current law as penalization (nodal balances) 
                    """
                    ### power generated on each bus
                    power += complex(candidate[0][count][0],candidate[0][count][1])
                    count += 1

                ### fixed demand on each bus
                power -= complex(self._network.get_buses()[i].get_Pd(),self._network.get_buses()[i].get_Qd())
                
                ### Bus shunt 
                power -= ( (complex(self._network.get_buses()[i].get_Gs(),self._network.get_buses()[i].get_Bs())) * (candidate[1][i][0]**2) )

                ### AC power flow
                for br in range(0,len(self._network.get_branches())):
                    if self._network.get_branches()[br].get_fbus() == i+1 :
                        flow += ((( complex(self._network.get_branches()[br].get_admittance().conjugate(), -1. *  self._network.get_branches()[br].get_b()/2) ) * ( (candidate[1][i][0]**2) / (abs(self.transformer(self._network.get_branches()[br].get_angle(), self._network.get_branches()[br].get_ratio())) * abs(self.transformer(self._network.get_branches()[br].get_angle(), self._network.get_branches()[br].get_ratio()))) )))
                        flow -= (((self._network.get_branches()[br].get_admittance().conjugate()) * ( complex(candidate[1][i][0] * candidate[1][(self._network.get_branches()[br].get_tbus())-1][0] * math.cos(candidate[1][i][1] - candidate[1][(self._network.get_branches()[br].get_tbus())-1][1]), candidate[1][i][0] * candidate[1][(self._network.get_branches()[br].get_tbus())-1][0] * math.sin(candidate[1][i][1] - candidate[1][(self._network.get_branches()[br].get_tbus())-1][1])) / self.transformer(self._network.get_branches()[br].get_angle(), self._network.get_branches()[br].get_ratio()) ) ) )

            power_flow += abs( abs(power) - abs(flow) )

            return cost, power_flow

        else :
            print("Please choose between : line_loss, fuel_cost")
            raise KeyError

    def voltage_bounds(self, candidate) -> bool:
        """
            Bus Voltage Limits: Voltages in AC power systems should not vary too far (typically ̆10%) 
        """
        checker = 1
        for i in range(0,len(self._network.get_buses())): 
            if self._network.get_buses()[i].get_Vmin() < candidate[1][i][0] and self._network.get_buses()[i].get_Vmax() > candidate[1][i][0]:
                continue
            else :
                checker = 0
                break

        if checker == 1: return True
        else : return False
     

    def generator_bounds(self,candidate) -> bool:
        """
            Characterization of a generation capability curve
        """
        ### This version use apparent power comparison TODO

        for g in range(0,len(self._network.get_all_generators())):
            if abs(self.AC_power(gen = self._network.get_all_generators()[g])[2]) > abs(complex(candidate[0][g][0], candidate[0][g][1])) or abs(self.AC_power(gen = self._network.get_all_generators()[g])[1]) < abs(complex(candidate[0][g][0], candidate[0][g][1])):
                return False
        return True

    def line_thermal_limit(self, candidate) -> bool: #TODO
        """
            AC power lines have thermal limits to prevent lines from sagging and automatic protection devices from activating. 
            Here we constraint the apparent power under voltage limit
            
            Polar form is used : Sij = Pij + i*Qij
        """
        for i in range(0,len(self._network.get_buses())):
            for br in range(0,len(self._network.get_branches())):
                if self._network.get_branches()[br].get_fbus() == i+1 :
                    pass 
                    if condition == None :
                        return False
        return True

    def phase_angle_difference(self, candidate) -> bool:
        """
            Implemented as a  linear relation of the real and imaginary components of (V_i V_j^*)
        """
        for i in range(0,len(self._network.get_buses())):
            for br in range(0,len(self._network.get_branches())):
                if self._network.get_branches()[br].get_fbus() == i+1 :
                    Vi_Vj_star = complex(candidate[1][i][0] * candidate[1][(self._network.get_branches()[br].get_tbus())-1][0] * math.cos(candidate[1][i][1] - candidate[1][(self._network.get_branches()[br].get_tbus())-1][1]), candidate[1][i][0] * candidate[1][(self._network.get_branches()[br].get_tbus())-1][0] * math.sin(candidate[1][i][1] - candidate[1][(self._network.get_branches()[br].get_tbus())-1][1]))
                    if ( math.tan(self._network.get_branches()[br].get_angmin()) *  Vi_Vj_star.real ) > Vi_Vj_star.imag or ( math.tan(self._network.get_branches()[br].get_angmax()) *  Vi_Vj_star.real ) < Vi_Vj_star.imag :
                        return False
        return True


    ### OPTiMiZATION ###

    def _opt_params(self, len_buses, len_var, bounds : bool = False) -> None :
        """
            Len_var is the number of variable to find : Pg, Qg, Vm and angle
        """
        self._optimizer.set_parametrization(self.get_opt_params(len_buses, len_var, bounds))

    def get_opt_params(self, len_buses, len_var, bounds : bool = False) -> ng.p.Tuple :
        if bounds is False :
            return ng.p.Array(shape=(len_buses, len_var)) #INCOMPLETE TODO
        else :
            lower_bounds_gen = []
            upper_bounds_gen = []
            lower_bounds_bus = []
            upper_bounds_bus = []
            n_rows = 0
            for b in range(0,len(self._network.get_buses())):
                low_b = [] 
                up_b = []
                for g in range(0,len(self._network.get_buses()[b].get_generators())):
                    low_g = []
                    up_g = []
                    n_rows += 1
                    low_g.append(self._network.get_buses()[b].get_generators()[g].get_Pmin())
                    low_g.append(self._network.get_buses()[b].get_generators()[g].get_Qmin())
                    up_g.append(self._network.get_buses()[b].get_generators()[g].get_Pmax())
                    up_g.append(self._network.get_buses()[b].get_generators()[g].get_Qmax())
                    if low_g[0] == up_g[0] :
                        up_g[0] = up_g[0]+1.e-10
                    elif low_g[1] == up_g[1] :
                        up_g[1] = up_g[1]+1.e-10
                    lower_bounds_gen.append(low_g)
                    upper_bounds_gen.append(up_g)

                low_b.append(self._network.get_buses()[b].get_Vmin())
                low_b.append(-180)
                up_b.append(self._network.get_buses()[b].get_Vmax())
                up_b.append(180)

                lower_bounds_bus.append(low_b)
                upper_bounds_bus.append(up_b)

            generators_params = ng.p.Array(shape=(n_rows, int(len_var/2)), lower = np.array(lower_bounds_gen), upper = np.array(upper_bounds_gen))
            buses_params = ng.p.Array(shape=(len(self._network.get_buses()), int(len_var/2)), lower = np.array(lower_bounds_bus), upper = np.array(upper_bounds_bus))

            return ng.p.Tuple(generators_params, buses_params)
            


    def optimizePG(self, optimizer: Optimizer = None, loss_type : str = "fuel_cost", step : int = 1,
                    plot : str = "default") -> None :

        # init params                
        self.step = step
        self.plot = plot

        # optimizer parametrization 
        if optimizer is not None : self.set_optimizer(optimizer)
        self._opt_params(len(self._network.get_buses()), 4, bounds = True)
        
        # init constraints
        constraints = {}
        #constraints.update({"voltage bounds":self.voltage_bounds})
        #constraints.update({"generator_bounds":self.voltage_bounds})
        #constraints.update({"voltage bounds":self.phase_angle_difference})
        
        #let's optimize
        results = self._optimizer.optimize(grid = self , func_to_optimize = self.loss_function, constraints=constraints, step = self.step)

        self.plotResults(results[-1], budgets = results[2], mode = self.plot, average_wide = 1)
        
        return results

    ### PLOTTING

    def plotResults(self, data : dict = {} , budgets : int = None, mode : str = "default", average_wide : int = 0):
        #set the moving average wide
        if average_wide == 0 :
            average_wide = math.ceil(len(data))
    
        if mode == "default" or mode == "save":
            try :
                plt.close("all")  
            except :
                pass

            label_y = list(data.keys())
            X = np.array([i for i in range(0,budgets,self.step)])
                
            #if label y = 1
            if len(label_y) == 1 or len(label_y) == 2 : 
                fig, axs = plt.subplots(2, figsize=(6, 6))        
                
                # data integration        
                it = 3 #index debut cycle
                for n_axs in range(0,len(label_y)):
                    smooth_value = self.moving_average(data[label_y[n_axs]],average_wide)
                    axs[n_axs].plot(X, smooth_value, marker = self._marker[it % len(smooth_value)],markevery = 0.1, alpha=0.5, lw=2, label=label_y[n_axs])
                    it = it + 1
                    
                    # plots parametrizations    
                    axs[n_axs].grid()
                    axs[n_axs].yaxis.set_tick_params(which='major', width=1.00, length=5)
                    axs[n_axs].xaxis.set_tick_params(which='major', width=1.00, length=5)
                    axs[n_axs].xaxis.set_tick_params(which='minor', width=0.75, length=2.5, labelsize=10)
                    axs[n_axs].set_xlabel('Budgets')
                    try :
                        axs[n_axs].set_ylabel(label_y[n_axs])
                    except :
                        pass
                    axs[n_axs].legend()
                

                for n_axs in range(0,2) :
                    if not axs[n_axs].has_data():
                        fig.delaxes(axs[n_axs])
                    
                fig.tight_layout()
                
                if mode == "save": 
                    try:
                        path = "results_"+datetime.now().strftime("%d_%m_%Y")
                        name = path+"/Evaluation_"+datetime.now().strftime("%d%m%Y_%H%M%S")+".png"
                        fig.savefig(name)
                        plt.show()
                    except FileNotFoundError:
                        warnings.warn("Can't find the directory "+path)
                        name = "Evaluation_"+datetime.now().strftime("%d%m%Y_%H%M%S")+".png"
                        fig.savefig(name)
                        plt.show()
                        
                else :
                    plt.show()
                
            else :
                #For label y more than 2
                max_col = math.ceil(len(label_y)/2)
                min_col = math.floor(len(label_y)/2)
                fig, axs = plt.subplots(2, max_col, figsize=(10, 8))        
            
                # data integration
                #texts=[]        
                for n_axs in range(0,max_col) :
                    it = 3 #index debut cycle
                    smooth_value = self.moving_average(data[label_y[n_axs]],average_wide)
                    axs[0][n_axs].plot(X, smooth_value, marker = self._marker[it % len(smooth_value)],markevery = 0.1, alpha=0.5, lw=2, label=label_y[n_axs])                
                    it = it + 1     
                
                for n_axs in range(0,min_col) :
                    it = 3 #index debut cycle
                    smooth_value = self.moving_average(data[label_y[max_col+n_axs]],average_wide)
                    axs[1][n_axs].plot(X, smooth_value, marker = self._marker[it % len(smooth_value)],markevery = 0.1, alpha=0.5, lw=2, label=label_y[max_col+n_axs])              
                    it = it + 1                

                # plots parametrizations   
                for row in range (0,2):
                    if row == 0 :
                        for n_axs in range(0,max_col) :
                            axs[row][n_axs].grid()
                            axs[row][n_axs].yaxis.set_tick_params(which='major', width=1.00, length=5)
                            axs[row][n_axs].xaxis.set_tick_params(which='major', width=1.00, length=5)
                            axs[row][n_axs].xaxis.set_tick_params(which='minor', width=0.75, length=2.5, labelsize=10)
                            axs[row][n_axs].set_xlabel('Budgets')
                            axs[row][n_axs].set_ylabel(label_y[n_axs])
                            axs[row][n_axs].legend()
                    else :
                        for n_axs in range(0,min_col) :
                            axs[row][n_axs].grid()
                            axs[row][n_axs].yaxis.set_tick_params(which='major', width=1.00, length=5)
                            axs[row][n_axs].xaxis.set_tick_params(which='major', width=1.00, length=5)
                            axs[row][n_axs].xaxis.set_tick_params(which='minor', width=0.75, length=2.5, labelsize=10)
                            axs[row][n_axs].set_xlabel('Budgets')
                            axs[row][n_axs].set_ylabel(label_y[max_col+n_axs])
                            axs[row][n_axs].legend()                        
                
                for row in range (0,2):
                    for n_axs in range(0,max_col) :
                        if not axs[row][n_axs].has_data():
                            fig.delaxes(axs[row][n_axs])
                        
                fig.tight_layout()
                
                if mode == "save": 
                    try:
                        path = "results_"+datetime.now().strftime("%d_%m_%Y")
                        name = path+"/Evaluation_"+datetime.now().strftime("%d%m%Y_%H%M%S")+".png"
                        fig.savefig(name)
                        plt.show()
                    except FileNotFoundError:
                        warnings.warn("Can't find the directory "+path)
                        name = "Evaluation_"+datetime.now().strftime("%d%m%Y_%H%M%S")+".png"
                        fig.savefig(name)
                        plt.show()
                        
                else :
                    plt.show()

        elif mode == "None" :
            pass
        else :
            warnings.warn("Choose an available option : default, save or None")
            #plt.show()
   
    def moving_average(self, x, w):
        return np.convolve(x, np.ones(w), 'valid') / w