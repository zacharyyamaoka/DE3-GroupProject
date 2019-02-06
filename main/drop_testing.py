import os
import sys
import numpy as np

sys.path.append(os.path.join(os.getcwd(), "utils"))
sys.path.append(os.path.join(os.getcwd(), "solver"))

from run_bullet import *
from parse_data_func import *
from load_structure import *
from save_structure import *
from solver_func import *
from Debugger import *

Viz = Debugger()
load_file = 'drone'
save_file = 'industry'

drop_h = 50 #dm
strut_K = 800
elastic_K = 5
#Load up structure
K, L, X = loadFusionStructure(load_file, strut_K = 800, elastic_K = 5, strut_L = 0.3, elastic_L = 0)

#find stability
K, L, X = find_stability(K, L, X, Viz, display_time=1)
save_solved_fusion360('iso',X,K,L,strut_K,elastic_K)

# K, L, X = find_stability(K, L, X)
# plt.clf()
#Save back to YAML
save_YAML(X,K,save_file)
save_DROP_YAML(save_file,translation = [0, drop_h, 0]) # dm

run_bullet("industry",3)
t, x, v, a = parse_data()
max_a, a_norm = get_max_a(a)

plt.figure(5)
plt.plot(t,a_norm)

drop_height = drop_h/10 #100 dm
exp_t = np.sqrt(2*drop_height/9.81)
ax = plt.gca()
# ax.set_xlim([exp_t-0.1,exp_t+0.1])
ax.text(0.9, 0.9, 'max: ' + str(round(max_a,3)) + " m/s^2", horizontalalignment='center',verticalalignment='center', transform=ax.transAxes)
# plt.show()
Viz.clear()
Viz.draw_Pos(x)
Viz.display(time=1, azimuth=45, altitude=20, drop_port=True)

# plt.show()

plt.pause(100)
