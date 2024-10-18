import os
from ament_index_python.packages import get_package_share_directory

# launch related imports
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PythonExpression
from launch_ros.actions import Node

# Defines variable to store the name of the script to run
script = LaunchConfiguration('script')
# Defines variable to store the type of backend to use ('cpp' or 'sim')
backend = LaunchConfiguration('backend')

# Defines parameters user can pass when launching
script_launch_arg = DeclareLaunchArgument()