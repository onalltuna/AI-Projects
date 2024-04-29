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


from audioop import avg
from doctest import FAIL_FAST
from hashlib import new
from xxlimited import foo
from util import manhattanDistance
from game import Directions
import random
import util

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
        scores = [self.evaluationFunction(
            gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(
            len(scores)) if scores[index] == bestScore]
        # Pick randomly among the best
        chosenIndex = random.choice(bestIndices)

        "Add more of your code here if you want to"

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
        newScaredTimes = [
            ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        currentScore = successorGameState.getScore()

        ghostPositions = successorGameState.getGhostPositions()
        futureGhostDistances = []

        for ghostP in ghostPositions:
            futureGhostDistances.append(
                abs(ghostP[0] - newPos[0]) + abs(ghostP[1] - newPos[1]))

        curPos = currentGameState.getPacmanPosition()
        foodDistanceSum1 = 0
        foodDistanceSum2 = 0

        for food in newFood.asList():
            foodDistanceSum1 = foodDistanceSum1 + \
                (abs(food[0] - curPos[0]) + abs(food[1] - curPos[1]))

        for food in newFood.asList():
            foodDistanceSum2 = foodDistanceSum2 + \
                (abs(food[0] - newPos[0]) + abs(food[1] - newPos[1]))

            if (foodDistanceSum2 < foodDistanceSum1):
                currentScore = currentScore + 50
            if (currentGameState.getFood().asList().__contains__(newPos)):
                currentScore = currentScore + 200
            if (futureGhostDistances.__contains__(0.0) or futureGhostDistances.__contains__(1.0)):
                currentScore = currentScore - 150000

        return currentScore



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

    def __init__(self, evalFn='scoreEvaluationFunction', depth='2'):
        self.index = 0  # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)


class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def maxValue(self, gameState, curDepth, index):

        x = -150000
        index2 = (index + 1) % gameState.getNumAgents()
        curAct = ""

        for act in gameState.getLegalActions(index):
            y = self.value(gameState.generateSuccessor(
                index, act), curDepth - 1, index2)
            if (y["Value"] > x):
                x = y["Value"]
                curAct = act

        return {"Action": curAct,
                "Value": x}

    def minValue(self, gameState, curDepth, index):

        x = 150000
        index2 = (index + 1) % gameState.getNumAgents()
        curAct = ""

        for act in gameState.getLegalActions(index):
            y = self.value(gameState.generateSuccessor(
                index, act), curDepth - 1, index2)
            if (y["Value"] < x):
                x = y["Value"]
                curAct = act

        return {"Action": curAct,
                "Value": x}

    def value(self, gameState, curDepth, index):

        if (gameState.isWin() or gameState.isLose() or curDepth == 0):
            return {"Action": "",
                    "Value": self.evaluationFunction(gameState)}

        if (index % gameState.getNumAgents() == 0):
            return self.maxValue(gameState, curDepth, index)
        elif (index % gameState.getNumAgents() != 0):
            return self.minValue(gameState, curDepth, index)

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"

        return self.value(gameState, self.depth * gameState.getNumAgents(), self.index)["Action"]

        util.raiseNotDefined()


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def value(self, gameState, curDepth, index, a, b):

        if (gameState.isWin() or gameState.isLose() or curDepth == 0):
            return {"Action": "",
                    "Value": self.evaluationFunction(gameState)}

        if (index % gameState.getNumAgents() == 0):
            return self.maxValue(gameState, curDepth, index, a, b)
        elif (index % gameState.getNumAgents() != 0):
            return self.minValue(gameState, curDepth, index, a, b)

    def maxValue(self, gameState, curDepth, index, a, b):

        x = -150000
        index2 = (index + 1) % gameState.getNumAgents()
        curAct = ""

        for act in gameState.getLegalActions(index):
            y = self.value(gameState.generateSuccessor(
                index, act), curDepth - 1, index2, a, b)
            if (y["Value"] > x):
                x = y["Value"]
                curAct = act
                if (x > b):
                    return {"Action": curAct,
                            "Value": x}
                a = max(a, x)

        return {"Action": curAct,
                "Value": x}

    def minValue(self, gameState, curDepth, index, a, b):

        x = 150000
        index2 = (index + 1) % gameState.getNumAgents()
        curAct = ""

        for act in gameState.getLegalActions(index):
            y = self.value(gameState.generateSuccessor(
                index, act), curDepth - 1, index2, a, b)
            if (y["Value"] < x):
                x = y["Value"]
                curAct = act
                if (x < a):
                    return {"Action": curAct,
                            "Value": x}
                b = min(b, x)

        return {"Action": curAct,
                "Value": x}

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        return self.value(gameState, self.depth * gameState.getNumAgents(), self.index, -15000, 15000)["Action"]




class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def maxValue(self, gameState, curDepth, index):

        x = -150000
        index2 = (index + 1) % gameState.getNumAgents()
        curAct = ""

        for act in gameState.getLegalActions(index):
            y = self.value(gameState.generateSuccessor(
                index, act), curDepth - 1, index2)
            if (y["Value"] > x):
                x = y["Value"]
                curAct = act

        return {"Action": curAct,
                "Value": x}

    def minValue(self, gameState, curDepth, index):

        acts = gameState.getLegalActions(index)
        numActs = len(acts)
        index2 = (index + 1) % gameState.getNumAgents()
        t = 0

        for act in acts:
            y = self.value(gameState.generateSuccessor(
                index, act), curDepth - 1, index2)
            t += y["Value"]

        return {"Action": act,
                "Value": t / numActs}

    def value(self, gameState, curDepth, index):

        if (gameState.isWin() or gameState.isLose() or curDepth == 0):
            return {"Action": "",
                    "Value": self.evaluationFunction(gameState)}

        if (index % gameState.getNumAgents() == 0):
            return self.maxValue(gameState, curDepth, index)
        elif (index % gameState.getNumAgents() != 0):
            return self.minValue(gameState, curDepth, index)

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        return self.value(gameState, self.depth * gameState.getNumAgents(), self.index)["Action"]




def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: First, I get the score of the current state. 
    Then I subtracted the average distances to the capsules from the score in a weighted manner. 
    Then I added/subtracted (depending on whether ghosts are scared or not) the average distances to the ghosts 
    again in a weighted manner.
    """
    "*** YOUR CODE HERE ***"
    x = 0
    y2 = 0

    capsules = currentGameState.getCapsules()

    x += currentGameState.getScore()

    for capsule in capsules:
        y2 += (util.manhattanDistance(capsule,
               currentGameState.getPacmanPosition()))

    if (len(capsules) != 0):
        x -= 2*(y2 / len(capsules))

    ghostStates = currentGameState.getGhostStates()
    ghostPositions = currentGameState.getGhostPositions()

    newScaredTimes = [
        ghostState.scaredTimer for ghostState in ghostStates]

    for ghostP in ghostPositions:
        if (newScaredTimes[0] >= 1):
            x += 55 / \
                (util.manhattanDistance(currentGameState.getPacmanPosition(), ghostP))
        else:
            x -= 55 * \
                (util.manhattanDistance(currentGameState.getPacmanPosition(), ghostP))
    return x


# Abbreviation
better = betterEvaluationFunction
