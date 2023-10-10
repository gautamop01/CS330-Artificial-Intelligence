'''

                                                                        [ Group Number : 21 ]
                                                                          GAUTAM KUMAR MAHAR
                                                                           KanwarRaj Singh
                                                                           
'''

# valueIterationAgents.py
# -----------------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


# valueIterationAgents.py
# -----------------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


import mdp, util

from learningAgents import ValueEstimationAgent
import collections

class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp: mdp.MarkovDecisionProcess, discount = 0.9, iterations = 100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the RESULTulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
              mdp.isTerminal(state)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter() # A Counter is a dict with default 0
        self.runValueIteration()

    def runValueIteration(self):
        # Write value iteration code here
        "*** YOUR CODE HERE ***"
        for _ in range(1, self.iterations+1): #Run self.iteration times of value iteration algorithm
            PREV_VALUE = self.values.copy() # Copy old self.values to avoid overwriting problem when updating the current self.values
            for state in self.mdp.getStates():
                if self.mdp.isTerminal(state): # If current state is terminal state, then set its value to 0
                    self.values[state] = 0
                    continue
                MAXI_VALUE = -1e9 # Initalize MAXI_VALUE to a small value, this variable will track the value of all possible actions
                for action in self.mdp.getPossibleActions(state): # Iterate all possible action
                    SUM_OF_ALL_STATE = 0
                    for (nextState, prob) in self.mdp.getTransitionStatesAndProbs(state, action): # Get all the possible state and their coresponding probability
                        # Use the main formula of value iteration method to update self.values
                        # Noticed that I use PREV_VALUE to compute the correct update value
                        SUM_OF_ALL_STATE += prob * (self.mdp.getReward(state, action, nextState) + self.discount*PREV_VALUE[nextState]) 
                    MAXI_VALUE = max(MAXI_VALUE, SUM_OF_ALL_STATE) # Taking max over the corRESULTponding value of all possible state
                self.values[state] = MAXI_VALUE # set self.values to the maximum possible value
                

    def getValue(self, state):
            """
            Return the value of the state (computed in __init__).
            """
            return self.values[state]

    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        "*** YOUR CODE HERE ***"
        RESULT = 0 # Initialize q value
        for (nextState, prob) in self.mdp.getTransitionStatesAndProbs(state, action): # Get all teh possible state and their coresponding probability
            RESULT += prob * (self.mdp.getReward(state, action, nextState) + self.discount*self.values[nextState]) # Compute q-value using formula
        return RESULT # return q value

    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        "*** YOUR CODE HERE ***"
        #check for terminal
        if self.mdp.isTerminal(state): # If this state is a terminal state, then agents can't move. Therefore, return None
            return None
        actions = self.mdp.getPossibleActions(state) # Otherwise, get all possible actions
        Q_VAL = util.Counter() # Initailze a Counter to track every q value after taking action
        for action in actions:
            Q_VAL[action] = self.getQValue(state, action) # Using getQValue to get q-value after taking this action

        return Q_VAL.argMax() # argMax will return the key (which is action in this function) that has the highest q-value
        


    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)
