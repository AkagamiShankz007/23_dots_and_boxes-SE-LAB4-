from board import Board
from rules import valid_move, completed_boxes


class DotsAndBoxes:
    def __init__(self):
        self.board = Board()
        self.current = 0
        self.scores = [0, 0]
        self._state_history = []

    def apply_move(self, orientation, row, col):
        if not valid_move(self.board, orientation, row, col):
            raise ValueError("Invalid or already-used move.")

        if self.board.is_complete():
            raise ValueError("The board is already complete.")

        self._state_history.append({"scores": self.scores.copy(), "current": self.current, "box_owners": dict(self.board.box_owners)})
        before = set(self.board.completed)
        self.board.add_line(orientation, row, col)
        newly_completed = completed_boxes(self.board, before)

        if newly_completed:
            owner_by_box = {box: self.current + 1 for box in self.board.completed - before}
            self.board.set_box_owners(owner_by_box)
            self.scores[self.current] += newly_completed
            return newly_completed

        self.current = 1 - self.current
        return 0

    def undo_last_move(self):
        if not self._state_history:
            print("No moves to undo.")
            return False

        previous = self._state_history.pop()
        self.board.undo_last_move()
        self.scores = previous["scores"]
        self.current = previous["current"]
        self.board.box_owners = dict(previous["box_owners"])
        print("Last move undone.")
        return True

    def run(self):
        print("Dots and Boxes")
        print("Enter moves as H row col or V row col.")
        print("Rows and columns start at 0.")
        print("Use 'UNDO' to undo the previous move.")
        print("Example: H 0 1")

        while not self.board.is_complete():
            self.board.display(self.scores, self.current)
            raw = input(f"Player {self.current + 1}, move: ").strip().upper()

            if raw in {"UNDO", "U"}:
                self.undo_last_move()
                continue

            parts = raw.split()
            if len(parts) != 3:
                print("Invalid format.")
                continue

            orientation, row, col = parts
            if not row.isdigit() or not col.isdigit():
                print("Row and column must be numbers.")
                continue

            row, col = int(row), int(col)

            try:
                newly_completed = self.apply_move(orientation, row, col)
            except ValueError as exc:
                print(exc)
                continue

            if newly_completed:
                print(f"Player {self.current + 1} completed {newly_completed} box(es) and plays again.")
            else:
                print(f"Player {self.current + 1} moved.")

        self.board.display(self.scores, self.current)
        print("Game over!")
        if self.scores[0] == self.scores[1]:
            print("The game is a draw.")
        else:
            winner = 1 if self.scores[0] > self.scores[1] else 2
            print(f"Player {winner} wins!")
