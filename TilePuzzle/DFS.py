from TileMain import GameState


def solve(curr_state):
    if curr_state.solved():
        return True
    previous = set()
    previous.add(str(curr_state))

    for possible_move in curr_state.generate_moves():
        curr_state.make_move(possible_move)
        previous.add(str(curr_state))
        curr_state.undo_move(possible_move)

    for possible_move in curr_state.generate_moves():
        curr_state.make_move(possible_move)
        test = solve2(curr_state, previous, possible_move, 1)
        curr_state.undo_move(possible_move)
        if test:
            return test

    return False


def solve2(curr_state, previous, prev_move, depth):
    if depth >= 128:
        return False

    if curr_state.solved():
        test = [prev_move]
        return test

    possible_moves = []

    for possible_move in curr_state.generate_moves():
        curr_state.make_move(possible_move)
        if str(curr_state) not in previous:
            previous.add(str(curr_state))
            possible_moves.append(possible_move)
        curr_state.undo_move(possible_move)

    for possible_move in possible_moves:
        curr_state.make_move(possible_move)
        test = solve2(curr_state, previous, possible_move, depth + 1)
        if test:
            test2 = [prev_move]
            curr_state.undo_move(possible_move)
            return test2 + test
        curr_state.undo_move(possible_move)

    return False


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
    if moves:
        # moves.pop()
        print "moves: " + str(moves) + "\n"
        for move in moves:
            state.make_move(move)
            for i in state.puzzle:
                print i
            print "\n"
    else:
        print "Puzzle is not solvable"
