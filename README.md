# RL Starter Files

RL starter files in order to immediatly train, visualize and evaluate an agent **without writing any line of code**.

<p align="center">
    <img width="300" src="README-rsrc/visualize-keycorridor.gif" alt=""/>
</p>

<p align="center">
    <img width="300" src="/Users/ccall/Documents/minigrid_torch/README-rsrc/visualize-keycorridor.gif"/>
</p>

![image info](README-rsrc/visualize-keycorridor.gif)


These files are suited for [`gym-minigrid`](https://github.com/maximecb/gym-minigrid) environments 
and [`torch-ac`](https://github.com/lcswillems/torch-ac) RL algorithms. 
They are easy to adapt to other environments and RL algorithms.

## Features

- **Script to train**, including:
  - Log in txt, CSV and Tensorboard
  - Save model
  - Stop and restart training
  - Use A2C or PPO algorithms
- **Script to visualize**, including:
  - Act by sampling or argmax
  - Save as Gif
- **Script to evaluate**, including:
  - Act by sampling or argmax
  - List the worst performed episodes

## Installation cdc
NOTE: python > 3.7.7 is a problem
#### 1. Create a conda environment  
```
conda create -n minigrid python=3.7.7 
conda activate minigrid
```
    
#### 2. Clone this repository
```
git clone https://github.com/drucej/minigrid_torch.git
git checkout ccall_dev
```

#### 3. Install mini-grid and dependencies
```
cd <path-to>minigrid_torch/gym_minigrid
pip install -e .
```

#### 4. Install RL sandbox (depends on local mini-grid)
```
cd <path-to>minigrid_torch
pip install -e .
```

## Create Docker image cdc

#### 1. Create docker image (dockerfile at top level) 
```
(docker system prune -a --volumes) or equivalent
docker build -t rl_sandbox
```

#### 2. Run docker image (note jupyter is serving on port 8889)
```
docker run -p 6006:6006 -p 8889:8889 --rm -it --name rl_sandbox rl_sandbox:latest
```

This will return a prompt: `root@f553584171ae:/home/rl_sandbox# `  
showing you are running as root in the rl_sandbox home directory  
You can run as the rl_sandbox user:
```
su rl_sandbox
```
This will return a prompt: `$`  
Currently, the sandbox user's account isn't properly set up so tab completions, etc. are disabled.

####3. Set up data (needed by the example Jupyter Notebook)
In a new terminal, run
```
python -m scripts.train --algo ppo --env MiniGrid-DoorKey-6x6-v0 --model DoorKey6 --save-interval 10 --frames 80000
```

#### 3. Run Jupyter 

 #####Run as root
```
docker exec -it rl_sandbox bash
jupyter notebook --ip=0.0.0.0 --allow-root
```

#####Run as rl_sandbox user
```
su rl_sandbox
docker exec -it rl_sandbox bash
jupyter notebook --ip=0.0.0.0 
```
   
you can now log in to Jupyter via your browser using the token '1234'
   ```
   localhost:8889/?token=1234
   ```

#### 4. Run Tensorboard
In a new terminal (home directory is /home/rl_sandbox)  
```
docker exec -it rl_sandbox bash
tensorboard --logdir=storage/tensorboard --bind_all
```
you can now access Tensorboard via your browser 
   ```
   localhost:6006
   ```

#### 5. Stopping and Exiting Applications

Both Jupyter and Tensorboard servers are stopped with `^c`  (control c)   
In each case, you then need to exit the bash shell with `exit`  
You also exit the Docker shell with `exit`


## Installation jd

1. Clone this repository.

2. Install `gym-minigrid` environments and `torch-ac` RL algorithms:

```
pip3 install -r requirements.txt
```

**Note:** If you want to modify `torch-ac` algorithms, you will need to rather install a cloned version, i.e.:
```
git clone https://github.com/lcswillems/torch-ac.git
cd torch-ac
pip3 install -e .
```

## Example of use

Train, visualize and evaluate an agent on the `MiniGrid-DoorKey-5x5-v0` environment:

<p align="center"><img src="README-rsrc/doorkey.png"></p>

1. Train the agent on the `MiniGrid-DoorKey-5x5-v0` environment with PPO algorithm:

```
python -m scripts.train --algo ppo --env MiniGrid-DoorKey-5x5-v0 --model DoorKey --save-interval 10 --frames 80000
```

<p align="center"><img src="README-rsrc/train-terminal-logs.png"></p>

2. Visualize agent's behavior:

```
python3 -m scripts.visualize --env MiniGrid-DoorKey-5x5-v0 --model DoorKey
```

<p align="center"><img src="README-rsrc/visualize-doorkey.gif"></p>

3. Evaluate agent's performance:

```
python3 -m scripts.evaluate --env MiniGrid-DoorKey-5x5-v0 --model DoorKey
```

<p align="center"><img src="README-rsrc/evaluate-terminal-logs.png"></p>

**Note:** More details on the commands are given below.

## Other examples

### Handle textual instructions

In the `GoToDoor` environment, the agent receives an image along with a textual instruction. To handle the latter, add `--text` to the command:

```
python3 -m scripts.train --algo ppo --env MiniGrid-GoToDoor-5x5-v0 --model GoToDoor --text --save-interval 10 --frames 1000000
```

<p align="center"><img src="README-rsrc/visualize-gotodoor.gif"></p>

### Add memory

In the `RedBlueDoors` environment, the agent has to open the red door then the blue one. To solve it efficiently, when it opens the red door, it has to remember it. To add memory to the agent, add `--recurrence X` to the command:

```
python3 -m scripts.train --algo ppo --env MiniGrid-RedBlueDoors-6x6-v0 --model RedBlueDoors --recurrence 4 --save-interval 10 --frames 1000000
```

<p align="center"><img src="README-rsrc/visualize-redbluedoors.gif"></p>

## Files

This package contains:
- scripts to:
  - train an agent \
  in `script/train.py` ([more details](#scripts-train))
  - visualize agent's behavior \
  in `script/visualize.py` ([more details](#scripts-visualize))
  - evaluate agent's performances \
  in `script/evaluate.py` ([more details](#scripts-evaluate))
- a default agent's model \
in `model.py` ([more details](#model))
- utilitarian classes and functions used by the scripts \
in `utils`

These files are suited for [`gym-minigrid`](https://github.com/maximecb/gym-minigrid) environments and [`torch-ac`](https://github.com/lcswillems/torch-ac) RL algorithms. They are easy to adapt to other environments and RL algorithms by modifying:
- `model.py`
- `utils/format.py`

<h2 id="scripts-train">scripts/train.py</h2>

An example of use:

```bash
python3 -m scripts.train --algo ppo --env MiniGrid-DoorKey-5x5-v0 --model DoorKey --save-interval 10 --frames 80000
```

The script loads the model in `storage/DoorKey` or creates it if it doesn't exist, then trains it with the PPO algorithm on the MiniGrid DoorKey environment, and saves it every 10 updates in `storage/DoorKey`. It stops after 80 000 frames.

**Note:** You can define a different storage location in the environment variable `PROJECT_STORAGE`.

More generally, the script has 2 required arguments:
- `--algo ALGO`: name of the RL algorithm used to train
- `--env ENV`: name of the environment to train on

and a bunch of optional arguments among which:
- `--recurrence N`: gradient will be backpropagated over N timesteps. By default, N = 1. If N > 1, a LSTM is added to the model to have memory.
- `--text`: a GRU is added to the model to handle text input.
- ... (see more using `--help`)

During training, logs are printed in your terminal (and saved in text and CSV format):

<p align="center"><img src="README-rsrc/train-terminal-logs.png"></p>

**Note:** `U` gives the update number, `F` the total number of frames, `FPS` the number of frames per second, `D` the total duration, `rR:μσmM` the mean, std, min and max reshaped return per episode, `F:μσmM` the mean, std, min and max number of frames per episode, `H` the entropy, `V` the value, `pL` the policy loss, `vL` the value loss and `∇` the gradient norm.

During training, logs are also plotted in Tensorboard:

<p><img src="README-rsrc/train-tensorboard.png"></p>

<h2 id="scripts-visualize">scripts/visualize.py</h2>

An example of use:

```
python3 -m scripts.visualize --env MiniGrid-DoorKey-5x5-v0 --model DoorKey
```

<p align="center"><img src="README-rsrc/visualize-doorkey.gif"></p>

In this use case, the script displays how the model in `storage/DoorKey` behaves on the MiniGrid DoorKey environment.

More generally, the script has 2 required arguments:
- `--env ENV`: name of the environment to act on.
- `--model MODEL`: name of the trained model.

and a bunch of optional arguments among which:
- `--argmax`: select the action with highest probability
- ... (see more using `--help`)

<h2 id="scripts-evaluate">scripts/evaluate.py</h2>

An example of use:

```
python3 -m scripts.evaluate --env MiniGrid-DoorKey-5x5-v0 --model DoorKey
```

<p align="center"><img src="README-rsrc/evaluate-terminal-logs.png"></p>

In this use case, the script prints in the terminal the performance among 100 episodes of the model in `storage/DoorKey`.

More generally, the script has 2 required arguments:
- `--env ENV`: name of the environment to act on.
- `--model MODEL`: name of the trained model.

and a bunch of optional arguments among which:
- `--episodes N`: number of episodes of evaluation. By default, N = 100.
- ... (see more using `--help`)

<h2 id="model">model.py</h2>

The default model is discribed by the following schema:

<p align="center"><img src="README-rsrc/model.png"></p>

By default, the memory part (in red) and the langage part (in blue) are disabled. They can be enabled by setting to `True` the `use_memory` and `use_text` parameters of the model constructor.

This model can be easily adapted to your needs.
