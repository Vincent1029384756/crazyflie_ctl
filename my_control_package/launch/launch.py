import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PythonExpression
from launch_ros.actions import Node

def generate_launch_description():
    # Declare script and backend as launch arguments
    script = LaunchConfiguration('script')
    backend = LaunchConfiguration('backend')

    # Declare the arguments for dynamic configuration
    script_launch_arg = DeclareLaunchArgument('script', default_value='')
    backend_launch_arg = DeclareLaunchArgument('backend', default_value='cpp')

    # Include the Crazyflie launch file
    crazyflie_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory('crazyflie'), 'launch'),
            '/launch.py']),
        launch_arguments={
            'backend': backend,
            }.items()
    )
    
    # Node configuration for the dynamically launched script
    my_node = Node(
        package='my_control_package',
        executable=script,  # Pass the dynamic script name
        name=script,
        output='screen',
        parameters=[{
            'use_sim_time': PythonExpression(["'", backend, "' == 'sim'"])
        }]
    )

    # Add the EmergencyNode
    emergency_node = Node(
        package='my_control_package', 
        executable='emergency_node',    
        name='emergency_node',
        output='screen'
    )

    battery_node = Node(
        package='my_control_package',
        executable='battery_reader',
        name='battery_node',
        output='screen'
    )

    # Return the launch description with all components
    return LaunchDescription([
        script_launch_arg,
        backend_launch_arg,
        crazyflie_launch,
        my_node,
        emergency_node,
        battery_node
    ])