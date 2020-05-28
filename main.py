try:
    import pygame
    import sys
    import math
    import os
except:
    import install_req  # install packages
import threading
from Heap import Heap
import Grid
import AStar

pygame.init()
screen = pygame.display.set_mode((800, 800))

openSet = Heap()
closedSet = []
path = []
grey = (220, 220, 220)
pink = (255, 125, 125)

screen.fill(grey)
Grid.Init(pygame, screen)


loop = True
while loop:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # exiting game
            pygame.quit()
            sys.exit(1)
        if event.type == pygame.MOUSEBUTTONUP:
            Grid.lastDoing = -1
        if pygame.mouse.get_pressed()[0]:
            if Grid.start == -1 or Grid.end == -1:
                Grid.SetTarget(pygame.mouse.get_pos())
            else:
                Grid.SetObstacle(pygame.mouse.get_pos())
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                loop = False
                break

Grid.SetNeighbours()
Grid.start.parent = Grid.start
openSet.push(Grid.start)


while AStar.Solve(Grid.start, Grid.end, openSet, closedSet, path, steps=True):
    if pygame.event.poll().type == pygame.QUIT:
        pygame.quit()
        sys.exit(0)
    pygame.display.update()


def Clear(cPath=False):
    global openSet, closedSet, path
    for o in openSet.items:
        o.Show(grey, 0)
        o.Show((255, 255, 255), 1)
        o.gCost = 0
        o.hCost = 0
        o.fCost = 0
    for c in closedSet:
        c.gCost = 0
        c.hCost = 0
        c.fCost = 0
        c.parent = None
        if c in path and not cPath:
            continue
        c.Show(grey, 0)
        c.Show((255, 255, 255), 1)
    if cPath:
        for p in path:
            p.Show(grey, 0)
            p.Show((255, 255, 255), 1)
        path = []
    openSet.clear()
    closedSet = []
    Grid.start.gCost = 0
    Grid.start.hCost = 0
    Grid.start.fCost = 0
    Grid.start.Show(pink, 0)
    Grid.end.Show(pink, 0)


selected = None
Clear()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # exiting game
            pygame.quit()
            sys.exit(1)
        if event.type == pygame.MOUSEBUTTONDOWN:
            selected = Grid.GetNodeFromPos(
                pygame.mouse.get_pos(), onlyTargets=True)
        if pygame.mouse.get_pressed()[0]:
            if selected != None:
                moveTo = Grid.GetNodeFromPos(pygame.mouse.get_pos())
                if Grid.MoveTargets(selected, moveTo):
                    selected = moveTo
        if event.type == pygame.MOUSEBUTTONUP:
            selected = None
    if Grid.isChanged and selected == None:
        Grid.isChanged = False
        Clear(True)
        Grid.start.parent = Grid.start
        openSet.push(Grid.start)
        AStar.Solve(Grid.start, Grid.end, openSet, closedSet, path)
