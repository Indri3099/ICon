# This is a sample Python script.

# Press Maiusc+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from dataclasses import dataclass, field
from queue import PriorityQueue


class Node:
    f: int = 0
    g: int = 0
    h: int = 0

    def __init__(self, value, x, y):
        self.parent = None
        self.value = value
        self.x = x
        self.y = y

    def set_parent(self, node):
        self.parent = node

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def get_val(self):
        return self.value

    def is_same(self, node):
        return self.value == node.value

    def set_g(self, value):
        self.g = value
        self.set_f()

    def set_h(self, value):
        self.h = value
        self.set_f()

    def set_f(self):
        self.f = self.g + self.h

    def __str__(self):
        return str(self.value)


# @dataclass(order=True)
# class PrioritizedItem:
#     priority: float
#     counter: int
#     item: object = field()
#
#     def get_node(self):
#         return self.item
#
#     def __str__(self):
#         return str(item)

class Graph:
    def __init__(self):
        self.node = []
        self.connections = {}

    def addnode(self, node):
        self.node.append(node)

    def connect(self, node1, node2, weight):
        if type(weight).__name__ != "int" and type(weight).__name__ != "float":
            raise Exception("Weight can only be a integer value and not {}".format(type(weight).__name__))
        if node1 in self.node and node2 in self.node:
            if node1 in self.connections:
                all_nodes = self.connections.get(node1)
                all_nodes[node2] = weight
            else:
                self.connections[node1] = {node2: weight}
            # Utile solo se il grafo non è orientato--------------------
            if node2 in self.connections:
                all_nodes = self.connections.get(node2)
                all_nodes[node1] = weight
            else:
                self.connections[node2] = {node1: weight}
            # -----------------------------------------------------------
        else:
            raise Exception("{} - {} is not a valid path".format(node1, node2))

    def pathweight(self, node1, node2):
        if node1 in self.connections and node2 in self.connections:
            # if node1 in self.connections or node2 in self.connections:
            connection1 = self.connections.get(node1)
            if node2 in connection1:
                return connection1.get(node2)
            else:
                raise Exception("{} & {} are not connected".format(node1, node2))
        else:
            raise Exception("{} - {} is not a valid path".format(node1, node2))

    def connection(self, node):
        result = []
        if node in self.connections:
            for connection_nodes in self.connections.get(node):
                result.append(connection_nodes)
            return result
        else:
            return result
            # raise Exception("{} is not a valid node".format(node))

    def connectionmap(self, node):
        if node in self.connections:
            return self.connections.get(node)
        else:
            raise Exception("{} is not a valid node".format(node))

    def nodes(self):
        return self.node

    def __str__(self):
        return self.__class__.__name__

    @staticmethod
    def euristic(node1, node2):
        return abs(node1.get_x() - node2.get_x()) + abs(node1.get_y() - node2.get_y())

    def min_euristic(self, node):
        minimum = 666
        tempnode = Node(0, 0, 0)
        for noding in self.connections.get(node):
            newmin = self.euristic(node, noding)
            if newmin < minimum:
                tempnode = noding
                minimum = newmin
        return tempnode

    def a_star(self, start, goal):

        if start not in self.connections or goal not in self.connections:
            raise Exception("Non sono stati forniti nodi validi.")

        open_list = list()
        start.set_g(0)
        start.set_h(self.euristic(start, goal))
        closed_list = list()
        open_list.append(start)


        while len(open_list) != 0:
            current = minSearch(open_list)
            open_list.remove(current)
            if current == goal:
                break
            successor: Node
            for successor in self.connection(current):
                successor_current_cost = current.g + self.pathweight(current, successor)
                if successor in open_list:
                    if successor.g <= successor_current_cost:
                        break
                elif successor in closed_list:
                    if successor.g <= successor_current_cost:
                        continue
                else:
                    open_list.append(successor)
                    successor.set_h(self.euristic(successor, goal))
                successor.set_g(successor_current_cost)
                successor.set_parent(current)
            closed_list.append(current)

def minSearch(list: list()):
    min = Node("", 100, 100)
    min.set_g(9999)
    min.set_h(9999)
    for item in list:
        item: Node()
        if item.f <= min.f:
            min = item
    return min


def printPath(node, path):
    node: Node()
    if node.parent == None:
        path.append(node)
    else:
        printPath(node.parent, path)
        path.append(node)


graph = Graph()
A = Node("A", 1, 2)
B = Node("B", 3, 5)
C = Node("C", 2, 3)
D = Node("D", 6, 2)
E = Node("E", 12, 6)
#
# A = Node("A", 1, 1)
# B = Node("B", 1, 1)
# C = Node("C", 1, 1)
# D = Node("D", 1, 1)
# E = Node("E", 1, 1)

graph.addnode(A)
graph.addnode(B)
graph.addnode(C)
graph.addnode(D)
graph.addnode(E)
graph.connect(E, A, 2)
graph.connect(A, D, 5)
graph.connect(A, B, 1)
graph.connect(E, B, 1)
graph.connect(A, C, 1)
graph.connect(C, D, 1)

goal = D
graph.a_star(E, goal)
path = list()
printPath(goal, path)

for node in path:
    if node != goal:
        print(node, end="->")
    else:
        print(node)
print("Costo= " + str(goal.g))

# for item in final_list:
#     print(item)