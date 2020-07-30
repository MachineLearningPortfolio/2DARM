import numpy as np 
import matplotlib.pyplot as plt

class RobotArm:

    def __init__(self, length=1., theta=0, omega=0, alpha=0, mass=1, has_ball=True):
        np.random.seed()
        self.dt = 0.01
        self.length = length
        self.theta = theta
        self.omega = omega
        self.alpha = alpha
        self.mass = mass
        self.inertia = 1/3*self.mass*self.length**2 #rod
        self.has_ball = has_ball
        self.position = [-self.length*np.cos(theta), -self.length*np.sin(theta)]
        self.velocity = [self.length*omega*np.sin(theta), -self.length*omega*np.cos(theta)]
        self.target = np.random.rand()*10+1

    def get_state(self):
        return np.array([self.theta, self.omega, self.alpha, self.target], dtype=np.float32)

    def reset(self):
        self.__init__()
        return self.get_state()

    def step(self, action):
        d_acc = 0
        if action == 0:
            d_acc = 0
        elif action == 1:
            d_acc = 0.01
        elif action == 2:
            d_acc = -0.01
        elif action == 3:
            while self.position[1] > -self.length:
                self.velocity = [self.velocity[0], self.velocity[1] - 9.82 * self.dt]
                self.position = [self.position[0] + self.velocity[0] * self.dt,
                                 self.position[1] + self.velocity[1] * self.dt]
            return [self.get_state(), 1/np.abs(self.target - self.position[0]), True, {}]

        self.alpha = self.mass*9.82*self.length*np.cos(self.theta)/(2*self.inertia)-self.omega/10+d_acc
        self.omega += self.alpha*self.dt
        self.theta += self.omega*self.dt
        self.position = [-self.length*np.cos(self.theta), -self.length*np.sin(self.theta)]
        self.velocity = [self.length*self.omega*np.sin(self.theta), -self.length*self.omega*np.cos(self.theta)]
        return [self.get_state(), -np.abs(self.target - self.position[0]), False, {}]

    def plot(self):
        x2 = -self.length*np.cos(self.theta)
        y2 = -self.length*np.sin(self.theta)
        plt.plot([0, x2], [0, y2])
        if self.has_ball:
            plt.scatter(x2, y2, color='w', edgecolors='k')
