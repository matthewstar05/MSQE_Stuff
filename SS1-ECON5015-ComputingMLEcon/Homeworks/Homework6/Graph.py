"""
ECON 5015: Homework 6
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
