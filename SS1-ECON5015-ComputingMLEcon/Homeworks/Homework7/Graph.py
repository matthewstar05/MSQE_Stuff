"""
ECON 5015: Homework 6 & 7
Matthew Suban
@matthewsuban
"""

# the graph class is a collection of nodes & edges,
# see node method below
class Graph:
    def __init__(self):
        self.nodes = {} # name -> node

    def size(self):
        return len(self.nodes)

    def add_nodes(self, names):
        for name in names:
            if name not in self.nodes: # skip if already there
                self.nodes[name] = Node(name)

    def add_edge(self, n1, n2, w):
        if n1 in self.nodes and n2 in self.nodes:
            # undirected so add it both ways
            self.nodes[n1].add_edge(n2, w)
            self.nodes[n2].add_edge(n1, w)

    def get_names(self):
        return list(self.nodes.keys())

    def get_node(self, n):
        if n in self.nodes:
            return self.nodes[n]
        return -1

    # Homework 7, shortest_path method
    def shortest_path(self, n1, n2):
        # compute the shortest path from n1 to n2
        # return -1 if n1 or n2 is not in the graph
        if n1 not in self.nodes or n2 not in self.nodes:
            return -1

        # initialize the distance and path dictionaries
        E = {n: 0 for n in self.nodes}
        D = {n: 1 for n in self.nodes}
        path = {n: None for n in self.nodes}

        # iterate until the distance dictionary is equal to the previous distance dictionary
        while D != E:
            D = dict(E)
            for n in self.nodes:
                if n == n2:
                    continue
                node = self.nodes[n]
                best_d = None
                best_m = None
                for m in node.get_neighbors():
                    dm = node.get_weight(m) + D[m]
                    if best_d is None or dm < best_d:
                        best_d = dm
                        best_m = m
                E[n] = best_d
                path[n] = best_m

        # construct the route
        route = [n1]
        while route[-1] != n2:
            route.append(path[route[-1]])

        return [D[n1], route, D] # return the distance, route, and distance dictionary

class Node:
    def __init__(self, name):
        self.name = name
        self.edges = {} # neighbor -> weight

    def get_weight(self, n):
        if n in self.edges:
            return self.edges[n]
        return -1

    def add_edge(self, n, w):
        self.edges[n] = w # overwrites old weight too

    def num_neighbors(self):
        return len(self.edges)

    def get_neighbors(self):
        return list(self.edges.keys())
