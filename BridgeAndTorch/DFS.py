from BridgeAndTorchMain import GameState


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
    if depth >= 256:
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
    num_people = input("How many people are there: ")
    peopleTimes = []
    print "Please input " + str(num_people) + " times in ascending order"
    for _ in range(num_people):
        i = input()
        peopleTimes.append(i)

    state = GameState(peopleTimes, range(num_people), [], False)
    moves = solve(state)

    print "crossed: " + str(state.crossed)
    print "not crossed: " + str(state.notCrossed)
    print "\n"
    if moves:
        print "moves: " + str(moves) + "\n"
        for move in moves:
            state.make_move(move)
            print "crossed: " + str(state.crossed)
            print "not crossed: " + str(state.notCrossed)
            print "\n"
    else:
        print "Puzzle is not solvable"
