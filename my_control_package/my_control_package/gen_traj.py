#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.gridspec as gridspec
import argparse
import pandas as pd
# import scipy.interpolate
import scipy.optimize

import uav_trajectory

import rclpy
from rclpy.node import Node
from std_msgs.msg import Bool 


# computes the difference between current interpolation and desired values
def func(coefficients, times, values, piece_length):
  result = 0
  i = 0
  for t, value in zip(times, values):
    if t > (i+1) * piece_length:
      i = i + 1
    estimate = np.polyval(coefficients[i*8:(i+1)*8], t - i * piece_length)
    # print(coefficients[i*8:(i+1)*8], t - i * piece_length, estimate)
    result += (value - estimate) ** 2 #np.sum((values - estimates) ** 2)
  # print(coefficients, result)
  return result

# constraint to match values between spline pieces
# def func_eq_constraint_val(coefficients, i, piece_length):
#   result = 0
#   end_val = np.polyval(coefficients[(i-1)*8:i*8], piece_length)
#   start_val = np.polyval(coefficients[i*8:(i+1)*8], 0)
#   return end_val - start_val

def func_eq_constraint_der(coefficients, i, piece_length, order):
  result = 0
  last_der = np.polyder(coefficients[(i-1)*8:i*8], order)
  this_der = np.polyder(coefficients[i*8:(i+1)*8], order)

  end_val = np.polyval(last_der, piece_length)
  start_val = np.polyval(this_der, 0)
  return end_val - start_val

def func_eq_constraint_der_value(coefficients, i, t, desired_value, order):
  result = 0
  der = np.polyder(coefficients[i*8:(i+1)*8], order)

  value = np.polyval(der, t)
  return value - desired_value

# def func_eq_constraint(coefficients, tss, yawss):
#   result = 0
#   last_derivative = None
#   for ts, yaws, i in zip(tss, yawss, range(0, len(tss))):
#     derivative = np.polyder(coefficients[i*8:(i+1)*8])
#     if last_derivative is not None:
#       result += np.polyval(derivative, 0) - last_derivative
#     last_derivative = np.polyval(derivative, tss[-1])


  # # apply coefficients to trajectory
  # for i,p in enumerate(traj.polynomials):
  #   p.pyaw.p = coefficients[i*8:(i+1)*8]
  # # evaluate at each timestep and compute the sum of squared differences
  # result = 0
  # for t,yaw in zip(ts,yaws):
  #   e = traj.eval(t)
  #   result += (e.yaw - yaw) ** 2
  # return result

def generate_trajectory(data, num_pieces):
  piece_length = data[-1,0] / num_pieces

  x0 = np.zeros(num_pieces * 8)

  constraints = []
  # piecewise values and derivatives have to match
  for i in range(1, num_pieces):
    for order in range(0, 4):
      constraints.append({'type': 'eq', 'fun': func_eq_constraint_der, 'args': (i, piece_length, order)})

  # zero derivative at the beginning and end
  for order in range(1, 3):
    constraints.append({'type': 'eq', 'fun': func_eq_constraint_der_value, 'args': (0, 0, 0, order)})
    constraints.append({'type': 'eq', 'fun': func_eq_constraint_der_value, 'args': (num_pieces-1, piece_length, 0, order)})


  resX = scipy.optimize.minimize(func, x0, (data[:,0], data[:,1], piece_length), method="SLSQP", options={"maxiter": 1000}, 
    constraints=constraints
    )
  resY = scipy.optimize.minimize(func, x0, (data[:,0], data[:,2], piece_length), method="SLSQP", options={"maxiter": 1000}, 
    constraints=constraints
    )
  resZ = scipy.optimize.minimize(func, x0, (data[:,0], data[:,3], piece_length), method="SLSQP", options={"maxiter": 1000}, 
    constraints=constraints
    )

  resYaw = scipy.optimize.minimize(func, x0, (data[:,0], data[:,4], piece_length), method="SLSQP", options={"maxiter": 1000}, 
    constraints=constraints
    )

  traj = uav_trajectory.Trajectory()
  traj.polynomials = [uav_trajectory.Polynomial4D(
    piece_length, 
    np.array(resX.x[i*8:(i+1)*8][::-1]),
    np.array(resY.x[i*8:(i+1)*8][::-1]),
    np.array(resZ.x[i*8:(i+1)*8][::-1]),
    np.array(resYaw.x[i*8:(i+1)*8][::-1])) for i in range(0, num_pieces)]
    
  traj.duration = data[-1,0]
  return traj


class GenTraj(Node):

    def __init__(self, inputPath: str, thinnedPath: str, outPath: str, num_pieces: int):
        super().__init__('start_flight_publisher')
        self.get_logger().info('Trajectory generation node initializing...')

        self.publisher_ = self.create_publisher(Bool, 'start_flight', 10)

        self.inputPath = inputPath
        self.thinnedPath = thinnedPath
        self.outPath = outPath
        self.num_pieces = num_pieces
    
    def publish_bool(self, var: bool):
        msg = Bool()
        msg.data = var
        self.publisher_.publish(msg)
        self.get_logger().info(f'Start_flight: {msg.data}')


    def thin_data(self):
        # read csv into data frame
        df = pd.read_csv(self.inputPath)

        # keep every nth row
        df_thinned = df.iloc[::10]
        df_thinned.to_csv(self.thinnedPath, index=False)
        self.get_logger().info(f"Data thinned and saved to {self.thinnedPath}")
    
    def gen_traj(self):
        data = np.loadtxt(self.thinnedPath, delimiter=',', skiprows=1)
        traj = generate_trajectory(data, self.num_pieces)
        traj.savecsv(self.outPath)
        self.get_logger().info(f"Trajectory saved to {self.outPath}")
    

def main(args=None):
    inputPath = '/home/vincent/matlab_code/Vincent_dynamic_example_250225/robot_waypoints.csv'
    thinnedPath = '/home/vincent/path_data/thinned.csv'
    outPath = '/home/vincent/path_data/traj.csv'
    rclpy.init(args=args)
    node = GenTraj(inputPath, thinnedPath, outPath, 10)

    # Explicitly call functions (order matters)
    node.thin_data()
    node.gen_traj()
    node.publish_bool(True)

    node.get_logger().info("All tasks completed. Shutting down.")
    node.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
   main()
