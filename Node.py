class Node:
    def __init__(self, xpos,ypos):
        self.xpos = xpos
        self.ypos = ypos
        self.gCost = 0 
        self.hCost = 0
        self.fCost = 0
        self.neighbours = []
        self.parent = None
        self.Walkable = True
        self.closed = False
    
    def Draw(self,color,border):
        if self.closed == False:
            pygame.draw.rect(screen,color,(self.xpos * w,self.ypos * h, w,h),border)
            pygame.display.update()