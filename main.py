import DERobotArm as gym
from net import Agent
from utils import plotLearning
import numpy as np
import matplotlib.pyplot as plt

if __name__ == '__main__':
    env = gym.RobotArm()
    agent = Agent(gamma=0.99, epsilon=1.0, batch_size=512, input_dims=[4],
                  n_actions=4, max_mem_size=100000, eps_end=0.0001, eps_dec = 5e-5)
    scores, eps_history = [], []
    n_games = 5000
    
    plt.ion()

    for i in range(n_games):
        plt.clf()
        
        score = 0
        observation = env.reset()
        
        done = False
        plot = i % 100 == 0

        ii = 0
        while not done:
            action = agent.choose_action(observation)
            observation_, reward, done, info = env.step(action, plot, ii)
            score += reward
            agent.store_transition(observation, action, reward,
                                   observation_, done)
            agent.learn()
            if info == True:
                done = True
            
            if plot:
                env.plot()
                plt.scatter(observation[3], -1)
                plt.title([observation, action])
                plt.show()
                plt.pause(0.01)
                plt.cla()
                plt.axis([-2,11,-1,2])
                plt.gca().set_aspect('equal', adjustable='box')

            observation = observation_
            ii += 1


        scores.append(score)
        eps_history.append(agent.epsilon)

        avg_score = np.mean(scores[-100:])
        print('episode ', i, 'score %.2f' % score,
              'average score %.2f' % avg_score,
              'epsilon %.2f' % agent.epsilon)
    x = [i + 1 for i in range(n_games)]
    filename = 'lunar_lander.png'
    plotLearning(x, scores, eps_history, filename)
