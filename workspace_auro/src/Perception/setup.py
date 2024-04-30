from setuptools import find_packages, setup

package_name = "Perception"

setup(
    name=package_name,
    version="0.0.0",
    packages=find_packages(exclude=["test"]),
    data_files=[
        ("share/ament_index/resource_index/packages", ["resource/" + package_name]),
        ("share/" + package_name, ["package.xml"]),
    ],
    install_requires=["setuptools"],
    zip_safe=True,
    maintainer="user",
    maintainer_email="ashwinnkal@users.noreply.github.com",
    description="Contains all funtionalities / nodes related to perception + sensorfusion of the robot",
    license="MIT License",
    tests_require=["pytest"],
    entry_points={
        "console_scripts": ['parse_lidar = Perception.parse_lidar:main',
                            'parse_camera = Perception.parse_camera:main'],
    },
)
