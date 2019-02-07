from drop_testing import *

max_accels = []
params = []

iter = 100

# default params
drop_h = 50 #dm
strut_K = 900
elastic_K = 5
strut_L = 0.3
elastic_L = 0

parameters = [drop_h,strut_K,elastic_K,strut_L,elastic_L]

data = drop_test("feb7",parameters)
print(data['max_a'])
print(data['L_actual'])
