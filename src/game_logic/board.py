import random
class BoardData:
    def __init__(self, size=4):
        '''数字の初期設定(0埋め)'''
        self.size = size
        self.grid: list[list[int]] = [[0 for _ in range(size)] for _ in range(size)]

    def print_board(self):
        '''
        ボードの数字一覧を表示する
        '''
        for i in range(self.size):
            for j in range(self.size):
                print(self.grid[i][j], end=' , ')
            print()

    def spawn_tile(self):
        '''
        ランダムに生成する数字を2or4を決める
        その後空いているタイルに値をセットする
        TODO:時間あったらmain側の呼び出しで最初に4が出たら次は2出るようにしたいかも
        '''

        # 2 or 4の選定
        random_list=[2,4]
        tile = random_list[random.randint(0,1)]

        # 空いている位置から数字をランダムに配置する
        empty_cell_list=self.get_empty_cells()
        if empty_cell_list:
            random_position = random.choice(empty_cell_list)
            row, col = random_position
            self.grid[row][col] = tile
        
    def get_board_state(self):
        '''
        ボードの数字一覧を返す
        '''
        result_lists=[]
        for i in range(self.size):
            for j in range(self.size):
                result_lists.append(self.grid[i][j])
        return result_lists
            
        

    def set_tile(self, row: int, col: int, value: int):
        pass
        

    def get_empty_cells(self):
        empty_cells=[]
        for i in range(self.size):
            for j in range(self.size):
                if(self.grid[i][j] == 0):
                    empty_cells.append((i,j))
        return empty_cells
    
    # def num_check(self,num:int):
    #     if 
        
if __name__ == "__main__":
    # BoardDataクラスのテストコード
    print("=== BoardData テスト開始 ===")
    
    # テスト: ボードの初期化
    print("\nボードの初期化テスト")
    board = BoardData()
    print(f"ボードサイズ: {board.size}x{board.size}")
    print("初期状態のボード:")
    board.print_board()

    # テスト:　ボードの初期化(数字の配置)
    print("\n数字の初期位置テスト")
    print("初期状態のボード:")
    board.spawn_tile()
    board.spawn_tile()
    board.print_board()

    # テスト: 空のセルの取得
    print("\n 空のセルの取得テスト")
    empty_cells = board.get_empty_cells()
    print(f"空のセル数: {len(empty_cells)}")
    print(f"空のセル: {empty_cells}")
    
    # テスト: ボード状態の取得
    print("ボード状態の取得テスト")
    state = board.get_board_state()
    print("取得した状態:")
    for i, row in enumerate(state):
        print(f"{i}: {row}")


    # # テスト: 数字の設定
    # print("\n 数字の設定テスト")
    # print("位置(0,0)に2を設定")
    # board.set_tile(0, 0, 2)
    # print("位置(1,1)に4を設定")
    # board.set_tile(1, 1, 4)
    # print("位置(2,3)に8を設定")
    # board.set_tile(2, 3, 8)
    # print("位置(3,2)に16を設定")
    # board.set_tile(3, 2, 16)
    # print("数字設定後のボード:")
    # board.print_board()
    
    # # テスト: 範囲外の設定テスト
    # print("\n範囲外の設定テスト")
    # result1 = board.set_tile(-1, 0, 32)  # 範囲外
    # result2 = board.set_tile(4, 4, 64)   # 範囲外
    # result3 = board.set_tile(0, 1, 128)  # 正常
    # print(f"(-1,0)に32を設定: {result1} (False であるべき)")
    # print(f"(4,4)に64を設定: {result2} (False であるべき)")
    # print(f"(0,1)に128を設定: {result3} (True であるべき)")
    
    # print("\n最終的なボード:")
    # board.print_board()
    
    # # テスト6: 大きな数字のテスト
    # print("6. 大きな数字のテスト")
    # board.set_tile(3, 3, 2048)
    # print("位置(3,3)に2048を設定:")
    # board.print_board()

    

    
    # print("=== テスト完了 ===")
    # print(f"ボードは数字を正常に保持できています！")