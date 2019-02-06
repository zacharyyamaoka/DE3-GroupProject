import subprocess
import time

def run_bullet(file, run_time):
    # call("ls",shell=True,cwd="~/Documents/Tensegrity_DE3/NTRTsim-master/build/dev/introWorkspace")
    sim = subprocess.Popen(["./App3BarYAML",file], cwd="/home/zy2016/Documents/Tensegrity_DE3/NTRTsim-master/build/dev/introWorkspace")
    time.sleep(run_time)
    sim.kill()
    return sim

sim = run_bullet("iso",5)
