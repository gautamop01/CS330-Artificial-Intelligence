# # Define a class for a Bayesian Network
# class BayesNet:
#     def __init__(self):
#         self.variables = {}  # Initialize a dictionary to store variables and their values
#         self.cpt = {}  # Initialize a dictionary to store Conditional Probability Tables (CPTs)

#     def add_variable(self, variable, values):
#         self.variables[variable] = values  # Add variable names and their possible values to the dictionary
#         self.cpt[variable] = {}  # Initialize an empty CPT for the variable

#     def set_cpt(self, variable, parents, probabilities):
#         try:
#             self.cpt[variable][tuple(parents)] = probabilities  # Set the CPT for a variable given its parents
#         except:
#             return  # Handle exceptions gracefully

# # Define an adjacency list and parents dictionary for the Bayesian Network
# # adj_list = {'B': ['A'], 'E': ['A'], 'A': ['J', 'K'], 'J': [], 'M': ['K'], 'K' : []}  # Define the parent-child relationships
# # parents = {'A': ['B', 'E'], 'B': [], 'E': [], 'J': ['A'], 'K': ['A'], 'M': ['K'], 'M':[]}  # Define the parents of each variable
# adj_list = {'B': ['A'], 'E': ['A'], 'A': ['J', 'K'], 'J': [],'K':[], 'M': []}  # Define the parent-child relationships
# parents = {'A': ['B', 'E'], 'B': [], 'E': [], 'J': ['A'],'K':['A'], 'M': ['K']}  # Define the parents of each variable

# # Function to load a Bayesian Network from a file
# def load_bayesian_network(file_path):
#     network = BayesNet()  # Create an instance of the BayesNet class
#     with open(file_path, 'r') as file:  # Open the file for reading
#         lines = file.read().splitlines()  # Read the lines from the file and split them

#     variables_line = lines[0].split(', ')  # Split the first line to get variable names
#     variable_names = variables_line[1:]  # Extract variable names
#     for variable in variable_names:
#         network.add_variable(variable, ['+{}'.format(variable.lower()), '-{}'.format(variable.lower())])
#         # Add variables and their possible values to the network

#     variable_index = 1  # Initialize an index for processing lines
#     current_variable = None  # Initialize a variable to keep track of the current variable being processed
#     while variable_index < len(lines):
#         line = lines[variable_index]  # Get the current line
#         if not line:
#             variable_index += 1  # If the line is empty, move to the next line
#             continue
#         if line == '|':
#             variable_index += 1  # If the line is a pipe ("|"), move to the next line
#             continue
#         if line == 'Query:':
#             break  # If the line is "Query:", exit the loop as CPTs are finished
#         if ',' not in line:
#             current_variable = line.strip()  # Set the current variable based on the line
#             variable_index += 1  # Move to the next line
#         else:
#             variable_values = line.strip().split(', ')  # Split the line to get variable values
#             parents = [v for v in variable_values[1:] if v in variable_names]  # Extract parent variable names
#             probabilities_line = lines[variable_index + 1].split(', ')  # Get the line with probabilities
#             try:
#                 probabilities = [float(probabilities_line[i]) for i in range(1, len(probabilities_line))]
#             except:
#                 probabilities = []  # Extract and convert probabilities to a list, handle exceptions
#             network.set_cpt(current_variable, parents, probabilities)  # Set the CPT for the current variable
#             variable_index += 2  # Move to the next variable

#     return network  # Return the constructed Bayesian network

# # Define variable names, variables, and conditional probability tables
# variable_names = ['B', 'E', 'A', 'J','K', 'M']  # Define the names of the variables
# variables = {'B': ['+b', '-b'], 'E': ['+e', '-e'], 'A': ['+a', '-a'], 'J': ['+j', '-j'], 'K':['+k', '-k'], 'M': ['+m', '-m']}
# # Define possible values for each variable
# cpts = {
#     'B': {'+b': 0.001, '-b': 0.999},  # Define the CPT for variable B
#     'E': {'+e': 0.002, '-e': 0.998},  # Define the CPT for variable E
#     'A': {('+b', '+e', '+a'): 0.95, ('+b', '+e', '-a'): 0.05, ('+b', '-e', '+a'): 0.94, ('+b', '-e', '-a'): 0.06,
#           ('-b', '+e', '+a'): 0.29, ('-b', '+e', '-a'): 0.71, ('-b', '-e', '+a'): 0.001, ('-b', '-e', '-a'): 0.999},
#     # Define the CPT for variable A
#     'J': {('+a', '+j'): 0.9, ('+a', '-j'): 0.1, ('-a', '+j'): 0.05, ('-a', '-j'): 0.95},  # Define the CPT for variable J
#     'M': {('+a', '+m'): 0.7, ('+a', '-m'): 0.3, ('-a', '+m'): 0.01, ('-a', '-m'): 0.99},


#     # Define the CPT for variable M
#     'K': {('+m','+k'): 0.9, ( '-m','+k',): 0.6, ('+m','-k'): 0.1, ( '-m','-k'): 0.4}
# }

# # Define a query
# query = {'query_variable': 'B', 'query_value': '+b', 'evidence': {'J': '+j', 'M': '+m', 'K':'+k'}}
# # Define a query with the query variable, its value, and evidence variables with their values

# # Function to parse a Bayesian Network from a file
# def Parse(file_path):
#     network = BayesNet()  # Create an instance of the BayesNet class
#     with open(file_path, 'r') as file:  # Open the file for reading
#         lines = file.read().splitlines()  # Read the lines from

# Example usage
adj_list = {
    'B': ['A'],
    'E': ['A'],
    'A': ['J', 'K'],
    'J': [],
    'K': ['M'],
    'M': [],

}

parents = {
    'A': ['B', 'E'],
    'B': [],
    'E': [],
    'J': ['A'],
    'K': ['A'],
    'M': ['K'],
}

variable_names = ['B', 'E', 'A', 'J','K', 'M']

variables = {
    'B': ['+b', '-b'],
    'E': ['+e', '-e'],
    'A': ['+a', '-a'],
    'J': ['+j', '-j'],
    'K': ['+k', '-k'],
    'M': ['+m', '-m']
}

cpts = {
    'B': {'+b': 0.001, '-b': 0.999},
    'E': {'+e': 0.002, '-e': 0.998},
    'A': {('+b', '+e', '+a'): 0.95, ('+b', '+e', '-a'): 0.05, ('+b', '-e', '+a'): 0.94, ('+b', '-e', '-a'): 0.06,
          ('-b', '+e', '+a'): 0.29, ('-b', '+e', '-a'): 0.71, ('-b', '-e', '+a'): 0.001, ('-b', '-e', '-a'): 0.999},
    'J': {('+a', '+j'): 0.9, ('+a', '-j'): 0.1, ('-a', '+j'): 0.05, ('-a', '-j'): 0.95},
    'M': {('+a', '+m'): 0.7, ('+a', '-m'): 0.3, ('-a', '+m'): 0.01, ('-a', '-m'): 0.99},
    'K': {('+k','+m'): 0.9, ( '+k','-m',): 0.1, ('-k','+m'): 0.1, ( '-k','-m'): 0.9}
}

query = {
    'query_variable': 'B',
    'query_value': '+b',
    'evidence': {'J': '+j', 'M': '+m','K':'+k'}
}

