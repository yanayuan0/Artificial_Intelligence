from collections import deque
import tensorflow
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import Adam, SGD
import numpy as np
import random
import matplotlib.pyplot as plt
import time

"""
The structure of the Q-learning algorithm is based on code provided here:
https://medium.com/@ts1829/solving-mountain-car-with-q-learning-b77bf71b1de2
but with modifications to operate more efficiently using Keras
(i.e. batch updates instead of online updates)
"""

class DQNAgent:
    """
    A Deep Q-Learning Agent.

    Given the size of the state space and action space, creates a neural
    network to approximate the Q-Learning table. 

    This basic framework should work for any RL problem, but each new
    problem will likely need a different neural network model and
    different settings for the hyperparameters.
    """
    def __init__(self, state_size, action_size):
        self.state_size = state_size
        self.action_size = action_size
        self.memory = deque(maxlen=65536)
        # Read the paper to determine how best to set all of
        # these hyperparameters
        self.gamma = 0.99
        self.epsilon = 0.5
        self.epsilon_min = 0.0
        self.epsilon_decay = 0.99
        self.learning_rate = 0.0001
        self.model = self._build_model()
        self.history = []
        
    def _build_model(self):
        """
        Construct a neural network model using keras. 

        We need outputs to be both negative and positive, so use a linear
        activation function.
        """
        # Read the paper to determine the best architecture
        model = Sequential()
        model.add(Dense(256, input_dim=self.state_size, activation='relu'))
        model.add(Dense(128, activation='relu'))
        model.add(Dense(self.action_size, activation='linear'))
        model.compile(loss='mse',
                      optimizer=Adam(learning_rate=self.learning_rate))
        model.summary()
        return model
    
    def save_weights(self, filename="model.h5"):
        """
        Saves the network weights to a file.
        """
        self.model.save_weights(filename)
            
    def load_weights(self, filename="model.h5"):
        """
        Reloads the network weights from a file.
        """
        self.model.load_weights(filename)
        
    def remember(self, state, action, reward, next_state, done):
        """
        Stores the given experience in the memory.
        """ 
        self.memory.append((state, action, reward, next_state, done))

    def epsilon_greedy_act(self, state):
        """
        Given a state, chooses whether to explore or to exploit based
        on the self.epsilon probability.
        """
        if np.random.rand() <= self.epsilon:
            return random.randrange(self.action_size)
        else:
            return self.greedy_act(state)

    def greedy_act(self, state):
        """
        Given a state, chooses the action with the best value.
        """
        act_values = self.model.predict(state,verbose=0)
        return np.argmax(act_values[0])  # returns action
    
    def replay(self, batch_size, iterations):
        """
        Selects a random sample of experiences from the memory to
        train on using batch updates.
        """
        for i in range(iterations):
            minibatch = random.sample(self.memory, batch_size)

            states = np.asarray([state[0] for state, action, reward, \
                                 next_state, done in minibatch])
            nextStates = np.asarray([next_state[0] for state, action, \
                                     reward, next_state, done in minibatch])
            rewards = np.asarray([reward for state, action, reward, \
                                  next_state, done in minibatch])
            actions = np.asarray([action for state, action, reward, \
                                  next_state, done in minibatch])
            notdone = np.asarray([not(done) for state, action, reward, \
                                  next_state, done in minibatch]).astype(int)
            nextVals = np.amax(self.model.predict(nextStates,verbose=0), axis=1)
            targets =  rewards + (nextVals * notdone * self.gamma)
            targetFs = self.model.predict(states,verbose=0)
            for i in range(len(minibatch)):
                targetFs[i, actions[i]] = targets[i]
            self.model.fit(states, targetFs, epochs=1, verbose=0)
    
    def plot_history(self, show=True):
        """
        Plots the rewards per episode over number of episodes. 
        If show is True, displays the plot. Saves plot to a file. 
        """
        plt.figure(1)
        plt.plot(self.history)
        plt.xlabel("Episode")
        plt.ylabel("Reward")
        plt.savefig("LunarRewardByEpisode.png")
        if show:
            plt.show()

    def train(self, env, episodes, steps, batchSize, batchIterations,\
              envName):
        """
        Train the agent in the environment env for the given number
        of episodes, where each episode is at most steps long.  Use
        the batchSize and batchIterations when calling replay. The
        agent should follow the epsilon-greedy policy. 
        
        Returns: None
        Side Effects:
        -Every 50 episodes saves the agent's weights to a filename
         of the form: envName_episode_#.h5, it must have the h5 extension
        -Updates self.history with total rewards received per episode
        -Prints a summary of reward received each episode
        """
        self.history = []
        for i in range(episodes):
            state, _ = env.reset()
            state = np.reshape(state, [1,self.state_size])
            if (i+1)%50==0:
                filename = envName + "_episode_" + str(i+1) + ".h5"
                self.save_weights(filename)
            total_reward = 0
            for j in range(steps):
                action = self.epsilon_greedy_act(state)
                result = env.step(action)
                next_state, reward, done, _, _ = result
                total_reward += reward
                next_state = np.reshape(next_state, [1,self.state_size])
                self.remember(state,action,reward,next_state,done)
                state = next_state
                if len(self.memory) > batchSize: #####
                    self.replay(batchSize,batchIterations)
                if done:
                    break
            self.history.append(total_reward)
            print("Episode ended after", j, "steps, total reward:", total_reward )
            if self.epsilon > self.epsilon_min:
                self.epsilon = self.epsilon*self.epsilon_decay
        filename = envName + "_episode_" + str(episodes) + ".h5"
        self.save_weights(filename)

    def test(self, env, episodes, steps):
        """
        Test the agent in the environment env for the given number
        of episodes, where each episode is a most steps long, when
        the agent follows its greedy policy.

        Returns: None
        Side Effects:
        -Renders the environment to see the agent in action.
        -Prints a summary of reward received at the end of each episode.
        """
        self.history = []
        for i in range(episodes):
            state, _ = env.reset()
            state = np.reshape(state, [1,self.state_size])
            total_reward = 0
            for j in range(steps):
                action = self.greedy_act(state)
                result = env.step(action)
                next_state, reward, done, _, _ = result
                total_reward += reward
                next_state = np.reshape(next_state, [1,self.state_size])
                state = next_state
                if done:
                    break
            self.history.append(total_reward)
            print("Episode ended after", j, "steps, total reward:", total_reward )

