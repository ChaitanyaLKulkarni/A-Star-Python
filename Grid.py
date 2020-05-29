pygame = ""
screen = ""
cols = 35
rows = 35
grid = []
ws = 0
hs = 0
w = 0
h = 0
lastDoing = -1
grey = (220, 220, 220)
pink = (255, 125, 125)
black = (0, 0, 0)
start = -1
end = -1
isChanged = False


def Init(pobject, screenobj):
    global pygame, screen, w, h, ws, hs, grid
    pygame = pobject
    screen = screenobj
    ws, hs = pygame.display.get_surface().get_size()
    w = ws / cols
    h = hs / rows
    grid = [0 for i in range(cols)]

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
        grid[0][i].walls = [True, True, True, True]
        grid[0][i].visited = True
        grid[cols-1][i].walls = [True, True, True, True]
        grid[cols-1][i].visited = True
        grid[cols-1][i].Show(grey, 0)
        grid[i][0].Show(grey, 0)
        grid[i][0].walls = [True, True, True, True]
        grid[i][0].visited = True
        grid[i][rows-1].Show(grey, 0)
        grid[i][rows-1].walls = [True, True, True, True]
        grid[i][rows-1].visited = True


def GetNodeFromPos(pos, onlyTargets=False):
    x = pos[0]
    y = pos[1]
    g1 = x // (ws // cols)
    g2 = y // (hs // rows)
    if onlyTargets:
        if grid[g1][g2] == start or grid[g1][g2] == end:
            return grid[g1][g2]
        else:
            return None
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
        node.walls = [False, True, True, False]
        # node.obstacle = not node.obstacle
        if node.obstacle:
            node.Show((0, 0, 0), 0)  # setting black
        else:
            node.Show(grey, 0)
            node.Show((255, 255, 255), 0)


def SetNeighbours():
    for i in range(cols):
        for j in range(rows):
            grid[i][j].addNeighbours()


def MoveTargets(selected, moveTo):
    global start, end, isChanged
    if moveTo == selected:  # moveTo.obstacle or
        return None
    if selected == start:
        if moveTo == end:
            return None

        selected.Show(grey, 0)
        selected.Show((255, 255, 255), 0)
        start = moveTo

    elif selected == end:
        if moveTo == start:
            return None

        selected.Show(grey, 0)
        selected.Show((255, 255, 255), 0)
        end = moveTo
    start.Show(pink, 0)
    end.Show(pink, 0)
    isChanged = True
    return moveTo


class Node:
    def __init__(self, xpos, ypos):
        self.xpos = xpos
        self.ypos = ypos
        self.gCost = 0
        self.hCost = 0
        self.fCost = 0
        self.neighbours = []
        self.parent = None
        self.walls = [True, True, True, True]  # Top , Right , Bottom, Left
        self.heapIndex = -1
        self.visited = False

    def Show(self, color, st):

        pygame.draw.rect(screen, color, (self.xpos *
                                         w, self.ypos * h, w, h), st)

        if self.walls[0]:  # Top
            pygame.draw.line(screen, black, (self.xpos * w,
                                             self.ypos * h), (self.xpos * w + w,
                                                              self.ypos * h), 2)
        if self.walls[1]:  # Right
            pygame.draw.line(screen, black, (self.xpos * w + w,
                                             self.ypos * h), (self.xpos * w + w,
                                                              self.ypos * h + h), 2)
        if self.walls[2]:  # Bottom
            pygame.draw.line(screen, black, (self.xpos * w,
                                             self.ypos * h + h), (self.xpos * w + w,
                                                                  self.ypos * h + h), 2)
        if self.walls[3]:  # left
            pygame.draw.line(screen, black, (self.xpos * w,
                                             self.ypos * h), (self.xpos * w,
                                                              self.ypos * h + h), 2)

        pygame.display.update()

    def DrawTo(self, other):
        pygame.draw.line(screen, (148, 86, 86),
                         (self.xpos * w + w/2, self.ypos * h + h/2),
                         (other.xpos * w + w/2, other.ypos * h + h/2))
        pygame.display.update()

    def addNeighbours(self):
        x = self.xpos
        y = self.ypos
        top, bottom, right, left = [False, False, False, False]

        # top
        if y > 0 and not self.walls[0] and not grid[x][y-1].walls[2]:
            top = True
            self.neighbours.append(grid[x][y-1])
        # right
        if x < cols - 1 and not self.walls[1] and not grid[x + 1][y].walls[3]:
            right = True
            self.neighbours.append(grid[x + 1][y])
        # bottom
        if y < rows - 1 and not self.walls[2] and not grid[x][y + 1].walls[0]:
            bottom = True
            self.neighbours.append(grid[x][y+1])
        # left
        if x > 0 and not self.walls[3] and not grid[x - 1][y].walls[1]:
            left = True
            self.neighbours.append(grid[x-1][y])

        return

        """ For Diagonal Travel
        # bottom left
        if (x > 0 and y > 0) and (bottom or left):
            self.neighbours.append(grid[x-1][y-1])
        # top left
        if (x > 0 and y < rows - 1) and (top or left):
            self.neighbours.append(grid[x-1][y+1])

        # bottom right
        if (x < cols - 1 and y > 0) and (bottom or right):
            self.neighbours.append(grid[x+1][y-1])

        # top right
        if (x < cols - 1 and y < rows - 1) and (top or right):
            self.neighbours.append(grid[x+1][y+1])
        """

    def GetNotVisitedNeighbours(self):
        ret = []
        x = self.xpos
        y = self.ypos
        # top
        if y > 0 and not grid[x][y-1].visited:
            ret.append(grid[x][y-1])
        # right
        if x < cols - 1 and not grid[x + 1][y].visited:
            ret.append(grid[x + 1][y])
        # bottom
        if y < rows - 1 and not grid[x][y + 1].visited:
            ret.append(grid[x][y+1])
        # left
        if x > 0 and not grid[x - 1][y].visited:
            ret.append(grid[x-1][y])
        return ret

    def __lt__(self, other):
        return self.fCost < other.fCost
