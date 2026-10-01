class Board:
    def __init__(self, rows=2, cols=2):
        self.rows = rows
        self.cols = cols
        self.horizontal = [[False] * cols for _ in range(rows + 1)]
        self.vertical = [[False] * (cols + 1) for _ in range(rows)]
        self.completed = set()
        self.box_owners = {}
        self.move_history = []

    def add_line(self, orientation, row, col):
        from rules import valid_move

        if self.is_complete():
            raise ValueError("The board is already complete.")

        if not valid_move(self, orientation, row, col):
            raise ValueError("Invalid or already-used move.")

        self.move_history.append(
            {
                "horizontal": [line[:] for line in self.horizontal],
                "vertical": [line[:] for line in self.vertical],
                "completed": set(self.completed),
                "box_owners": dict(self.box_owners),
            }
        )

        if orientation == "H":
            self.horizontal[row][col] = True
        else:
            self.vertical[row][col] = True

        self._update_completed()
        return len(self.completed - self.move_history[-1]["completed"])

    def undo_last_move(self):
        if not self.move_history:
            raise ValueError("No moves to undo.")

        previous = self.move_history.pop()
        self.horizontal = [line[:] for line in previous["horizontal"]]
        self.vertical = [line[:] for line in previous["vertical"]]
        self.completed = set(previous["completed"])
        self.box_owners = dict(previous["box_owners"])

    def _update_completed(self):
        completed = set()
        for r in range(self.rows):
            for c in range(self.cols):
                if (
                    self.horizontal[r][c]
                    and self.horizontal[r + 1][c]
                    and self.vertical[r][c]
                    and self.vertical[r][c + 1]
                ):
                    completed.add((r, c))
        self.completed = completed

    def set_box_owners(self, owner_by_box):
        for box, owner in owner_by_box.items():
            self.box_owners[box] = owner

    def is_complete(self):
        total = self.rows * (self.cols + 1) + self.cols * (self.rows + 1)
        used = sum(map(sum, self.horizontal)) + sum(map(sum, self.vertical))
        return used == total

    def display(self, scores, current):
        print()
        print(f"Scores: P1={scores[0]}  P2={scores[1]} | Turn: P{current + 1}")

        for r in range(self.rows + 1):
            print(".".join("---" if self.horizontal[r][c] else "   " for c in range(self.cols)))
            if r < self.rows:
                middle = []
                for c in range(self.cols + 1):
                    wall = "|" if self.vertical[r][c] else " "
                    middle.append(wall)
                    if c < self.cols:
                        owner = self.box_owners.get((r, c))
                        marker = " " if owner is None else str(owner)
                        middle.append(f" {marker} ")
                print("".join(middle))
        print()
