from TileMain import GameState
from copy import deepcopy
from Queue import PriorityQueue
import time


class Node:
    parent = None

    def __init__(self, parent, prev_move, node_state):
        self.parent = parent
        self.move = prev_move
        self.state = deepcopy(node_state)

    def score(self):
        return self.state.score()


def solve(starting_state):
    previous = set()
    node = Node(None, None, starting_state)
    queue = PriorityQueue()
    previous.add(str(starting_state))

    for possible_move in starting_state.generate_moves():
        starting_state.make_move(possible_move)
        new_node = Node(node, possible_move, starting_state)
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
        node.state.make_move(possible_move)
        if str(node.state) not in previous:
            new_node = Node(node, possible_move, node.state)
            queue.put((new_node.score(), time.time(), new_node))
            previous.add(str(node.state))
        node.state.undo_move(possible_move)
    return False


def solved(node):
    path = []
    while node.parent:
        path.append(node.move)
        node = node.parent
    path.reverse()
    return path


if __name__ == "__main__":
    x = input("Please choose the height of the playing field: ")
    y = input("Please choose the width of the playing field: ")
    zeroes = input("Please choose the number of blank spaces on the playing field: ")
    puzzle = []
    print("Please input the playing field one number at a time, left to right, top row to bottom row. Put 0 for the "
          "empty space")
    for i in xrange(x):
        row = []
        for j in xrange(y):
            row.append(input())
        puzzle.append(row)

    for i in puzzle:
        print i

    state = GameState(puzzle, zeroes)
    moves = solve(state)
    print "\n"
    if isinstance(moves, list):
        print "moves: " + str(moves) + "\n"
        for move in moves:
            state.make_move(move)
            for i in state.puzzle:
                print i
            print "\n"
    else:
        print "Puzzle is not solvable"
