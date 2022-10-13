import gym
from urdfenvs.robots.iris import IrisDrone
from pdm2022.env.maze import *
from pdm2022.goal.static import goal1
import numpy as np

def run_point_robot(n_steps=1000, render=False, goal=True, obstacles=True):
    robots = [
        IrisDrone(mode="vel"),
    ]
    env = gym.make(
        "urdf-env-v0",
        dt=0.01, robots=robots, render=render
    )
    # action = np.array([0.1, 0.0, 1.0])
    # pos0 = np.array([0.0, -2, 0.0])
    # vel0 = np.array([1.0, 0.0, 0.0])
    pos0 = np.array([-2.0, 0.0, 1.2, 0., 0.0, 0.0, 1.])
    action = np.ones(4) * 830.2
    ob = env.reset(pos=pos0)
    print(f"Initial observation : {ob}")
    env.add_walls()
    if obstacles:
        env.add_obstacle(wallObst1)
        env.add_obstacle(wallObst2)
        env.add_obstacle(wallObst3)
    if goal:
        env.add_goal(goal1)
    history = []
    for _ in range(n_steps):
        ob, _, _, _ = env.step(action)
        history.append(ob)
    env.close()
    return history


if __name__ == "__main__":
    run_point_robot(render=True)
