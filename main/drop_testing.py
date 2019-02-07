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

def drop_test(file, params, show_accel=True, show_pos=False):
    #Inputs - File name and structure paremters
    #Returns - Max acceleration
    #Load up structure
    if show_pos:
        Viz = Debugger()
    load_file = file
    save_file = file

    drop_h = params[0] #dm
    strut_K = params[1]
    elastic_K = params[2]
    strut_L = params[3]
    elastic_L = params[4]

    K, L, X = loadFusionStructure(load_file, strut_K, elastic_K, strut_L, elastic_L)

    #find stability
    K, L, X = find_stability(K, L, X)
    # K, L, X = find_stability(K, L, X, Viz, display_time=1)
    overwrite_fusion360_file(load_file,X,K,L,strut_K,elastic_K)

    #Save back to YAML
    save_YAML(X,K,save_file)
    save_DROP_YAML(save_file,translation = [0, drop_h, 0]) # dm

    run_bullet(save_file,3)
    t, x, v, a = parse_data()
    max_a, a_norm = get_max_a(a)
    L_actual = get_actual_L(X)

    if show_accel:
        plt.figure(5)
        plt.plot(t,a_norm)

        drop_height = drop_h/10 #100 dm
        exp_t = np.sqrt(2*drop_height/9.81)
        ax = plt.gca()
        ax.set_xlim([exp_t-0.1,exp_t+0.1])
        ax.text(0.9, 0.9, 'max: ' + str(round(max_a,3)) + " m/s^2", horizontalalignment='center',verticalalignment='center', transform=ax.transAxes)

    if show_pos:
        Viz.clear()
        Viz.draw_Pos(x)
        Viz.display(time=1, azimuth=45, altitude=20, drop_port=True)

    if show_pos or show_accel:
        plt.pause(3)

    data_pkg = dict()
    data_pkg['K'] = K
    data_pkg['L'] = L
    data_pkg['X'] = X
    data_pkg['L_actual'] = L_actual
    data_pkg['max_a'] = max_a
    data_pkg['x'] = x
    data_pkg['v'] = v
    data_pkg['a'] = a
    data_pkg['t'] = t

    return data_pkg

# max_a = drop_test("feb7",parameters)
