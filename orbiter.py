import numpy as np
from vectors import *

class Orbiter:
    def __init__(self, pos: Vec3, vel: Vec3, radius: float, color: tuple):
        self.pos = pos
        self.vel = vel
        self.radius = radius
        self.color = color
        self.mass = 4*np.pi*(self.radius**3)/3

    def update(self, others: list['Orbiter'], gravStrength: float):
        accel = Vec3(0, 0, 0)
        for other in others:
            if other != self:
                rel = other.pos - self.pos
                accel = accel + rel*(gravStrength*other.mass/(rel.mag()**3))
                if rel.mag() > other.radius:
                    accel = accel + rel*(gravStrength*other.mass/(rel.mag()**3))
                else:
                    newMass = 4*np.pi*(rel.mag()**3)/3
                    accel = accel + rel*(gravStrength*newMass/(rel.mag()**3))
        self.vel = self.vel + accel
        self.pos = self.pos + self.vel