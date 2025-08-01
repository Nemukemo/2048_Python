import sys
import os
# 親ディレクトリをパスに追加してgame_logicをインポート可能にする
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import wx
import game_logic.board as board
import game_logic.scoring as scoring
import game_logic.movement as movement
import game_logic.maneger as maneger

class GameBoard(wx.Frame):
    def __init__(self, *args, **kw):
        super(GameBoard, self).__init__(*args, **kw)

        # ゲームマネージャーの初期化
        self.manager = maneger.GameManager()

        self.panel = wx.Panel(self)

        # メイン縦方向のsizer
        main_sizer = wx.BoxSizer(wx.VERTICAL)

        # ==== スコア部分 ====
        self.score_text = wx.StaticText(self.panel, label=f"Score: {scoring.get_score()}")
        font = self.score_text.GetFont()
        font.PointSize += 8
        font = font.Bold()
        self.score_text.SetFont(font)

        # スコア部分を中央に配置
        main_sizer.Add(self.score_text, proportion=0, flag=wx.ALIGN_CENTER_HORIZONTAL | wx.TOP | wx.BOTTOM, border=10)

        # ==== 操作説明 ====
        instruction_text = wx.StaticText(self.panel, label="矢印キーで移動")
        instruction_font = instruction_text.GetFont()
        instruction_font.PointSize += 2
        instruction_text.SetFont(instruction_font)
        main_sizer.Add(instruction_text, proportion=0, flag=wx.ALIGN_CENTER_HORIZONTAL | wx.BOTTOM, border=5)

        # ==== グリッド部分 ====
        grid_sizer = wx.GridSizer(4, 4, 5, 5)

        # 16個のタイル用StaticTextを作成
        self.tiles = []
        for i in range(4):
            row = []
            for j in range(4):
                tile = wx.StaticText(
                    self.panel, 
                    label="", 
                    size=(80, 80),
                    style=wx.ALIGN_CENTER | wx.ST_NO_AUTORESIZE
                )
                tile.SetBackgroundColour(self.get_tile_color(0))
                
                # フォント設定
                tile_font = tile.GetFont()
                tile_font.SetPointSize(18)
                tile_font.SetWeight(wx.FONTWEIGHT_BOLD)
                tile.SetFont(tile_font)
                
                grid_sizer.Add(tile, 1, flag=wx.EXPAND)
                row.append(tile)
            self.tiles.append(row)

        # グリッド部分をexpandさせる
        main_sizer.Add(grid_sizer, proportion=1, flag=wx.EXPAND | wx.ALL, border=10)

        # ==== リセットボタン ====
        reset_button = wx.Button(self.panel, label="新しいゲーム")
        reset_button.Bind(wx.EVT_BUTTON, self.on_reset)
        main_sizer.Add(reset_button, proportion=0, flag=wx.ALIGN_CENTER_HORIZONTAL | wx.BOTTOM, border=10)

        self.panel.SetSizer(main_sizer)
        self.Centre()
        self.SetSize((400, 550))

        # ==== キーボードイベントバインド ====
        # パネルとフレーム両方にキーイベントをバインド
        self.panel.SetCanFocus(True)
        
        # アクセラレータテーブルを設定（矢印キーを確実にキャッチ）
        accel_tbl = wx.AcceleratorTable([
            (wx.ACCEL_NORMAL, wx.WXK_UP, wx.ID_ANY),
            (wx.ACCEL_NORMAL, wx.WXK_DOWN, wx.ID_ANY),
            (wx.ACCEL_NORMAL, wx.WXK_LEFT, wx.ID_ANY),
            (wx.ACCEL_NORMAL, wx.WXK_RIGHT, wx.ID_ANY),
            (wx.ACCEL_NORMAL, wx.WXK_F5, wx.ID_ANY)
        ])
        self.SetAcceleratorTable(accel_tbl)
        
        # キーイベントをバインド
        self.Bind(wx.EVT_KEY_DOWN, self.on_key)
        self.panel.Bind(wx.EVT_KEY_DOWN, self.on_key)
        self.Bind(wx.EVT_CHAR_HOOK, self.on_key)  # より確実にキーをキャッチ
        
        # マウスクリックでフォーカスを設定
        self.panel.Bind(wx.EVT_LEFT_DOWN, self.on_click)

        # ゲーム初期化
        self.init_game()
        self.update_board()
        
        # フォーカスを設定（初期化後）
        self.panel.SetFocus()
        self.Show()

    def on_click(self, event):
        """マウスクリックでフォーカスを設定"""
        self.panel.SetFocus()
        event.Skip()

    def init_game(self):
        """ゲームを初期化"""
        # ボードをリセット
        self.manager.board = board.BoardData()
        scoring.reset_score()
        
        # 初期タイルを2つ生成
        self.manager.board.spawn_tile()
        self.manager.board.spawn_tile()

    def get_tile_color(self, value):
        """数値に応じてタイルの色を返す（blankなし版）"""
        colors = {
            0: wx.Colour(205, 193, 180),      # 空のタイル
            2: wx.Colour(238, 228, 218),      # 2
            4: wx.Colour(237, 224, 200),      # 4
            8: wx.Colour(242, 177, 121),      # 8
            16: wx.Colour(245, 149, 99),      # 16
            32: wx.Colour(246, 124, 95),      # 32
            64: wx.Colour(246, 94, 59),       # 64
            128: wx.Colour(237, 207, 114),    # 128
            256: wx.Colour(237, 204, 97),     # 256
            512: wx.Colour(237, 200, 80),     # 512
            1024: wx.Colour(237, 197, 63),    # 1024
            2048: wx.Colour(237, 194, 46),    # 2048 - 金色
        }
        return colors.get(value, wx.Colour(60, 58, 50))  # それ以上の値用

    def get_text_color(self, value):
        """数値に応じてテキストの色を返す"""
        if value <= 4:
            return wx.Colour(119, 110, 101)  # 濃いグレー
        else:
            return wx.Colour(249, 246, 242)  # 白っぽい色

    def update_board(self):
        """ボードとスコアを更新"""
        for i in range(4):
            for j in range(4):
                value = self.manager.board.grid[i][j]
                tile = self.tiles[i][j]
                
                # 背景色を設定
                tile.SetBackgroundColour(self.get_tile_color(value))
                
                # テキスト色を設定
                tile.SetForegroundColour(self.get_text_color(value))
                
                # テキストを設定（0の場合は空文字）
                if value == 0:
                    tile.SetLabel("")
                else:
                    tile.SetLabel(str(value))

        # スコアを更新
        self.score_text.SetLabel(f"Score: {scoring.get_score()}")
        
        # 画面を更新
        self.panel.Layout()
        self.Refresh()

    def on_key(self, event):
        """キーボードイベントハンドラ"""
        key = event.GetKeyCode()
        print(f"キーが押されました: {key}")  # デバッグ用
        
        direction_map = {
            wx.WXK_UP: 'up',
            wx.WXK_DOWN: 'down',
            wx.WXK_LEFT: 'left',
            wx.WXK_RIGHT: 'right'
        }

        if key in direction_map:
            direction = direction_map[key]
            print(f"移動方向: {direction}")  # デバッグ用
            
            # 移動を実行
            moved = movement.move_board(self.manager.board, direction)
            print(f"移動結果: {moved}")  # デバッグ用
            
            if moved:
                # 新しいタイルを生成
                self.manager.board.spawn_tile()
                self.update_board()
                print("ボードを更新しました")  # デバッグ用

                # ゲーム終了チェック
                if self.manager.is_game_over():
                    wx.CallAfter(self.show_game_over)
            else:
                print("移動できませんでした")  # デバッグ用
            
        elif key == wx.WXK_F5:  # F5でリセット
            self.on_reset(None)
            
        event.Skip()

    def show_game_over(self):
        """ゲームオーバーダイアログを表示"""
        final_score = scoring.get_score()
        message = f"ゲームオーバー！\n最終スコア: {final_score}\n\n新しいゲームを始めますか？"
        
        dlg = wx.MessageDialog(
            self, 
            message, 
            "ゲームオーバー", 
            wx.YES_NO | wx.ICON_INFORMATION
        )
        
        result = dlg.ShowModal()
        dlg.Destroy()
        
        if result == wx.ID_YES:
            self.init_game()
            self.update_board()

    def on_reset(self, event):
        """リセットボタンのイベントハンドラ"""
        dlg = wx.MessageDialog(
            self, 
            "新しいゲームを始めますか？\n現在のスコアは失われます。", 
            "新しいゲーム", 
            wx.YES_NO | wx.ICON_QUESTION
        )
        
        result = dlg.ShowModal()
        dlg.Destroy()
        
        if result == wx.ID_YES:
            self.init_game()
            self.update_board()

if __name__ == '__main__':
    app = wx.App(False)
    frame = GameBoard(None, title="2048 Game")
    app.MainLoop()
