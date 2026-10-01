def valid_move(board, orientation, row, col):
    if board is None or orientation not in {"H", "V"}:
        return False

    if not isinstance(row, int) or not isinstance(col, int):
        return False

    if board.is_complete():
        return False

    if orientation == "H":
        return (
            0 <= row <= board.rows
            and 0 <= col < board.cols
            and not board.horizontal[row][col]
        )

    return (
        0 <= row < board.rows
        and 0 <= col <= board.cols
        and not board.vertical[row][col]
    )


def completed_boxes(board, before):
    if board is None or before is None:
        return 0
    return len(board.completed - set(before))
