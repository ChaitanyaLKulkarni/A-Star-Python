try:
    import pygame
    import sys
    import math
    from tkinter import *
    from tkinter import ttk
    from tkinter import messagebox
    import os
except:
    import install_req  # install packages

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
        self.closed = False
    
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
        

cols = 40
rows = 40
grid = [0 for i in range(cols)]
openSet = []
closedSet = []
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

def SetTarget(pos):
    global start,end
    x = pos[0]
    y = pos[1]
    g1 = x // (800 // cols)
    g2 = y // (800 // rows)
    node = grid[g1][g2]
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
    x = pos[0]
    y = pos[1]
    g1 = x // (800 // cols)
    g2 = y // (800 // rows)
    
    node = grid[g1][g2]
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
openSet.append(start)

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

def main():
    if len(openSet) > 0:
        #TODO: Use heap to get loweset more efficiently
        lowesetIndex = 0
        for i in range(1,len(openSet)):
            if openSet[i].fCost < openSet[lowesetIndex].fCost:
                lowesetIndex = i
        current = openSet[lowesetIndex]
        if start!=current or end!=current:
            current.Show(blue,0)
        if current == end:
            #print("Donee")
            while current.parent != current:
                current.Show(blue,0)
                current = current.parent
            start.Show((255,0,0),0)
            end.Show((255,0,0),0)
            start.Show((0,0,0),3)
            end.Show((0,0,0),3)
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        pygame.quit()   
                        sys.exit(0)
                        break
        else:
            openSet.pop(lowesetIndex)
            closedSet.append(current)

            neighbours = current.neighbours
            for neighbour in neighbours:
                if neighbour not in closedSet:
                    newG,newH = GetGHFrom(current,neighbour)
                    if neighbour not in openSet:
                            openSet.append(neighbour)
                            neighbour.gCost = newG + 10
                    if neighbour.gCost > newG:
                        neighbour.gCost = newG
                        neighbour.hCost = newH
                        neighbour.parent = current
                        neighbour.fCost = neighbour.gCost + neighbour.hCost
                    neighbour.Show(green,0)
            if start!=current:
                current.Show(red,0)
    else:
        print("No Solution Found")
        ag = True
        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN or pygame.QUIT:
                    ag = False
                    pygame.quit()   
                    sys.exit(0)
                    break
        
while True:
    if pygame.event.poll().type == pygame.QUIT:
        pygame.quit()
        sys.exit(0)
    pygame.display.update()
    main()