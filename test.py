### test function

import PGSimulator as pgs

### init empty network
print(pgs)
net = pgs.PGSimulator()
print(net.get_network())

## init optimizers
opt_CMA = pgs.Optimizer(opt = ["CMA"], budget = [1000], num_worker = 1) 
opt_CMA_30 = pgs.Optimizer(opt = ["CMA"], budget = [200], num_worker = 30)
opt_NGOpt = pgs.Optimizer(opt = ["NGOpt"], budget = [1000], num_worker = 1) 

### load dataset on matlab
"""
    Case3_lmdb
"""
print("CASE 3")
net.set_data_matlab("PGSimulator/data/pglib-opf/pglib_opf_case3_lmbd.m")
#print(net.get_network_data())

### Optimization
#print(net.optimizePG(loss_type = "fuel_cost"))

print(net.optimizePG(optimizer = opt_NGOpt, loss_type = "fuel_cost"))
#Default optimizer (OnePlusOne)
#print(net.optimizePG(loss_type = "fuel_cost"))

"""
    case5_pjm
"""
print("CASE 5")
net.set_data_matlab("PGSimulator/data/pglib-opf/pglib_opf_case5_pjm.m")
#print(net.get_network_data())

### Optimization
#print(net.optimizePG(loss_type = "fuel_cost"))

print(net.optimizePG(optimizer = opt_NGOpt, loss_type = "fuel_cost"))
#Default optimizer (OnePlusOne)
#print(net.optimizePG(loss_type = "fuel_cost"))

"""
    case14_ieee
"""
print("CASE 14")
net.set_data_matlab("PGSimulator/data/pglib-opf/pglib_opf_case14_ieee.m")
#print(net.get_network_data())

### Optimization
#print(net.optimizePG(loss_type = "fuel_cost"))

print(net.optimizePG(optimizer = opt_NGOpt, loss_type = "fuel_cost"))
#Default optimizer (OnePlusOne)
#print(net.optimizePG(loss_type = "fuel_cost"))

### Test unitaire des fonctions
#print(net.AC_power(net.get_network().get_buses()[0]))
