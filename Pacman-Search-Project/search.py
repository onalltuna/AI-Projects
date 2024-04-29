# search.py
# ---------
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


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

from ctypes import sizeof
from logging import NullHandler
from operator import contains, rshift
from platform import node
from sre_parse import State
from tkinter import W
import util


class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return [s, s, w, s, w, w, s, w]


def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"

    from game import Directions
    S = Directions.SOUTH
    W = Directions.WEST
    E = Directions.EAST
    N = Directions.NORTH

    #stack data structure will be used for implementing DFS algorithm
    stack = util.Stack()
    #keep visited nodes in a list to prevent revisitng
    visited = []
    list = []
    path = []

    #Each node is represented with a dictionary
    #it holds the State, Path(to reach the node), Cost(to reach the node),
    # From(from which node we can reach this node), and is it the start node

    #startind node:
    node = {
        "State": problem.getStartState(),
        "Path": path,
        "Cost": 0,
        "From": (0, 0),
        "IsStart": True
    }

    #push starting node to the stack
    stack.push(node)

    #iterative versin of DFS algorithm: while stack is not empty pop an element from the stack
    #if it is not visited visit(add  it to visited list chek if it is the goal state and and its neighbours to the stack)
    #if the current node is the goal then return its path which represents the path from starting node to the goal node
    while (stack.isEmpty() == False):
        cur = stack.pop()
        if (visited.__contains__(cur["State"]) == False):
            visited.append(cur["State"])
            if (problem.isGoalState(cur["State"])):
                newPath = []
                newPath.extend(cur["Path"])
                list.extend(newPath)
                break
            for neighour in problem.getSuccessors(cur["State"])[::-1]:
                newPath = []
                newPath.extend(cur["Path"])
                newPath.append(neighour[1])
                stack.push({
                        "State": neighour[0],
                        "Path": newPath,
                        "Cost": len(newPath),
                        "From": cur["State"],
                        "IsStart": False
                        })
    return list
    util.raiseNotDefined()


def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"

    from game import Directions
    S = Directions.SOUTH
    W = Directions.WEST
    E = Directions.EAST
    N = Directions.NORTH


    #implementation of BFS is very similar to DFS
    # main difference is the data sturcture(Queue for BFS and stack for DFS)
    queue = util.Queue()
    visited = []
    list = []
    path = []

    state = []
    state = problem.getStartState()

    node = {
        "State": state,
        "Path": path,
        "Cost": 0,
        "From": (0, 0),
        "IsStart": True
    }

    queue.push(node)

    while (queue.isEmpty() == False):
        cur = queue.pop()
        if (visited.__contains__(cur["State"]) == False):
            visited.append(cur["State"])
            if (problem.isGoalState(cur["State"])):
                newPath = []
                newPath.extend(cur["Path"])
                list.extend(newPath)
                break
            for neighbour in problem.getSuccessors(cur["State"])[::-1]:
                newPath = []
                newPath.extend(cur["Path"])
                newPath.append(neighbour[1])
                queue.push({
                        "State": neighbour[0],
                        "Path": newPath,
                        "Cost": len(newPath),
                        "IsStart": False
                        })
    return list
    util.raiseNotDefined()


def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"

    #implementation UCS is very similar to DFS and BFS
    # main difference is that UCS uses a priorty queue as the data structure and 
    # calclates the cost of reaching to any node
    # cost of a node equals to cost of its parent + cost of the edge between the node and its parent

    pq = util.PriorityQueue()
    visited = []
    list = []
    path = []

    node = {
        "State": problem.getStartState(),
        "Path": path,
        "Cost": 0,
        "From": (0, 0),
        "IsStart": True
    }

    pq.push(node, node["Cost"])

    while (pq.isEmpty() == False):
        current = pq.pop()
        if (visited.__contains__(current["State"]) == False):
            visited.append(current["State"])
            if (problem.isGoalState(current["State"])):
                newPath = []
                newPath.extend(current["Path"])
                list.extend(newPath)
                break
            for child in problem.getSuccessors(current["State"]):
                newPath = []
                newPath.extend(current["Path"])
                newPath.append(child[1])
                pq.push({
                    "State": child[0],
                    "Path": newPath,
                    "Cost": current["Cost"] + child[2],
                    "From": current["State"],
                    "IsStart": False
                }, current["Cost"] + child[2])

    return list

    util.raiseNotDefined()


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"

    from game import Directions
    S = Directions.SOUTH
    W = Directions.WEST
    E = Directions.EAST
    N = Directions.NORTH

    open = []
    closed = []

    path = []
    state = []
    g = 0
    h = heuristic(problem.getStartState(), problem)
    f = g + h
    c = []

    c.append(g)
    c.append(h)
    c.append(f)
    state.append(problem.getStartState())
    state.append(c)

    node = {
        "Location": problem.getStartState(),
        "Path": path,
        "From": (0, 0),
        "IsStart": True,
        "g": 0,
        "h": h,
        "f": f,
        "State": state
    }
    open.append(node)

    while (open.__len__() != 0):
        openT = sorted(open, key=lambda i: i['f'])
        curNode = openT[0]
        if (problem.isGoalState(curNode["Location"])):
            return curNode["Path"]

        open.remove(curNode)
        closed.append(curNode)
        neigs = []
        neigs.extend(problem.getSuccessors(curNode["Location"]))
        for n in neigs:
            if any(d["Location"] == n[0] for d in closed):
                continue
            cost = curNode["g"] + n[2]
            if any(d["Location"] == n[0] for d in open):
                res = next(
                    (sub for sub in open if sub["Location"] == n[0]), None)
                if (cost < res["g"]):
                    open.remove(res)
            if any(d["Location"] == n[0] for d in closed):
                res = next(
                    (sub for sub in closed if sub["Location"] == n[0]), None)
                if (cost < res["g"]):
                    closed.remove(res)
            if not any(d["Location"] == n[0] for d in open):
                if not any(d["Location"] == n[0] for d in closed):
                    gN = cost
                    hN = heuristic(n[0], problem)
                    fN = gN + hN
                    pathN = []
                    pathN.extend(curNode["Path"])
                    pathN.append(n[1])
                    newNode = {"Location": n[0],
                               "Path": pathN,
                               "From": curNode["Location"],
                               "IsStart": False,
                               "g": gN,
                               "h": hN,
                               "f": fN}
                    open.append(newNode)

    return path
    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
