class GameState:
    def __init__(self, puzzle, zeroes=1):
        self.zeroes = zeroes
        self.puzzle = puzzle
        self.solution = []
        self.generate_solution(len(puzzle), len(puzzle[0]))

    def solved(self):
        return self.puzzle == self.solution

    def generate_solution(self, x, y):
        x_end = x - 1
        y_end = y - 1
        x_start, y_start = 0, 0
        solution = []
        for _ in range(x):
            solution.append([])

        for row in solution:
            for _ in range(y):
                row.append(None)

        current = 1
        while True:
            for i in range(y_start, y_end + 1):
                if current >= x * y + 1 - self.zeroes:
                    solution[x_start][i] = 0
                else:
                    solution[x_start][i] = current
                current += 1
            x_start += 1
            if x_start > x_end:
                break
            for i in range (x_start, x_end + 1):
                if current >= x * y + 1 - self.zeroes:
                    solution[i][y_end] = 0
                else:
                    solution[i][y_end] = current
                current += 1
            y_end -= 1
            if y < y_start:
                break
            i = y_end
            while i >= y_start:
                if current >= x * y + 1 - self.zeroes:
                    solution[x_end][i] = 0
                else:
                    solution[x_end][i] = current
                current += 1
                i -= 1
            x_end -= 1
            if x_end < x_start:
                break
            i = x_end
            while i >= x_start:
                if current >= x * y + 1 - self.zeroes:
                    solution[i][y_start] = 0
                else:
                    solution[i][y_start] = current
                current += 1
                i -= 1
            y_start += 1
            if y_start > y_end:
                break
        self.solution = solution

    def generate_moves(self):
        moves = []
        for i in range(len(self.puzzle)):
            for j in range(len(self.puzzle[0])):
                if not self.puzzle[i][j]:
                    if i != len(self.puzzle) - 1:
                        moves.append([[i, j], [i + 1, j]])
                    if j != len(self.puzzle[0]) - 1:
                        moves.append([[i, j], [i, j + 1]])
                    if i != len(self.puzzle) - 1 and j != len(self.puzzle[0]) - 1:
                        moves.append([[i, j], [i + 1, j + 1]])
                    if i != len(self.puzzle) - 1 and j != 0:
                        moves.append([[i, j], [i + 1, j - 1]])
                else:
                    if i != len(self.puzzle) - 1 and not self.puzzle[i + 1][j]:
                        moves.append([[i, j], [i + 1, j]])
                    if i != len(self.puzzle) - 1 and j != len(self.puzzle[0]) - 1 and not self.puzzle[i + 1][j + 1]:
                        moves.append([[i, j], [i + 1, j + 1]])
                    if j != len(self.puzzle[0]) - 1 and not self.puzzle[i][j + 1]:
                        moves.append([[i, j], [i, j + 1]])
                    if i != len(self.puzzle) - 1 and j != 0 and not self.puzzle[i + 1][j - 1]:
                        moves.append([[i, j], [i + 1, j - 1]])
                    if i < len(self.puzzle) - 2 and j != 0 and self.puzzle[i + 2][j - 1]:
                        moves.append([[i, j], [i + 2, j - 1]])
                    if i < len(self.puzzle) - 2 and j != len(self.puzzle[0]) - 1 and self.puzzle[i + 2][j + 1]:
                        moves.append([[i, j], [i + 2, j + 1]])
                    if i != 0 and j < len(self.puzzle[0]) - 2 and self.puzzle[i - 1][j + 2]:
                        moves.append([[i, j], [i - 1, j + 2]])
                    if i != len(self.puzzle) - 1 and j < len(self.puzzle[0]) - 2 and self.puzzle[i + 1][j + 2]:
                        moves.append([[i, j], [i + 1, j + 2]])
        return moves

    def make_move(self, move):
        [[i, j], [k, l]] = move
        temp = self.puzzle[i][j]
        self.puzzle[i][j] = self.puzzle[k][l]
        self.puzzle[k][l] = temp

    def undo_move(self, move):
        self.make_move(move)

    def score(self):
        diff = 0
        for r in range(len(self.puzzle)):
            for c in range(len(self.puzzle[0])):
                if self.puzzle[r][c] != self.solution[r][c]:
                    diff += 1
        return diff

    def score2(self):
        diff = 0
        for r in range(len(self.puzzle)):
            for c in range(len(self.puzzle[0])):
                diff += abs(self.puzzle[r][c] - self.solution[r][c])
        return diff

    def average_score(self):
        return (self.score()+self.score2())/2

    def __str__(self):
        ret = ""
        for row in self.puzzle:
            for item in row:
                ret += str(item)
        return ret



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
    while not state.solved():
        moves = state.generate_moves()
        print moves
        state.make_move(moves[input()])
        for i in state.puzzle:
            print i
