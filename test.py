### test function

import PGSimulator as pgs

### init empty network
print(pgs)
net = pgs.PGSimulator()
print(net.get_network())

### load dataset on matlab

net.set_data_matlab("PGSimulator/data/pglib-opf/pglib_opf_case3_lmbd.m")
print(net.get_network_data())
