'''

                                                                        [ Group Number : 21 ]
                                                                          GAUTAM KUMAR MAHAR
                                                                           KanwarRaj Singh
                                                                           
'''

import random  # Import the random module for generating random numbers
from topologicalSort import TopologicalSort  # Import a custom module named "_topologicalSorting" that contains a TopologicalSort class

class BayesianNetwork:
    def __init__(self):
        self.variables = {}  # Initialize a dictionary to store variable names and their possible values
        self.cpt = {}  # Initialize a dictionary to store conditional probability tables

    def add_variable(self, variable, values):
        self.variables[variable] = values  # Add a variable name and its possible values to the dictionary
        self.cpt[variable] = {}  # Initialize the conditional probability table for this variable

    def set_cpt(self, variable, parents, probabilities):
        # Set the conditional probability table for a variable given its parents
        self.cpt[variable][tuple(parents)] = probabilities

    def get_cpt(self, variable, parents):
        if variable in self.cpt:
            prob = self.cpt[variable].get(tuple(parents), None)  # Retrieve conditional probabilities from the table
        return 1  # Return a default value of 1 if not found
    

# Define a function for calculating the query probability
def calculate_query_probability(sorted_nodes, variable_names, variables, cpts, query):
    num_samples = 100000  # Adjust the number of samples as needed
    evidence = query['evidence']  # Extract evidence from the query
    query_variable = query['query_variable']  # Extract the variable for which the probability is being calculated
    query_value = query['query_value']  # Extract the value to compare against

    count_match = 0

    # Loop to generate samples and calculate the probability
    for _ in range(num_samples):
        samples = prior_sampling_with_evidence(sorted_nodes, variable_names, variables, cpts, evidence)
        canCount = True

        # Check if the sample matches the evidence for each observed variable
        for k in evidence:
            if samples[k] != evidence[k]:
                canCount = False

        # Check if the sample matches the query conditions
        if samples[query_variable] == query_value and canCount:
            count_match += 1

    probability = count_match / num_samples  # Calculate the probability
    return probability

# Define a function for choosing a value based on a probability
def choose_from_probability(variable, plusProb):
    r = random.random()
    if r <= plusProb:
        return variable[0]  # Choose the first value in the variable
    else:
        return variable[1]  # Choose the second value in the variable

# Define a function for generating samples
def sampling(sorted_nodes, variable_names, variables, cpts, evidence):
    samples = {}

    # Loop through sorted nodes to sample values
    for node in sorted_nodes:
        cpt = cpts[node]
        parent = parents[node] 
        values = variables[node]

        if not parent:
            # If no parents, sample according to the marginal distribution
            samples[node] = choose_from_probability(values, cpt[values[0]])
        else:
            # If there are parents, sample according to the conditional distribution
            parent_values = tuple(samples[p] for p in parent)
            probabilities = [cpt[parent_values + (value,)] for value in values]
            samples[node] = choose_from_probability(values, probabilities[0])

    return samples


# -------------- START --------------

def prior_sampling_with_evidence(sorted_nodes, variable_names, variables, cpts, evidence):
    samples = {}  # Initialize an empty dictionary to store sampled values

    for node in sorted_nodes:
        cpt = cpts[node]  # Get the conditional probability table for the current node
        parent = parents[node]  # Get the parents of the current node
        values = variables[node]  # Get the possible values for the current node

        if not parent:
            # If there are no parents, sample according to the marginal distribution
            samples[node] = random.choice(values)  # Choose a value randomly from the possible values
        else:
            # If there are parents, sample according to the conditional distribution
            parent_values = tuple(samples[p] for p in parent)  # Collect values of parent nodes from samples
            probabilities = [cpt[parent_values + (value,)] for value in values]  # Collect conditional probabilities
            samples[node] = random.choices(values, probabilities)[0]  # Choose a value based on probabilities

    return samples  # Return the sampled values as a dictionary

# Define a function for rejection sampling
def rejection_sampling(adj_list, variable_names, variables, cpts, query):
    num_samples = 50000  # Adjust the number of samples as needed
    evidence = query['evidence']  # Extract evidence from the query
    query_variable = query['query_variable']  # Extract the variable for which the probability is being calculated
    query_value = query['query_value']  # Extract the value to compare against

    count_match = 0
    count_total = 0
    i = 0

    # Loop to perform rejection sampling
    while count_total != num_samples:
        samples = sampling(adj_list, variable_names, variables, cpts, evidence)
        canCount = True

        # Check if the sample matches the evidence for each observed variable
        for k in evidence:
            if samples[k] != evidence[k]:
                canCount = False
                break

        if canCount:
            count_total += 1

        # Check if the sample matches the query conditions
        if samples[query_variable] == query_value and canCount:
            count_match += 1

        i += 1

    # Print debugging information (optional)
    # print(i, count_match, count_total)

    probability = count_match / count_total  # Calculate the final probability
    return probability


