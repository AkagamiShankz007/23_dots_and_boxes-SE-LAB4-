# Scenario 23 - Dots and Boxes

## Overview

Dots and Boxes is a turn-based grid game. Players draw one line at a time between adjacent dots. Completing the fourth side of a box claims that box, earns a point, and gives the same player another turn.

The starter project is deliberately split into separate modules for game flow, board state, and rule validation. Read the existing implementation carefully before changing it.

## How to run

From this folder:

```text
python main.py
```

Enter moves in the form:

```text
H row column
```

or

```text
V row column
```

Rows and columns start at zero.

## Task 1 — Reproduce and investigate the bug

Run several games and deliberately create situations where a move completes one or more boxes.

Compare the score and turn behaviour before and after box completion. Identify the incorrect behaviour, trace it through the board and game-state logic, and fix it without replacing the modular structure.

Your before-change video should capture the broken behaviour clearly.

## Task 2 — Add a meaningful feature

Add a substantial gameplay feature that requires changes across more than one module.

The feature should make the game more complete rather than simply changing text or appearance. It should interact correctly with the existing board state and turn/score system.

## Task 3 — Validation and robustness

Strengthen input and game-state handling.

The program should safely handle malformed commands, invalid coordinates, repeated lines, and moves made after the board is already complete. Invalid input must not corrupt the board or score.

## Task 4 — Testing and quality

Create or expand automated tests covering the important game rules.

Include tests for at least:
- a valid horizontal move
- a valid vertical move
- an invalid/repeated move
- completion of a box
- the end-of-game condition

Document the changes you made and any design decisions that were important to the solution.

## Constraints

- Keep the project modular.
- Do not replace the game with an unrelated implementation.
- Preserve the existing gameplay.
- Avoid putting all new logic into `main.py`.
- Keep third-party dependencies out unless there is a clear need for them.

## Submission Checklist

Submission is only the following three things:

- [ ] A 10-second video of gameplay **before** your changes, showing the bug/broken behavior
- [ ] A 10-second video of gameplay **after** your changes, showing the bug fixed and the new features working
- [ ] The Chat/LLM used page link, with the complete chat history

## Completed work

This project now includes a fix for the box-completion scoring flow and a more robust game state model.

### Bug fix

The scoring and turn logic was tightened so that a player only keeps the turn when their move captures at least one box. The board now recalculates the completed-box set from the current board state instead of only adding entries incrementally, which keeps the game state consistent and prevents stale or duplicated box records.

### Gameplay feature

A move-history/undo feature was added. It spans the board and game modules: the board records each prior line placement, and the game restores the previous score, current player, and board layout when the user enters `UNDO` or `U`. This is a meaningful gameplay addition because it lets players recover from mistakes without breaking the identity of the active turn or the scoreboard.

### Validation and robustness

Input validation now rejects malformed commands, non-numeric coordinates, repeated lines, and moves attempted after the board is complete. Invalid moves raise clear errors instead of mutating the board or the score counter.

### Testing

The project now includes automated tests covering a valid horizontal move, a valid vertical move, an invalid/repeated move, box completion scoring, undo behaviour, and the end-of-game condition.

### Design decisions

- The project remains modular: board state remains in `board.py`, rule checks remain in `rules.py`, and turn/score logic stays in `game.py`.
- Board validation is performed centrally through the rule checks and the `Board.add_line` method so invalid state changes are rejected before they can alter the game.
- The undo operation restores both the board and the match state, keeping the turn and score history consistent.
