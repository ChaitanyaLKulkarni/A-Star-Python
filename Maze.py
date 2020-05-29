import random
#import time


def Create(pygame, screen, gird):
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
