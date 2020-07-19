import numpy as np 
import matplotlib.pyplot as plt
import math

class RobotArm:

    def __init__(self, armLength=0.5, upperAngle=0, lowerAngle=0, upperX=0, upperY=2, upperVel=0, lowerVel=0):
        self.armLength = armLength
        self.upperPos = {'x': upperX, 'y': upperY}
        self.upperAngle = upperAngle
        self.upperVel = upperVel
        self.lowerPos = {'x': upperX+armLength*np.cos(self.upperAngle), 'y': upperY+armLength*np.sin(self.upperAngle)}
        self.lowerAngle = lowerAngle
        self.lowerVel = lowerVel
        self.handPos = {'x': self.lowerPos['x']+armLength*np.cos(self.lowerAngle), 'y': self.lowerPos['y']+armLength*np.sin(self.lowerAngle)}

    def getPosition(self):
        return self.upperPos['x'], self.upperPos['y'], self.lowerPos['x'], self.lowerPos['y'], self.handPos['x'], self.handPos['y']

    def setVelocity(self, upperVel, lowerVel):
        self.upperVel = upperVel
        self.lowerVel = lowerVel

    def setPosition(self):
        self.upperAngle += self.upperVel
        self.lowerAngle += self.lowerVel
        self.lowerPos['x'] = self.upperPos['x']+self.armLength*np.cos(self.upperAngle)
        self.lowerPos['y'] = self.upperPos['y']+self.armLength*np.sin(self.upperAngle)
        self.handPos['x'] = self.lowerPos['x']+self.armLength*np.cos(self.lowerAngle)
        self.handPos['y'] = self.lowerPos['y']+self.armLength*np.sin(self.lowerAngle)

    def plotArm(self):
        x1, y1, x2, y2, x3, y3 = self.getPosition()
        plt.plot([x1, x2, x3], [y1, y2, y3], linewidth=3, c='k', marker='o', mfc='gray', mec='k')
        plt.axis([-2, 2, 0, 4])


arm = RobotArm(upperAngle=math.pi/3, lowerAngle=math.pi/6)
plt.figure()
plt.ion()
upperVel = 0.1*(int(np.random.rand())*2-1)
lowerVel = 0.1*(int(np.random.rand())*2-1)
arm.setVelocity(upperVel, lowerVel)
for i in range(1000):
    arm.plotArm()
    if np.mod(i, 10) == 0:
        upperVel = 0.1*(np.round(np.random.rand())*2-1)
        lowerVel = 0.1*(np.round(np.random.rand())*2-1)
        arm.setVelocity(upperVel, lowerVel)
    arm.setPosition()
    plt.pause(0.01)
    plt.cla()
plt.show()
plt.ioff()