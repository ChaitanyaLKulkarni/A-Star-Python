try:
    import pygame
    import sys
    import math
    import os
except:
    import install_req  # install packages

from Heap import Heap

pygame.init()
screen = pygame.display.set_mode((800, 800))

class Node:
    def __init__(self, xpos,ypos):
        self.xpos = xpos
        self.ypos = ypos
        self.gCost = 0 
        self.hCost = 0
        self.fCost = 0
        self.neighbours = []
        self.parent = None
        self.obstacle = False
        self.heapIndex = -1
    
    def Show(self, color, st):
        pygame.draw.rect(screen, color, (self.xpos * w, self.ypos * h, w, h), st)
        pygame.display.update()

    def addNeighbours(self,grid):
        x = self.xpos
        y = self.ypos

        if x < cols - 1 and not grid[x + 1][y].obstacle: #right
            self.neighbours.append(grid[x + 1][y])
        if x > 0 and  not grid[x - 1][y].obstacle: #left
            self.neighbours.append(grid[x-1][y])
        if y < rows - 1 and not grid[x][y + 1].obstacle: #Top
            self.neighbours.append(grid[x][y+1])
        if y > 0 and not grid[x][y-1].obstacle: #bottom
            self.neighbours.append(grid[x][y-1])
        if (x > 0 and y > 0) and not grid[x-1][y-1].obstacle: #bottom left
            self.neighbours.append(grid[x-1][y-1])
        if (x > 0 and y < rows - 1) and not grid[x-1][y+1].obstacle: #top left
            self.neighbours.append(grid[x-1][y+1])
        if (x < cols -1 and y > 0) and not grid[x+1][y-1].obstacle: #bottom right
            self.neighbours.append(grid[x+1][y-1])
        if (x < cols - 1 and y < rows - 1) and not grid[x+1][y+1].obstacle: #top right
            self.neighbours.append(grid[x+1][y+1])
        
    def __lt__(self,other):
        return self.fCost < other.fCost

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

screen.fill(grey)


for i in range(cols):
    grid[i] = [0 for i in range(rows)]

# Create Nodes
for i in range(cols):
    for j in range(rows):
        grid[i][j] = Node(i, j)

#showing all nodes
for i in range(cols):
    for j in range(rows):
        grid[i][j].Show((255,255,255), 1)

#Creating border around 
for i in range(0,rows):
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
    global start,end
    node = GetNodeFromPos(pos)
    if node == start:
        node.Show(grey, 0)
        node.Show((255,255,255), 1)
        start = -1
        return
    elif start == -1:
        start = node
    else:
        end = node
    node.Show(pink,0)


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
            node.Show((0,0,0),0) #setting black
        else:
            node.Show(grey, 0)
            node.Show((255,255,255), 1)

  
loop = True
while loop:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: #exiting game
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

def GetGHFrom(curr,neighbour):
    Gcost = 0
    if curr.xpos == neighbour.xpos or curr.ypos == neighbour.ypos:
        Gcost = curr.gCost + 1
    else:
        Gcost = curr.gCost + 1.4

    HCost = 0
    if end.xpos == neighbour.xpos:
        HCost = 1 * abs(end.xpos - neighbour.xpos)
    elif end.ypos == neighbour.ypos:
        HCost = 1 * abs(end.ypos - neighbour.ypos)
    else:
        minA = min(abs(end.xpos - neighbour.xpos) ,  abs(end.ypos - neighbour.ypos))
        maxA = max(abs(end.xpos - neighbour.xpos) , abs(end.ypos - neighbour.ypos))
        HCost = 1.4 * minA
        HCost += 1 * maxA - minA
    
    return Gcost,HCost

def AStar(steps):
    while openSet.count() > 0:
        #TODO: Use heap to get loweset more efficiently
        current = openSet.pop()
        if current == end:
            #print("Donee")
            while current.parent != current:
                path.append(current)
                current.Show(blue,0)
                current = current.parent
            start.Show((255,0,0),0)
            end.Show((255,0,0),0)
            start.Show((0,0,0),3)
            end.Show((0,0,0),3)
            return False
        else:
            closedSet.append(current)   

            neighbours = current.neighbours
            for neighbour in neighbours:
                if neighbour not in closedSet:
                    newG,newH = GetGHFrom(current,neighbour)
                    if neighbour not in openSet.items or neighbour.gCost > newG:
                        neighbour.gCost = newG
                        neighbour.hCost = newH
                        neighbour.parent = current
                        neighbour.fCost = neighbour.gCost + neighbour.hCost
                        if neighbour not in openSet.items:
                            openSet.push(neighbour)
                        else:
                            openSet.updateItem(neighbour)
                    if steps: neighbour.Show(green,0)
            if start!=current and steps:
                current.Show(red,0)
        if steps: break
    if openSet.count() == 0:
        print("No Solution Found")
        return False
    return True
        
while AStar(steps = True):
    if pygame.event.poll().type == pygame.QUIT:
        pygame.quit()
        sys.exit(0)
    pygame.display.update()

def Clear():
    global openSet,closedSet,path
    for o in openSet.items:
        o.Show(grey,0)
        o.Show((255,255,255), 1)
        o.gCost = 0
        o.hCost = 0
        o.fCost = 0
    for c in closedSet:
        c.gCost = 0
        c.hCost = 0
        c.fCost = 0
        c.parent = None
        if c in path and False:
            continue
        c.Show(grey,0)
        c.Show((255,255,255), 1)
    openSet.clear()
    closedSet=[]
    path=[]
    start.gCost = 0
    start.hCost = 0
    start.fCost = 0
    start.Show(pink,0)
    end.Show(pink,0)

def MoveTargets(selected,moveTo):
    global start,end
    if moveTo.obstacle or moveTo == selected:
        return False
    if selected == start:
        if moveTo == end:
            return False
        
        selected.Show(grey,0)
        selected.Show((255,255,255), 1)
        start = moveTo

    elif selected == end:
        if moveTo == start:
            return False

        selected.Show(grey,0)
        selected.Show((255,255,255), 1)
        end = moveTo
    start.Show(pink,0)
    end.Show(pink,0)
    return True

selected = None
prevStart = start
prevEnd = end
Clear()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: #exiting game
            pygame.quit()
            sys.exit(1)
        if event.type == pygame.MOUSEBUTTONDOWN:
            selected = GetNodeFromPos(pygame.mouse.get_pos())
            if selected != start and selected != end:
                selected = None
        if pygame.mouse.get_pressed()[0]:
                if selected != None: 
                    moveTo = GetNodeFromPos(pygame.mouse.get_pos())
                    if MoveTargets(selected,moveTo):
                        selected = moveTo
        if event.type == pygame.MOUSEBUTTONUP:
            selected = None
    if prevStart != start or prevEnd != end and selected == None:
        path = []
        Clear()
        prevStart = start
        prevEnd = end
        start.parent = start
        openSet.push(start)
        AStar(steps=False)