# def likelihood_weighting(sorted_nodes, variable_names, variables, cpts, query, parents):
#     num_samples = 100000  # Adjust the number of samples as needed
#     evidence = query['evidence']
#     query_variable = query['query_variable']
#     query_value = query['query_value']

#     count_match = 0
#     weighted_count_match = 0

#     for _ in range(num_samples):
#         samples = prior_sampling_with_evidence(sorted_nodes, variable_names, variables, cpts, evidence, parents)
#         canCount = True
#         for k in evidence:
#             if samples[k] != evidence[k]:
#                 canCount = False
#         if canCount:
#             if samples[query_variable] == query_value:
#                 weighted_count_match += 1
#             count_match += 1

#     probability = weighted_count_match / count_match if count_match > 0 else 0
#     return probability

def calculate_prob(variable,sample,evidence,query_variable,query_value):

    bn = BayesianNetwork()
    ans1,ans2=False,True
    if sample[query_variable]==query_value:
        ans1=True
    for var in evidence:
        if sample[var]!=evidence[var]:
            ans2=False
            break
    
    return ans1,ans2,bn.get_cpt(variable,sample)


# Define a function for likelihood weighting
def likelihood_weighting(adj_list, variable_names, variables, cpts, query):
    num_samples = 500000  # Specify the number of samples
    num_csamples = 0  # Initialize the count of consistent samples
    evidence = query['evidence']  # Extract evidence from the query
    query_variable = query['query_variable']  # Extract the variable for which the probability is being calculated
    query_value = query['query_value']  # Extract the value to compare against

    count_match = 0  # Initialize the count of matching samples

    for i in range(num_samples):
        weighted_count = 0  # Initialize weighted_count inside the loop
        weighted_total = 0  # Initialize weighted_total inside the loop
        samples = sampling(adj_list, variable_names, variables, cpts, evidence)

        # Calculate the consistency of the query variable and evidence
        ans1, ans2, prob = calculate_prob(query_variable, samples, evidence, query_variable, query_value)
        
        if ans2:
            num_csamples += 1
            if ans1:
                count_match += 1

        if samples[query_variable] == query_value:
            weighted_count += 1  # Increment the count of weighted matching samples
        weighted_total += 1 # Increment the count of total weighted samples
        
        # count_match += weighted_count  # Optional: Count matching samples

    # Calculate the final probability based on consistent samples
    probability = count_match / num_csamples
    return probability



# def calculate_conditional_prob(variable, sample, adj_list, cpts):
#     parent_values = tuple(sample[parent] for parent in adj_list[variable])
#     conditional_probabilities = [cpts[variable][parent_values + (value,)] for value in variables[variable]]
#     total_probability = sum(conditional_probabilities)
#     normalized_probabilities = [p / total_probability for p in conditional_probabilities]
#     return normalized_probabilities

def calculate_conditional_prob(variable, sample, adj_list, cpts, variables):
    parent_values = tuple(sample[parent] for parent in adj_list[variable])
    
    if variable in cpts and parent_values in cpts[variable]:
        conditional_probabilities = [cpts[variable][parent_values][value] for value in variables[variable]]
    else:
        # Handle missing conditional probabilities gracefully
        conditional_probabilities = [0.0] * len(variables[variable])

    total_probability = sum(conditional_probabilities)
    
    if total_probability != 0:
        normalized_probabilities = [p / total_probability for p in conditional_probabilities]
    else:
        # If total_probability is 0, assign equal probabilities to all values
        num_values = len(variables[variable])
        normalized_probabilities = [1.0 / num_values] * num_values

    return normalized_probabilities



