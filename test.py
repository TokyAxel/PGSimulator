### test function

import PGSimulator as pgs

### init empty network
print(pgs)
net = pgs.PGSimulator()
print(net.get_network())

## init optimizers
opt_CMA = pgs.Optimizer(opt = ["CMA"], budget = [20], num_worker = 1) 
opt_CMA_30 = pgs.Optimizer(opt = ["CMA"], budget = [20], num_worker = 30)

### load dataset on matlab

net.set_data_matlab("PGSimulator/data/pglib-opf/pglib_opf_case3_lmbd.m")
print(net.get_network_data())

### Optimization
print(net.optimizePG())

### Test unitaire des fonctions
print(net.S(net.get_network().get_buses()[0]))
