import numpy as np 
import matplotlib.pyplot as plt

class Ball:

    def __init__(self, x=1, y=1, vx=1, vy=2):
        self.mass = 1
        self.position = {'x': x, 'y': y}  
        self.velocity = {'x': vx, 'y': vy}

    def getX(self):
        return self.position['x']

    def getY(self):
        return self.position['y']

    def setState(self, x, y, vx, vy):
        self.position = {'x': x, 'y': y}  
        self.velocity = {'x': vx, 'y': vy}

    def update(self, dt):
        self.setState(self.position['x'], self.position['y'], self.velocity['x'], self.velocity['y']-9.81*dt)
        self.setState(self.position['x']+self.velocity['x']*dt, self.position['y']+self.velocity['y']*dt, self.velocity['x'], self.velocity['y'])

dt = 0.01

ball = Ball(vx=3, vy=6)
plt.figure()
plt.ion()

while ball.getY() > 0.999:
    ball.update(dt)
    plt.scatter(ball.getX(), ball.getY())
    plt.axis([0, 5, 0, 5])
    plt.draw()
    plt.pause(0.01)
    plt.cla()
plt.ioff()
plt.show()
