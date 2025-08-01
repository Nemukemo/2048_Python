from . import board
from . import movement
from . import scoring
import msvcrt  # Windowsのキーボード入力
import time

class GameManager:
    def __init__(self):
        self.board = board.BoardData()

    def get_keyboard_input(self):
        """
        矢印キー入力を受け取る（Windows用）
        """
        while True:
            if msvcrt.kbhit():  # キーが押されているかチェック
                key = msvcrt.getch()
                
                if key == b'\xe0':  # 矢印キーの場合
                    key = msvcrt.getch()
                    if key == b'H':    # 上矢印
                        return 'up'
                    elif key == b'P':  # 下矢印
                        return 'down'
                    elif key == b'K':  # 左矢印
                        return 'left'
                    elif key == b'M':  # 右矢印
                        return 'right'
                elif key == b'\x1b':   # ESCキー
                    return 'quit'
                elif key in (b'w', b'W'):  # WASDキーも対応
                    return 'up'
                elif key in (b's', b'S'):
                    return 'down'
                elif key in (b'a', b'A'):
                    return 'left'
                elif key in (b'd', b'D'):
                    return 'right'
            
            time.sleep(0.05)  # CPU使用率を下げる

    def play(self):
        self.board.spawn_tile()
        self.board.spawn_tile()
        scoring.reset_score()
        print("=== 2048ゲーム ===")
        print("矢印キーまたはWASDで移動、ESCで終了")
        print(f"現在のスコア: {scoring.get_score()}")
        self.board.print_board()  # 最初の盤面表示

        while True:
            if self.is_game_over():
                print("ゲーム終了！")
                print(f"最終スコア: {scoring.get_score()}")
                break

            # 入力受付
            direction = self.get_keyboard_input()
            
            if direction == 'quit':
                print("ゲームを終了します。")
                print(f"最終スコア: {scoring.get_score()}")
                break

            # 実際に移動があった場合のみ処理
            moved = movement.move_board(self.board, direction)
            if moved:
                self.board.spawn_tile()
                print(f"\n現在のスコア: {scoring.get_score()}")
                self.board.print_board()
            else:
                print("その方向には移動できません。")

    def is_game_over(self) -> bool:
        """
        ゲーム終了条件をチェック
        空きセルがないかつ、どの方向にも移動できない場合にTrue
        """
        # 空きセルがある場合はゲーム継続
        if self.board.get_empty_cells():
            return False
        
        # 全方向で移動可能性をチェック
        directions = ['up', 'down', 'left', 'right']
        for direction in directions:
            # 一時的にボードをコピーして移動テスト
            test_board = board.BoardData(size=self.board.size)
            test_board.grid = [row[:] for row in self.board.grid]
            if movement.move_board(test_board, direction):
                # 移動可能だった場合、ゲーム継続
                return False
        
        # どの方向にも移動できない場合はゲーム終了
        return True
    
if __name__ == "__main__":
    game = GameManager()
    game.play()
