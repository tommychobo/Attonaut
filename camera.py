import numpy as np
from vectors import *

class Camera:
    def __init__(self, pos: Vec3, theta: float, phi: float,\
                  fovX: float, fovY: float, zMin: float):
        self.pos = pos
        self.theta = theta
        self.phi = phi
        self.orient = Vec3(0, 0, 0)
        self.orient.spherical(1, self.theta, self.phi)
        self.fovX = fovX
        self.fovY = fovY
        self.zMin = zMin
        self.axes = self.updateRelAxes()

    def incrOrient(self, deltaTheta: float, deltaPhi: float) -> Vec3:
        self.phi -= deltaPhi
        self.theta += deltaTheta
        if self.phi < -np.pi/2:
            self.phi = -np.pi/2
        if self.phi > np.pi/2:
            self.phi = np.pi/2
        if self.theta > 2*np.pi:
            self.theta = self.theta - 2*np.pi
        if self.theta < 0:
            self.theta = self.theta + 2*np.pi
        self.orient.spherical(1, self.theta, self.phi)
        self.updateRelAxes()
        return self.orient
    
    def updateRelAxes(self) -> list[Vec3]:
        self.axes = [Vec3]*3
        self.axes[2] = self.orient * -1.0
        self.axes[0] = Vec3(-1.0*self.orient.vZ, 0, self.orient.vX)
        self.axes[0] = self.axes[0] / self.axes[0].mag()
        self.axes[1] = self.axes[2].cross(self.axes[0])
        return self.axes

    def screenCoords(self, vec: Vec3, width: int, height: int) -> Vec3:
        rel = vec - self.pos
        rel = Vec3(rel*self.axes[0], rel*self.axes[1], rel*self.axes[2])
        if np.abs(rel.vZ) < self.zMin:
            return None
        scr = Vec3(rel.vX / ( rel.vZ * -1.0 * self.fovX ), \
                rel.vY / ( rel.vZ * -1.0 * self.fovY ), \
                rel.vZ * -1.0)
        return Vec3((scr.vX+1)*(width/2), (-scr.vY+1)*(height/2), scr.vZ)