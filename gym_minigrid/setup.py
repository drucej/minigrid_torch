from setuptools import setup

setup(
    name='gym_minigrid',
    version='1.0.1',
    keywords='memory, environment, agent, rl, openaigym, openai-gym, gym',
    url='https://github.com/maximecb/gym-minigrid',
    description='Minimalistic gridworld package for OpenAI Gym',
    packages=['gym_minigrid', 'gym_minigrid.envs'],
    # need numpy >= 1.16.0 and < 1.19.0 for tensorflow compatability
    install_requires=[
        'numpy==1.18.0',
        'gym>=0.9.6',
        'numpy>=1.16.0<=1.18.0',
        'matplotlib'
    ]
)
