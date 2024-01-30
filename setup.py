from setuptools import find_packages, setup

def get_requirements(requirements_file):
    with open(requirements_file) as file:
        requirements_list = file.readlines()
        requirements_list = [req.replace('\n','') for req in requirements_list]
        return requirements_list
        



setup(
    name='src',
    packages=find_packages(),
    version='0.1.0',
    description='Predict the trip duration of taxis in NY city',
    author='Himanshu Arora',
    license='MIT',
    install_requires = get_requirements('requirements.txt')
)
