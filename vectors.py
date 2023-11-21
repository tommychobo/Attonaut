import numpy as np

class Vec3:
    def __init__(self, vX:float, vY:float, vZ:float):
        self.vX = vX
        self.vY = vY
        self.vZ = vZ

    def __add__(self, other: 'Vec3') -> 'Vec3':
        return Vec3(self.vX+other.vX, self.vY+other.vY, self.vZ+other.vZ)
    
    def __sub__(self, other: 'Vec3') -> 'Vec3':
        return Vec3(self.vX-other.vX, self.vY-other.vY, self.vZ-other.vZ)
    
    def __mul__(self, other):
        if isinstance(other, Vec3):
            return self.vX*other.vX + self.vY*other.vY + self.vZ*other.vZ
        return Vec3(self.vX*other, self.vY*other, self.vZ*other)
    
    def __truediv__(self, scalar: float) -> 'Vec3':
        if scalar == 0:
            return Vec3(0, 0, 0)
        return Vec3(self.vX/scalar, self.vY/scalar, self.vZ/scalar)
    
    def __str__(self):
        return f"Vec({self.vX}, {self.vY}, {self.vZ})"
    
    def cross(self, other: 'Vec3') -> 'Vec3':
        i: float = self.vY*other.vZ - self.vZ*other.vY
        j: float = self.vZ*other.vX - self.vX*other.vZ
        k: float = self.vX*other.vY - self.vY*other.vX
        return Vec3(i, j, k)
    
    def mag(self) -> float:
        return np.sqrt(self.vX*self.vX + self.vY*self.vY + self.vZ*self.vZ)
    
    def spherical(self, mag: float, theta: float, phi: float):
        self.vX = mag*np.cos(phi)*np.cos(theta)
        self.vZ = mag*np.cos(phi)*np.sin(theta)
        self.vY = mag*np.sin(phi)
