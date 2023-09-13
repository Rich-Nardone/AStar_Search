
# This class represent a graph
class Graph:

    # Initialize the class
    def __init__(self, graph_dict=None, directed=True):
        self.graph_dict = graph_dict or {}
        self.directed = directed
        if not directed:
            self.make_undirected()

    # Create an undirected graph by adding symmetric edges
    def make_undirected(self):
        for a in list(self.graph_dict.keys()):
            for (b, dist) in self.graph_dict[a].items():
                self.graph_dict.setdefault(b, {})[a] = dist

    # Add a link from A and B of given distance, and also add the inverse link if the graph is undirected
    def connect(self, A, B, distance=1):
        self.graph_dict.setdefault(A, {})[B] = distance
        if not self.directed:
            self.graph_dict.setdefault(B, {})[A] = distance

    # Get neighbors or a neighbor
    def get(self, a, b=None):
        links = self.graph_dict.setdefault(a, {})
        if b is None:
            return links
        else:
            return links.get(b)

    # Return a list of nodes in the graph
    def nodes(self):
        s1 = set([k for k in self.graph_dict.keys()])
        s2 = set([k2 for v in self.graph_dict.values() for k2, v2 in v.items()])
        nodes = s1.union(s2)
        return list(nodes)

# This class represent a node
class Node:

    # Initialize the class
    def __init__(self, name:str, parent:str):
        self.name = name
        self.parent = parent
        self.g = 0 # Distance to start node
        self.h = 0 # Distance to goal node
        self.f = 0 # Total cost

    # Compare nodes
    def __eq__(self, other):
        return self.name == other.name

    # Sort nodes
    def __lt__(self, other):
         return self.f < other.f

    # Print node
    def __repr__(self):
        return ('({0},{1})'.format(self.position, self.f))

# A* search
def astar_search(graph, heuristics, start, end):
    
    # Create lists for open nodes and closed nodes
    open = []
    closed = []
    # Create a start node and an goal node
    start_node = Node(start, None)
    goal_node = Node(end, None)

    # Add the start node
    open.append(start_node)
    steps=0
    
    # Loop until the open list is empty
    while len(open) > 0:
        weights = ''
        steps+=1
        # Sort the open list to get the node with the lowest cost first
        open.sort()

        # Get the node with the lowest cost
        current_node = open.pop(0)

        # Add the current node to the closed list
        closed.append(current_node)
        
        # Check if we have reached the goal, return the path
        if current_node == goal_node:
            path = []
            while current_node != start_node:
                path.append(current_node.name + ': ' + str(current_node.g))
                current_node = current_node.parent
            path.append(start_node.name + ': ' + str(start_node.g))
            # Return reversed path
            return path[::-1]

        # Get neighbours
        neighbors = graph.get(current_node.name)
        
        
        # Loop neighbors
        for key, value in neighbors.items():
 
            # Create a neighbor node
            neighbor = Node(key, current_node)

            # Check if the neighbor is in the closed list
            if(neighbor in closed):
                continue

            # Calculate full path cost
            
            neighbor.g = current_node.g + graph.get(current_node.name, neighbor.name)
            neighbor.h = heuristics.get(neighbor.name)
            neighbor.f = neighbor.g + neighbor.h
            weights+=(neighbor.name+' g('+str(neighbor.g)+') +'+' h('+str(neighbor.h)+')'+' = f('+str(neighbor.f)+'),')
            # Check if neighbor is in open list and if it has a lower f value
            for node in open: 
                if (neighbor == node and neighbor.f > node.f):
                    continue

            # Everything is green, add neighbor to open list
            open.append(neighbor)
        weights_arr = weights.split(',')
        weights = ''
        for i in range(len(weights_arr)):
            if(weights_arr[i+1] == ''):
                weights+= weights_arr[i]+'.'
                break
            weights+= weights_arr[i]+', '
        print('Step '+str(steps)+': '+current_node.name+' --> '+weights)
    # Return None, no path is found
    return None

# The main entry point for this module
def main():
    
    # Create a graph
    graph = Graph()

    # Create graph connections (Actual distance)
    graph.connect('Oradea', 'Zerind', 71)
    graph.connect('Oradea', 'Sibiu', 151)
    graph.connect('Zerind', 'Arad', 75)
    graph.connect('Arad', 'Sibiu', 140)
    graph.connect('Arad', 'Timisoara', 118)
    graph.connect('Timisoara', 'Lugoj', 111)
    graph.connect('Lugoj', 'Mehadia', 70)
    graph.connect('Mehadia', 'Dobreta', 75)
    graph.connect('Dobreta', 'Craiova', 120)
    graph.connect('Craiova', 'Rimnicu Vilcea', 146)
    graph.connect('Craiova', 'Piesti', 138)
    graph.connect('Rimnicu Vilcea', 'Sibiu', 80)
    graph.connect('Rimnicu Vilcea', 'Pitesti', 97)
    graph.connect('Pitesti', 'Bucharest', 101)
    graph.connect('Sibiu', 'Fagaras', 99)
    graph.connect('Fagaras', 'Bucharest', 211)
    graph.connect('Bucharest', 'Giurgiu', 90)
    graph.connect('Bucharest', 'Urziceni', 85)
    graph.connect('Urziceni', 'Hirsova', 98)
    graph.connect('Urziceni', 'Vaslui', 142)
    graph.connect('Hirsova', 'Eforie', 86)
    graph.connect('Vaslui', 'Iasi', 92)
    graph.connect('Iasi', 'Neamt', 87)

    # Make graph undirected, create symmetric connections
    graph.make_undirected()

    # Create heuristics (straight-line distance to Bucharest)
    heuristics = {}
    heuristics['Arad'] = 366
    heuristics['Bucharest'] = 0
    heuristics['Craiova'] = 160
    heuristics['Dobreta'] = 242
    heuristics['Eforie'] = 161
    heuristics['Fagaras'] = 176
    heuristics['Giurgiu'] = 77
    heuristics['Hirsova'] = 151
    heuristics['Iasi'] = 226
    heuristics['Lugoj'] = 244
    heuristics['Mehadia'] = 241
    heuristics['Neamt'] = 234
    heuristics['Oradea'] = 380
    heuristics['Pitesti'] = 100
    heuristics['Rimnicu Vilcea'] = 193
    heuristics['Sibiu'] = 253
    heuristics['Timisoara'] = 329
    heuristics['Urziceni'] = 80
    heuristics['Vaslui'] = 199
    heuristics['Zerind'] = 374
    
    # Run the search algorithm
    path = astar_search(graph, heuristics, 'Arad', 'Bucharest')
    print('Path:')
    print(path)
# Tell python to run main method
if __name__ == "__main__": main()