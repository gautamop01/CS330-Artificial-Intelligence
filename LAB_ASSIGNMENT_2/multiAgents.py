'''
    Group number - 21
    Name - Gautam Kuamr Mahar 
    Roll N - 2103114

    Name - kanwar raj singh
    Roll N - 1903122
'''


# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scoresult = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scoresult)
        bestIndices = [index for index in range(len(scoresult)) if scoresult[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        # util.pause()
        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        curPos = currentGameState.getPacmanPosition()

        # Go Forward! You can go straight or in a turn, but never halt or reverse direction.
        if action == Directions.STOP or action == Directions.REVERSE[currentGameState.getPacmanState().getDirection()]:
            return -99999

        result = successorGameState.getScore()
        # Calculate average distance from ghosts to encourage staying away from them.
        avrage_dist_from_the_ghost = 0
        if len(newGhostStates) > 0:
            avrage_dist_from_the_ghost = sum([util.manhattanDistance(newPos, ghost.getPosition()) for ghost in newGhostStates])
            avrage_dist_from_the_ghost /= len(newGhostStates)
        result += avrage_dist_from_the_ghost

        # Calculate average distance from food to encourage getting closer to food.
        FOODLIST = newFood.asList() # (From Question instruction) Note: Remember that newFood has the function asList()
        avrage_dist_from_the_FOOD = 0
        if len(FOODLIST) > 0:
            avrage_dist_from_the_FOOD = sum([util.manhattanDistance(newPos, food) for food in FOODLIST])
            avrage_dist_from_the_FOOD /= len(FOODLIST)
        result -= avrage_dist_from_the_FOOD

        return result

def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(AGENT_INDEX):
        Returns a list of legal actions for an agent
        AGENT_INDEX=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(AGENT_INDEX, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        value, action = self._max_value(gameState, 0, 1)
        return action

    def _value(self, gameState, AGENT_INDEX, depth):
        # Check if the game is already in a win or lose state, return the evaluation value and no action.
        if gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState), None

        if AGENT_INDEX == 0:
        # If the current agent is Pacman (agent 0), check if the maximum depth is reached, return value and no action.
            if depth == self.depth:
                return self.evaluationFunction(gameState), None
            # Call _max_value for the next ply with incremented depth.
            return self._max_value(gameState, AGENT_INDEX, depth + 1)

        # For other agents, call _min_value.
        return self._min_value(gameState, AGENT_INDEX, depth)

    def _max_value(self, gameState, AGENT_INDEX, depth):
        v = float("-inf")
        a = None
        AGENT_NEXT = (AGENT_INDEX + 1) % gameState.getNumAgents()
        # Explore legal actions for the current agent (Pacman).
        for action in gameState.getLegalActions(AGENT_INDEX):
            # Get the value from the next ply by recursively calling _value.
            value, _ = self._value(gameState.generateSuccessor(AGENT_INDEX, action), AGENT_NEXT, depth)
            if value > v:
                v = value
                a = action
        return v, a

    def _min_value(self, gameState, AGENT_INDEX, depth):
        v = float("inf")
        a = None
        AGENT_NEXT = (AGENT_INDEX + 1) % gameState.getNumAgents()
       # Explore legal actions for the ghost agent.
        for action in gameState.getLegalActions(AGENT_INDEX):
            # Get the value from the next ply by recursively calling _value.
            value, _ = self._value(gameState.generateSuccessor(AGENT_INDEX, action), AGENT_NEXT, depth)
            if value < v:
                v = value
                a = action
        return v, a


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        alpha, beta = float("-inf"), float("inf")
        value, action = self._max_value(gameState, 0, alpha, beta, 1)
        return action

    def _value(self, gameState, AGENT_INDEX, alpha, beta, depth):
           # Check if the game is already in a win or lose state, return the evaluation value and no action.
        if gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState), None

        if AGENT_INDEX == 0:
        # If the current agent is Pacman (agent 0), check if the maximum depth is reached, return value and no action.
            if depth == self.depth:
                return self.evaluationFunction(gameState), None
             # Call _max_value for the next ply with incremented depth.
            return self._max_value(gameState, AGENT_INDEX, alpha, beta, depth + 1)
        # For other agents, call _min_value
        return self._min_value(gameState, AGENT_INDEX, alpha, beta, depth)

    def _max_value(self, gameState, AGENT_INDEX, alpha, beta, depth):
        v = float("-inf")
        a = None
        local_alpha = alpha

        AGENT_NEXT = (AGENT_INDEX + 1) % gameState.getNumAgents()
        # Explore legal actions for the current agent (Pacman).
        for action in gameState.getLegalActions(AGENT_INDEX):
            # Get the value from the next ply by recursively calling _value.
            value, _ = self._value(gameState.generateSuccessor(AGENT_INDEX, action), AGENT_NEXT, local_alpha, beta, depth)
            if value > v:
                v = value
                a = action
                if v > beta:
                    return v, a # Prune the search if value exceeds beta.
                local_alpha = max(local_alpha, v)  # Update alpha.

        return v, a

    def _min_value(self, gameState, AGENT_INDEX, alpha, beta, depth):
        v = float("inf")
        a = None
        local_beta = beta

        AGENT_NEXT = (AGENT_INDEX + 1) % gameState.getNumAgents()
        # Explore legal actions for the ghost agent.
        for action in gameState.getLegalActions(AGENT_INDEX):
            # Get the value from the next ply by recursively calling _value.
            value, _ = self._value(gameState.generateSuccessor(AGENT_INDEX, action), AGENT_NEXT, alpha, local_beta, depth)
            if value < v:
                v = value
                a = action
                if v < alpha:
                    return v, a # Prune the search if value falls below alpha.
                local_beta = min(local_beta, v)  # Update beta.

        return v, a


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        value, action = self._max_value(gameState, 0, 1)
        return action

    def _value(self, gameState, AGENT_INDEX, depth):
        # Check if the game is already in a win or lose state, return the evaluation value and no action.
        if gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState), None

        if AGENT_INDEX == 0:
            # If the current agent is Pacman (agent 0), check if the maximum depth is reached, return value and no action.
            if depth == self.depth:
                return self.evaluationFunction(gameState), None
            # Call _max_value for the next ply with incremented depth.
            return self._max_value(gameState, AGENT_INDEX, depth + 1)
        # For other agents, call _exp_value.
        return self._exp_value(gameState, AGENT_INDEX, depth)

    def _max_value(self, gameState, AGENT_INDEX, depth):
        v = float("-inf")
        a = None
        AGENT_NEXT = (AGENT_INDEX + 1) % gameState.getNumAgents()
        # Explore legal actions for the current agent (Pacman)
        for action in gameState.getLegalActions(AGENT_INDEX):
            # Get the value from the next ply by recursively calling _value.
            value, _ = self._value(gameState.generateSuccessor(AGENT_INDEX, action), AGENT_NEXT, depth)
            if value > v:
                v = value
                a = action
        return v, a

    def _exp_value(self, gameState, AGENT_INDEX, depth):
        v = 0
        actions = gameState.getLegalActions(AGENT_INDEX)
        p = 1 / len(actions)   # Probability of each action for the ghost.

        AGENT_NEXT = (AGENT_INDEX + 1) % gameState.getNumAgents()
        for action in actions:
             # Get the value from the next ply by recursively calling _value.
            value, _ = self._value(gameState.generateSuccessor(AGENT_INDEX, action), AGENT_NEXT, depth)
            v += p * value # # Accumulate expected values with probabilities.
        return v, None

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: Prefer states that maximize score, while keeping pacman
                 near the food with scared ghosts
    """
    # Extract useful information from the current game state
    pos = currentGameState.getPacmanPosition()
    food = currentGameState.getFood()
    ghostStates = currentGameState.getGhostStates()
    scaredTimes = [ghostState.scaredTimer for ghostState in ghostStates]
    power_pellets = currentGameState.getCapsules()

    # favor states that will increase our score
    result = currentGameState.getScore()

    # Let's prefer states that maximize the time ghosts are scared
    result += sum(scaredTimes)

    # Let's favor states that get us nearer to food.
    FOODLIST = food.asList()
    avrage_dist_from_the_FOOD = 0
    if len(FOODLIST) > 0:
        avrage_dist_from_the_FOOD = sum([util.manhattanDistance(pos, food) for food in FOODLIST])
        avrage_dist_from_the_FOOD /= len(FOODLIST)
    result -= avrage_dist_from_the_FOOD

    return result

# Abbreviation
better = betterEvaluationFunction