# This readme is for our final project submission, do rollover edits for submitting along the final project.

## Else, add all raw informations that could be ellabrated / referenced for our faster project development to primer101.md file.

## **things below the border will be deleted after final merge, until it is used as todos, donts or checklist for everyone**

---

# 1. Project Abstract / Intro

## 1.1 Getting started

## 1.2 Requirements

- Framework: ROS2 Humble
- OS: ubuntu22
- Simulator: Gezebo
- check pip requirement.txt, ros2 pkg's for packages,
-

# 2. Project mindmap

this section will contain the flowdiagrams to display the entire process of the project, and explains each part of the processes.

## 2.1 subsections for each modules, say perception.

## Authors

## Bibliography / Citations

## License

MIT License

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

# 3 Explanation of the Code

NavigationAndPlanning
- SLAM
    - the SLAM toolbox has many differnet modes- we'll be running it in Online (working on a live adta stream rather than recorded logs) and Asynchronous (Always process the most recent scan to avoid lagging, even if that means skipping scans)
- This code uses the ROS slam_toolbox for localization and Navigation/Planning
- Localization is NOT Navigation
- Navigation uses the MAP we get from SLAM, but this is where we calculate a path to reach an objective (like how do I reach this object)
- We can either use Feature SLAM or Grid SLAM
- the SLAM toolbox we're using is a Grid based SLAM

Localization
- Uses Odometry: Odometry effectively measures robot velocity (through wheel angular position)- this is integrated *smoothly* over time to estimate position
    - But this needs to be corrected
- We introduce a "map" frame- the robot's position (base_link) is compared to this frame, and then the "odom" frame, or world coordinate frame

# Steps (From Video, "Easy SLAM with ROS using slam_toolbox" by Articualted Robotics)
- do "cp /opt/ros/humble/share/slam_toolbox/config/mapper_params_online_async.yaml ." into this workspace
- if we look in the "# ROS Parameters" section of this file, we see it reads from the /scan topic of the actual TurtleBot 4
    - we can change mode to be "mapping" or "localization"
- to use in real life, do "ros2 launch slam_toolbox_online_async_launch.py params_file:=/Chemical-Plant-Inspector/workspace_auro/src/NavigationAndPlanning/NavigationAndPlanning/mapper_params_online_async.yaml use_sim_time:=false
- 