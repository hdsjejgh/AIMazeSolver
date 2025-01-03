from collections import deque


class Node:
    def __init__(self,state,parent,action,steps):
        self.state = state
        self.parent = parent
        self.action = action
        self.steps = steps

class StackFrontier:
    def __init__(self):
        self.frontier = [];
    def AddNode(self,node):
        self.frontier.append(node)
    def GetNode(self, x):
        return self.frontier.pop()
    def empty(self):
        return len(self.frontier)==0
    def contains(self,state):
        return any(node.state==state for node in self.frontier)

class QueueFrontier:
    def __init__(self):
        self.frontier = deque([])
    def GetNode(self, x):
        return self.frontier.popleft()
    def AddNode(self,node):
        self.frontier.append(node)
    def empty(self):
        return len(self.frontier)==0
    def contains(self,state):
        return any(node.state==state for node in self.frontier)

class HeuristicFrontier: #frontier that returns node closest to goal
    def __init__(self):
        self.frontier = []

    def GetNode(self,goal):
        def GetDist(node,goal):
            total = 0
            for i in range(2):
                total += abs(goal[i] - node.state[i])+node.steps
            return total
        min = 0
        for i,ii in enumerate(self.frontier):
            if GetDist(ii,goal) < min:
                min = i
        node = self.frontier[min]
        self.frontier.pop(min)
        return node

    def AddNode(self,node):
        self.frontier.append(node)
    def empty(self):
        return len(self.frontier)==0
    def contains(self,state):
        return any(node.state==state for node in self.frontier)


class Maze:
    def __init__(self, file,frontierType=StackFrontier):
        with open(file) as f:
            self.contents = f.read().splitlines()
        self.height = len(self.contents)
        self.width = max(len(x) for x in self.contents)
        self.frontier = frontierType()
        self.walls=[]
        for r in range(len(self.contents)):
            row = []
            for c in range(len(self.contents[r])):
                try:
                    square = self.contents[r][c]
                    if square=="B":
                        self.goal = (r,c)
                        row.append(False)
                    elif square=="A":
                        self.start = (r,c)
                        row.append(False)
                    elif square == " ":
                        row.append(False)
                    else:
                        row.append(True)
                except IndexError:
                    row.append(True)
            self.walls.append(row)
        self.explored = set()
        self.solution = None
    def neighbors(self, state):
        row, col = state
        candidates = [
            ("up", (row - 1, col)),
            ("down", (row + 1, col)),
            ("left", (row, col - 1)),
            ("right", (row, col + 1))
        ]

        result = []
        for action, (r, c) in candidates:
            if 0 <= r < self.height and 0 <= c < self.width and not self.walls[r][c]:
                result.append((action, (r, c)))
        return result
    def solve(self):
        steps=0
        start = Node(self.start, None, None,steps)
        self.frontier.AddNode(start)
        while True:
            if self.frontier.empty():
                print("No solution")
                return
            node = self.frontier.GetNode(self.goal)
            steps+=1
            if node.state == self.goal:
                self.solution = self.getSol(node)
                self.print()
                print("Solution found")
                return
            self.explored.add(node.state)
            for action, sta in self.neighbors(node.state):
                if (not self.frontier.contains(sta)) and (sta not in self.explored):
                    self.frontier.AddNode(Node(state=sta,parent=node,action=action,steps=steps))
    def getSol(self,node):
        solution =[]
        while (node.parent!=None):
            solution.append(node.parent.state)
            node = node.parent
        return solution
    def print(self):
        result = ""
        for r in range(len(self.contents)):
            row = ""
            for c in range(len(self.contents[r])):

                try:
                    if self.contents[r][c]=="#":
                        row+="■"
                    elif self.contents[r][c] in ("B","A"):
                        row+="#"
                    elif self.contents[r][c]==" ":
                        if (r,c) in self.solution:
                            row+="O"
                        elif (r,c) in self.explored:
                            row+="."
                        else:
                            row+=" "
                except:
                    row += "■"
            row+="\n"
            result+=row
        print(result)


m1=Maze("maze4.txt",QueueFrontier)#solves maze with QueueFrontier (Breadth First Search)
m1.solve()

m2=Maze("maze4.txt",StackFrontier)#solves maze with StackFrontier (Depth First Search)
m2.solve()

m3=Maze("maze5.txt",HeuristicFrontier)#solves maze with StackFrontier (Depth First Search)
m3.solve()