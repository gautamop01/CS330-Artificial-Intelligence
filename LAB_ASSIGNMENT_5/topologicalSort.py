class TopologicalSort:
    def __init__(self, vertices, bayes_net):
        self.graph = bayes_net  # Initialize the Bayesian network graph
        self.num_vertices = vertices  # Store the number of vertices in the graph

    def topologicalSortUtil(self, vertex, visited, stack):
        visited[vertex] = True  # Mark the current node as visited

        # Visit all adjacent nodes of the current node
        for neighbor in self.graph[vertex]:
            if visited[neighbor] == False:
                # If the adjacent node has not been visited, recursively call the function
                self.topologicalSortUtil(neighbor, visited, stack)

        stack.append(vertex)  # Add the current node to the result stack

    def topologicalSort(self):
        visited = dict()

        # Initialize the visited dictionary for all vertices to False
        for vertex in self.num_vertices:
            visited[vertex] = False

        result_stack = []  # Initialize an empty stack to store the result

        for vertex in self.num_vertices:
            if visited[vertex] == False:
                # If the vertex has not been visited, call the sorting utility function
                self.topologicalSortUtil(vertex, visited, result_stack)

        print(result_stack[::-1])  # Print the topological sort result in reverse order
        return result_stack[::-1]  # Return the topological sort result in reverse order