# Define a function for Gibbs sampling
def gibbs_sampling(adj_list, variable_names, variables, cpts, query, num_samples):
    # Initialize a count for consistent samples and create an initial random sample
    count_cmatch = 0
    sample = {variable: random.choice(variables[variable]) for variable in variable_names}
    num_csamples = 0
    
    query_variable = query['query_variable']  # Extract the query variable from the query
    query_value = query['query_value']  # Extract the query value from the query
    evidence = query['evidence']  # Extract evidence from the query
    
    count_match = 0

    for _ in range(num_samples):
        # Iterate through variables in a random order
        for variable in random.sample(variable_names, len(variable_names)):
            if variable != query_variable and variable not in evidence:
                # Calculate the conditional distribution for the current variable given the sample and evidence
                conditional_probabilities = calculate_conditional_prob(variable, sample, adj_list, cpts, variables)
                
                # Sample a new value for the current variable based on the conditional distribution
                new_value = random.choices(variables[variable], conditional_probabilities)
                sample[variable] = new_value[0]

        # Check if the sample is consistent with the provided evidence
        canCount = True
        for k in evidence:
            if sample[k] != evidence[k]:
                canCount = False
                break
        
        if canCount:
            # Check if the query variable in the sample matches the specified query value
            if sample[query_variable] == query_value:
                count_match += 1
        # Generate a new sample for the next iteration
        sample = sampling(adj_list, variable_names, variables, cpts, evidence)

        # Check the consistency and calculate the probability of the query
        ansQueryVariableAllValsFlag, ansEvidenceVarsAllValsFlag, prob = calculate_prob(query_variable, sample, evidence, query_variable, query_value)
        
        if ansEvidenceVarsAllValsFlag:
            num_csamples += 1
            if ansQueryVariableAllValsFlag:
                count_cmatch += 1
        
    # Calculate the final probability based on consistent samples
    probability = count_cmatch / num_csamples
    return probability



# Define the calculate_conditional_prob function as previously shown

# Example usage:
# probability = gibbs_sampling(adj_list, variable_names, variables, cpts, query, num_samples=100000)
# print(f'P({query["query_variable"]}={query["query_value"]} | {", ".join(f"{var}={val}" for var, val in query["evidence"].items())}) = {probability}')


from parse import *

sortedN = TopologicalSort(variable_names, adj_list)
ls = sortedN.topologicalSort()

sortDict = {i: adj_list[i] for i in ls}


# probability = gibbs_sampling(adj_list, variable_names, variables, cpts, query, num_samples=100000)
# print(f'P({query["query_variable"]}={query["query_value"]} | {", ".join(f"{var}={val}" for var, val in query["evidence"].items())}) = {probability}')


# Likelihood Weighting
print("Likelihood Weighting :")
probability_likelihood_weighting = likelihood_weighting(sortDict, ls, variables, cpts, query)
print(f'P({query["query_variable"]}={query["query_value"]} | {", ".join(f"{var}={val}" for var, val in query["evidence"].items())}) = {probability_likelihood_weighting}')

# # Gibbs Sampling
# num_samples_gibbs = 50000  # Adjust the number of Gibbs samples as needed
# probability_gibbs = gibbs_sampling(sortDict, ls, variables, cpts, query, num_samples_gibbs)
# print(f'Gibbs Sampling: P({query["query_variable"]}={query["query_value"]} | {", ".join(f"{var}={val}" for var, val in query["evidence"].items())}) = {probability_gibbs}')

# Print an empty line for separation
print('')

# Print a message indicating the start of prior sampling
print("Prior Sampling :")

# Call the 'prior_sampling_with_evidence' function to generate samples and print the result
print(prior_sampling_with_evidence(sortDict, ls, variables, cpts, query))

# Calculate the probability of the query using prior sampling and print the result
probability = calculate_query_probability(sortDict, ls, variables, cpts, query)
print(f'P({query["query_variable"]}={query["query_value"]} | {", ".join(f"{var}={val}" for var, val in query["evidence"].items())}) = {probability}')

# -------------
# Print an empty line for separation
print('')

# Print a message indicating the start of Gibbs sampling
print("Gibbs Sampling :")

# Set the number of samples for Gibbs sampling
num_samples = 5000000 

# Calculate the probability of the query using Gibbs sampling and print the result
probability = gibbs_sampling(adj_list, variable_names, variables, cpts, query, num_samples)
print(f'Sample = P({query["query_variable"]}={query["query_value"]} | {", ".join(f"{var}={val}" for var, val in query["evidence"].items())}) = {probability}')

# Print an empty line for separation
print('')

# Print a message indicating the start of rejection sampling
print("Rejection Sampling :")

# Calculate the probability of the query using rejection sampling and print the result
probability = rejection_sampling(sortDict, ls, variables, cpts, query)
print(f'P({query["query_variable"]}={query["query_value"]} | {", ".join(f"{var}={val}" for var, val in query["evidence"].items())}) = {probability}')
