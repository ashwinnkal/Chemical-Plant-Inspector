from setuptools import find_packages, setup

package_name = "Interfaces"

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
    description="This package provides the interfaces required / used with other connecting applications. Example, a comm node to output infos regarding location with an UI.",
    license="MIT License",
    tests_require=["pytest"],
    entry_points={
        "console_scripts": [],
    },
)
