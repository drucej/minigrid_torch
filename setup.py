from setuptools import setup, find_packages

setup(
    name='rl_sandbox',
    version='0.0.1',
    keywords='agent, rl, gym-minigrid, train, visualize, evaluate',
    url='https://github.com/drucej/minigrid_torch',
    description='RL starter files to train, visualize and evaluate an agent **without writing any line of code**',
    packages=find_packages(exclude=("gym_minigrid", ".idea")),
    # see gym_minigrid setup.py for additional dependencies
    install_requires=[
        'gym_minigrid',
        'six>=1.12.0',
        'array2gif',
        'jupyter',
        'tensorboardX>=1.6',
        'tensorboard>=2.4',
        'tensorflow==2.3.1',
        'torch-ac>=1.1.0'
    ]
)
