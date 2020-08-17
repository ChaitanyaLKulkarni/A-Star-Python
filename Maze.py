import random
#import time


def BacktrackingCreate(pygame, screen, gird):

    for i in range(1, len(gird)-1):
        for j in range(1, len(gird[0])-1):
            gird[i][j].walls = [True for _ in range(4)]

    current = gird[1][1]
    current.visited = True
    stack = []
    stack.append(current)
    while len(stack) > 0:
        current = stack.pop()
        current.Show((224, 146, 49), 0)
        # time.sleep(0.05)
        neighbours = current.GetNotVisitedNeighbours()
        if len(neighbours) > 0:
            stack.append(current)
            nextN = random.choice(neighbours)
            # Next top
            if current.xpos == nextN.xpos and current.ypos > nextN.ypos:
                current.walls[0] = False
                nextN.walls[2] = False
            # Right
            elif current.xpos < nextN.xpos and current.ypos == nextN.ypos:
                current.walls[1] = False
                nextN.walls[3] = False
            # Bottom
            elif current.xpos == nextN.xpos and current.ypos < nextN.ypos:
                current.walls[2] = False
                nextN.walls[0] = False
            # Left
            elif current.xpos > nextN.xpos and current.ypos == nextN.ypos:
                current.walls[3] = False
                nextN.walls[1] = False
            current.Show((255, 255, 255), 0)
            nextN.Show((255, 255, 255), 0)
            nextN.visited = True
            stack.append(nextN)
        current.Show((255, 255, 255), 0)


def RecurciveDivisionCreate(pygame, screen, grid):
    for i in range(1, len(grid)-1):
        for j in range(1, len(grid[0])-1):
            grid[i][j].walls = [False for _ in range(4)]
            grid[i][j].Show((255, 255, 255), 0)
    # TODO: Add Recursive Implementation
    #divide(grid, 1, 1, len(grid) - 1, len(grid[0]) - 1)
