#!/usr/bin/env python3

from crazyflie_py import Crazyswarm
import numpy as np

def main():

    swarm = Crazyswarm()
    timeHelper = swarm.timeHelper
    allcfs = swarm.allcfs

    allcfs.takeoff(targetHeight=0.5, duration=2)
    timeHelper.sleep(3.0)
    
    for cf in allcfs.crazyflies:
        pos = np.array(cf.initialPosition) + np.array([0.7,0,0.5])
        cf.goTo(pos, 0, 8.0)
        timeHelper.sleep(8.0)
    

    for cf in allcfs.crazyflies:
        pos_2 = np.array(cf.initialPosition) + np.array([0.7,-0.7,0.5])
        cf.goTo(pos_2, 0, 8.0)
        timeHelper.sleep(8.0)

    allcfs.land(targetHeight=0.02, duration=3)
    timeHelper.sleep(3.0)

if __name__ == '__main__':
    main()
