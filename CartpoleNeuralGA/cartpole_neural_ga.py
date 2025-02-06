import numpy as np
from neural_ga import *
import gym
from neural_net import *
from time import sleep

class CartPoleNeuralGA(NeuralGA):
    """
    An example of using GAs to evolve the weights of a neural network
    to solve reinforcement learning problems like the Cart Pole from
    open AI gym.
    """
    def __init__(self, env, steps, in_size, out_size, hid_sizes, popsize):
        """
        In order to do RL learning, need the env and number of steps to
        run the environment when determining fitness.  Also need, all
        of the network specifications. 
        """
        self.env = env
        self.steps = steps

        # Call the parent class constructor
        super(CartPoleNeuralGA, self).__init__(in_size, out_size, hid_sizes,
                                         popsize)

    def fitness(self, chromosome, render=False, wtsFile=None):
        """
        Creates a neural network of the right size using the NeuralGA
        class variables in_size, out_size, and hid_sizes.

        If the wtsFile is not None, reads the weights from that file.
        Otherwise sets the weights based on the given chromosome.

        Tests out the neural network for one episode. When render is
        True, show what's happening in the env.

        Returns: Total reward received while executing steps
        """
        network = Network(self.in_size, self.out_size, self.hid_sizes)
        if wtsFile is not None:
            network.readWeights(wtsFile)
        else:
            network.setWeights(chromosome)
        state,_ = self.env.reset()
        total_reward = 0
        for i in range(self.steps):
            if render: self.env.render()
            output = network.predict(state)
            action = np.argmax(output)
            result = self.env.step(action)
            next_state, reward, done, _, _ = result
            total_reward += reward
            state = next_state
            if done:
                break
        if total_reward>self.bestEverScore:
            # self.bestEverScore = total_reward
            network.saveWeights()
        return total_reward
                               
    def isDone(self):
        """
        Stop when the best score ever found is equal to the maximum fitness.
        """
        if self.bestEverScore >= self.steps:
            return True


def main():
    env = gym.make("CartPole-v1")
    in_size = 4
    out_size = 2
    hid_sizes = [10]
    ga = CartPoleNeuralGA(env, 200, in_size, out_size, hid_sizes, 25)
    # When evolving network weights, lower the probability of crossover,
    # and increase the probability of mutation
    bestFound = ga.evolve(100, 0.1, 0.1)
    env.close()
    ga.plotStats("Cart Pole")

if __name__ == '__main__':
    main()
    
