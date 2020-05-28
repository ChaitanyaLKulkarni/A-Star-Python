try:
    import pygame
    import sys
    import math
    import os
except:
    import install_req  # install packages
import threading
from Heap import Heap
from Node import Node
import AStar

pygame.init()
screen = pygame.display.set_mode((800, 800))

cols = 50
rows = 50
grid = [0 for i in range(cols)]
openSet = Heap()
closedSet = []
path = []
pink = (255, 125, 125)
red = (150, 50, 50)
green = (0, 255, 0)
blue = (0, 0, 255)
grey = (220, 220, 220)
w = 800 / cols
h = 800 / rows
cameFrom = []
start = -1
end = -1
lastDoing = -1

Node.Init(pygame, screen, cols, rows)
screen.fill(grey)


for i in range(cols):
    grid[i] = [0 for i in range(rows)]

# Create Nodes
for i in range(cols):
    for j in range(rows):
        grid[i][j] = Node(i, j)

# showing all nodes
for i in range(cols):
    for j in range(rows):
        grid[i][j].Show((255, 255, 255), 1)

# Creating border around
for i in range(0, rows):
    grid[0][i].Show(grey, 0)
    grid[0][i].obstacle = True
    grid[cols-1][i].obstacle = True
    grid[cols-1][i].Show(grey, 0)
    grid[i][0].Show(grey, 0)
    grid[i][0].obstacle = True
    grid[i][rows-1].Show(grey, 0)
    grid[i][rows-1].obstacle = True


def GetNodeFromPos(pos):
    x = pos[0]
    y = pos[1]
    g1 = x // (800 // cols)
    g2 = y // (800 // rows)

    return grid[g1][g2]


def SetTarget(pos):
    global start, end
    node = GetNodeFromPos(pos)
    if node == start:
        node.Show(grey, 0)
        node.Show((255, 255, 255), 1)
        start = -1
        return
    elif start == -1:
        start = node
    else:
        end = node
    node.Show(pink, 0)


def SetObstacle(pos):
    global lastDoing
    node = GetNodeFromPos(pos)
    if node != start and node != end:
        if lastDoing == -1:
            lastDoing = node.obstacle
        if lastDoing != node.obstacle:
            return
        node.obstacle = not node.obstacle
        if node.obstacle:
            node.Show((0, 0, 0), 0)  # setting black
        else:
            node.Show(grey, 0)
            node.Show((255, 255, 255), 1)


loop = True
while loop:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # exiting game
            pygame.quit()
            sys.exit(1)
        if event.type == pygame.MOUSEBUTTONUP:
            lastDoing = -1
        if pygame.mouse.get_pressed()[0]:
            if start == -1 or end == -1:
                SetTarget(pygame.mouse.get_pos())
            else:
                SetObstacle(pygame.mouse.get_pos())
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                loop = False
                break

for i in range(cols):
    for j in range(rows):
        grid[i][j].addNeighbours(grid)
start.parent = start
openSet.push(start)


while AStar.Solve(start, end, openSet, closedSet, path, steps=True):
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
    start.gCost = 0
    start.hCost = 0
    start.fCost = 0
    start.Show(pink, 0)
    end.Show(pink, 0)


def MoveTargets(selected, moveTo):
    global start, end
    if moveTo.obstacle or moveTo == selected:
        return False
    if selected == start:
        if moveTo == end:
            return False

        selected.Show(grey, 0)
        selected.Show((255, 255, 255), 1)
        start = moveTo

    elif selected == end:
        if moveTo == start:
            return False

        selected.Show(grey, 0)
        selected.Show((255, 255, 255), 1)
        end = moveTo
    start.Show(pink, 0)
    end.Show(pink, 0)
    return True


selected = None
prevStart = start
prevEnd = end
Clear()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # exiting game
            pygame.quit()
            sys.exit(1)
        if event.type == pygame.MOUSEBUTTONDOWN:
            selected = GetNodeFromPos(pygame.mouse.get_pos())
            if selected != start and selected != end:
                selected = None
        if pygame.mouse.get_pressed()[0]:
            if selected != None:
                moveTo = GetNodeFromPos(pygame.mouse.get_pos())
                if MoveTargets(selected, moveTo):
                    selected = moveTo
        if event.type == pygame.MOUSEBUTTONUP:
            selected = None
    if prevStart != start or prevEnd != end and selected == None:
        Clear(True)
        prevStart = start
        prevEnd = end
        start.parent = start
        openSet.push(start)
        AStar.Solve(start, end, openSet, closedSet, path)
