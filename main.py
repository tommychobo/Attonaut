import pygame
from pygame import Color
from pygame import Surface
import sys
import random
from vectors import *
from camera import *
from orbiter import *

pygame.init()

WIDTH, HEIGHT = 1280, 760
GRAV = 0.0000000003
BACK_COLOR = (0, 0, 0)


def pointCloud(numPts: int, width: float):
    cloud = [Orbiter]*numPts
    for i in range(numPts):
        rx = random.randrange(0, width*255)
        ry = random.randrange(0, width*255)
        rz = random.randrange(0, width*255)
        rad = random.randrange(30, 500)/10
        cloud[i] = Orbiter(Vec3(rx/255.0, ry/255.0, rz/255.0), Vec3(0.3, 0, 0), \
                            rad, (int(rx/(width)), int(ry/(width)), int(rz/(width))))
    return cloud

def sortZ(pts: list[tuple]) -> list[tuple]:
    length = len(pts)
    if length <= 1:
        return pts
    for i in range(length-1):
        iz = pts[i][0].vZ
        jMax = pts[i]
        jMaxInd = i
        for j in range(i+1, length):
            if pts[j][0].vZ > jMax[0].vZ:
                jMax = pts[j]
                jMaxInd = j
        temp = pts[i]
        pts[i] = pts[jMaxInd]
        pts[jMaxInd] = temp
    return pts

def drawOrbiter(screen: Surface, screenPos: Vec3, orb: Orbiter):
    color = Color(int(orb.color[0]), int(orb.color[1]), int(orb.color[2]))
    pygame.draw.circle(screen, color, (screenPos.vX, screenPos.vY), 1+orb.radius/screenPos.vZ)



def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Attonaut")
    cam = Camera(Vec3(1.5, 1.5, 3), -np.pi/2, 0, 0.7, 0.5, 0.01)
    orbiters: list[Orbiter] = pointCloud(40, 10)
    # the sun:
    orbiters.append(Orbiter(Vec3(0,0,25), Vec3(0.03, 0, 0), 1000, (255, 255, 0)))
    lines = [(1, 5), (2, 4), (20, 21)]
    speed = 0.03
    rotSpeed = 0.001
    rClick = False
    lClick = False
    pygame.mouse.set_visible(False)
    pygame.event.set_grab(True)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        mouseRel = pygame.mouse.get_rel()
        cam.incrOrient(mouseRel[0]*rotSpeed, mouseRel[1]*rotSpeed)
        screenPts = []

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            cam.pos = cam.pos - (cam.axes[2]*speed)
        if keys[pygame.K_s]:
            cam.pos = cam.pos + (cam.axes[2]*speed)
        if keys[pygame.K_a]:
            cam.pos = cam.pos - (cam.axes[0]*speed)
        if keys[pygame.K_d]:
            cam.pos = cam.pos + (cam.axes[0]*speed)
        if keys[pygame.K_SPACE]:
            cam.pos = cam.pos + (cam.axes[1]*speed)
        if keys[pygame.K_LSHIFT]:
            cam.pos = cam.pos - (cam.axes[1]*speed)

        if pygame.mouse.get_pressed()[0] and lClick == False:
            lClick = True
            speed *= 2
            print(f"speed = {speed}")
        if pygame.mouse.get_pressed()[2] and rClick == False:
            rClick = True
            speed /= 2
            print(f"speed = {speed}")
        
        if pygame.mouse.get_pressed()[0] == False:
            lClick = False
        if pygame.mouse.get_pressed()[2] == False:
            rClick = False
        
        screen.fill(BACK_COLOR)
        screenOrbs: list[tuple] = []
        for i in range(len(orbiters)):
            scrCoords = cam.screenCoords(orbiters[i].pos, WIDTH, HEIGHT)
            if scrCoords != None:
                screenOrbs.append((scrCoords, orbiters[i]))

        screenOrbs = sortZ(screenOrbs)

        for scrOrb in screenOrbs:
            drawOrbiter(screen, scrOrb[0], scrOrb[1])


        #for n in range(len(lines)):
        #    pt1 = cam.screenCoords(points[lines[n][0]][0], WIDTH, HEIGHT)
        #    pt2 = cam.screenCoords(points[lines[n][1]][0], WIDTH, HEIGHT)
        #    if pt1 != None and pt2 != None and pt1.vZ > 0 and pt2.vZ > 0:
        #        pygame.draw.line(screen, (0, 128, 128), \
        #                            (pt1.vX, pt1.vY), (pt2.vX, pt2.vY))
        for i in range(len(orbiters)):
            orbiters[i].update(orbiters, GRAV)
        pygame.display.update()
        
        pygame.time.delay(20)

if __name__ == "__main__":
    main()

