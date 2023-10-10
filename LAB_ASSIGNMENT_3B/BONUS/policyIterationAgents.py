'''

                                                                        [ Group Number : 21 ]
                                                                          GAUTAM KUMAR MAHAR
                                                                           KanwarRaj Singh
                                                                           
'''
import mdp, util
import numpy as np

from learningAgents import ValueEstimationAgent

class PolicyIterationAgent(ValueEstimationAgent):
    def __init__(self, mdp, discount = 0.9, iterations = 20):
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        states = self.mdp.getStates()
        # initialize policy arbitrarily
        self.policy = {}
        for state in states:
            if self.mdp.isTerminal(state):
                self.policy[state] = None
            else:
                self.policy[state] = self.mdp.getPossibleActions(state)[0]
        # initialize policyValues dict
        self.policyValues = {}
        for state in states:
            self.policyValues[state] = 0

        for i in range(self.iterations):
            self.runPolicyEvaluation()  # In step 1 call policy evaluation to get state values under policy, updating self.policyValues
            self.runPolicyImprovement() # In step 2 call policy improvement, which updates self.policy

    def runPolicyEvaluation(self):
        "*** YOUR CODE HERE ***"
        states = self.mdp.getStates()
        Transiition = np.zeros((len(states), len(states)))
        Rew = np.zeros(len(states))
        statelist = {}
        x = 0
        for state in states:
            statelist[state] = x
            x += 1
        for state in states:
            if not self.mdp.isTerminal(state):
                actions = self.mdp.getPossibleActions(state)
                reward = self.mdp.getReward(state)
                i = statelist[state]
                Rew[i] = reward                
                action = self.policy[state]
                Transiitionitions = self.mdp.getTransiitionitionStatesAndProbs(state, action)
                for Transiitionition in Transiitionitions:
                    tState = Transiitionition[0]
                    tProb = Transiitionition[1]
                    j = statelist[tState]
                    Transiition[i][j] = tProb            
        I = np.eye(len(states))
        A = I - self.discount * Transiition
        V = np.linalg.solve(A, Rew)
        for state in states:
            x = statelist[state]
            self.policyValues[state] = V[x]



#  Run policy improvement using self.policyValues. Should update self.policy. 
    def runPolicyImprovement(self):
        "*** YOUR CODE HERE ***"
        states = self.mdp.getStates()
        for state in states:
            if not self.mdp.isTerminal(state):
                actions = self.mdp.getPossibleActions(state)
                if actions != ():
                    Expectd_Utility = {}
                    for action in actions:
                        qvalue = self.computeQValueFromValues(state, action)
                        Expectd_Utility[action] = qvalue
                    self.policy[state] = max(Expectd_Utility, key = Expectd_Utility.get)
                else:
                    self.policy[state] = None
            else:
                self.policy[state] = None


# Compute the Q-value of action in state from the
    def computeQValueFromValues(self, state, action):
        "*** YOUR CODE HERE ***"
        qvalue = 0.0
        for nextstate, prob in self.mdp.getTransiitionitionStatesAndProbs(state, action):
            Reward = self.mdp.getReward(state)
            qvalue += prob * (Reward + (self.discount * self.policyValues[nextstate]))
        return qvalue
        
    def getValue(self, state):
        return self.policyValues[state]

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)

    def getPolicy(self, state):
        return self.policy[state]

    def getAction(self, state):
        return self.policy[state]
        
        
        
        
