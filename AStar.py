
start = ""
end = ""

colors = {"Targets": (255, 125, 125),
          "OpenSet": (109, 220, 160),
          "ClosedSet": (224, 146, 49),
          "Path": (109, 166, 160)}


def GetGHFrom(curr, neighbour):
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
        minA = min(abs(end.xpos - neighbour.xpos),
                   abs(end.ypos - neighbour.ypos))
        maxA = max(abs(end.xpos - neighbour.xpos),
                   abs(end.ypos - neighbour.ypos))
        HCost = 1.4 * minA
        HCost += 1 * maxA - minA

    return Gcost, HCost


def SetColors(_name, _value):
    if _name in colors:
        colors[_name] = _value
    else:
        print('Only use "Targets" , "OpenSet", "ClosedSet" , "Path"')


def Solve(_start, _end, openSet, closedSet, path, steps=False):
    global start, end
    start = _start
    end = _end
    while openSet.count() > 0:
        current = openSet.pop()
        if current == end:
            # print("Donee")
            prev = current
            while current.parent != current:
                path.append(current)
                current.Show(colors["Path"], 0)
                prev.DrawTo(current)
                prev = current
                current = current.parent
            start.Show((255, 0, 0), 0)
            end.Show((255, 0, 0), 0)
            # start.Show((0, 0, 0), 3)
            # end.Show((0, 0, 0), 3)
            return False
        else:
            closedSet.append(current)

            neighbours = current.neighbours
            for neighbour in neighbours:
                if neighbour not in closedSet:
                    newG, newH = GetGHFrom(current, neighbour)
                    if neighbour not in openSet.items or neighbour.gCost > newG:
                        neighbour.gCost = newG
                        neighbour.hCost = newH
                        neighbour.parent = current
                        neighbour.fCost = neighbour.gCost + neighbour.hCost
                        if neighbour not in openSet.items:
                            openSet.push(neighbour)
                        else:
                            openSet.updateItem(neighbour)
                    if steps:
                        neighbour.Show(colors["OpenSet"], 0)
            if start != current and steps:
                current.Show(colors["ClosedSet"], 0)
        if steps:
            break
    if openSet.count() == 0:
        print("No Solution Found")
        return False
    return True
