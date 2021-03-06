# Copyright 2019 ROBOTIS CO., LTD.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# /* Author: Darby Lim */

import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.actions import ExecuteProcess
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    use_sim_time = True
    world = 'worlds/cafe.world'
    launch_file_dir = os.path.join(get_package_share_directory('confbot_bringup'), 'launch')

    return LaunchDescription([
        DeclareLaunchArgument(
            'use_sim_time',
            default_value=str(use_sim_time),
            description='Use simulation (Gazebo) clock if true'),
        ExecuteProcess(
            cmd=[
                'gazebo', '--verbose', world,
                '-s', 'libgazebo_ros_factory.so', '-s', 'libgazebo_ros_init.so'
            ],
            output='screen'),

        IncludeLaunchDescription(
            PythonLaunchDescriptionSource([launch_file_dir, '/confbot_state_publisher.launch.py']),
            launch_arguments={'use_sim_time': LaunchConfiguration('use_sim_time')}.items(),
        ),
        # publishing static transforms for caster wheels
        # TODO remove this once thee is a joint_state_controller for gazebo/ros2
        Node(
            package='tf2_ros',
            node_executable='static_transform_publisher',
            node_name='static_tf_caster_wheel_front',
            arguments=[
                '0.4', '0.0', '-0.05', '0', '0', '0', 'base_link', 'caster_wheel_front_link']),
        Node(
            package='tf2_ros',
            node_executable='static_transform_publisher',
            node_name='static_tf_caster_wheel_rear',
            arguments=[
                '-0.4', '0.0', '-0.05', '0', '0', '0', 'base_link', 'caster_wheel_rear_link']),
    ])
