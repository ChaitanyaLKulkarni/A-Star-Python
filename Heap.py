class Heap:
    def __init__(self):
        self.items = []
        self.currentIndex = 0

    def push(self,item):
        item.heapIndex = self.currentIndex
        self.items.append(item)
        self.SortUp(item)
        self.currentIndex+=1

    def pop(self):
        retItem = self.items.pop(0)
        self.currentIndex -=1
        if self.currentIndex > 0:
            self.items.insert(0,self.items.pop())
            self.items[0].heapIndex = 0
            self.SortDown(self.items[0])
        return retItem

    def updateItem(self,item):
        self.SortUp(item)

    def contains(self,item):
        return self.items[item.heapIndex] == item

    def count(self):
        return self.currentIndex

    def clear(self):
        self.currentIndex = 0
        self.items = []
    

    def SortDown(self,item):
        while True:
            childIndexLeft = item.heapIndex * 2 + 1
            childIndexRight = item.heapIndex * 2 + 2
            swapIndex = 0

            if childIndexLeft < self.currentIndex:
                swapIndex = childIndexLeft

                if childIndexRight < self.currentIndex:
                    if self.items[childIndexRight] < self.items[childIndexLeft]:
                        swapIndex = childIndexRight

                if self.items[swapIndex] < item:
                    self.Swap(item,self.items[swapIndex])
                else:
                    break
            else:
                break


    def SortUp(self,item):
        parentIndex = (item.heapIndex-1) // 2
        while parentIndex >= 0:
            if item < self.items[parentIndex]:
                self.Swap(self.items[parentIndex],item)
            else:
                break
            parentIndex = (item.heapIndex-1) // 2
    
    def Swap(self,itemA,itemB):
        self.items[itemA.heapIndex],self.items[itemB.heapIndex] = self.items[itemB.heapIndex] , self.items[itemA.heapIndex]
        itemA.heapIndex , itemB.heapIndex = itemB.heapIndex, itemA.heapIndex