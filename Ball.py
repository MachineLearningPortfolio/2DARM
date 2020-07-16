import numpy as np 
import matplotlib.pyplot as plt
import matplotlib.animation as animation

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


class AnimatedScatter(object):
    def __init__(self):
        self.stream = self.data_stream()
        self.fig, self.ax = plt.subplots()
        self.ax.plot([1,3],[1.0, 1.0], c='k')
        self.ax.plot([5,6],[1.0, 1.0], c='k')
        self.ani = animation.FuncAnimation(self.fig, self.update, interval=10,
                                          init_func=self.setup_plot, blit=True)
        self.ball = Ball(vx=3, vy=6)

    def setup_plot(self):
        x, y = next(self.stream).T
        self.scat = self.ax.scatter(x, y, vmin=0, vmax=1,
                                    cmap="jet", edgecolor="k")
        self.ax.axis([1, 6, 0.5, 3])
        return self.scat,

    def data_stream(self):
        while True:
            self.ball.update(dt)
            yield np.c_[self.ball.getX(), self.ball.getY()]
            if self.ball.getY() < 1:
                self.ball.setState(1, 1, np.random.randint(0.1,7), np.random.randint(0.1,7))

    def update(self, i):
        data = next(self.stream)
        self.scat.set_offsets(data)
        return self.scat,


if __name__ == '__main__':
    a = AnimatedScatter()
    plt.show()