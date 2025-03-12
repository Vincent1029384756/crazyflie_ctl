import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, OpaqueFunction
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
    
    # Conditionally include `my_node` based on the script argument
    def launch_my_node(context, *args, **kwargs):
        script_value = context.perform_substitution(script)
        if script_value:  # Only add `my_node` if `script` is non-empty
            return [
                Node(
                    package='my_control_package',
                    executable=script_value,
                    name=script_value,
                    output='screen',
                    parameters=[{
                        'use_sim_time': PythonExpression(["'", backend, "' == 'sim'"])
                    }]
                )
            ]
        return []

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

    dip_detect = Node(
        package="my_control_package",
            executable="dip_detect",
            name="altitude_dip_detector",
            output="screen"
    )

    # Return the launch description with all components
    return LaunchDescription([
        script_launch_arg,
        backend_launch_arg,
        crazyflie_launch,
        emergency_node,
        battery_node,
        dip_detect,
        OpaqueFunction(function=launch_my_node)
    ])