import gym
from cartpole_neural_ga import *

def main():
    """
    This program allows you to re-test the best weights ever found.
    """
    in_size = 4
    out_size = 2
    hid_sizes = [10]
    env = gym.make("CartPole-v1", render_mode="human")
    ga = CartPoleNeuralGA(env, 200, in_size, out_size, hid_sizes, 25)
    result = ga.fitness(None, True, "bestEver.wts")
    print("Test run total fitness:", result)
    env.close()

main()
