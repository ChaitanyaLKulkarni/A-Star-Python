A* Algorithm:
    Cost of moving straight is 1
    Cost of moving diagonally is 1.4

    Top left represent G-cost: distance from starting node
    top right representH-Cost: distance from end node
    middle represent F-Cost = G cost + h cost

    Calcuate neighbor costs
        only update nieghbor if f cost is lower 
            set neighbor-> prev to current node 
    Choice one w/ Lowest F-cost
        mark that as close
        calculate cost of niegbhor
        repeat

    If There are more than 1 with loweset F cost:
        check closeset h cost

Algo:

OpenList //for storing nodes to be evaluated
ClosedList //the set of nodes already evaluated

add Start to OpenList

while len(OpenList) > 0:
    current = node in OpenList w/ lowest f_cost
    remove current from OpenList
    add Current to ClosedList

    if current is Target node :
        return and backtrack the path

    foreach neighbor of target node
        if neighbour is not traversable or in Closed
            continue to next
        
        if new path to neighbour is shorter or not in OpenList
            set f_cost of neighbour
            set parent of neghbhour to current
            if neighbour no in OpenList 
                add to OpenList
