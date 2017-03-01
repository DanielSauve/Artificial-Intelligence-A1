from BridgeAndTorchMain import GameState
from copy import deepcopy
from Queue import Queue


class Node:
    parent = None

    def __init__(self, parent, move, state):
        self.parent = parent
        self.move = move
        self.state = deepcopy(state)


def solve(state):
    previous = set()
    node = Node(None, None, state)
    queue = Queue()
    previous.add(str(state))

    for possible_move in state.generate_moves():
        state.make_move(possible_move)
        new_node = Node(node, possible_move, state)
        queue.put(new_node)
        previous.add(str(state))
        state.undo_move(possible_move)

    while not queue.empty():
        test = solve2(queue.get(), queue, previous)
        if test:
            print test
            return test


def solve2(node, queue, previous):
    if node.state.solved():
        return solved(node)
    for possible_move in node.state.generate_moves():
        node.state.make_move(possible_move)
        if str(node.state) not in previous:
            new_node = Node(node, possible_move, node.state)
            queue.put(new_node)
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
