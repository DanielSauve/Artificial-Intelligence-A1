class GameState:
    def __init__(self, people_times, not_crossed, crossed, torch):
        self.peopleTimes = people_times
        self.notCrossed = not_crossed
        self.crossed = crossed
        self.torch = torch

    def solved(self):
        return len(self.notCrossed) == 0

    def generate_moves(self):
        if not self.torch:
            return self.power_set_len_2(self.notCrossed)
        else:
            return self.crossed

    def make_move(self, move):
        if self.torch:
            self.torch = not self.torch
            self.crossed.remove(move)
            self.notCrossed.append(move)
            self.sort_people()
            return self.peopleTimes[move]
        else:
            time = 0
            self.torch = not self.torch
            for i in move:
                self.notCrossed.remove(i)
                self.crossed.append(i)
                time = max(time, self.peopleTimes[i])
            self.sort_people()
            return time

    def undo_move(self, move):
        if self.torch:
            for i in move:
                self.crossed.remove(i)
                self.notCrossed.append(i)
        else:
            self.notCrossed.remove(move)
            self.crossed.append(move)
        self.torch = not self.torch
        self.sort_people()

    def sort_people(self):
        list.sort(self.notCrossed)
        list.sort(self.crossed)

    def __str__(self):
        ret = ""
        for i in self.notCrossed:
            ret += str(i)
        ret += "x"
        for i in self.crossed:
            ret += str(i)
        ret += str(self.torch)
        return ret

    def score(self):
        return len(self.notCrossed)

    @staticmethod
    def power_set_len_2(people):
        result = [[]]
        for x in people:
            result.extend([subset + [x] for subset in result])
        ret = []
        for i in result:
            if len(i) == 2:
                ret.append(i)
        ret.sort()
        return ret


if __name__ == "__main__":
    num_people = input("How many people are there: ")
    peopleTimes = []
    print "Please input " + str(num_people) + " times in ascending order"
    for _ in range(num_people):
        i = input()
        peopleTimes.append(i)

    state = GameState(peopleTimes, range(num_people), [], False)
    time = 0
    while not state.solved():
        print "crossed: " + str(state.crossed)
        print "not crossed: " + str(state.notCrossed)
        possible_moves = state.generate_moves()
        print "select a move (0 indexed)"
        print possible_moves
        index = input()
        time += state.make_move(possible_moves[index])
    print ("Congratulations, you won in " + str(time) + " minutes")
