import board

def move_board(board, direction: str) -> bool:
    """
    指定された方向に盤面を移動・マージする。
    盤面に変化があった場合は True、なかった場合は False を返す。
    """
    if direction not in ("up", "down", "left", "right"):
        print(f"無効な方向: {direction}")
        return False

    moved = False

    # 方向ごとに board.grid を操作
    for i in range(board.size):
        # 各行または列を抽出
        line = []
        if direction in ("left", "right"):
            line = board.grid[i][:]
        else:
            line = [board.grid[j][i] for j in range(board.size)]

        if direction in ("right", "down"):
            line.reverse()

        # マージ処理
        new_line, changed = merge_line(line)
        if changed:
            moved = True

        if direction in ("right", "down"):
            new_line.reverse()

        # 更新
        for j in range(board.size):
            if direction in ("left", "right"):
                board.grid[i][j] = new_line[j]
            else:
                board.grid[j][i] = new_line[j]

    return moved


def merge_line(line):
    """
    1列の処理：数字を詰めて、マージして、新しい列と変更有無を返す。
    """
    new_line = [num for num in line if num != 0]
    merged_line = []
    skip = False
    changed = False

    for i in range(len(new_line)):
        if skip:
            skip = False
            continue

        if i + 1 < len(new_line) and new_line[i] == new_line[i + 1]:
            merged_line.append(new_line[i] * 2)
            skip = True
            changed = True
        else:
            merged_line.append(new_line[i])

    merged_line += [0] * (len(line) - len(merged_line))
    if merged_line != line:
        changed = True

    return merged_line, changed


# テストコード
if __name__ == "__main__":
    # サンプル盤面のテスト
    b = board.BoardData(size=4)
    b.grid = [
        [2, 2, 4, 0],
        [0, 4, 4, 0],
        [2, 0, 2, 2],
        [0, 0, 0, 0]
    ]

    print("テスト：レフトに移動")
    print("Before move:")
    b.print_board()

    moved = move_board(b, "left")

    print("\nAfter move (left):")
    b.print_board()

    print("\nMoved:", moved)

    print("\nテスト：ライトに移動")
    moved = move_board(b, "right")
    print("\nAfter move (right):")
    b.print_board()
    print("\nMoved:", moved)

    print("\nテスト：アップに移動")
    moved = move_board(b, "up")
    print("\nAfter move (up):")
    b.print_board()
    print("\nMoved:", moved)

    print("\nテスト：ダウンに移動")
    moved = move_board(b, "down")
    print("\nAfter move (down):")
    b.print_board()
    print("\nMoved:", moved)

    print("バグが発生しうる動作")
    moved = move_board(b, "over")
    print("\nAfter move (invalid direction):")
    b.print_board()
    print("\nMoved:", moved)
