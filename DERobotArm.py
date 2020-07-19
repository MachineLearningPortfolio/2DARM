import numpy as np 
import matplotlib.pyplot as plt
import matplotlib.patches

class RobotArm:

    def __init__(self, length=1, theta=0, omega=0, alpha=0, mass=1, has_ball=True):
        self.length = length
        self.theta = theta
        self.omega = omega
        self.alpha = alpha
        self.mass = mass
        self.inertia = 1/3*self.mass*self.length**2 #rod
        self.has_ball = has_ball

    def get_state(self):
        return self.theta, self.omega, self.alpha

    def get_length(self):
        return self.length

    def update(self, dt):
        self.alpha = self.mass*9.82*self.length*np.cos(self.theta)/(2*self.inertia)-self.omega/10
        self.omega += self.alpha*dt
        self.theta += self.omega*dt

    def plot(self):
        x2 = -self.length*np.cos(self.theta)
        y2 = -self.length*np.sin(self.theta)
        plt.plot([0, x2], [0, y2])
        if self.has_ball:
            plt.scatter(x2, y2, color='w', edgecolors='k')

    def drop(self):
        self.has_ball = False

class Ball:
    def __init__(self, theta, omega, _, length):
        self.mass = 1
        self.position = [-length*np.cos(theta), -length*np.sin(theta)]
        self.velocity = [length*omega*np.sin(theta), -length*omega*np.cos(theta)]

    def update(self, dt):
        self.velocity = [self.velocity[0], self.velocity[1]-9.82*dt]
        self.position = [self.position[0] + self.velocity[0]*dt, 
                self.position[1] + self.velocity[1]*dt]

    def plot(self):
        plt.scatter(*self.position, color='w', edgecolors='k')

dt = 0.01
drop_point = 60
target = 2.66
axis = [-1, 4, -2, 2]
ground_level = -1
sun_radius = 0.2

arm = RobotArm(length=0.9)
fig = plt.figure()
ax = fig.add_subplot(111, aspect='equal')
ax.set_facecolor('#02d8e9')
plt.ion()
for i in range(1000):
    arm.update(dt)
    arm.plot()
    if i == drop_point:
        arm.drop()
        ball = Ball(*arm.get_state(), arm.get_length())
    if i > drop_point:
        ball.update(dt)
        ball.plot()
        if ball.position[1] < ground_level:
            break
    ax.add_patch(matplotlib.patches.Rectangle((axis[0], axis[2]), axis[1]-axis[0], np.abs(axis[2]-ground_level), fc='#388004'))
    ax.add_patch(matplotlib.patches.Circle((axis[1], axis[3]), (axis[3]-axis[2])*sun_radius, fc='#fff917'))
    plt.scatter(target, -1.1, marker='x', c='k', s=1000)
    plt.title(i)
    plt.axis(axis)
    plt.show()
    plt.pause(0.01)
    plt.cla()
