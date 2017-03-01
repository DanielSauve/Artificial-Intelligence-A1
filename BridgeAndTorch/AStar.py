from BridgeAndTorchMain import GameState
from copy import deepcopy
from Queue import PriorityQueue
import time


class Node:
    parent = None

    def __init__(self, parent, prev_move, node_state, cost):
        self.parent = parent
        self.move = prev_move
        self.state = deepcopy(node_state)
        self.cost = cost

    def score(self):
        return (self.state.score() + self.cost)/2


def solve(starting_state):
    previous = set()
    node = Node(None, None, starting_state, 0)
    queue = PriorityQueue()
    previous.add(str(starting_state))

    for possible_move in starting_state.generate_moves():
        cost = starting_state.make_move(possible_move)
        new_node = Node(node, possible_move, starting_state, cost)
        queue.put((new_node.score(), time.time(), new_node))
        previous.add(str(starting_state))
        starting_state.undo_move(possible_move)

    while not queue.empty():
        (_, _, prio) = queue.get()
        test = solve2(prio, queue, previous)
        if test:
            return test


def solve2(node, queue, previous):
    if node.state.solved():
        return solved(node)
    for possible_move in node.state.generate_moves():
        cost = node.state.make_move(possible_move)
        if str(node.state) not in previous:
            new_node = Node(node, possible_move, node.state, cost)
            queue.put((new_node.score(), time.time(), new_node))
            previous.add(str(node.state))
        node.state.undo_move(possible_move)
    return False


def solved(node):
    moves = []
    while node.parent:
        moves.append(node.move)
        node = node.parent
    moves.reverse()
    return moves


if __name__ == "__main__":
    num_people = input("How many people are there: ")
    peopleTimes = []
    print "Please input " + str(num_people) + " times in ascending order"
    for _ in range(num_people):
        i = input()
        peopleTimes.append(i)

    state = GameState(peopleTimes, range(num_people), [], False)
    moves = solve(state)
    if moves:
        print "moves: " + str(moves) + "\n"
        for move in moves:
            state.make_move(move)
            print "crossed: " + str(state.crossed)
            print "not crossed: " + str(state.notCrossed)
            print "\n"
