Makesure you install these
  **Nav2** - [Github](https://github.com/ros-planning/navigation2) and [Documentation](https://navigation.ros.org/)
  
  **Slam_toolbox** - [Github](https://github.com/SteveMacenski/slam_toolbox)

  To install, do:
  1. "sudo apt install ros-humble-twist-mux"
  2. "sudo apt install ros-humble-navigation2" to get the "from nav2_simple_commander.robot_navigator import BasicNavigator" working, on the website, https://navigation.ros.org/getting_started/index.html
      - But this is only in simulation. To get the actual robot to do this, we use the below...
  3. "sudo apt install ros-humble-slam-toolbox"
  4. "pip3 install transforms3d"
  5. "sudo apt install ros-humble-gazebo-ros-pkgs"
      - This is to follow the README.md file in the "SLAM" folder

3. **Build the workspace:**
   ```sh
   cd ~/sim_roam_ws
   colcon build --symlink-install

4. **Source the setup script:**
   ```sh
   source /install/setup.bash
   
## Hey make sure you do this for robot to be initialised within gazebo


1. **Copy the entire robot_description package to the Gazebo models directory**
   
   ```sh
   cp -r robot_description ~/.gazebo/models/robot_description

2. **Remove all contents from the copied robot_description package except for the meshes directory**

   - Navigate to the robot_description directory in the Gazebo models directory:

       cd ~/.gazebo/models/robot_description

   - Then, remove all directories except for meshes:

#### to run

#### In window 1,
`ros2 launch robot_simulation house_sim.launch.py`

#### In window 2,
`ros2 launch robot_simulation autonomous_navigation.launch.py`

#### In windows 3,
`ros2 run robot_patrol robot_patrol` 
