import numpy as np
import pybullet as p
import time
import math


class Drone:

    def __init__(self):
        p_id = p.connect(p.GUI)
        p.setGravity(0, 0, -10)
        plane = p.loadURDF("plane.urdf")
        dronePos = [0, 0, 0.2]
        self.drone = p.loadURDF("quadrotor.urdf", dronePos)
        #p.createConstraint(self.drone, -1, -1, -1, p.JOINT_PRISMATIC, [0, 0, 1], [0, 0, 0], [0, 0, 0])    #Constrain to move only in a particular direction(to prevent flipping out)

    def show(self, x_action, y_action, z_action):
        #force_x = 10*x_action
        force_y = 25*y_action
        #force_z = 10*z_action
        p.applyExternalForce(self.drone, -1, [0, 0, force_y], [0, 0, 0], p.WORLD_FRAME)
        #p.applyExternalForce(self.drone, -1, [0, force_x, 0], [0, 0, 0], p.WORLD_FRAME)
        # p.applyExternalForce(self.drone, -1, [force_z, 0, 0], [0, 0, 0], p.WORLD_FRAME)
        p.stepSimulation()
        time.sleep(1. / 240.)

